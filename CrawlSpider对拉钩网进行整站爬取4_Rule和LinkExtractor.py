# Rule
# crawl.py
"""
This modules implements the CrawlSpider which is the recommended spider to use
for scraping typical web sites that requires crawling pages.

See documentation in docs/topics/spiders.rst
"""

import copy
import six

from scrapy.http import Request, HtmlResponse
from scrapy.utils.spider import iterate_spider_output
from scrapy.spiders import Spider


def identity(x):
    return x


class Rule(object):
                                #callback：回调函数      #cb_kwargs：传递给link_extractor的参数    #process_links：可以添加对links做预处理的函数
    def __init__(self, link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=identity):
        self.link_extractor = link_extractor  #link_extractor用于抽取url  #follow：满足rule的url还是否需要进一步跟踪    #process_request：对request做处理（示例：identity）
        self.callback = callback
        self.cb_kwargs = cb_kwargs or {}
        self.process_links = process_links
        self.process_request = process_request
        if follow is None:
            self.follow = False if callback else True
        else:
            self.follow = follow


class CrawlSpider(Spider):  #CrawlSpider继承自Spider  #入口函数为start_requests，默认callback parse函数

    rules = ()

    def __init__(self, *a, **kw):
        super(CrawlSpider, self).__init__(*a, **kw)
        self._compile_rules()

    def parse(self, response):  #CrawlSpider不能覆盖parse函数
        return self._parse_response(response, self.parse_start_url, cb_kwargs={}, follow=True)  #parse函数调用_parse_response

    def parse_start_url(self, response):  #CrawlSpider不能覆盖parse函数#可以选择重载parse_start_url
        return []

    def process_results(self, response, results):  #CrawlSpider不能覆盖parse函数#可以选择重载process_results
        return results

    def _build_request(self, rule, link):
        r = Request(url=link.url, callback=self._response_downloaded)  #调用_response_downloaded
        r.meta.update(rule=rule, link_text=link.text)
        return r

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return  #如果没有response，直接返回
        seen = set()
        for n, rule in enumerate(self._rules):    #enumerate方法用于迭代
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]  #去重
            if links and rule.process_links:
                links = rule.process_links(links)  #可以自定义对links做处理
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)  #调用_build_request
                yield rule.process_request(r)  #处理好link之后，对每个link yield 一个request

    def _response_downloaded(self, response):
        rule = self._rules[response.meta['rule']]  #rule
        return self._parse_response(response, rule.callback, rule.cb_kwargs, rule.follow)  #调用_parse_response  #rule.callback  使用rule指定的callback函数

    def _parse_response(self, response, callback, cb_kwargs, follow=True):  # _parse_response是CrawlSpider的核心函数
        if callback:
            cb_res = callback(response, **cb_kwargs) or ()
            cb_res = self.process_results(response, cb_res)  #可以重载process_results，从而避免重载parse函数
            for requests_or_item in iterate_spider_output(cb_res):
                yield requests_or_item

        if follow and self._follow_links:  #调用我们设置的rule
            for request_or_item in self._requests_to_follow(response):  #调用_requests_to_follow函数
                yield request_or_item

    def _compile_rules(self):
        def get_method(method):
            if callable(method):
                return method
            elif isinstance(method, six.string_types):
                return getattr(self, method, None)

        self._rules = [copy.copy(r) for r in self.rules]
        for rule in self._rules:
            rule.callback = get_method(rule.callback)
            rule.process_links = get_method(rule.process_links)
            rule.process_request = get_method(rule.process_request)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CrawlSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider._follow_links = crawler.settings.getbool(
            'CRAWLSPIDER_FOLLOW_LINKS', True)
        return spider

    def set_crawler(self, crawler):
        super(CrawlSpider, self).set_crawler(crawler)
        self._follow_links = crawler.settings.getbool('CRAWLSPIDER_FOLLOW_LINKS', True)  #取settings.py中的CRAWLSPIDER_FOLLOW_LINKS






# lxmlhtml.py
# LinkExtractor
"""
Link extractor based on lxml.html
"""
import six
from six.moves.urllib.parse import urljoin

import lxml.etree as etree
from w3lib.html import strip_html5_whitespace
from w3lib.url import canonicalize_url

from scrapy.link import Link
from scrapy.utils.misc import arg_to_iter, rel_has_nofollow
from scrapy.utils.python import unique as unique_list, to_native_str
from scrapy.utils.response import get_base_url
from scrapy.linkextractors import FilteringLinkExtractor


# from lxml/src/lxml/html/__init__.py
XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"

_collect_string_content = etree.XPath("string()")


def _nons(tag):
    if isinstance(tag, six.string_types):
        if tag[0] == '{' and tag[1:len(XHTML_NAMESPACE)+1] == XHTML_NAMESPACE:
            return tag.split('}')[-1]
    return tag


class LxmlParserLinkExtractor(object):
    def __init__(self, tag="a", attr="href", process=None, unique=False,
                 strip=True, canonicalized=False):
        self.scan_tag = tag if callable(tag) else lambda t: t == tag
        self.scan_attr = attr if callable(attr) else lambda a: a == attr
        self.process_attr = process if callable(process) else lambda v: v
        self.unique = unique
        self.strip = strip
        if canonicalized:
            self.link_key = lambda link: link.url
        else:
            self.link_key = lambda link: canonicalize_url(link.url,
                                                          keep_fragments=True)

    def _iter_links(self, document):
        for el in document.iter(etree.Element):
            if not self.scan_tag(_nons(el.tag)):
                continue
            attribs = el.attrib
            for attrib in attribs:
                if not self.scan_attr(attrib):
                    continue
                yield (el, attrib, attribs[attrib])

    def _extract_links(self, selector, response_url, response_encoding, base_url):
        links = []
        # hacky way to get the underlying lxml parsed document
        for el, attr, attr_val in self._iter_links(selector.root):
            # pseudo lxml.html.HtmlElement.make_links_absolute(base_url)
            try:
                if self.strip:
                    attr_val = strip_html5_whitespace(attr_val)
                attr_val = urljoin(base_url, attr_val)
            except ValueError:
                continue  # skipping bogus links
            else:
                url = self.process_attr(attr_val)
                if url is None:
                    continue
            url = to_native_str(url, encoding=response_encoding)
            # to fix relative links after process_value
            url = urljoin(response_url, url)
            link = Link(url, _collect_string_content(el) or u'',
                        nofollow=rel_has_nofollow(el.get('rel')))
            links.append(link)
        return self._deduplicate_if_needed(links)

    def extract_links(self, response):
        base_url = get_base_url(response)
        return self._extract_links(response.selector, response.url, response.encoding, base_url)

    def _process_links(self, links):
        """ Normalize and filter extracted links

        The subclass should override it if neccessary
        """
        return self._deduplicate_if_needed(links)

    def _deduplicate_if_needed(self, links):
        if self.unique:
            return unique_list(links, key=self.link_key)
        return links


class LxmlLinkExtractor(FilteringLinkExtractor):
#allow：正则表达式，如果url匹配，完成提取      #deny：正则表达式，如果url匹配，抛弃该url  #allow_domains：规定在某个域名之下才做处理
    def __init__(self, allow=(), deny=(), allow_domains=(), deny_domains=(), restrict_xpaths=(),  #restrict_xpaths:进一步限定url
                 tags=('a', 'area'), attrs=('href',), canonicalize=False,  #tags:从a标签和area标签里去寻找url  #attrs：取href
                 unique=True, process_value=None, deny_extensions=None, restrict_css=(),  #restrict_css：进一步限定url
                 strip=True):
        tags, attrs = set(arg_to_iter(tags)), set(arg_to_iter(attrs))
        tag_func = lambda x: x in tags
        attr_func = lambda x: x in attrs
        lx = LxmlParserLinkExtractor(
            tag=tag_func,
            attr=attr_func,
            unique=unique,
            process=process_value,
            strip=strip,
            canonicalized=canonicalize
        )

        super(LxmlLinkExtractor, self).__init__(lx, allow=allow, deny=deny,
            allow_domains=allow_domains, deny_domains=deny_domains,
            restrict_xpaths=restrict_xpaths, restrict_css=restrict_css,
            canonicalize=canonicalize, deny_extensions=deny_extensions)

    def extract_links(self, response):  #crawl里面会调用extract_links方法
        base_url = get_base_url(response)
        if self.restrict_xpaths:
            docs = [subdoc  #编译xpath处理变量
                    for x in self.restrict_xpaths
                    for subdoc in response.xpath(x)]
        else:
            docs = [response.selector]
        all_links = []
        for doc in docs:
            links = self._extract_links(doc, response.url, response.encoding, base_url)
            all_links.extend(self._process_links(links))
        return unique_list(all_links)


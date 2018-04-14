# -*- coding: utf-8 -*-

print(enumerate("123"))  #<enumerate object at 0x000002717C6231F8>

for a in enumerate("123"):  #enumerate方法用于迭代
    print(a)
#(0, '1')
#(1, '2')
#(2, '3')





#crawl.py
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

    def __init__(self, link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=identity):
        self.link_extractor = link_extractor
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

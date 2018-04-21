# C:\Users\admin\AppData\Local\Programs\Python\Python36\Lib\site-packages\scrapy\spidermiddlewares
# 文档  http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/spider-middleware.html
# depth.py:爬取深度的设置
# httperror.py：状态的设置，比如是不是要把404的也抓取下来，等等。



# depth.py
"""
Depth Spider Middleware

See documentation in docs/topics/spider-middleware.rst
"""

import logging

from scrapy.http import Request

logger = logging.getLogger(__name__)


class DepthMiddleware(object):

    def __init__(self, maxdepth, stats=None, verbose_stats=False, prio=1):
        self.maxdepth = maxdepth
        self.stats = stats
        self.verbose_stats = verbose_stats
        self.prio = prio

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        maxdepth = settings.getint('DEPTH_LIMIT')
        verbose = settings.getbool('DEPTH_STATS_VERBOSE')
        prio = settings.getint('DEPTH_PRIORITY')
        return cls(maxdepth, crawler.stats, verbose, prio)

    def process_spider_output(self, response, result, spider):
        def _filter(request):
            if isinstance(request, Request):
                depth = response.meta['depth'] + 1
                request.meta['depth'] = depth
                if self.prio:
                    request.priority -= depth * self.prio
                if self.maxdepth and depth > self.maxdepth:
                    logger.debug(
                        "Ignoring link (depth > %(maxdepth)d): %(requrl)s ",
                        {'maxdepth': self.maxdepth, 'requrl': request.url},
                        extra={'spider': spider}
                    )
                    return False
                elif self.stats:
                    if self.verbose_stats:
                        self.stats.inc_value('request_depth_count/%s' % depth,
                                             spider=spider)
                    self.stats.max_value('request_depth_max', depth,
                                         spider=spider)
            return True

        # base case (depth=0)
        if self.stats and 'depth' not in response.meta:
            response.meta['depth'] = 0
            if self.verbose_stats:
                self.stats.inc_value('request_depth_count/0', spider=spider)

        return (r for r in result or () if _filter(r))



# httperror.py
"""
HttpError Spider Middleware

See documentation in docs/topics/spider-middleware.rst
"""
import logging

from scrapy.exceptions import IgnoreRequest

logger = logging.getLogger(__name__)


class HttpError(IgnoreRequest):
    """A non-200 response was filtered"""

    def __init__(self, response, *args, **kwargs):
        self.response = response
        super(HttpError, self).__init__(*args, **kwargs)


class HttpErrorMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.handle_httpstatus_all = settings.getbool('HTTPERROR_ALLOW_ALL')
        self.handle_httpstatus_list = settings.getlist('HTTPERROR_ALLOWED_CODES')

    def process_spider_input(self, response, spider):
        if 200 <= response.status < 300:  # common case
            return
        meta = response.meta
        if 'handle_httpstatus_all' in meta:
            return
        if 'handle_httpstatus_list' in meta:
            allowed_statuses = meta['handle_httpstatus_list']
        elif self.handle_httpstatus_all:
            return
        else:
            allowed_statuses = getattr(spider, 'handle_httpstatus_list', self.handle_httpstatus_list)
        if response.status in allowed_statuses:
            return
        raise HttpError(response, 'Ignoring non-200 response')

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, HttpError):
            spider.crawler.stats.inc_value('httperror/response_ignored_count')
            spider.crawler.stats.inc_value(
                'httperror/response_ignored_status_count/%s' % response.status
            )
            logger.info(
                "Ignoring response %(response)r: HTTP status code is not handled or not allowed",
                {'response': response}, extra={'spider': spider},
            )
            return []

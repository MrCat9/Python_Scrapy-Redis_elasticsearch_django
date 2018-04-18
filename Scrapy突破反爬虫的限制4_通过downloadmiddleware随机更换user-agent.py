# ��user_agent_list�� ��ÿ��requestʱ����user_agent_list�����ȡ��һ��
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
]

headers = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': ""
    } 

import random  #���������
random_index = random.randint(0, len(user_agent_list)-1)
random_agent = user_agent_list[random_index]
headers["User-Agent"] = random_agent



# ͨ��downloadmiddleware�������user-agent
# ��settings.py�а�ע��ȥ��
#DOWNLOADER_MIDDLEWARES = {
#    'test_scrapy_spider.middlewares.TestJobboleDownloaderMiddleware': 543,
#}



# scrapy�и��Դ���useragent  C:\Users\admin\AppData\Local\Programs\Python\Python36\Lib\site-packages\scrapy\downloadermiddlewares\useragent.py
"""Set User-Agent header per spider or use a default value from settings"""

from scrapy import signals


class UserAgentMiddleware(object):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, user_agent='Scrapy'):  #Ĭ��user_agentΪScrapy
        self.user_agent = user_agent

    @classmethod  #��̬����
    def from_crawler(cls, crawler):  #���ݵ�ǰ���������
        o = cls(crawler.settings['USER_AGENT'])  #ȥsettings.py��ȡUSER_AGENT��ȡ�����Ļ���Ĭ�ϵ�USER_AGENT-->Scrapy
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)

    def process_request(self, request, spider):  #����request
        if self.user_agent:
            request.headers.setdefault(b'User-Agent', self.user_agent)


# ����pip
# cmder��
C:\Users\admin
�� python -m pip install --upgrade pip



# https://github.com/hellysmile/fake-useragent  ����л�useragent
# ��װ��
# cmder��
C:\Users\admin
�� pip install fake-useragent



# fake-useragentʹ��
# -*- coding: utf-8 -*-
from fake_useragent import UserAgent

ua = UserAgent()  #����ʵ��

print(ua.ie)  #Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)
print(ua.ie)  #Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)
print(ua.firefox)  #Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0
print(ua.chrome)  #Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36

print(ua.random)  #Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0
print(ua.random)  #Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36

# user_agent ��  https://fake-useragent.herokuapp.com/browsers/0.1.8  #���İ汾�ſ��ܻ��



# cmder��
C:\Users\admin
�� pip list  #�鿴�Ѱ�װ



# test_scrapy_spider\test_scrapy_spider\settings.py
# -*- coding: utf-8 -*-

import os  #���ڻ�ȡ��ǰ�ļ���setting.py����·��

# Scrapy settings for test_scrapy_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'test_scrapy_spider'

SPIDER_MODULES = ['test_scrapy_spider.spiders']
NEWSPIDER_MODULE = 'test_scrapy_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'test_scrapy_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'test_scrapy_spider.middlewares.TestJobboleSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'test_scrapy_spider.middlewares.RandomUserAgentMiddlware': 543,  # ���� RandomUserAgentMiddlware
    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  #��Ĭ�ϵ�useragentȡ��
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'test_scrapy_spider.pipelines.JsonExporterPipeline': 2,  #����ԽС��Խ�ȴ���
    #'scrapy.pipelines.images.ImagesPipeline': 1
    #'test_scrapy_spider.pipelines.ArticleImagePipeline': 1,  #���ö��ƻ���pipeline��ArticleImagePipeline��
    #'test_scrapy_spider.pipelines.MysqlPipeline': 1
    'test_scrapy_spider.pipelines.MysqlTwistedPipline': 1
}
IMAGES_URLS_FIELD = 'front_image_url'  #����images items���ĸ���ͼƬ��url  #images��Ҫ����һ������
#os.path.dirname(__file__)  #��ȡ��ǰ�ļ���Ŀ¼���ƣ�test_scrapy_spider��  #__file__�ǵ�ǰ�ļ���setting.py��������
project_dir =  os.path.abspath(os.path.dirname(__file__))  #��ȡ��ǰ�ļ���Ŀ¼��·��
IMAGES_STORE = os.path.join(project_dir, 'images')  #ͼƬ���صı���·��  ��������Ϊ����·��  Ҫ���ڹ���Ŀ¼�£�����ʹ�����·������settings.py��ͬ��Ŀ¼���½�images
                                                    #ͼƬ������ project_dirĿ¼�µ�images�ļ���
                                                    #Ҫ����ͼƬ��ҪPIL��
                                                    #��cmd�°�װPIL��
                                                    #pip install -i https://pypi.douban.com/simple pillow
# IMAGES_MIN_HEIGHT = 100 #��������ͼƬ����С�߶�  #����ͼƬ������settng.py������
# IMAGES_MIN_WIDTH = 100
# '''���Ҫʵ���Լ�������Ҳ����������Ӧ�ĺ����ﵽ������pipelines�н����࣬�̳�ImagesPipeline�Ϳ�����'''

# ��F:\eclipse\������\������\test_scrapy_spider\test_scrapy_spider\settings.py �£�����F:\eclipse\������\������\test_scrapy_spider\test_scrapy_spider Ϊ��Ŀ¼
# ��Ϊ��Ȼ��eclipse���Ѿ��� F:\eclipse\������\������\test_scrapy_spider\test_scrapy_spider ��ӵ�path���ˣ�����cmd�»�δ���
import sys  #import os  ������д����
# sys.path.insert(0, "F:\eclipse\������\������\test_scrapy_spider\test_scrapy_spider")  #��F:\eclipse\������\������\test_scrapy_spider\test_scrapy_spider ��ӵ�path
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  #F:\eclipse\������\������\test_scrapy_spider  ����·��
sys.path.insert(0, os.path.join(BASE_DIR, 'test_scrapy_spider'))  #��F:\eclipse\������\������\test_scrapy_spider\test_scrapy_spider ��ӵ�path��
             #���ڵ�0������������F:\eclipse\������\������\test_scrapy_spider\test_scrapy_spider������Ҫimport��module

# user_agent_list = [
#     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
# ]

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"

RANDOM_UA_TYPE = "random"  #ѡ��Ҫ������ɵ�ua���ͣ�ie��Firefox��chrome�ȣ�  #random��ʾ���һ�������

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DBNAME = "article_spider"

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"



# test_scrapy_spider\test_scrapy_spider\middlewares.py
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent


class TestScrapySpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn��t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TestScrapySpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgentMiddlware(object):
    #�������user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        # self.user_agent_list = crawler.settings.get("user_agent_list", [])  #ȡsettings.py�е�user_agent_list
        self.ua = UserAgent()  #ʵ����
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")  #ȡsettings.py�е�RANDOM_UA_TYPE��ȡ�����Ļ���random

    @classmethod  #��̬����
    def from_crawler(cls, crawler):  #����crawler
        return cls(crawler)

    def process_request(self, request, spider):
        # request.headers.setdefault('User-Agent', random(������))
        def get_ua():  # �ں����ﶨ�庯��  #��̬���Կ�����������̬���Բ���
            return getattr(self.ua, self.ua_type)  #����дself.ua.self.ua_type

        # request.headers.setdefault('User-Agent', self.ua.random)
        # random_agent = get_ua()
        request.headers.setdefault('User-Agent', get_ua())



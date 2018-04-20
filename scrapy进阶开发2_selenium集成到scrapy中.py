# test_scrapy_spider\test_scrapy_spider\middlewares.py
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent

from tools.crawl_xici_ip import GetIP  #��F:\eclipse\������\������\test_scrapy_spider ��ӵ�path������import  
#��settings.py������ sys.path.insert(1, BASE_DIR)  #��F:\eclipse\������\������\test_scrapy_spider ��ӵ�path��
#��eclipse�¿����Ҽ�����Ŀ¼-->PyDev-->set as source folder (add to PYTHONPATH)

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
        # request.meta["proxy"] = "http://39.77.104.193:8118"  #����ip����  # http://(ip):(�˿ں�)

class RandomProxyMiddleware(object):
    #��̬����ip����
    def process_request(self, request, spider):
        get_ip = GetIP()
        request.meta["proxy"] = get_ip.get_random_ip()

# ������ÿ��url������һ��chrome  #����chrome��Ҫʱ��
# from selenium import webdriver
# from scrapy.http import HtmlResponse
# class JSPageMiddleware(object):  #д��middleware��Ҫȥsettings.py��������Ч
#     #ͨ��chrome����̬��ҳ  #������ɺ��ִ��spider�е�parse
#     def process_request(self, request, spider):
#         if spider.name == "jobbole_spider":  #�ò������ߵ��������
#             browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")
#             browser.get(request.url)
#             import time
#             time.sleep(3)
#             print ("����:{0}".format(request.url))
#             # Ϊ����download���ظ����أ�return HtmlRespons()  #����HtmlResponse��scrapy�Ͳ�����download���ͣ����Ƿ��ظ�spider
#             return HtmlResponse(url=browser.current_url, body=browser.page_source, encoding="utf-8", request=request)
#                                                                                        # Ĭ��encoding��ASCII��������ʲô���뿴��ҳ

# Ϊ�˲�ÿ�ζ���һ��chrome  #����ʵ���˹���һ��chrome��������spider�رպ�chromeȴû�ر�
# from selenium import webdriver
# from scrapy.http import HtmlResponse
# class JSPageMiddleware(object):  #д��middleware��Ҫȥsettings.py��������Ч
# 
#     def __init__(self):
#         self.browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")  # ���������browser
#         super(JSPageMiddleware, self).__init__()
#     
#     #ͨ��chrome����̬��ҳ  #������ɺ��ִ��spider�е�parse
#     def process_request(self, request, spider):
#         if spider.name == "jobbole_spider":  #�ò������ߵ��������
#             # browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")
#             self.browser.get(request.url)
#             import time
#             time.sleep(3)
#             print ("����:{0}".format(request.url))
#             # Ϊ����download���ظ����أ�return HtmlRespons()  #����HtmlResponse��scrapy�Ͳ�����download���ͣ����Ƿ��ظ�spider
#             return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding="utf-8", request=request)
#                                                                                        # Ĭ��encoding��ASCII��������ʲô���뿴��ҳ

# �� def __init__(self): �ŵ�spider��  #��browser�ŵ�spider��  #����һ��spiderһ��chrome
from selenium import webdriver
from scrapy.http import HtmlResponse
class JSPageMiddleware(object):  #д��middleware��Ҫȥsettings.py��������Ч
    #ͨ��chrome����̬��ҳ  #������ɺ��ִ��spider�е�parse  #scrapy���첽�ģ����ܸߡ�����chrome�����ܽ���  #Ҫ�ĳ��첽�ģ�������дdownload  https://github.com/flisky/scrapy-phantomjs-downloader
    def process_request(self, request, spider):
        if spider.name == "jobbole_spider":  #�ò������ߵ��������
            # browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")
            spider.browser.get(request.url)
            import time
            time.sleep(3)
            print ("����:{0}".format(request.url))
            # Ϊ����download���ظ����أ�return HtmlRespons()  #����HtmlResponse��scrapy�Ͳ�����download���ͣ����Ƿ��ظ�spider
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)
#                                                                                       # Ĭ��encoding��ASCII��������ʲô���뿴��ҳ



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
DOWNLOAD_DELAY = 10  #10������һ��
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False  #����cookie

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
    'test_scrapy_spider.middlewares.JSPageMiddleware': 1,
    #'test_scrapy_spider.middlewares.RandomUserAgentMiddlware': 543,  # ���� RandomUserAgentMiddlware
    #'test_scrapy_spider.middlewares.RandomProxyMiddleware': 544,
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
sys.path.insert(1, BASE_DIR)  #��F:\eclipse\������\������\test_scrapy_spider ��ӵ�path��

# user_agent_list = [
#     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
# ]

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"

RANDOM_UA_TYPE = "random"  #ѡ��Ҫ������ɵ�ua���ͣ�ie��Firefox��chrome�ȣ�  #random��ʾ���һ�������

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True  #�Զ����������ٶ�
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



# test_scrapy_spider\test_scrapy_spider\spiders\jobbole_spider.py
# -*- coding: utf-8 -*-
import scrapy
import re
import datetime  #Ϊ�˽����µĴ���ʱ��д�����ݿ⣬Ҫ��str���͵�create_timeת��Ϊdate����
from scrapy.http import Request  #��ȡ��url�󣬽�url����scrapy ����    #from scrapy.http import Request
from urllib import parse  #�����py2 �Ǿ���import urlparse
from items import JobboleArticleItem, ArticleItemLoader  #�����Զ����ItemLoader -->ArticleItemLoader
from utils.common import get_md5  #��url��MD5
from scrapy.loader import ItemLoader  #��itemloader����ά��
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals  #�ź�

class JobboleSpiderSpider(scrapy.Spider):
    name = 'jobbole_spider'
    allowed_domains = ['blog.jobbple.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']  #�����list�����ǿ��Է�����Ҫ��ȡ��url

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")  # ���������browser
        super(JobboleSpiderSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)  #�ź�ӳ��  #��spider�ر�ʱ��signals.spider_closed��-->�ر�chrome��self.spider_closed��
    
    def spider_closed(self, spider):
        #�������˳���ʱ��ر�chrome
        print ("spider closed")
        self.browser.quit()  #�ر�chrome


    def parse(self, response):  #ÿһ��url������뵽�������
        '''
        1. ��ȡ�����б�ҳ�е�����url������scrapy���غ󲢽��н���
        2. ��ȡ��һҳ��url������scrapy�������أ� ������ɺ󽻸�parse
        '''
        
        #�����б�ҳ�е���������url������scrapy���غ󲢽��н���
        
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            #��ʱ��ȡ����url����һ��������������Ҫ��ȫ
            #response.url + post_url
            
            image_url = post_node.css('img::attr(src)').extract_first("")
            post_url = post_node.css('::attr(href)').extract_first("")
            
            #������urljoin����ȫ
            yield Request(url = parse.urljoin(response.url, post_url), meta = {'front_image_url':image_url}, callback = self.parse_detail)
            #�� yield �Ϳ��԰�Request ����scrapy����
            #�޷�����parse_detail -->����Request�� ��dont_filter=True��ΪTrue
            #Request��meta�����������Ǵ�����Ϣ����һ������
            #print(post_url)
            
        #��ȡ��һҳ������scrapy��������
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        #.next �� .page-numbers��û�пո񣬴���ƥ��ͬʱ�У�.next ��.page-numbers����class
        if next_url:
            yield Request(url = parse.urljoin(response.url, next_url), callback = self.parse)
            
            
            
    def parse_detail(self, response):
        #��ȡ���¾����ֶ�(xpath)
#         title = response.xpath('//*[@id="post-113789"]/div[1]/h1/text()').extract()[0]
#         
#         create_date = response.xpath('//*[@id="post-113789"]/div[2]/p/text()[1]').extract()[0].strip().replace('��', '').strip()
#         
#         praise_nums = response.xpath('//*[@id="113789votetotal"]/text()').extract()
#         if praise_nums:
#             praise_nums = int(praise_nums[0])
#         else:
#             praise_nums = 0
#         
#         fav_nums = response.xpath('//*[@id="post-113789"]/div[3]/div[12]/span[2]/text()').extract()[0]
#         match_re = re.match(r'.*?(\d+).*', fav_nums)
#         if match_re:
#             fav_nums = int(match_re.group(1))
#         else:
#             fav_nums = 0
#         
#         comment_nums = response.xpath('//*[@id="post-113789"]/div[3]/div[12]/a/span/text()').extract()[0]
#         match_re = re.match(r'.*?(\d+).*', comment_nums)
#         if match_re:
#             comment_nums = int(match_re.group(1))
#         else:
#             comment_nums = 0
#         
#         content = response.xpath('//*[@id="post-113789"]/div[3]').extract()[0]
#         
#         tag_list = response.xpath('//*[@id="post-113789"]/div[2]/p/a/text()').extract()
#         tag_list = [element for element in tag_list if not element.strip().endswith('����')] 
#         tags = ','.join(tag_list)
        
        
        
        #����ͨ��cssѡ������ȡ�ֶ�
#         article_item = JobboleArticleItem()  #ʵ����
#         
#         front_image_url = response.meta.get('front_image_url', '')  #get key=front_image_url ��ֵ�����û��key=front_image_url���ش�''(��)
#         #���·���ͼ
#         
#         title = response.css('.entry-header h1::text').extract()[0]
#         
#         create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('��', '').strip()
#         
#         praise_nums = response.css('.vote-post-up h10::text').extract_first()
#         if praise_nums:
#             praise_nums = int(praise_nums[0])
#         else:
#             praise_nums = 0
#         
#         fav_nums = response.css('.bookmark-btn::text').extract()[0]
#         match_re = re.match(r'.*?(\d+).*', fav_nums)
#         if match_re:
#             fav_nums = int(match_re.group(1))
#         else:
#             fav_nums = 0
#         
#         comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
#         match_re = re.match(r'.*?(\d+).*', comment_nums)
#         if match_re:
#             comment_nums = int(match_re.group(1))
#         else:
#             comment_nums = 0
#         
#         content = response.css("div.entry").extract()[0]
#         
#         tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
#         tag_list = [element for element in tag_list if not element.strip().endswith('����')] 
#         tags = ','.join(tag_list)
#         
#         #���ֵ��items
#         article_item['title'] = title
#         article_item['url'] = response.url
#         article_item['url_object_id'] = get_md5(response.url)  #��url��MD5
#         
#         try:  #Ϊ�˽����µĴ���ʱ��д�����ݿ⣬Ҫ��str���͵�create_timeת��Ϊdate����
#             create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()  #����ʽΪ%Y/%m/%d ��str����ת��Ϊdate����
#         except Exception as e:
#             create_date = datetime.datetime.now().date()
#         article_item['create_date'] = create_date
#         
#         article_item['front_image_url'] = [front_image_url]  #images��Ҫ����һ������
#         article_item['praise_nums'] = praise_nums
#         article_item['fav_nums'] = fav_nums
#         article_item['comment_nums'] = comment_nums
#         article_item['tags'] = tags
#         article_item['content'] = content
        
        #ͨ��itemLoader����item
        front_image_url = response.meta.get('front_image_url', '')  #get key=front_image_url ��ֵ�����û��key=front_image_url���ش�''(��)
        #item_loader = ItemLoader(item=JobboleArticleItem(), response=response)  #����ItemLoaderʵ��
        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)  #�����Զ���� ItemLoader
#         ItemLoader.add_css(self, field_name, css)
#         ItemLoader.add_xpath(self, field_name, xpath)
#         ItemLoader._add_value(self, field_name, value)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        
        article_item = item_loader.load_item()
        #����Ĭ�ϵ�item�����Ļ������������⣺1.ֵ����list 2.����Ҫ��ȡ����ֵ�н�������re����ȡ�ȣ�
        #-->ȥ�޸�items.py  #1.��items.py ��Field()������TakeFirst���д���  2.��items.py ��Field()������MapCompose���д���
        
        yield article_item  #����yield֮��item�ᴫ�ݵ�pipelines.py

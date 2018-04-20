# test_scrapy_spider\test_scrapy_spider\middlewares.py
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent

from tools.crawl_xici_ip import GetIP  #将F:\eclipse\···\···\test_scrapy_spider 添加到path里后才能import  
#在settings.py里配置 sys.path.insert(1, BASE_DIR)  #将F:\eclipse\···\···\test_scrapy_spider 添加到path里
#在eclipse下可以右键工程目录-->PyDev-->set as source folder (add to PYTHONPATH)

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
        # that it doesn’t have a response associated.

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
    #随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        # self.user_agent_list = crawler.settings.get("user_agent_list", [])  #取settings.py中的user_agent_list
        self.ua = UserAgent()  #实例化
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")  #取settings.py中的RANDOM_UA_TYPE，取不到的话用random

    @classmethod  #静态方法
    def from_crawler(cls, crawler):  #传递crawler
        return cls(crawler)

    def process_request(self, request, spider):
        # request.headers.setdefault('User-Agent', random(···))
        def get_ua():  # 在函数里定义函数  #动态语言可以这样，静态语言不行
            return getattr(self.ua, self.ua_type)  #不能写self.ua.self.ua_type

        # request.headers.setdefault('User-Agent', self.ua.random)
        # random_agent = get_ua()
        request.headers.setdefault('User-Agent', get_ua())
        # request.meta["proxy"] = "http://39.77.104.193:8118"  #设置ip代理  # http://(ip):(端口号)

class RandomProxyMiddleware(object):
    #动态设置ip代理
    def process_request(self, request, spider):
        get_ip = GetIP()
        request.meta["proxy"] = get_ip.get_random_ip()

# 这样会每个url都启动一个chrome  #启动chrome需要时间
# from selenium import webdriver
# from scrapy.http import HtmlResponse
# class JSPageMiddleware(object):  #写好middleware后，要去settings.py中配置生效
#     #通过chrome请求动态网页  #请求完成后会执行spider中的parse
#     def process_request(self, request, spider):
#         if spider.name == "jobbole_spider":  #用伯乐在线的爬虫测试
#             browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")
#             browser.get(request.url)
#             import time
#             time.sleep(3)
#             print ("访问:{0}".format(request.url))
#             # 为了让download不重复下载，return HtmlRespons()  #遇到HtmlResponse，scrapy就不会向download发送，而是返回给spider
#             return HtmlResponse(url=browser.current_url, body=browser.page_source, encoding="utf-8", request=request)
#                                                                                        # 默认encoding是ASCII，具体用什么编码看网页

# 为了不每次都打开一个chrome  #这样实现了共用一个chrome，但这样spider关闭后chrome却没关闭
# from selenium import webdriver
# from scrapy.http import HtmlResponse
# class JSPageMiddleware(object):  #写好middleware后，要去settings.py中配置生效
# 
#     def __init__(self):
#         self.browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")  # 用属于类的browser
#         super(JSPageMiddleware, self).__init__()
#     
#     #通过chrome请求动态网页  #请求完成后会执行spider中的parse
#     def process_request(self, request, spider):
#         if spider.name == "jobbole_spider":  #用伯乐在线的爬虫测试
#             # browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")
#             self.browser.get(request.url)
#             import time
#             time.sleep(3)
#             print ("访问:{0}".format(request.url))
#             # 为了让download不重复下载，return HtmlRespons()  #遇到HtmlResponse，scrapy就不会向download发送，而是返回给spider
#             return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding="utf-8", request=request)
#                                                                                        # 默认encoding是ASCII，具体用什么编码看网页

# 把 def __init__(self): 放到spider里  #把browser放到spider里  #这样一个spider一个chrome
from selenium import webdriver
from scrapy.http import HtmlResponse
class JSPageMiddleware(object):  #写好middleware后，要去settings.py中配置生效
    #通过chrome请求动态网页  #请求完成后会执行spider中的parse  #scrapy是异步的，性能高。加入chrome后，性能降低  #要改成异步的，考虑重写download  https://github.com/flisky/scrapy-phantomjs-downloader
    def process_request(self, request, spider):
        if spider.name == "jobbole_spider":  #用伯乐在线的爬虫测试
            # browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")
            spider.browser.get(request.url)
            import time
            time.sleep(3)
            print ("访问:{0}".format(request.url))
            # 为了让download不重复下载，return HtmlRespons()  #遇到HtmlResponse，scrapy就不会向download发送，而是返回给spider
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)
#                                                                                       # 默认encoding是ASCII，具体用什么编码看网页



# test_scrapy_spider\test_scrapy_spider\settings.py
# -*- coding: utf-8 -*-

import os  #用于获取当前文件（setting.py）的路径

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
DOWNLOAD_DELAY = 10  #10秒下载一次
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False  #禁用cookie

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
    #'test_scrapy_spider.middlewares.RandomUserAgentMiddlware': 543,  # 配置 RandomUserAgentMiddlware
    #'test_scrapy_spider.middlewares.RandomProxyMiddleware': 544,
    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  #将默认的useragent取消
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'test_scrapy_spider.pipelines.JsonExporterPipeline': 2,  #数字越小，越先处理
    #'scrapy.pipelines.images.ImagesPipeline': 1
    #'test_scrapy_spider.pipelines.ArticleImagePipeline': 1,  #调用定制化的pipeline（ArticleImagePipeline）
    #'test_scrapy_spider.pipelines.MysqlPipeline': 1
    'test_scrapy_spider.pipelines.MysqlTwistedPipline': 1
}
IMAGES_URLS_FIELD = 'front_image_url'  #告诉images items中哪个是图片的url  #images需要接受一个数组
#os.path.dirname(__file__)  #获取当前文件的目录名称（test_scrapy_spider）  #__file__是当前文件（setting.py）的名称
project_dir =  os.path.abspath(os.path.dirname(__file__))  #获取当前文件的目录的路径
IMAGES_STORE = os.path.join(project_dir, 'images')  #图片下载的保存路径  可以配置为绝对路径  要存在工程目录下，可以使用相对路径。在settings.py的同级目录下新建images
                                                    #图片储存在 project_dir目录下的images文件夹
                                                    #要下载图片需要PIL库
                                                    #下cmd下安装PIL库
                                                    #pip install -i https://pypi.douban.com/simple pillow
# IMAGES_MIN_HEIGHT = 100 #设置下载图片的最小高度  #过滤图片可以在settng.py中设置
# IMAGES_MIN_WIDTH = 100
# '''如果要实现自己的需求，也可以重载相应的函数达到需求，在pipelines中建立类，继承ImagesPipeline就可以了'''

# 在F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider\settings.py 下，设置F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider 为根目录
# 因为虽然在eclipse里已经将 F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider 添加到path里了，但在cmd下还未添加
import sys  #import os  在上面写过了
# sys.path.insert(0, "F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider")  #将F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider 添加到path
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  #F:\eclipse\···\···\test_scrapy_spider  工程路径
sys.path.insert(0, os.path.join(BASE_DIR, 'test_scrapy_spider'))  #将F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider 添加到path里
             #放在第0个，会优先在F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider里找需要import的module
sys.path.insert(1, BASE_DIR)  #将F:\eclipse\···\···\test_scrapy_spider 添加到path里

# user_agent_list = [
#     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
# ]

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"

RANDOM_UA_TYPE = "random"  #选择要随机生成的ua类型（ie、Firefox、chrome等）  #random表示随机一种浏览器

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True  #自动控制下载速度
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
import datetime  #为了将文章的创建时间写入数据库，要把str类型的create_time转换为date类型
from scrapy.http import Request  #提取出url后，将url交给scrapy 下载    #from scrapy.http import Request
from urllib import parse  #如果是py2 那就是import urlparse
from items import JobboleArticleItem, ArticleItemLoader  #调用自定义的ItemLoader -->ArticleItemLoader
from utils.common import get_md5  #对url做MD5
from scrapy.loader import ItemLoader  #用itemloader便于维护
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals  #信号

class JobboleSpiderSpider(scrapy.Spider):
    name = 'jobbole_spider'
    allowed_domains = ['blog.jobbple.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']  #在这个list中我们可以放入需要爬取的url

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")  # 用属于类的browser
        super(JobboleSpiderSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)  #信号映射  #当spider关闭时（signals.spider_closed）-->关闭chrome（self.spider_closed）
    
    def spider_closed(self, spider):
        #当爬虫退出的时候关闭chrome
        print ("spider closed")
        self.browser.quit()  #关闭chrome


    def parse(self, response):  #每一个url都会进入到这个函数
        '''
        1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
        '''
        
        #解析列表页中的所有文章url并交给scrapy下载后并进行解析
        
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            #有时候取到的url不是一完整的域名，需要补全
            #response.url + post_url
            
            image_url = post_node.css('img::attr(src)').extract_first("")
            post_url = post_node.css('::attr(href)').extract_first("")
            
            #下面用urljoin来补全
            yield Request(url = parse.urljoin(response.url, post_url), meta = {'front_image_url':image_url}, callback = self.parse_detail)
            #用 yield 就可以把Request 交给scrapy下载
            #无法进入parse_detail -->进入Request， 将dont_filter=True设为True
            #Request中meta参数的作用是传递信息给下一个函数
            #print(post_url)
            
        #提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        #.next 与 .page-numbers间没有空格，代表匹配同时有（.next 和.page-numbers）的class
        if next_url:
            yield Request(url = parse.urljoin(response.url, next_url), callback = self.parse)
            
            
            
    def parse_detail(self, response):
        #提取文章具体字段(xpath)
#         title = response.xpath('//*[@id="post-113789"]/div[1]/h1/text()').extract()[0]
#         
#         create_date = response.xpath('//*[@id="post-113789"]/div[2]/p/text()[1]').extract()[0].strip().replace('·', '').strip()
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
#         tag_list = [element for element in tag_list if not element.strip().endswith('评论')] 
#         tags = ','.join(tag_list)
        
        
        
        #以下通过css选择器提取字段
#         article_item = JobboleArticleItem()  #实例化
#         
#         front_image_url = response.meta.get('front_image_url', '')  #get key=front_image_url 的值，如果没有key=front_image_url，回传''(空)
#         #文章封面图
#         
#         title = response.css('.entry-header h1::text').extract()[0]
#         
#         create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·', '').strip()
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
#         tag_list = [element for element in tag_list if not element.strip().endswith('评论')] 
#         tags = ','.join(tag_list)
#         
#         #填充值到items
#         article_item['title'] = title
#         article_item['url'] = response.url
#         article_item['url_object_id'] = get_md5(response.url)  #对url做MD5
#         
#         try:  #为了将文章的创建时间写入数据库，要把str类型的create_time转换为date类型
#             create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()  #将格式为%Y/%m/%d 的str类型转换为date类型
#         except Exception as e:
#             create_date = datetime.datetime.now().date()
#         article_item['create_date'] = create_date
#         
#         article_item['front_image_url'] = [front_image_url]  #images需要接受一个数组
#         article_item['praise_nums'] = praise_nums
#         article_item['fav_nums'] = fav_nums
#         article_item['comment_nums'] = comment_nums
#         article_item['tags'] = tags
#         article_item['content'] = content
        
        #通过itemLoader加载item
        front_image_url = response.meta.get('front_image_url', '')  #get key=front_image_url 的值，如果没有key=front_image_url，回传''(空)
        #item_loader = ItemLoader(item=JobboleArticleItem(), response=response)  #定义ItemLoader实例
        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)  #改用自定义的 ItemLoader
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
        #调用默认的item方法的话会有两个问题：1.值都是list 2.还需要对取出的值行进处理（做re的提取等）
        #-->去修改items.py  #1.在items.py 的Field()里面用TakeFirst进行处理  2.在items.py 的Field()里面用MapCompose进行处理
        
        yield article_item  #调用yield之后，item会传递到pipelines.py

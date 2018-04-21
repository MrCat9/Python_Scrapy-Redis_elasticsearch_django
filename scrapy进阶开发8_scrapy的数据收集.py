# 数据收集(Stats Collection)  文档  http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/stats.html
# 摘自http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/stats.html
# Scrapy提供了方便的收集数据的机制。数据以key/value方式存储，值大多是计数值。
# 该机制叫做数据收集器(Stats Collector)，可以通过 Crawler API 的属性 stats 来使用。
# 在下面的章节常见数据收集器使用方法将给出例子来说明。

# 获取数据:
>>> stats.get_value('pages_crawled')
8

# 获取所有数据:
>>> stats.get_stats()
{'pages_crawled': 1238, 'start_time': datetime.datetime(2009, 7, 14, 21, 47, 28, 977139)}

# 设置数据:
stats.set_value('hostname', socket.gethostname())

# 当新的值比原来的值大时设置数据:
stats.max_value('max_items_scraped', value)

# 无论数据收集(stats collection)开启或者关闭，数据收集器永远都是可用的。
# 因此您可以import进自己的模块并使用其API(增加值或者设置新的状态键(stat keys))。
# 该做法是为了简化数据收集的方法: 您不应该使用超过一行代码来收集您的spider，Scrpay扩展或任何您使用数据收集器代码里头的状态。

# C:\Users\admin\AppData\Local\Programs\Python\Python36\Lib\site-packages\scrapy\statscollectors.py
"""
Scrapy extension for collecting scraping stats
"""
import pprint
import logging

logger = logging.getLogger(__name__)


class StatsCollector(object):

    def __init__(self, crawler):
        self._dump = crawler.settings.getbool('STATS_DUMP')
        self._stats = {}

    def get_value(self, key, default=None, spider=None):
        return self._stats.get(key, default)

    def get_stats(self, spider=None):
        return self._stats

    def set_value(self, key, value, spider=None):
        self._stats[key] = value

    def set_stats(self, stats, spider=None):
        self._stats = stats

    def inc_value(self, key, count=1, start=0, spider=None):
        d = self._stats
        d[key] = d.setdefault(key, start) + count

    def max_value(self, key, value, spider=None):
        self._stats[key] = max(self._stats.setdefault(key, value), value)

    def min_value(self, key, value, spider=None):
        self._stats[key] = min(self._stats.setdefault(key, value), value)

    def clear_stats(self, spider=None):
        self._stats.clear()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider, reason):
        if self._dump:
            logger.info("Dumping Scrapy stats:\n" + pprint.pformat(self._stats),
                        extra={'spider': spider})
        self._persist_stats(self._stats, spider)

    def _persist_stats(self, stats, spider):
        pass


class MemoryStatsCollector(StatsCollector):

    def __init__(self, crawler):
        super(MemoryStatsCollector, self).__init__(crawler)
        self.spider_stats = {}

    def _persist_stats(self, stats, spider):
        self.spider_stats[spider.name] = stats


class DummyStatsCollector(StatsCollector):

    def get_value(self, key, default=None, spider=None):
        return default

    def set_value(self, key, value, spider=None):
        pass

    def set_stats(self, stats, spider=None):
        pass

    def inc_value(self, key, count=1, start=0, spider=None):
        pass

    def max_value(self, key, value, spider=None):
        pass

    def min_value(self, key, value, spider=None):
        pass



# 测试数据收集器
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
    start_urls = ['http://blog.jobbole.com/all-posts/test404']  #在这个list中我们可以放入需要爬取的url

#     def __init__(self):
#         self.browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")  # 用属于类的browser
#         super(JobboleSpiderSpider, self).__init__()
#         dispatcher.connect(self.spider_closed, signals.spider_closed)  #信号映射  #当spider关闭时（signals.spider_closed）-->关闭chrome（self.spider_closed）
#     
#     def spider_closed(self, spider):
#         #当爬虫退出的时候关闭chrome
#         print ("spider closed")
#         self.browser.quit()  #关闭chrome

    #收集伯乐在线所有404的url以及404页面数  #测试数据收集器  #spider默认情况下只处理200--300之间的页面
    handle_httpstatus_list = [404]  #处理404

    def __init__(self):
        self.fail_urls = []  #保存404的页面


    def parse(self, response):  #每一个url都会进入到这个函数
        '''
        1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
        '''
        
        #解析列表页中的所有文章url并交给scrapy下载后并进行解析
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")  #变量值+1
        
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
    #'test_scrapy_spider.middlewares.JSPageMiddleware': 1,
    'test_scrapy_spider.middlewares.RandomUserAgentMiddlware': 543,  # 配置 RandomUserAgentMiddlware
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



# 可以在 self下看到 fail_urls	<class 'list'>: ['http://blog.jobbole.com/all-posts/test404']	
# 可以在 self下的crawler下的stats下的_stats看到 'failed_url' (2323284819888)	int: 1	

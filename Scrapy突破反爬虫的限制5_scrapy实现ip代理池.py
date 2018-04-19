# 百度本机ip可以查到出口ip

# cmder下查看本机ip
C:\Users\admin
λ ipconfig



# 代理ip原理
# http://www.xicidaili.com/  西刺免费代理IP



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
        request.meta["proxy"] = "http://39.77.104.193:8118"  #设置ip代理  # http://(ip):(端口号)



#
# -*- coding: utf-8 -*-

list = [(1, "a"), (2, "b"), (3, "c")]

print(list)  #[(1, 'a'), (2, 'b'), (3, 'c')]

print(list[2][1])  #c



# 为了设置ip地址代理池，需要爬取http://www.xicidaili.com/  西刺免费代理IP  上的ip
# 在工程目录 F:\eclipse\···\···\test_scrapy_spider 下新建tools
# tools下新建 crawl_xici_ip.py  用于爬取西刺的高匿代理ip
# test_scrapy_spider\tools\crawl_xici_ip.py
# -*- coding: utf-8 -*-

import requests
from scrapy.selector import Selector  #用于解析网页
import MySQLdb

conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="article_spider", charset="utf8")  #连接数据库
cursor = conn.cursor()


def crawl_ips():
    #爬取西刺的免费ip代理
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    for i in range(2920):  #页数  #第i页
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)

        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")  #取出每一行


        ip_list = []  #存放ip
        for tr in all_trs[1:]:  #从第二行开始迭代，因为第一行是表头
            speed_str = tr.css(".bar::attr(title)").extract()[0]  #取这个ip的速度，用于过滤掉太慢的ip
            if speed_str:
                speed = float(speed_str.split("秒")[0])  #取出速度（str），然后转成float
            all_texts = tr.css("td::text").extract()  #取这一行的所有信息

            ip = all_texts[0]  #取这一行的ip
            port = all_texts[1]  #取这一行的端口号
            proxy_type = all_texts[5]  #取这一行的代理类型（HTTP、HTTPS）

            ip_list.append((ip, port, proxy_type, speed))  #添加  #传tuple进去

        for ip_info in ip_list:  # 每提取完一页，写入数据库
            cursor.execute(                                          #str    str   float  str
                "insert proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, 'HTTP') ON DUPLICATE KEY UPDATE port=VALUES(port)".format(
                    ip_info[0], ip_info[1], ip_info[3]
                )
            )

            conn.commit()  #提交

# print (crawl_ips())  #测试是否能够写入数据库

class GetIP(object):  #取出数据库中的ip
    def delete_ip(self, ip):
        #从数据库中删除无效的ip
        delete_sql = """
            delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)  #执行sql语句
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        #判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http":proxy_url,
                # "https":proxy_url2  #也可以添加https的代理
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:  #try执行完有错误跳到except，没错误跳到else
            print ("invalid ip and port")
            self.delete_ip(ip)  #删除无效ip
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:  #200以内都是成功访问  #是有效的ip
                print ("effective ip")
                return True
            else:  #没有异常，但返回的状态码错误，也是无效ip
                print  ("invalid ip and port")
                self.delete_ip(ip)
                return False


    def get_random_ip(self):
        #从数据库中随机获取一个可用的ip
        random_sql = """
              SELECT ip, port FROM proxy_ip
            ORDER BY RAND()
            LIMIT 1
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():  # cursor.fetchall()返回tuple
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)  #返回有效的代理ip
            else:
                return self.get_random_ip()  #取到无效的ip，就重新取



if __name__ == "__main__":
    get_ip = GetIP()
    print(get_ip.get_random_ip())



# 在数据库article_spider的tables下，新建表 proxy_ip
Field Name              Datatype        Len         Default     PK?     Not Null
ip                      varchar         20                       √         √
port                    varchar         10                                 √
speed                   float
proxy_type              varchar         5

# sql语句  SELECT + 表字段名 + FROM +数据表名+ WHERE + 筛选条件



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
    'test_scrapy_spider.middlewares.RandomUserAgentMiddlware': 543,  # 配置 RandomUserAgentMiddlware
    'test_scrapy_spider.middlewares.RandomProxyMiddleware': 544,
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



# https://github.com/aivarsk/scrapy-proxies 开源的库-->设置代理ip

# https://github.com/scrapy-plugins/scrapy-crawlera    -->设置代理ip

# http://www.theonionrouter.com/    tor，洋葱浏览器


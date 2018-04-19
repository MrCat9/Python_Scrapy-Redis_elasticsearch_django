# �ٶȱ���ip���Բ鵽����ip

# cmder�²鿴����ip
C:\Users\admin
�� ipconfig



# ����ipԭ��
# http://www.xicidaili.com/  ������Ѵ���IP



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
        request.meta["proxy"] = "http://39.77.104.193:8118"  #����ip����  # http://(ip):(�˿ں�)



#
# -*- coding: utf-8 -*-

list = [(1, "a"), (2, "b"), (3, "c")]

print(list)  #[(1, 'a'), (2, 'b'), (3, 'c')]

print(list[2][1])  #c



# Ϊ������ip��ַ����أ���Ҫ��ȡhttp://www.xicidaili.com/  ������Ѵ���IP  �ϵ�ip
# �ڹ���Ŀ¼ F:\eclipse\������\������\test_scrapy_spider ���½�tools
# tools���½� crawl_xici_ip.py  ������ȡ���̵ĸ������ip
# test_scrapy_spider\tools\crawl_xici_ip.py
# -*- coding: utf-8 -*-

import requests
from scrapy.selector import Selector  #���ڽ�����ҳ
import MySQLdb

conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="article_spider", charset="utf8")  #�������ݿ�
cursor = conn.cursor()


def crawl_ips():
    #��ȡ���̵����ip����
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    for i in range(2920):  #ҳ��  #��iҳ
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)

        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")  #ȡ��ÿһ��


        ip_list = []  #���ip
        for tr in all_trs[1:]:  #�ӵڶ��п�ʼ��������Ϊ��һ���Ǳ�ͷ
            speed_str = tr.css(".bar::attr(title)").extract()[0]  #ȡ���ip���ٶȣ����ڹ��˵�̫����ip
            if speed_str:
                speed = float(speed_str.split("��")[0])  #ȡ���ٶȣ�str����Ȼ��ת��float
            all_texts = tr.css("td::text").extract()  #ȡ��һ�е�������Ϣ

            ip = all_texts[0]  #ȡ��һ�е�ip
            port = all_texts[1]  #ȡ��һ�еĶ˿ں�
            proxy_type = all_texts[5]  #ȡ��һ�еĴ������ͣ�HTTP��HTTPS��

            ip_list.append((ip, port, proxy_type, speed))  #���  #��tuple��ȥ

        for ip_info in ip_list:  # ÿ��ȡ��һҳ��д�����ݿ�
            cursor.execute(                                          #str    str   float  str
                "insert proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, 'HTTP') ON DUPLICATE KEY UPDATE port=VALUES(port)".format(
                    ip_info[0], ip_info[1], ip_info[3]
                )
            )

            conn.commit()  #�ύ

# print (crawl_ips())  #�����Ƿ��ܹ�д�����ݿ�

class GetIP(object):  #ȡ�����ݿ��е�ip
    def delete_ip(self, ip):
        #�����ݿ���ɾ����Ч��ip
        delete_sql = """
            delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)  #ִ��sql���
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        #�ж�ip�Ƿ����
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http":proxy_url,
                # "https":proxy_url2  #Ҳ�������https�Ĵ���
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:  #tryִ�����д�������except��û��������else
            print ("invalid ip and port")
            self.delete_ip(ip)  #ɾ����Чip
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:  #200���ڶ��ǳɹ�����  #����Ч��ip
                print ("effective ip")
                return True
            else:  #û���쳣�������ص�״̬�����Ҳ����Чip
                print  ("invalid ip and port")
                self.delete_ip(ip)
                return False


    def get_random_ip(self):
        #�����ݿ��������ȡһ�����õ�ip
        random_sql = """
              SELECT ip, port FROM proxy_ip
            ORDER BY RAND()
            LIMIT 1
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():  # cursor.fetchall()����tuple
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)  #������Ч�Ĵ���ip
            else:
                return self.get_random_ip()  #ȡ����Ч��ip��������ȡ



if __name__ == "__main__":
    get_ip = GetIP()
    print(get_ip.get_random_ip())



# �����ݿ�article_spider��tables�£��½��� proxy_ip
Field Name              Datatype        Len         Default     PK?     Not Null
ip                      varchar         20                       ��         ��
port                    varchar         10                                 ��
speed                   float
proxy_type              varchar         5

# sql���  SELECT + ���ֶ��� + FROM +���ݱ���+ WHERE + ɸѡ����



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
    'test_scrapy_spider.middlewares.RandomProxyMiddleware': 544,
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



# https://github.com/aivarsk/scrapy-proxies ��Դ�Ŀ�-->���ô���ip

# https://github.com/scrapy-plugins/scrapy-crawlera    -->���ô���ip

# http://www.theonionrouter.com/    tor����������


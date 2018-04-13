#将数据保存到MySQL中



'''  datetime  #为了将文章的创建时间写入数据库，要把str类型的create_time转换为date类型
# -*- coding: utf-8 -*-

import datetime

print(datetime.datetime.now())  #2018-04-03 16:49:03.234972
print(datetime.datetime.now().__class__)  #<class 'datetime.datetime'>

print(datetime.datetime.now().date())  #2018-04-03
print(datetime.datetime.now().date().__class__)  #<class 'datetime.date'>

create_date = '1234/05/23'
print(datetime.datetime.strptime(create_date, '%Y/%m/%d'))  #1234-05-23 00:00:00
print(datetime.datetime.strptime(create_date, '%Y/%m/%d').__class__)  #<class 'datetime.datetime'>
print(datetime.datetime.strptime(create_date, '%Y/%m/%d').date())  #1234-05-23
#将格式为%Y/%m/%d 的str类型转换为date类型
print(datetime.datetime.strptime(create_date, '%Y/%m/%d').date().__class__)  #<class 'datetime.date'>
'''



#为了将文章的创建时间写入数据库，要把str类型的create_time转换为date类型，修改 jobbole_spider.py
# jobbole_spider.py    #要对工程test_jobbole 目录下的test_jobbole文件进行设置：右键-->PyDev-->Set as Source Folder (add to PYTHONPATH)
# -*- coding: utf-8 -*-
import scrapy
import re
import datetime  #为了将文章的创建时间写入数据库，要把str类型的create_time转换为date类型
from scrapy.http import Request  #提取出url后，将url交给scrapy 下载    #from scrapy.http import Request
from urllib import parse  #如果是py2 那就是import urlparse
from items import JobboleArticleItem
from utils.common import get_md5  #对url做MD5

class JobboleSpiderSpider(scrapy.Spider):
    name = 'jobbole_spider'
    allowed_domains = ['blog.jobbple.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']  #在这个list中我们可以放入需要爬取的url

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
        #提取文章具体字段
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
        article_item = JobboleArticleItem()  #实例化
        
        front_image_url = response.meta.get('front_image_url', '')  #get key=front_image_url 的值，如果没有key=front_image_url，回传''(空)
        #文章封面图
        
        title = response.css('.entry-header h1::text').extract()[0]
        
        create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·', '').strip()
        
        praise_nums = response.css('.vote-post-up h10::text').extract_first()
        if praise_nums:
            praise_nums = int(praise_nums[0])
        else:
            praise_nums = 0
        
        fav_nums = response.css('.bookmark-btn::text').extract()[0]
        match_re = re.match(r'.*?(\d+).*', fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        
        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(r'.*?(\d+).*', comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        
        content = response.css("div.entry").extract()[0]
        
        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith('评论')] 
        tags = ','.join(tag_list)
        
        #填充值到items
        article_item['title'] = title
        article_item['url'] = response.url
        article_item['url_object_id'] = get_md5(response.url)  #对url做MD5
        
        try:  #为了将文章的创建时间写入数据库，要把str类型的create_time转换为date类型
            create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()  #将格式为%Y/%m/%d 的str类型转换为date类型
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item['create_date'] = create_date
        
        article_item['front_image_url'] = [front_image_url]  #images需要接受一个数组
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['tags'] = tags
        article_item['content'] = content
        
        yield article_item  #调用yield之后，item会传递到pipelines.py
              
        pass



#新建数据库 article_spider
#新建表 jobbole_article
Field Name              Datatype        Len         Default     PK?     Not Null
title                   varchar         200                                √
create_date             date                        
url                     varchar         300                                √
url_object_id           varchar         50                      √          √
front_image_url         varchar         300         
front_image_path        varchar         200         
praise_nums             int             11          0                      √
fav_nums                int             11          0                      √
comment_nums            int             11          0                      √
tags                    varchar         200         
content                 longtext                                           √



#安装MySQL的驱动
#cmd下
pip install -i https://pypi.douban.com/simple/ mysqlclient



# pipelines.py
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs  #用codecs来完成文件的打开和写入
import json
from scrapy.exporters import JsonItemExporter  #将json文件输出
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi  #使MySQLdb的一些操作变成异步的操作

class TestJobbolePipeline(object):  #pipeline 主要用来做数据存储的   #这个pipeline的数字为300，大，后执行
    def process_item(self, item, spider):  #pipelines.py 会接受item  #要去settings.py中取消注释 ITEM_PIPELINES
        return item



class JsonWithEncodingPipeline(object):  #在setting.py里配置这个pipeline的数字为2
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf_8')
    
    def process_item(self, item, spider):  #pipelines.py 会接受item  在这里将item写入文件
        #调用process_item时要记得return item， 因为下一pipeline可能还需要处理item
        lines = json.dump(dict(item), ensure_ascii=False) + '\n'  #ensure_ascii=False 不设为False的话写入中文会出错，会直接写入Unicode
        self.file.write(lines)
        return item
    
    def spider_clsede(self, spider):  #当spider关闭时会调用这个函数
        self.file.close()



class MysqlPipeline(object):  #写好pipeline后，要把pipeline配置到setting.py中
    #采用同步的机制写入mysql  插入数据库的速度可能会小于spider的解析速度 -->考虑用异步
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'article_spider', charset='utf8', use_unicode=True)  #连接数据库
        #配置可以写到setting.py 中
        # MYSQL_HOST = "127.0.0.1"
        # MYSQL_USER = "root"
        # MYSQL_PASSWORD = "123456"
        # MYSQL_DBNAME = "article_spider"
        # MySQLdb.connect的参数
        # MySQLdb.connect('host', 'user', 'password', 'dbname', charset='utf8', use_unicode=True)
        # conn = pymysql.Connect(host='127.0.0.1', user='root', passwd='123456', port=3306, db='pymysql_test01')
        self.cursor = self.conn.cursor()
        
    def process_item(self, item, spider):  #重载 process_item方法
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()
        
        
        
class MysqlTwistedPipline(object):  #写好pipeline后，要把pipeline配置到setting.py中
    #'''异步插入mysql'''
    def __init__(self, dbpool):
        self.dbpool = dbpool
    
    @classmethod
    def from_settings(cls, settings):  #这个方法可以读取setting.py中的值   # cls指的是MysqlTwistedPipline 这个类
        #'''传入settings的参数'''
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)  #传入可变化的参数dbparms
        #dbpool = adbapi.ConnectionPool("MySQLdb", host = settings["MYSQL_HOST"], db = settings["MYSQL_DBNAME"], ……)
        
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)  #do_insert为要异步执行的函数  #item为要插入的数据
        query.addErrback(self.handle_error) #处理异常

    def handle_error(self, failure):  #异步错误处理函数
        # 处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        #self.conn.commit()  #会自动commit
        


class JsonExporterPipeline(object):  #将json文件输出    #在setting.py里配置这个pipeline的数字为2，进行测试
    def __init__(self):
        #调用scrapy提供的json export导出json文件
        self.file = open('articleexporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf_8', ensure_ascii=False)  #用JsonItemExporter 做实例化
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        
    def process_item(self, item, spider):  #pipelines.py 会接受item  在这里将item写入文件
        #调用process_item时要记得return item， 因为下一pipeline可能还需要处理item
        self.exporter.export_item(item)
        return item



class ArticleImagePipeline(ImagesPipeline):  #定制化pipeline  ArticleImagePipeline  #这个pipeline的数字为1，小，先执行
    def item_completed(self, results, item, info):  #重载 item_completed
        for ok, value in results:
            image_file_path = value['path']  #保存图片的本地路径
        item['front_image_path'] = image_file_path  #保存图片的本地路径到items
        return item
    
    
    
# setting.py
# -*- coding: utf-8 -*-

# Scrapy settings for test_jobbole project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'test_jobbole'

SPIDER_MODULES = ['test_jobbole.spiders']
NEWSPIDER_MODULE = 'test_jobbole.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'test_jobbole (+http://www.yourdomain.com)'

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
#    'test_jobbole.middlewares.TestJobboleSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'test_jobbole.middlewares.TestJobboleDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'test_jobbole.pipelines.JsonExporterPipeline': 2,  #数字越小，越先处理
    #'scrapy.pipelines.images.ImagesPipeline': 1
    #'test_jobbole.pipelines.ArticleImagePipeline': 1  #调用定制化的pipeline（ArticleImagePipeline）
    #'test_jobbole.pipelines.MysqlPipeline': 1
    'test_jobbole.pipelines.MysqlTwistedPipline': 1
}
IMAGES_URLS_FIELD = 'front_image_url'  #告诉images items中哪个是图片的url  #images需要接受一个数组
import os  #用于获取当前文件（setting.py）的路径
#os.path.dirname(__file__)  #获取当前文件的目录名称（test_jobbole）  #__file__是当前文件（setting.py）的名称
project_dir =  os.path.abspath(os.path.dirname(__file__))  #获取当前文件的目录的路径
IMAGES_STORE = os.path.join(project_dir, 'images')  #图片下载的保存路径  可以配置为绝对路径  要存在工程目录下，可以使用相对路径。在settings.py的同级目录下新建images
                                                    #图片储存在 project_dir目录下的images文件夹
                                                    #要下载图片需要PIL库
                                                    #下cmd下安装PIL库
                                                    #pip install -i https://pypi.douban.com/simple pillow
# IMAGES_MIN_HEIGHT = 100 #设置下载图片的最小高度  #过滤图片可以在settng.py中设置
# IMAGES_MIN_WIDTH = 100
# '''如果要实现自己的需求，也可以重载相应的函数达到需求，在pipelines中建立类，继承ImagesPipeline就可以了'''


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

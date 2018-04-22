# https://github.com/rmax/scrapy-redis



需要的环境：
Python 2.7, 3.4 or 3.5 
Redis >= 2.8 
Scrapy >= 1.1 
redis-py >= 2.10



# 安装python redis
C:\Users\admin
λ pip install redis



# scrapy-redis的使用

# 在 settings.py 中配置
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  #必须设置
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  #去重的class
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300  #item会序列化，发送到redis中
}

# 在 spider 中不能继承 scrapy.Spider
# 要继承redisspider
from scrapy_redis.spiders import RedisSpider

class MySpider(RedisSpider):
    name = 'myspider'

    def parse(self, response):
        # do stuff
        pass

# 现在启动的话request使用的就不是本地的scheduler，而是 scrapy-redis 的scheduler

# 启动spider后，
scrapy runspider myspider.py
#要往队列里放一个初始化的url
redis-cli lpush myspider:start_urls http://google.com



# 测试：
# 新建一个scrapy项目
# cmder下
C:\Users\admin
λ f:

F:\cmder\vendor\git-for-windows
λ cd F:\eclipse\···\···

F:\eclipse\···\···
λ scrapy startproject ScrapyRedisTest

# 将该项目导入eclipse中，把 F:\eclipse\···\···\ScrapyRedisTest 添加到pythonpath中

# 在github上拷贝scrapy-redis源码  https://github.com/rmax/scrapy-redis

# 将C:\Users\admin\Desktop\scrapy-redis-master\src\scrapy_redis 拷贝到 F:\eclipse\···\···\ScrapyRedisTest 下

# 新建spider  jobbole

# 不同spider使用不同redis list 

# scrapy-redis将原本scheduler的队列从内存放入redis中

# next_requests将向redis要



# ScrapyRedisTest\ScrapyRedisTest\spiders\jobbole.py
# -*- coding: utf8 -*-

from scrapy.http import Request  #提取出url后，将url交给scrapy 下载    #from scrapy.http import Request
from urllib import parse  #如果是py2 那就是import urlparse
from scrapy_redis.spiders import RedisSpider

from items import JobboleArticleItem, ArticleItemLoader  #调用自定义的ItemLoader -->ArticleItemLoader
from myUtils.common import get_md5  #对url做MD5
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals  #信号

class JobboleSpider(RedisSpider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbple.com']
    redis_key = 'jobbole:start_urls'
    
    #收集伯乐在线所有404的url以及404页面数  #测试数据收集器  #spider默认情况下只处理200--300之间的页面
    handle_httpstatus_list = [404]  #处理404

    def __init__(self, **kwargs):
        self.fail_urls = []  #保存404的页面
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)
        #当spider关闭信号发出时，调用handle_spider_closed

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))
        #当spider关闭信号发出时，将fail_urls这个list用","join成str后添加到stats的failed_urls中
        # spider关闭信号发出时，会打印所有stats

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






# 在settings.py中设置
ROBOTSTXT_OBEY = False
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}

# ScrapyRedisTest\ScrapyRedisTest\settings.py
# -*- coding: utf8 -*-

# Scrapy settings for ScrapyRedisTest project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os
import sys

BOT_NAME = 'ScrapyRedisTest'

SPIDER_MODULES = ['ScrapyRedisTest.spiders']
NEWSPIDER_MODULE = 'ScrapyRedisTest.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ScrapyRedisTest (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3  #3秒下载一次
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
#    'ScrapyRedisTest.middlewares.ScrapyredistestSpiderMiddleware': 543,
#}

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'ScrapyRedisTest.middlewares.JSPageMiddleware': 1,
    'ScrapyRedisTest.middlewares.RandomUserAgentMiddlware': 543,  # 配置 RandomUserAgentMiddlware
    #'ScrapyRedisTest.middlewares.RandomProxyMiddleware': 544,
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
    #'ScrapyRedisTest.pipelines.JsonExporterPipeline': 2,  #数字越小，越先处理
    #'scrapy.pipelines.images.ImagesPipeline': 1
    #'ScrapyRedisTest.pipelines.ArticleImagePipeline': 1,  #调用定制化的pipeline（ArticleImagePipeline）
    #'ScrapyRedisTest.pipelines.MysqlPipeline': 1
    'ScrapyRedisTest.pipelines.MysqlTwistedPipline': 1
}
IMAGES_URLS_FIELD = 'front_image_url'  #告诉images items中哪个是图片的url  #images需要接受一个数组
#os.path.dirname(__file__)  #获取当前文件的目录名称（ScrapyRedisTest）  #__file__是当前文件（setting.py）的名称
project_dir =  os.path.abspath(os.path.dirname(__file__))  #获取当前文件的目录的路径
IMAGES_STORE = os.path.join(project_dir, 'images')  #图片下载的保存路径  可以配置为绝对路径  要存在工程目录下，可以使用相对路径。在settings.py的同级目录下新建images
                                                    #图片储存在 project_dir目录下的images文件夹
                                                    #要下载图片需要PIL库
                                                    #下cmd下安装PIL库
                                                    #pip install -i https://pypi.douban.com/simple pillow
# IMAGES_MIN_HEIGHT = 100 #设置下载图片的最小高度  #过滤图片可以在settng.py中设置
# IMAGES_MIN_WIDTH = 100
# '''如果要实现自己的需求，也可以重载相应的函数达到需求，在pipelines中建立类，继承ImagesPipeline就可以了'''

# 在F:\eclipse\···\···\ScrapyRedisTest\ScrapyRedisTest\settings.py 下，设置F:\eclipse\···\···\ScrapyRedisTest\ScrapyRedisTest 为根目录
# 因为虽然在eclipse里已经将 F:\eclipse\···\···\ScrapyRedisTest\ScrapyRedisTest 添加到path里了，但在cmd下还未添加
# sys.path.insert(0, "F:\eclipse\···\···\ScrapyRedisTest\ScrapyRedisTest")  #将F:\eclipse\···\···\ScrapyRedisTest\ScrapyRedisTest 添加到path
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  #F:\eclipse\···\···\ScrapyRedisTest  工程路径
sys.path.insert(0, os.path.join(BASE_DIR, 'ScrapyRedisTest'))  #将F:\eclipse\···\···\ScrapyRedisTest\ScrapyRedisTest 添加到path里
#             #放在第0个，会优先在F:\eclipse\···\···\ScrapyRedisTest\ScrapyRedisTest里找需要import的module
sys.path.insert(1, BASE_DIR)  #将F:\eclipse\···\···\ScrapyRedisTest 添加到path里

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






# ScrapyRedisTest\ScrapyRedisTest\items.py
# -*- coding: utf8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join  #用来对传入的值进行处理
import datetime
from scrapy.loader import ItemLoader  #为了不每个都要写outputoutput_processor = TakeFirst() 我们自定一个itemloader  与是要重载类ItemLoader
import re
from myUtils.common import extract_num
from ScrapyRedisTest.settings import SQL_DATETIME_FORMAT

from w3lib.html import remove_tags

class ScrapyredistestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def add_jobbole(value):  #传过来的value是一个str
    return value+"-jobbole"


def date_convert(value):
    value = value.strip().replace('·', '').strip()  #create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·', '').strip()
#                 #.strip()可以去掉str头尾的空格  #.replace('·', '')可以替换str中的，为空
    try:  #为了将文章的创建时间写入数据库，要把str类型的create_time转换为date类型
        create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()  #将格式为%Y/%m/%d 的str类型转换为date类型
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

def get_nums(value):
    match_re = re.match(r'.*?(\d+).*', value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums
    
    
def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value    
    

def return_value(value):
    return value



class ArticleItemLoader(ItemLoader):  #自定义itemloader
    default_output_processor = TakeFirst()  #这样就不用每个都写outputoutput_processor = TakeFirst()



class JobboleArticleItem(scrapy.Item):
#     title = scrapy.Field(
#         #input_processor = MapCompose(add_jobbole)  #title 会作为value 传递到add_jobbole方法中
#         #input_processor = MapCompose(lambda x:x+"--jobbole")
#         input_processor = MapCompose(lambda x:x+"--jobbole", add_jobbole),  #title中的每个值依次从左到右调用了两个函数
#         #output_processor = TakeFirst()
#         )
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),  #处理完后是一个list， list里有date
        #output_processor = TakeFirst()  #取出date， 使list类变成date类
        )
    url = scrapy.Field()
    url_object_id = scrapy.Field()  #url 进行md5处理，变成相同长度
    front_image_url = scrapy.Field(  #下载封面图片要在settings.py 中的 ITEM_PIPELINES 进行配置  #front_image_url 需要接收一个list  因为images需要接受一个数组
        output_processor = MapCompose(return_value)  #覆盖掉default_output_processor = TakeFirst() 使得传入的是一个list
        )
# """  settings.py 下
# ITEM_PIPELINES = {
#     'ScrapyRedisTest.pipelines.TestJobbolePipeline': 300,  #数字越小，越先处理
#     #'scrapy.pipelines.images.ImagesPipeline': 1
#     'ScrapyRedisTest.pipelines.ArticleImagePipeline': 1  #调用定制化的pipeline（ArticleImagePipeline）
# }
# IMAGES_URLS_FIELD = 'front_image_url'  #告诉images, items中哪个是图片的url  #images需要接受一个数组
# import os  #用于获取当前文件（setting.py）的路径
# #os.path.dirname(__file__)  #获取当前文件的目录名称（ScrapyRedisTest）  #__file__是当前文件（setting.py）的名称
# project_dir =  os.path.abspath(os.path.dirname(__file__))  #获取当前文件的目录的路径
# IMAGES_STORE = os.path.join(project_dir, 'images')  #图片下载的保存路径  可以配置为绝对路径  要存在工程目录下，可以使用相对路径。在settings.py的同级目录下新建images
#                                                     #图片储存在 project_dir目录下的images文件夹
#                                                     #要下载图片需要PIL库
#                                                     #下cmd下安装PIL库
#                                                     #pip install -i https://pypi.douban.com/simple pillow
# # IMAGES_MIN_HEIGHT = 100 #设置下载图片的最小高度  #过滤图片可以在settng.py中设置
# # IMAGES_MIN_WIDTH = 100
# # '''如果要实现自己的需求，也可以重载相应的函数达到需求，在pipelines中建立类，继承ImagesPipeline就可以了'''                              
# """
    front_image_path = scrapy.Field()  #本地图片路径
    praise_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
        )
    fav_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
        )
    comment_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
        )
    tags = scrapy.Field(  #这边的tags其实是tag_list，是一个list
        input_processor = MapCompose(remove_comment_tags),  #去掉tag中提取的评论
        output_processor = Join(',')  #不能用TakeFirst()，要用join，Join(',')中的','是在指定连接符
        )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                insert into jobbole_article(title, create_date, url, url_object_id, fav_nums, front_image_url, front_image_path, praise_nums, comment_nums, tags, content)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE fav_nums=VALUES(fav_nums), praise_nums=VALUES(praise_nums), comment_nums=VALUES(comment_nums)
            """
        params = (self["title"], self["create_date"], self["url"], self["url_object_id"], self["fav_nums"], self["front_image_url"], 'self["front_image_path"]', self["praise_nums"], self["comment_nums"], self["tags"], self["content"])

        return insert_sql, params



class ZhihuQuestionItem(scrapy.Item):
    #知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        #插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_question(zhihu_id, topics, url, title, content, create_time, update_time, answer_num, comments_num, watch_user_num, click_num, crawl_time, crawl_update_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
              watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)            
        """
        #以下对数组 list [] 进行处理
        #zhihu_id = int("".join(self["zhihu_id"]))
        zhihu_id = self["zhihu_id"][0]  #zhihu_id在zhihu.py中已经处理成int了
        topics = ",".join(self["topics"])
        #url = "".join(self["url"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))  #在utils里的common.py里定义方法extract_num  #用来提取数字
        comments_num = extract_num("".join(self["comments_num"]))

        if len(self["watch_user_num"]) == 2:
            self["watch_user_num"] = [x.replace(',', '') for x in self["watch_user_num"]]  #去掉['3,110', '824,551']中的,
            watch_user_num = int(self["watch_user_num"][0])
            click_num = int(self["watch_user_num"][1])
        else:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = 0

        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)  #strftime(SQL_DATETIME_FORMAT)可以把time类型转化成str类型  # (SQL_DATETIME_FORMAT)可以在settings.py中指定要转为哪种格式

#         create_time = datetime.datetime.now().date()  #填充date，使得数据库可以插入
#         update_time = datetime.datetime.now().date()
#         crawl_update_time = datetime.datetime.now().date()
        create_time = None  #填充date，使得数据库可以插入
        update_time = None
        crawl_update_time = None
        
        params = (zhihu_id, topics, url, title, content, create_time, update_time, answer_num, comments_num,
                  watch_user_num, click_num, crawl_time, crawl_update_time)

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    #知乎的问题回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        #插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, parise_num, comments_num,
              create_time, update_time, crawl_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), parise_num=VALUES(parise_num),
              update_time=VALUES(update_time)
        """
        # ON DUPLICATE KEY UPDATE当主键冲突时，更新……

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)  #从json传过来时，create_time是int类型的
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)  #从json传过来时，update_time是int类型的
        #.fromtimestamp可以把int转化成datetime  #.strftime把datetime转化成自定义模式（SQL_DATETIME_FORMAT）的字符串
        
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["parise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params



def remove_splash(value):
    #去掉工作城市的斜线
    return value.replace("/","")

def handle_jobaddr(value):  #value='\n                                                北京 -\n             海淀区\n                - 北京市海淀区科学院南路2号融科资讯中心A座316\n                              查看地图\n        '
    addr_list = value.split("\n")  #以\n为界，将str划分成list
    addr_list = [item.strip() for item in addr_list if item.strip()!="查看地图"]  #处理list，去掉空格和查看地图
    return "".join(addr_list)  #用空将处理过的list连成str

class LagouJobItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    #拉勾网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor = Join(",")
    )
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into lagou_job(title, url, url_object_id, salary, job_city, work_years, degree_need,
            job_type, publish_time, job_advantage, job_desc, job_addr, company_name, company_url,
            tags, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE salary=VALUES(salary), job_desc=VALUES(job_desc), publish_time=VALUES(publish_time)
        """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary"], self["job_city"],
            self["work_years"], self["degree_need"], self["job_type"],
            self["publish_time"], self["job_advantage"], self["job_desc"],
            self["job_addr"], self["company_name"], self["company_url"],
            self["tags"], self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params






# ScrapyRedisTest\ScrapyRedisTest\pipelines.py
# -*- coding: utf8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs  #用codecs来完成文件的打开和写入
import json
from scrapy.exporters import JsonItemExporter  #将json文件输出
import MySQLdb.cursors
from twisted.enterprise import adbapi  #使MySQLdb的一些操作变成异步的操作

class ScrapyredistestPipeline(object):
    def process_item(self, item, spider):
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
    
    def spider_closed(self, spider):  #当spider关闭时会调用这个函数
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
            insert into jobbole_article(title, create_date, url, url_object_id, fav_nums, front_image_url, front_image_path, praise_nums, comment_nums, tags, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"], item["fav_nums"], item["front_image_url"], 'item["front_image_path"]', item["praise_nums"], item["comment_nums"], item["tags"], item["content"]))
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
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):  #异步错误处理函数
        # 处理异步插入的异常
        print (failure)

#     def do_insert(self, cursor, item):
#         #执行具体的插入
#         #根据不同的item 构建不同的sql语句并插入到mysql中  #也可以在items.py里的class JobBoleArticleItem(scrapy.Item): 进行处理
#         if item.__class__.__name__ == "JobboleArticleItem":  #取当前实例的class的name
#             insert_sql = """
#                 insert into jobbole_article(title, create_date, url, url_object_id, fav_nums, front_image_url, front_image_path, praise_nums, comment_nums, tags, content)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"], item["fav_nums"], item["front_image_url"], 'item["front_image_path"]', item["praise_nums"], item["comment_nums"], item["tags"], item["content"]))
#             #TypeError: not all arguments converted during string formatting
#             #前后参数的数量不一致   如： %s的个数与后面传入的参数的个数不一致
#             #self.conn.commit()  #会自动commit

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中  #也可以在items.py里的class JobBoleArticleItem(scrapy.Item): 进行处理
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class JsonExporterPipeline(object):  #将json文件输出    #在setting.py里配置这个pipeline的数字为2，进行测试
    #调用scrapy提供的json export导出json文件
    def __init__(self):
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
        if 'front_image_path' in item:  #可能没有封面   #item类似于一个dict
            for ok, value in results:
                image_file_path = value['path']  #保存图片的本地路径
            item['front_image_path'] = image_file_path  #保存图片的本地路径到items
        return item






# ScrapyRedisTest\ScrapyRedisTest\middlewares.py
# -*- coding: utf8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent

from myTools.crawl_xici_ip import GetIP  #将F:\eclipse\···\···\ScrapyRedisTest 添加到path里后才能import  
#在settings.py里配置 sys.path.insert(1, BASE_DIR)  #将F:\eclipse\···\···\ScrapyRedisTest 添加到path里
#在eclipse下可以右键工程目录-->PyDev-->set as source folder (add to PYTHONPATH)


class ScrapyredistestSpiderMiddleware(object):
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


class ScrapyredistestDownloaderMiddleware(object):
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

# from pyvirtualdisplay import Display
# from selenium import webdriver
# display = Display(visible=0, size=(800, 600))  # visible=0 --> 不显示
# display.start()
# 
# browser = webdriver.Chrome()
# browser.get()






# ScrapyRedisTest\ScrapyRedisTest\myUtils\common.py
# -*- coding: utf8 -*-
import hashlib
import re

def get_md5(url):    # MD5摘要生成
    if isinstance(url, str):  #python中str == Unicode #判断是不是str，其实是判断是不是Unicode，python3中默认是Unicode编码
        url = url.encode(encoding='utf_8')  #如果是Unicode，则转换成utf-8，哈希只认utf-8
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()                      

def extract_num(text):
    #从字符串中提取出数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

if __name__ == "__main__":
    print(get_md5("http://jobbole.com".encode(encoding='utf_8')))  #注意：Unicode-objects must be encoded before hashing
    # 0efdf49af511fd88681529ef8c2e5fbf






# ScrapyRedisTest\ScrapyRedisTest\myTools\crawl_xici_ip.py
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






# ScrapyRedisTest\main.py
# -*- coding: utf-8 -*-

from scrapy.cmdline import execute  #调用这个函数可以执行scrapy的脚本

# import sys
# sys.path.append('F:\eclipse\···\···\ScrapyRedisTest')  #设置工程的目录  #复制工程ScrapyRedisTest的路径

import sys
import os
# os.path.abspath(__file__)  #获取当前文件的路径
# os.path.dirname(os.path.abspath(__file__))  #获取当前文件的文件夹的路径
print(os.path.abspath(__file__))  #F:\eclipse\···\···\ScrapyRedisTest\main.py
print(os.path.dirname(os.path.abspath(__file__)))  #F:\eclipse\···\···\ScrapyRedisTest
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  #设置工程的目录

execute(['scrapy', 'crawl', 'jobbole'])  #调用execute函数，执行scrapy命令



# ScrapyRedisTest\scrapy_redis\scheduler.py
import importlib
import six

from scrapy.utils.misc import load_object

from . import connection, defaults


# TODO: add SCRAPY_JOB support.
class Scheduler(object):
    """Redis-based scheduler

    Settings
    --------
    SCHEDULER_PERSIST : bool (default: False)
        Whether to persist or clear redis queue.
    SCHEDULER_FLUSH_ON_START : bool (default: False)
        Whether to flush redis queue on start.
    SCHEDULER_IDLE_BEFORE_CLOSE : int (default: 0)
        How many seconds to wait before closing if no message is received.
    SCHEDULER_QUEUE_KEY : str
        Scheduler redis key.
    SCHEDULER_QUEUE_CLASS : str
        Scheduler queue class.
    SCHEDULER_DUPEFILTER_KEY : str
        Scheduler dupefilter redis key.
    SCHEDULER_DUPEFILTER_CLASS : str
        Scheduler dupefilter class.
    SCHEDULER_SERIALIZER : str
        Scheduler serializer.

    """

    def __init__(self, server,
                 persist=False,
                 flush_on_start=False,
                 queue_key=defaults.SCHEDULER_QUEUE_KEY,
                 queue_cls=defaults.SCHEDULER_QUEUE_CLASS,
                 dupefilter_key=defaults.SCHEDULER_DUPEFILTER_KEY,
                 dupefilter_cls=defaults.SCHEDULER_DUPEFILTER_CLASS,
                 idle_before_close=0,
                 serializer=None):
        """Initialize scheduler.

        Parameters
        ----------
        server : Redis
            The redis server instance.
        persist : bool
            Whether to flush requests when closing. Default is False.
        flush_on_start : bool
            Whether to flush requests on start. Default is False.
        queue_key : str
            Requests queue key.
        queue_cls : str
            Importable path to the queue class.
        dupefilter_key : str
            Duplicates filter key.
        dupefilter_cls : str
            Importable path to the dupefilter class.
        idle_before_close : int
            Timeout before giving up.

        """
        if idle_before_close < 0:
            raise TypeError("idle_before_close cannot be negative")

        self.server = server
        self.persist = persist
        self.flush_on_start = flush_on_start
        self.queue_key = queue_key
        self.queue_cls = queue_cls
        self.dupefilter_cls = dupefilter_cls
        self.dupefilter_key = dupefilter_key
        self.idle_before_close = idle_before_close
        self.serializer = serializer
        self.stats = None

    def __len__(self):
        return len(self.queue)

    @classmethod
    def from_settings(cls, settings):
        kwargs = {
            'persist': settings.getbool('SCHEDULER_PERSIST'),
            'flush_on_start': settings.getbool('SCHEDULER_FLUSH_ON_START'),
            'idle_before_close': settings.getint('SCHEDULER_IDLE_BEFORE_CLOSE'),
        }

        # If these values are missing, it means we want to use the defaults.
        optional = {
            # TODO: Use custom prefixes for this settings to note that are
            # specific to scrapy-redis.
            'queue_key': 'SCHEDULER_QUEUE_KEY',
            'queue_cls': 'SCHEDULER_QUEUE_CLASS',
            'dupefilter_key': 'SCHEDULER_DUPEFILTER_KEY',
            # We use the default setting name to keep compatibility.
            'dupefilter_cls': 'DUPEFILTER_CLASS',
            'serializer': 'SCHEDULER_SERIALIZER',
        }
        for name, setting_name in optional.items():
            val = settings.get(setting_name)
            if val:
                kwargs[name] = val

        # Support serializer as a path to a module.
        if isinstance(kwargs.get('serializer'), six.string_types):
            kwargs['serializer'] = importlib.import_module(kwargs['serializer'])

        server = connection.from_settings(settings)
        # Ensure the connection is working.
        server.ping()

        return cls(server=server, **kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        instance = cls.from_settings(crawler.settings)
        # FIXME: for now, stats are only supported from this constructor
        instance.stats = crawler.stats
        return instance

    def open(self, spider):
        self.spider = spider

        try:
            self.queue = load_object(self.queue_cls)(
                server=self.server,
                spider=spider,
                key=self.queue_key % {'spider': spider.name},
                serializer=self.serializer,
            )
        except TypeError as e:
            raise ValueError("Failed to instantiate queue class '%s': %s",
                             self.queue_cls, e)

        self.df = load_object(self.dupefilter_cls).from_spider(spider)

        if self.flush_on_start:
            self.flush()
        # notice if there are requests already in the queue to resume the crawl
        if len(self.queue):
            spider.log("Resuming crawl (%d requests scheduled)" % len(self.queue))

    def close(self, reason):
        if not self.persist:
            self.flush()

    def flush(self):
        self.df.clear()
        self.queue.clear()

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):  #如果url错误且不在不要过滤的名单中 and url在爬取过的名单中
            self.df.log(request, self.spider)
            return False
        if self.stats:
            self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        self.queue.push(request)
        return True

    def next_request(self):
        block_pop_timeout = self.idle_before_close
        request = self.queue.pop(block_pop_timeout)
        if request and self.stats:
            self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
        return request

    def has_pending_requests(self):
        return len(self) > 0






# ScrapyRedisTest\scrapy_redis\dupefilter.py    #去重
import logging
import time

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from . import defaults
from .connection import get_redis_from_settings


logger = logging.getLogger(__name__)


# TODO: Rename class to RedisDupeFilter.
class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplicates filter.

    This class can also be used with default Scrapy's scheduler.

    """

    logger = logger

    def __init__(self, server, key, debug=False):
        """Initialize the duplicates filter.

        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        key : str
            Redis key Where to store fingerprints.
        debug : bool, optional
            Whether to log filtered requests.

        """
        self.server = server
        self.key = key
        self.debug = debug
        self.logdupes = True

    @classmethod
    def from_settings(cls, settings):
        """Returns an instance from given settings.

        This uses by default the key ``dupefilter:<timestamp>``. When using the
        ``scrapy_redis.scheduler.Scheduler`` class, this method is not used as
        it needs to pass the spider name in the key.

        Parameters
        ----------
        settings : scrapy.settings.Settings

        Returns
        -------
        RFPDupeFilter
            A RFPDupeFilter instance.


        """
        server = get_redis_from_settings(settings)
        # XXX: This creates one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        # TODO: Use SCRAPY_JOB env as default and fallback to timestamp.
        key = defaults.DUPEFILTER_KEY % {'timestamp': int(time.time())}
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(server, key=key, debug=debug)

    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.

        Parameters
        ----------
        crawler : scrapy.crawler.Crawler

        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.

        """
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        """Returns True if request was already seen.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        bool

        """
        fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        added = self.server.sadd(self.key, fp)
        return added == 0

    def request_fingerprint(self, request):  #生成request的指纹，用来查重
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)

    @classmethod
    def from_spider(cls, spider):
        settings = spider.settings
        server = get_redis_from_settings(settings)
        dupefilter_key = settings.get("SCHEDULER_DUPEFILTER_KEY", defaults.SCHEDULER_DUPEFILTER_KEY)
        key = dupefilter_key % {'spider': spider.name}
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(server, key=key, debug=debug)

    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.

        Parameters
        ----------
        reason : str, optional

        """
        self.clear()

    def clear(self):
        """Clears fingerprints data."""
        self.server.delete(self.key)

    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False






# Telnet console listening on 127.0.0.1:6023
# 运行后，即使没有url，也不会像单机爬虫那样关闭爬虫，而是会继续监听 127.0.0.1:6023

# cmder下
127.0.0.1:6379> lpush jobbole:start_urls http://blog.jobbole.com/all-posts  # lpush进去后，会立刻被spider取到
(integer) 1
127.0.0.1:6379> keys *
1) "name"
2) "mykey"
3) "course_set2"
4) "jobbole:start_urls"        #
5) "zcourses_set"
6) "myhash"
7) "courses"
8) "course_set"

# 为了查看redis中url的情况，在 ScrapyRedisTest\scrapy_redis\scheduler.py 下的 def next_request(self): 中打个断点
127.0.0.1:6379> keys *
1) "name"
2) "mykey"
3) "course_set2"
4) "jobbole:requests"
5) "zcourses_set"
6) "myhash"
7) "courses"
8) "course_set"
127.0.0.1:6379> type "jobbole:requests"  # jobbole:requests 是一个可排序对象，也可以设置为list
zset
127.0.0.1:6379> zrange jobbole:requests 0 100
1) "\x80\x04\x95\xba\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x03url\x94\x8c!http://blog.jobbole.com/all-posts\x94\x8c\bcallback\x94N\x8c\aerrback\x94N\x8c\x06method\x94\x8c\x03GET\x94\x8c\aheaders\x94}\x94\x8c\x04body\x94C\x00\x94\x8c\acookies\x94}\x94\x8c\x04meta\x94}\x94\x8c\t_encoding\x94\x8c\x05utf-8\x94\x8c\bpriority\x94K\x00\x8c\x0bdont_filter\x94\x88\x8c\x05flags\x94]\x94u."

# ScrapyRedisTest\scrapy_redis\scheduler.py 中的 def enqueue_request(self, request): 会接收spider yield 的url，push url进redis的"jobbole:requests"中
# ScrapyRedisTest\scrapy_redis\scheduler.py 中的 def next_request(self): 会把redis的"jobbole:requests"中的url取走



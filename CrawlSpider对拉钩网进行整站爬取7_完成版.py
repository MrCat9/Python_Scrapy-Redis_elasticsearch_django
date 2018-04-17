# test_scrapy_spider\test_scrapy_spider\spiders\lagou.py
# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from items import LagouJobItemLoader, LagouJobItem
from utils.common import get_md5

class LagouSpider(CrawlSpider):  #�̳�CrawlSpider  #CrawlSpider���ܸ���parse����  # _parse_response��CrawlSpider�ĺ��ĺ���
    name = 'lagou'                                 #����ѡ������parse_start_url����process_results
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com']

#     rules = (  # rules���Ruleʵ��  #
#         Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     )
# 
#     def parse_item(self, response):
#         i = {}
#         #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
#         #i['name'] = response.xpath('//div[@id="name"]').extract()
#         #i['description'] = response.xpath('//div[@id="description"]').extract()
#         return i

    rules = (  # rules���Ruleʵ��  #allowed_domains���ȹ���һЩurl
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),  #https://www.lagou.com/zhaopin/Python/?labelWords=label
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),  #https://www.lagou.com/gongsi/j173918.html
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),  #https://www.lagou.com/jobs/4155435.html
    )                           #ƥ�����re��url������parse_job
    #
    # def parse_start_url(self, response):  #���ﲻ��Ҫ����parse_start_url
    #     return []
    #
    # def process_results(self, response, results):  #���ﲻ��Ҫ����process_results
    #     return results

    def parse_job(self, response):
        #������������ְλ
        #pass  #debug��rule�Ƿ��ܽ���parse_job
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")

        item_loader.add_css("tags", '.position-label li::text')
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_value("crawl_time", datetime.now())

        job_item = item_loader.load_item()

        return job_item



# test_scrapy_spider\test_scrapy_spider\items.py
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join  #�����Դ����ֵ���д���
import datetime
from scrapy.loader import ItemLoader  #Ϊ�˲�ÿ����Ҫдoutputoutput_processor = TakeFirst() �����Զ�һ��itemloader  ����Ҫ������ItemLoader
import re
from utils.common import extract_num
from settings import SQL_DATETIME_FORMAT

from w3lib.html import remove_tags


class TestScrapySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def add_jobbole(value):  #��������value��һ��str
    return value+"-jobbole"


def date_convert(value):
    value = value.strip().replace('��', '').strip()  #create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('��', '').strip()
                 #.strip()����ȥ��strͷβ�Ŀո�  #.replace('��', '')�����滻str�еģ�Ϊ��
    try:  #Ϊ�˽����µĴ���ʱ��д�����ݿ⣬Ҫ��str���͵�create_timeת��Ϊdate����
        create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()  #����ʽΪ%Y/%m/%d ��str����ת��Ϊdate����
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
    #ȥ��tag����ȡ������
    if "����" in value:
        return ""
    else:
        return value    
    

def return_value(value):
    return value



class ArticleItemLoader(ItemLoader):  #�Զ���itemloader
    default_output_processor = TakeFirst()  #�����Ͳ���ÿ����дoutputoutput_processor = TakeFirst()



class JobboleArticleItem(scrapy.Item):
#     title = scrapy.Field(
#         #input_processor = MapCompose(add_jobbole)  #title ����Ϊvalue ���ݵ�add_jobbole������
#         #input_processor = MapCompose(lambda x:x+"--jobbole")
#         input_processor = MapCompose(lambda x:x+"--jobbole", add_jobbole),  #title�е�ÿ��ֵ���δ����ҵ�������������
#         #output_processor = TakeFirst()
#         )
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),  #���������һ��list�� list����date
        #output_processor = TakeFirst()  #ȡ��date�� ʹlist����date��
        )
    url = scrapy.Field()
    url_object_id = scrapy.Field()  #url ����md5���������ͬ����
    front_image_url = scrapy.Field(  #���ط���ͼƬҪ��settings.py �е� ITEM_PIPELINES ��������  #front_image_url ��Ҫ����һ��list  ��Ϊimages��Ҫ����һ������
        output_processor = MapCompose(return_value)  #���ǵ�default_output_processor = TakeFirst() ʹ�ô������һ��list
        )
# """  settings.py ��
# ITEM_PIPELINES = {
#     'test_scrapy_spider.pipelines.TestJobbolePipeline': 300,  #����ԽС��Խ�ȴ���
#     #'scrapy.pipelines.images.ImagesPipeline': 1
#     'test_scrapy_spider.pipelines.ArticleImagePipeline': 1  #���ö��ƻ���pipeline��ArticleImagePipeline��
# }
# IMAGES_URLS_FIELD = 'front_image_url'  #����images, items���ĸ���ͼƬ��url  #images��Ҫ����һ������
# import os  #���ڻ�ȡ��ǰ�ļ���setting.py����·��
# #os.path.dirname(__file__)  #��ȡ��ǰ�ļ���Ŀ¼���ƣ�test_scrapy_spider��  #__file__�ǵ�ǰ�ļ���setting.py��������
# project_dir =  os.path.abspath(os.path.dirname(__file__))  #��ȡ��ǰ�ļ���Ŀ¼��·��
# IMAGES_STORE = os.path.join(project_dir, 'images')  #ͼƬ���صı���·��  ��������Ϊ����·��  Ҫ���ڹ���Ŀ¼�£�����ʹ�����·������settings.py��ͬ��Ŀ¼���½�images
#                                                     #ͼƬ������ project_dirĿ¼�µ�images�ļ���
#                                                     #Ҫ����ͼƬ��ҪPIL��
#                                                     #��cmd�°�װPIL��
#                                                     #pip install -i https://pypi.douban.com/simple pillow
# # IMAGES_MIN_HEIGHT = 100 #��������ͼƬ����С�߶�  #����ͼƬ������settng.py������
# # IMAGES_MIN_WIDTH = 100
# # '''���Ҫʵ���Լ�������Ҳ����������Ӧ�ĺ����ﵽ������pipelines�н����࣬�̳�ImagesPipeline�Ϳ�����'''                              
# """
    front_image_path = scrapy.Field()  #����ͼƬ·��
    praise_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
        )
    fav_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
        )
    comment_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
        )
    tags = scrapy.Field(  #��ߵ�tags��ʵ��tag_list����һ��list
        input_processor = MapCompose(remove_comment_tags),  #ȥ��tag����ȡ������
        output_processor = Join(',')  #������TakeFirst()��Ҫ��join��Join(',')�е�','����ָ�����ӷ�
        )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                insert into jobbole_article(title, create_date, url, url_object_id, fav_nums, front_image_url, front_image_path, praise_nums, comment_nums, tags, content)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        params = (self["title"], self["create_date"], self["url"], self["url_object_id"], self["fav_nums"], self["front_image_url"], 'self["front_image_path"]', self["praise_nums"], self["comment_nums"], self["tags"], self["content"])

        return insert_sql, params



class ZhihuQuestionItem(scrapy.Item):
    #֪�������� item
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
        #����֪��question���sql���
        insert_sql = """
            insert into zhihu_question(zhihu_id, topics, url, title, content, create_time, update_time, answer_num, comments_num, watch_user_num, click_num, crawl_time, crawl_update_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
              watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)            
        """
        #���¶����� list [] ���д���
        #zhihu_id = int("".join(self["zhihu_id"]))
        zhihu_id = self["zhihu_id"][0]  #zhihu_id��zhihu.py���Ѿ������int��
        topics = ",".join(self["topics"])
        #url = "".join(self["url"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))  #��utils���common.py�ﶨ�巽��extract_num  #������ȡ����
        comments_num = extract_num("".join(self["comments_num"]))

        if len(self["watch_user_num"]) == 2:
            self["watch_user_num"] = [x.replace(',', '') for x in self["watch_user_num"]]  #ȥ��['3,110', '824,551']�е�,
            watch_user_num = int(self["watch_user_num"][0])
            click_num = int(self["watch_user_num"][1])
        else:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = 0

        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)  #strftime(SQL_DATETIME_FORMAT)���԰�time����ת����str����  # (SQL_DATETIME_FORMAT)������settings.py��ָ��ҪתΪ���ָ�ʽ

#         create_time = datetime.datetime.now().date()  #���date��ʹ�����ݿ���Բ���
#         update_time = datetime.datetime.now().date()
#         crawl_update_time = datetime.datetime.now().date()
        create_time = None  #���date��ʹ�����ݿ���Բ���
        update_time = None
        crawl_update_time = None
        
        params = (zhihu_id, topics, url, title, content, create_time, update_time, answer_num, comments_num,
                  watch_user_num, click_num, crawl_time, crawl_update_time)

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    #֪��������ش�item
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
        #����֪��question���sql���
        insert_sql = """
            insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, parise_num, comments_num,
              create_time, update_time, crawl_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), parise_num=VALUES(parise_num),
              update_time=VALUES(update_time)
        """
        # ON DUPLICATE KEY UPDATE��������ͻʱ�����¡���

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)  #��json������ʱ��create_time��int���͵�
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)  #��json������ʱ��update_time��int���͵�
        #.fromtimestamp���԰�intת����datetime  #.strftime��datetimeת�����Զ���ģʽ��SQL_DATETIME_FORMAT�����ַ���
        
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["parise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params



def remove_splash(value):
    #ȥ���������е�б��
    return value.replace("/","")

def handle_jobaddr(value):  #value='\n                                                ���� -\n             ������\n                - �����к�������ѧԺ��·2���ڿ���Ѷ����A��316\n                              �鿴��ͼ\n        '
    addr_list = value.split("\n")  #��\nΪ�磬��str���ֳ�list
    addr_list = [item.strip() for item in addr_list if item.strip()!="�鿴��ͼ"]  #����list��ȥ���ո�Ͳ鿴��ͼ
    return "".join(addr_list)  #�ÿս��������list����str

class LagouJobItemLoader(ItemLoader):
    #�Զ���itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    #������ְλ��Ϣ
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
            self["job_addr"], self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params



# test_scrapy_spider\main.py
# -*- coding: utf-8 -*-

from scrapy.cmdline import execute  #���������������ִ��scrapy�Ľű�

# import sys
# sys.path.append('F:\eclipse\������\������\test_scrapy_spider')  #���ù��̵�Ŀ¼  #���ƹ���test_scrapy_spider��·��

import sys
import os
# os.path.abspath(__file__)  #��ȡ��ǰ�ļ���·��
# os.path.dirname(os.path.abspath(__file__))  #��ȡ��ǰ�ļ����ļ��е�·��
print(os.path.abspath(__file__))  #F:\eclipse\������\������\test_scrapy_spider\main.py
print(os.path.dirname(os.path.abspath(__file__)))  #F:\eclipse\������\������\test_scrapy_spider
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  #���ù��̵�Ŀ¼

# execute(['scrapy', 'crawl', 'jobbole_spider'])  #����execute������ִ��scrapy����
# execute(['scrapy', 'crawl', 'zhihu'])
execute(["scrapy", "crawl", "lagou"])



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
#DOWNLOADER_MIDDLEWARES = {
#    'test_scrapy_spider.middlewares.TestJobboleDownloaderMiddleware': 543,
#}

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



# test_scrapy_spider\test_scrapy_spider\pipelines.py
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs  #��codecs������ļ��Ĵ򿪺�д��
import json
from scrapy.exporters import JsonItemExporter  #��json�ļ����
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi  #ʹMySQLdb��һЩ��������첽�Ĳ���

class TestScrapySpiderPipeline(object):  #pipeline ��Ҫ���������ݴ洢��   #���pipeline������Ϊ300���󣬺�ִ��
    def process_item(self, item, spider):  #pipelines.py �����item  #Ҫȥsettings.py��ȡ��ע�� ITEM_PIPELINES
        return item



class JsonWithEncodingPipeline(object):  #��setting.py���������pipeline������Ϊ2
    #�Զ���json�ļ��ĵ���
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf_8')
    
    def process_item(self, item, spider):  #pipelines.py �����item  �����ｫitemд���ļ�
        #����process_itemʱҪ�ǵ�return item�� ��Ϊ��һpipeline���ܻ���Ҫ����item
        lines = json.dump(dict(item), ensure_ascii=False) + '\n'  #ensure_ascii=False ����ΪFalse�Ļ�д�����Ļ������ֱ��д��Unicode
        self.file.write(lines)
        return item
    
    def spider_closed(self, spider):  #��spider�ر�ʱ������������
        self.file.close()


class MysqlPipeline(object):  #д��pipeline��Ҫ��pipeline���õ�setting.py��
    #����ͬ���Ļ���д��mysql  �������ݿ���ٶȿ��ܻ�С��spider�Ľ����ٶ� -->�������첽
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'article_spider', charset='utf8', use_unicode=True)  #�������ݿ�
        #���ÿ���д��setting.py ��
        # MYSQL_HOST = "127.0.0.1"
        # MYSQL_USER = "root"
        # MYSQL_PASSWORD = "123456"
        # MYSQL_DBNAME = "article_spider"
        # MySQLdb.connect�Ĳ���
        # MySQLdb.connect('host', 'user', 'password', 'dbname', charset='utf8', use_unicode=True)
        # conn = pymysql.Connect(host='127.0.0.1', user='root', passwd='123456', port=3306, db='pymysql_test01')
        self.cursor = self.conn.cursor()
        
    def process_item(self, item, spider):  #���� process_item����
        insert_sql = """
            insert into jobbole_article(title, create_date, url, url_object_id, fav_nums, front_image_url, front_image_path, praise_nums, comment_nums, tags, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"], item["fav_nums"], item["front_image_url"], 'item["front_image_path"]', item["praise_nums"], item["comment_nums"], item["tags"], item["content"]))
        self.conn.commit()
        
        
        
class MysqlTwistedPipline(object):  #д��pipeline��Ҫ��pipeline���õ�setting.py��
    #'''�첽����mysql'''
    def __init__(self, dbpool):
        self.dbpool = dbpool
    
    @classmethod
    def from_settings(cls, settings):  #����������Զ�ȡsetting.py�е�ֵ   # clsָ����MysqlTwistedPipline �����
        #'''����settings�Ĳ���'''
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)  #����ɱ仯�Ĳ���dbparms
        #dbpool = adbapi.ConnectionPool("MySQLdb", host = settings["MYSQL_HOST"], db = settings["MYSQL_DBNAME"], ����)
        
        return cls(dbpool)

    def process_item(self, item, spider):
        #ʹ��twisted��mysql�������첽ִ��
        query = self.dbpool.runInteraction(self.do_insert, item)  #do_insertΪҪ�첽ִ�еĺ���  #itemΪҪ���������
        query.addErrback(self.handle_error, item, spider) #�����쳣

    def handle_error(self, failure, item, spider):  #�첽��������
        # �����첽������쳣
        print (failure)

#     def do_insert(self, cursor, item):
#         #ִ�о���Ĳ���
#         #���ݲ�ͬ��item ������ͬ��sql��䲢���뵽mysql��  #Ҳ������items.py���class JobBoleArticleItem(scrapy.Item): ���д���
#         if item.__class__.__name__ == "JobboleArticleItem":  #ȡ��ǰʵ����class��name
#             insert_sql = """
#                 insert into jobbole_article(title, create_date, url, url_object_id, fav_nums, front_image_url, front_image_path, praise_nums, comment_nums, tags, content)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"], item["fav_nums"], item["front_image_url"], 'item["front_image_path"]', item["praise_nums"], item["comment_nums"], item["tags"], item["content"]))
#             #TypeError: not all arguments converted during string formatting
#             #ǰ�������������һ��   �磺 %s�ĸ�������洫��Ĳ����ĸ�����һ��
#             #self.conn.commit()  #���Զ�commit

    def do_insert(self, cursor, item):
        #ִ�о���Ĳ���
        #���ݲ�ͬ��item ������ͬ��sql��䲢���뵽mysql��  #Ҳ������items.py���class JobBoleArticleItem(scrapy.Item): ���д���
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class JsonExporterPipeline(object):  #��json�ļ����    #��setting.py���������pipeline������Ϊ2�����в���
    #����scrapy�ṩ��json export����json�ļ�
    def __init__(self):
        self.file = open('articleexporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf_8', ensure_ascii=False)  #��JsonItemExporter ��ʵ����
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        
    def process_item(self, item, spider):  #pipelines.py �����item  �����ｫitemд���ļ�
        #����process_itemʱҪ�ǵ�return item�� ��Ϊ��һpipeline���ܻ���Ҫ����item
        self.exporter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):  #���ƻ�pipeline  ArticleImagePipeline  #���pipeline������Ϊ1��С����ִ��
    def item_completed(self, results, item, info):  #���� item_completed
        if 'front_image_path' in item:  #����û�з���   #item������һ��dict
            for ok, value in results:
                image_file_path = value['path']  #����ͼƬ�ı���·��
            item['front_image_path'] = image_file_path  #����ͼƬ�ı���·����items
        return item



# test_scrapy_spider\test_scrapy_spider\utils\common.py
# -*- coding: utf-8 -*-
import hashlib
import re

def get_md5(url):    # MD5ժҪ����
    if isinstance(url, str):  #python��str == Unicode #�ж��ǲ���str����ʵ���ж��ǲ���Unicode��python3��Ĭ����Unicode����
        url = url.encode(encoding='utf_8')  #�����Unicode����ת����utf-8����ϣֻ��utf-8
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()                      

def extract_num(text):
    #���ַ�������ȡ������
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

if __name__ == "__main__":
    print(get_md5("http://jobbole.com".encode(encoding='utf_8')))  #ע�⣺Unicode-objects must be encoded before hashing
    # 0efdf49af511fd88681529ef8c2e5fbf

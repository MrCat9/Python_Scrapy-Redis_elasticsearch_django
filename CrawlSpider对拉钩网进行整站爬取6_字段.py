# ��scrapy shell �е���



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
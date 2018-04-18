# 在scrapy shell 中调试



# test_scrapy_spider\test_scrapy_spider\spiders\lagou.py
# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from items import LagouJobItemLoader, LagouJobItem
from utils.common import get_md5

class LagouSpider(CrawlSpider):  #继承CrawlSpider  #CrawlSpider不能覆盖parse函数  # _parse_response是CrawlSpider的核心函数
    name = 'lagou'                                 #可以选择重载parse_start_url或者process_results
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com']

#     rules = (  # rules里放Rule实例  #
#         Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     )
# 
#     def parse_item(self, response):
#         i = {}
#         #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
#         #i['name'] = response.xpath('//div[@id="name"]').extract()
#         #i['description'] = response.xpath('//div[@id="description"]').extract()
#         return i

    rules = (  # rules里放Rule实例  #allowed_domains会先过滤一些url
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),  #https://www.lagou.com/zhaopin/Python/?labelWords=label
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),  #https://www.lagou.com/gongsi/j173918.html
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),  #https://www.lagou.com/jobs/4155435.html
    )                           #匹配这个re的url，跳到parse_job
    #
    # def parse_start_url(self, response):  #这里不需要重载parse_start_url
    #     return []
    #
    # def process_results(self, response, results):  #这里不需要重载process_results
    #     return results

    def parse_job(self, response):
        #解析拉勾网的职位
        #pass  #debug看rule是否能进到parse_job
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
from scrapy.loader.processors import MapCompose, TakeFirst, Join  #用来对传入的值进行处理
import datetime
from scrapy.loader import ItemLoader  #为了不每个都要写outputoutput_processor = TakeFirst() 我们自定一个itemloader  与是要重载类ItemLoader
import re
from utils.common import extract_num
from settings import SQL_DATETIME_FORMAT

from w3lib.html import remove_tags


class TestScrapySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def add_jobbole(value):  #传过来的value是一个str
    return value+"-jobbole"


def date_convert(value):
    value = value.strip().replace('·', '').strip()  #create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·', '').strip()
                 #.strip()可以去掉str头尾的空格  #.replace('·', '')可以替换str中的，为空
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
#     'test_scrapy_spider.pipelines.TestJobbolePipeline': 300,  #数字越小，越先处理
#     #'scrapy.pipelines.images.ImagesPipeline': 1
#     'test_scrapy_spider.pipelines.ArticleImagePipeline': 1  #调用定制化的pipeline（ArticleImagePipeline）
# }
# IMAGES_URLS_FIELD = 'front_image_url'  #告诉images, items中哪个是图片的url  #images需要接受一个数组
# import os  #用于获取当前文件（setting.py）的路径
# #os.path.dirname(__file__)  #获取当前文件的目录名称（test_scrapy_spider）  #__file__是当前文件（setting.py）的名称
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

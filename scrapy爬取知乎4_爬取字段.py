#format
url = 'www.{0}.www.{1}.'
print(url.format(123, '456'))  #www.123.www.456.



# test_scrapy_spider\test_scrapy_spider\spiders\zhihu.py
# -*- coding: utf-8 -*-
import re
import json
import datetime

# try:
#     import urlparse as parse  #python2
# except:
#     from urllib import parse  #python3
from urllib import parse  #用于补全url

import scrapy
from scrapy.loader import ItemLoader
from items import ZhihuQuestionItem, ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    #question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }  #'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):  #采取深度优先
        """
        提取出html页面中的所有url 并跟踪这些url进行一步爬取
        如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]  #用于补全url
        all_urls = filter(lambda x:True if x.startswith("https") else False, all_urls)  #过滤非https开头的url
        for url in all_urls:
            #print(url)
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)  #提取question的ID
            if match_obj:
                #如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                #question_id = match_obj.group(2)
                #print(request_url, question_id)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                #pass
                #如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        #处理question页面， 从页面中提取出具体的question item  #在items.py里定义item
        if "QuestionHeader-title" in response.text:
            #处理新版本
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)  #通过re匹配zhihu_id
            if match_obj:
                question_id = int(match_obj.group(2))  #在数据库里定义了zhihu_id为int类型

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)  #通过re匹配zhihu_id  #也可以用meta获得zhihu_id
            item_loader.add_css("answer_num", ".List-headerText span::text")
            #item_loader.add_css("comments_num", ".QuestionHeader-actions button::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            #item_loader.add_css("watch_user_num", ".NumberBoard-value::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-itemValue::text")

            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")  #没加>，只有空格，是指在后代节点中寻找  #item_loader.add_css("topics", ".QuestionHeader-topics > .Popover div::text")  #加>，是指在子节点中寻找

            question_item = item_loader.load_item()
        else:
            #处理老版本页面的item提取
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)  #通过re匹配zhihu_id
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            # item_loader.add_css("title", ".zh-question-title h2 a::text") #title可能放在a标签里，也可能放在span标签里
            item_loader.add_xpath("title", "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")  #xpath有或
            item_loader.add_css("content", "#zh-question-detail")  # #取ID  .取class
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            # item_loader.add_css("watch_user_num", "#zh-question-side-header-wrap::text")
            item_loader.add_xpath("watch_user_num", "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")

            question_item = item_loader.load_item()
            
        #pass

        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers, callback=self.parse_answer)  #请求20条  #从0开始
        yield question_item  #发到pipelines.py

        #question页面里面也可以提取url
#         all_urls = response.css("a::attr(href)").extract()
#         all_urls = [parse.urljoin(response.url, url) for url in all_urls]  #用于补全url
#         all_urls = filter(lambda x:True if x.startswith("https") else False, all_urls)  #过滤非https开头的url
#         for url in all_urls:
#             #print(url)
#             match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)  #提取question的ID
#             if match_obj:
#                 #如果提取到question相关的页面则下载后交由提取函数进行提取
#                 request_url = match_obj.group(1)
#                 #question_id = match_obj.group(2)
#                 #print(request_url, question_id)
#                 yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
#             else:
#                 #pass
#                 #如果不是question页面则直接进一步跟踪
#                 yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_answer(self, reponse):
        #处理question的answer
        ans_json = json.loads(reponse.text)
        is_end = ans_json["paging"]["is_end"]  #判断是否还有后续的页面要请求
        #totals_answer = ans_json["paging"]["totals"]
        next_url = ans_json["paging"]["next"]

        #提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()  #申明实例
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None  #可能为匿名用户
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()  #取当前时间

            yield answer_item  #yield出去，交给pipelines.py

        if not is_end:  #如果还有后续页面，继续请求
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)


    def start_requests(self):  #从登陆页面获取数据，然后调用login  #第一个执行的函数，准备登录
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)]
                            # 知乎登陆的url： https://www.zhihu.com/signup?next=%2F/   #scrapy基于Twist框架，所以Request是异步的，要设置回掉函数（callback=self.login），不设置的话会默认调用parse
        
    def login(self, response):
        response_text = response.text  #从登陆页面获取数据
#         # match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, response_text)
#         match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)  # re默认只匹配第一行，为了匹配全部内容-->加上re.DOTALL
#         xsrf = ''  #从登陆页面获取xsrf 
#         if match_obj:
#             xsrf = (match_obj.group(1))

        xsrf = '123456'  #2018.4.5测试发现知乎现在不需要_xsrf

        if xsrf:  #后面的步骤都需要在获取到xsrf的情况下继续
            #post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": xsrf,
                "email": "···",
                "password": "···",
                "captcha": ""
            }

            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data":post_data}, callback=self.login_after_captcha)
                                                                        #传递post_data

    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n>")

        post_data = response.meta.get("post_data", {})  #没有post_data,则返回空字典
        post_url = "https://www.zhihu.com/login/email"
        post_data["captcha"] = captcha  #传递验证码
        return [scrapy.FormRequest(  #FormRequest可以完成表的提交  #FormRequest的参数
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login  #验证是否登陆成功  #只能传递函数名称
        )]

    def check_login(self, response):
        #验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":  #因为知乎要在登陆成功后才能开始爬取
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)
                                           #不要做filter  #不设置回掉函数的话会默认调用parse



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

class TestJobboleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def add_jobbole(value):  #传过来的value是一个str
    return value+"-jobbole"


def date_convert(value):
    value = value.strip().replace('·', '').strip()
    try:  #为了将文章的创建时间写入数据库，要把str类型的create_time转换为date类型
        create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()  #将格式为%Y/%m/%d 的str类型转换为date类型
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

#####create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·', '').strip()
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
    title = scrapy.Field(
        #input_processor = MapCompose(add_jobbole)  #title 会作为value 传递到add_jobbole方法中
        #input_processor = MapCompose(lambda x:x+"--jobbole")
        input_processor = MapCompose(lambda x:x+"--jobbole", add_jobbole),  #title中的每个值依次从左到右调用了两个函数
        #output_processor = TakeFirst()
        )
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




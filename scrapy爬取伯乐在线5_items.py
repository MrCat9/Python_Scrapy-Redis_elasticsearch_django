'''
Request中meta参数的作用
是传递信息给下一个函数，使用过程可以理解成：把需要传递的信息赋值给这个叫meta的变量，
但meta只接受字典类型的赋值，因此
要把待传递的信息改成“字典”的形式，即：
meta={'key1':value1,'key2':value2}

如果想在下一个函数中取出value1,
只需得到上一个函数的meta['key1']即可，
因为meta是随着Request产生时传递的，
下一个函数得到的Response对象中就会有meta，
即response.meta，
取value1则是value1=response.meta['key1']
这些信息可以是任意类型的，比如值、字符串、列表、字典......方法是把要传递的信息赋值给字典的键

作者：乌尔班
链接：https://www.zhihu.com/question/54773510/answer/146971644
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''



# main.py 下
# -*- coding: utf-8 -*-

from scrapy.cmdline import execute  #调用这个函数可以执行scrapy的脚本

# import sys
# sys.path.append('F:\eclipse\···\···\test_jobbole')  #设置工程的目录  #复制工程test_jobbole的路径

import sys
import os
# os.path.abspath(__file__)  #获取当前文件的路径
# os.path.dirname(os.path.abspath(__file__))  #获取当前文件的文件夹的路径
print(os.path.abspath(__file__))  #F:\eclipse\···\···\test_jobbole\main.py
print(os.path.dirname(os.path.abspath(__file__)))  #F:\eclipse\···\···\test_jobbole
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  #设置工程的目录

execute(['scrapy', 'crawl', 'jobbole_spider'])  #调用execute函数，执行scrapy命令



# jobbole_spider.py 下    #要对工程test_jobbole 目录下的test_jobbole文件进行设置：右键-->PyDev-->Set as Source Folder (add to PYTHONPATH)
# -*- coding: utf-8 -*-
import scrapy
import re
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
        article_item['create_date'] = create_date
        article_item['front_image_url'] = [front_image_url]  #images需要接受一个数组
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['tags'] = tags
        article_item['content'] = content
        
        yield article_item  #调用yield之后，item会传递到pipelines.py

        pass



# items.py 下
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestJobboleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()  #url 进行md5处理，变成相同长度
    front_image_url = scrapy.Field()  #下载封面图片要在settings.py 中的 ITEM_PIPELINES 进行配置
# """  settings.py 下
# ITEM_PIPELINES = {
#     'test_jobbole.pipelines.TestJobbolePipeline': 300,  #数字越小，越先处理
#     #'scrapy.pipelines.images.ImagesPipeline': 1
#     'test_jobbole.pipelines.ArticleImagePipeline': 1  #调用定制化的pipeline（ArticleImagePipeline）
# }
# IMAGES_URLS_FIELD = 'front_image_url'  #告诉images items中哪个是图片的url  #images需要接受一个数组
# import os  #用于获取当前文件（setting.py）的路径
# #os.path.dirname(__file__)  #获取当前文件的目录名称（test_jobbole）  #__file__是当前文件（setting.py）的名称
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
    praise_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()



# pipelines.py 下    #会先执行setting.py下的设定
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline

class TestJobbolePipeline(object):  #pipeline 主要用来做数据存储的   #这个pipeline的数字为300，大，后执行
    def process_item(self, item, spider):  #pipelines.py 会接受item  #要去settings.py中取消注释 ITEM_PIPELINES
        return item



class ArticleImagePipeline(ImagesPipeline):  #定制化pipeline  ArticleImagePipeline  #这个pipeline的数字为1，小，先执行
    def item_completed(self, results, item, info):  #重载 item_completed
        for ok, value in results:
            image_file_path = value['path']  #保存图片的本地路径
        item['front_image_path'] = image_file_path  #保存图片的本地路径到items
        return item



#在setting的同级目录下新建包utils  用来存放常用的函数
#在package utils 下新建python文件common.py
# common.py 下
# -*- coding: utf-8 -*-
import hashlib

def get_md5(url):    # MD5摘要生成
    if isinstance(url, str):  #python中str == Unicode
                              #判断是不是str，其实是判断是不是Unicode，python3中默认是Unicode编码
        url = url.encode(encoding='utf_8')  #如果是Unicode，则转换成utf-8，哈希只认utf-8
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    print(get_md5("http://jobbole.com".encode(encoding='utf_8')))  #注意：Unicode-objects must be encoded before hashing
    # 0efdf49af511fd88681529ef8c2e5fbf

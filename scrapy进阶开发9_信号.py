# 信号  文档  http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/signals.html
# 摘自 http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/signals.html
# Scrapy使用信号来通知事情发生。
# 您可以在您的Scrapy项目中捕捉一些信号(使用 extension)来完成额外的工作或添加额外的功能，扩展Scrapy。

# 虽然信号提供了一些参数，
# 不过处理函数不用接收所有的参数 - 信号分发机制(singal dispatching mechanism)仅仅提供处理器(handler)接受的参数。

# 您可以通过 信号(Signals) API 来连接(或发送您自己的)信号。



# 信号的使用示例
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

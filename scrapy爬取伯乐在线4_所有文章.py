'''
1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
'''

#解析列表页中的所有文章url并交给scrapy下载后并进行解析
#在scrapy shell 中进行调试
#cmd下：
C:\Users\admin>workon scrapy_test
(scrapy_test) C:\Users\admin>f:
(scrapy_test) F:\>cd F:\eclipse\···\···\test_jobbole
(scrapy_test) F:\eclipse\···\···\test_jobbole>scrapy shell http://blog.jobbole.com/all-posts/
>>> response.css('.floated-thumb .post-thumb a::attr(href)').extract()
#这样的话会有很多不是文章的url，因为class=floated-thumb包含了不是文章的url
#通过定位上层的class或其他东西来限定范围，调试
>>> response.css('#archive .floated-thumb .post-thumb a::attr(href)').extract()



#提取下一页
>>> response.css(".next.page-numbers::attr(href)").extract_first('')
'http://blog.jobbole.com/all-posts/page/2/'



#把调试后的结果整合到jobbole_spider.py
# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request  #提取出url后，将url交给scrapy 下载    #from scrapy.http import Request
from urllib import parse  #如果是py2 那就是import urlparse

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
        
        post_urls = response.css('#archive .floated-thumb .post-thumb a::attr(href)').extract()
        for post_url in post_urls:
            #有时候取到的url不是一完整的域名，需要补全
            #response.url + post_url
            
            #下面用urljoin来补全
            yield Request(url = parse.urljoin(response.url, post_url), callback = self.parse_detail)
            #用 yield 就可以把Request 交给scrapy下载    #无法进入parse_detail -->进入Request， 将dont_filter=True设为True
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
        
        pass

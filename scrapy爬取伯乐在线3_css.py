CSS选择器
表达式                         说明
*                             选择所有节点
#container                    选择id为container的节点
.container                    选取所有class包含container的节点
li a                          选取所有li 下的所有a节点
ul + p                        选择ul后面的第一个p元素（ul与p元素属于兄弟节点）
div#container > ul            选取id 为container的div的第一个ul 子元素
ul ~ p                        选取与ul相邻的所有p元素
a[title]                      选取所有有title属性的a元素
a[href="http://jobbole.com"]  选取所有href属性为jobbole.com 值的a 元素
a[href*="jobole"]             选取所有href属性包含jobbole的a 元素
a[href^="http"]               选取所有href属性值以http 开头的a 元索
a[href$=".jpg"]               选取所有href属性值以.jpg结尾的a元索
input[type=radio]:checked     选择选中的radio的元索
div:not(#container)           选取所有id非container的div属性
li:nth-child(3)               选取第三个li元索
tr:nth-child(2n)              第偶数个tr



#在scrapy shell下调试
cmd下
workon scrapy_test  #进入虚拟环境
f:  #切换到f盘  #进入保存工程的目录
cd F:\eclipse\···\···\test_jobbole\  #选择保存工程的目录  #进入工程的目录
scrapy shell http://blog.jobbole.com/113789/

#提取  http://blog.jobbole.com/113789/  这篇文章的标题
>>> response.css('.entry-header h1')
[<Selector xpath="descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' entry-header ')]/descendant-or-self::*/h1" data='<h1>深入学习 Redis（1）：Redis 内存模型</h1>'>]
>>> response.css('.entry-header h1').extract()
['<h1>深入学习 Redis（1）：Redis 内存模型</h1>']
>>> response.css('.entry-header h1::text').extract()
['深入学习 Redis（1）：Redis 内存模型']
>>> response.css('.entry-header h1::text').extract()[0]
'深入学习 Redis（1）：Redis 内存模型'

#提取  http://blog.jobbole.com/113789/  这篇文章的发表时间
>>> response.css('p.entry-meta-hide-on-mobile::text').extract()
['\r\n\r\n            2018/03/27 ·  ', '\r\n            \r\n            \r\n\r\n            \r\n             ·  ', ', ', '\r\n            \r\n']
>>> response.css('p.entry-meta-hide-on-mobile::text').extract()[0]
'\r\n\r\n            2018/03/27 ·  '
>>> response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip()
'2018/03/27 ·'
>>> response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·', '')    #去掉·
'2018/03/27 '
>>> response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·', '').strip()    #去掉 （空格）
'2018/03/27'

#提取  http://blog.jobbole.com/113789/  这篇文章的点赞数
>>> response.css('.vote-post-up h10::text').extract()
['2']
>>> response.css('.vote-post-up h10::text').extract()[0]
'2'
>>> int(response.css('.vote-post-up h10::text').extract()[0])
2
#对于点赞数为0的文章，如：  http://blog.jobbole.com/69/
>>> response.css('span.vote-post-up h10::text').extract()
[]
#>>> response.css('span.vote-post-up h10::text').extract()[0]    #会报错
#测试处理方法
praise_nums = []
if praise_nums:
    praise_nums = int(praise_nums[0])
else:
    praise_nums = 0
print(praise_nums)  #0

praise_nums = ["123"]
if praise_nums:
    praise_nums = int(praise_nums[0])
else:
    praise_nums = 0
print(praise_nums)  #123

#提取  http://blog.jobbole.com/113789/  这篇文章的收藏数
>>> response.css('span.bookmark-btn::text').extract()[0]
' 1 收藏'
>>> response.css('.bookmark-btn::text').extract()[0]
' 1 收藏'
#为了去掉‘收藏’两个字，使用正则表达式re
#测试正则表达式
import re
match_re = re.match(r'.*?(\d+).*', ' 123 收藏')
if match_re:
    print(match_re.group(1))  #123

match_re = re.match(r'.*?(\d+).*', '  收藏')
if match_re:
    print(match_re.group(1))  #

#提取  http://blog.jobbole.com/113789/  这篇文章的评论数
>>> response.css("a[href='#article-comment'] span::text").extract()[0]
'  评论'
#正则表达式

#提取  http://blog.jobbole.com/113789/  这篇文章的正文
>>> response.css("div.entry").extract()[0]

#提取  http://blog.jobbole.com/113789/  这篇文章的文章标签
>>> response.css("p.entry-meta-hide-on-mobile a::text").extract()
['IT技术', 'Redis', '数据库']
#如果要提取有评论的文章，如  http://blog.jobbole.com/112125/  这篇文章的文章标签
>>> response.css("p.entry-meta-hide-on-mobile a::text").extract()
['职场', ' 2 评论 ', '工程师']
#要过滤掉‘ ？ 评论’
tag_list = ['职场', ' 1 评论 ', '工程师']
tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
print(tag_list)  #['职场', '工程师']
tags = ','.join(tag_list)  #join方法
print(tags)  #职场,工程师
#join方法
list = ['1','2','3','4','5','6']
print(list)  #['1', '2', '3', '4', '5', '6']
lista = 'a'.join(list)  #join方法
print(lista)  #1a2a3a4a5a6



#将调试结果整合到 jobbole_spider.py 下：
# -*- coding: utf-8 -*-
import scrapy
import re


class JobboleSpiderSpider(scrapy.Spider):
    name = 'jobbole_spider'
    allowed_domains = ['blog.jobbple.com']
    start_urls = ['http://blog.jobbole.com/113789/']  #在这个list中我们可以放入需要爬取的url

    def parse(self, response):  #每一个url都会进入到这个函数
        title = response.xpath('//*[@id="post-113789"]/div[1]/h1/text()').extract()[0]
        
        create_date = response.xpath('//*[@id="post-113789"]/div[2]/p/text()[1]').extract()[0].strip().replace('·', '').strip()
        
        praise_nums = response.xpath('//*[@id="113789votetotal"]/text()').extract()
        if praise_nums:
            praise_nums = int(praise_nums[0])
        else:
            praise_nums = 0
        
        fav_nums = response.xpath('//*[@id="post-113789"]/div[3]/div[12]/span[2]/text()').extract()[0]
        match_re = re.match(r'.*?(\d+).*', fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        
        comment_nums = response.xpath('//*[@id="post-113789"]/div[3]/div[12]/a/span/text()').extract()[0]
        match_re = re.match(r'.*?(\d+).*', comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        
        content = response.xpath('//*[@id="post-113789"]/div[3]').extract()[0]
        
        tag_list = response.xpath('//*[@id="post-113789"]/div[2]/p/a/text()').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith('评论')] 
        tags = ','.join(tag_list)
        
        
        
        #以下通过css选择器提取字段
        title = response.css('.entry-header h1::text').extract()[0]
        
        create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·', '').strip()
        
        praise_nums = response.css('.vote-post-up h10::text').extract()
        if praise_nums:
            praise_nums = int(praise_nums[0])
        else:
            praise_nums = 0
        
        fav_nums = response.css('.bookmark-btn::text').extract()[0]
        match_re = re.match(r'.*?(\d+).*', fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
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
#在main.py下debug
#按F6逐行执行，观察变量的值是否正确（观察爬取结果是否正确）



#  .extract_first() 方法
>>> response.css("p.entry-meta-hide-on-mobile a::text").extract()
['职场', ' 2 评论 ', '工程师']
>>> response.css("p.entry-meta-hide-on-mobile a::text").extract_first()
'职场'

>>> response.xpath('//*[@id="69votetotal"]').extract()
['<h10 id="69votetotal"></h10>']
>>> response.xpath('//*[@id="69votetotal"]/text()').extract()
[]
>>> response.xpath('//*[@id="69votetotal"]/text()').extract_first()   #不会报错
>>>
# >>> response.xpath('//*[@id="69votetotal"]/text()').extract()[0]    #会报错
>>> response.xpath('//*[@id="69votetotal"]/text()').extract_first(0)    #可以选择当.extract()的结果为[]时，返回0
0

>>> response.xpath('//*[@id="113789votetotal"]/text()').extract()
['2']
>>> response.xpath('//*[@id="113789votetotal"]/text()').extract()[0]
'2'
>>> response.xpath('//*[@id="113789votetotal"]/text()').extract_first(0)    #当.extract()的结果不为[]时，正常返回[]中的第一个元素，不会返回0
'2'

#所以  praise_nums  可以改写成
        praise_nums = response.css('.vote-post-up h10::text').extract_first(0)

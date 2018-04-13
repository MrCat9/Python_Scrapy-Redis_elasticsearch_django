#xpath简介
1. xpath使用路径表达式在xml和html中进行导航。
2. xpath包含标准函数库。
3. xpath是一个w3c的标准。



#xpath节点关系
1. 父节点
2. 子节点
3. 同胞节点
4. 先辈节点
5. 后代节点



#xpath语法
表达式                  说明
article                选取所有article元素的所有子节点
/article               选取根元素article
article/a              选取所有属于article的子元素的a元素（是子元素，不是后代元素）
//div                  选取所有div子元素(不论出现在文档任何地方)
article//div           选取所有属于article元素的后代的div元素，不管它出现在article之下的任何位置
//@class               选取所有名为class的属性
/article/div[1]        选取属于article 子元素的第一个div元素
/article/div[last()]   选取属于article 子元素的最后一个div元素
/article/div[last()-1] 选取属于article 子元素的倒数第二个div元素
//div[@lang]           选取所有拥有lang属性的div元素
//div[@lang='eng']     选取所有lang属性为eng的div元素
/div/*                 选取属于div元素的所有子节点
//*                    选取所有元素
//div[@*]              选取所有带属性的div元素
/div/a|//div/p         选取所有div元素的a和p元素
//span|//ul            选取文档中的span和u元素
article/div/p|//span   选取所有属于article 元素的div元素的p元素以及文档中所有的span元素



#测试xpath
#在jobbole_spider.py下：
# -*- coding: utf-8 -*-
import scrapy
class JobboleSpiderSpider(scrapy.Spider):
    name = 'jobbole_spider'
    allowed_domains = ['blog.jobbple.com']
    start_urls = ['http://blog.jobbole.com/113789/']  #在这个list中我们可以放入需要爬取的url

    def parse(self, response):  #每一个url都会进入到这个函数
        #获取文章的标题  #html文件在F:\eclipse\···\···\test_jobbole\test_jobbole\spiders\test.html
        #/html/body/div[3]/div[3]/div[1]/div[1]/h1
        #也可以使用chrome的复制xpath的功能    #//*[@id="post-113789"]/div[1]/h1
        re_selector = response.xpath('/html/body/div[3]/div[3]/div[1]/div[1]/h1')
        print(re_selector)  #[]  #js会动态生成，导致该条xpath是错的
        re_re_selector = response.xpath('/html/body/div[1]/div[3]/div[1]/div[1]/h1')
        print(re_re_selector)  
        #[<Selector xpath='/html/body/div[1]/div[3]/div[1]/div[1]/h1' data='<h1>深入学习 Redis（1）：Redis 内存模型</h1>'>]  #修改后
        re2_selector = response.xpath('//*[@id="post-113789"]/div[1]/h1')  #id是唯一的，可以用来定位
        print(re2_selector)  
        #[<Selector xpath='//*[@id="post-113789"]/div[1]/h1' data='<h1>深入学习 Redis（1）：Redis 内存模型</h1>'>]
        re3_selector = response.xpath('//*[@id="post-113789"]/div[1]/h1/text()')
        print(re3_selector)  
        #[<Selector xpath='//*[@id="post-113789"]/div[1]/h1/text()' data='深入学习 Redis（1）：Redis 内存模型'>]
        re4_selector = response.xpath('//div[@class="entry-header"]/h1/text()')  #该html刚好只有一个div的class是entry-header
        print(re4_selector)                                                      #class是可以重复的，在用来定位之前要 ctrl+f 检查一下
        #[<Selector xpath='//div[@class="entry-header"]/h1/text()' data='深入学习 Redis（1）：Redis 内存模型'>]
        pass
#在main.py中运行python



#在scrapy shell下调试，效率更高
cmd下
workon scrapy_test  #进入虚拟环境
f:  #切换到f盘  #进入保存工程的目录
cd F:\eclipse\···\···\test_jobbole\  #选择保存工程的目录  #进入工程的目录
scrapy shell http://blog.jobbole.com/113789/

#提取  http://blog.jobbole.com/113789/  这篇文章的标题
>>> title = response.xpath('//*[@id="post-113789"]/div[1]/h1/text()')
>>> title  #xpath返回的对象还是一个xpath，使得这个放回对象可以继续使用xpath进行定位
[<Selector xpath='//*[@id="post-113789"]/div[1]/h1/text()' data='深入学习 Redis（1）：Redis 内存模型'>]
>>> title.extract()  #extract()方法会把xpath对象变成一个数组，就无法再用xpath进行定位了
['深入学习 Redis（1）：Redis 内存模型']
>>> title.extract()[0]
'深入学习 Redis（1）：Redis 内存模型'

#提取  http://blog.jobbole.com/113789/  这篇文章的发表时间
>>> create_date = response.xpath('//*[@id="post-113789"]/div[2]/p/text()[1]')
>>> create_date
[<Selector xpath='//*[@id="post-113789"]/div[2]/p/text()[1]' data='\r\n\r\n            2018/03/27 ·  '>]
>>> create_date.extract()
['\r\n\r\n            2018/03/27 ·  ']
>>> create_date.extract()[0]
'\r\n\r\n            2018/03/27 ·  '
>>> create_date.extract()[0].strip()
'2018/03/27 ·'
>>> create_date.extract()[0].strip().replace('·', '')    #去掉·
'2018/03/27 '
>>> create_date.extract()[0].strip().replace('·', '').strip()    #去掉 （空格）
'2018/03/27'

'''
contains()用法
response.xpath("//span[contains(@class, 'vote-post-up')]")
表示在span标签中class属性中含有 vote-post-up 即为符合
'''
#提取  http://blog.jobbole.com/113789/  这篇文章的点赞数
>>> response.xpath('//*[@id="113789votetotal"]/text()')
[<Selector xpath='//*[@id="113789votetotal"]/text()' data='1'>]
>>> response.xpath('//*[@id="113789votetotal"]/text()').extract()
['1']
>>> response.xpath('//*[@id="113789votetotal"]/text()').extract()[0]
'1'
>>> int(response.xpath('//*[@id="113789votetotal"]/text()').extract()[0])
1
#或者
>>> response.xpath('//*[@id="post-113789"]/div[3]/div[12]/span[1]')
[<Selector xpath='//*[@id="post-113789"]/div[3]/div[12]/span[1]' data='<span data-post-id="113789" class=" btn-'>]
>>> response.xpath('//*[@id="post-113789"]/div[3]/div[12]/span[1]/h10')
[<Selector xpath='//*[@id="post-113789"]/div[3]/div[12]/span[1]/h10' data='<h10 id="113789votetotal">1</h10>'>]
>>> response.xpath('//*[@id="post-113789"]/div[3]/div[12]/span[1]/h10/text()')
[<Selector xpath='//*[@id="post-113789"]/div[3]/div[12]/span[1]/h10/text()' data='1'>]
>>> response.xpath('//*[@id="post-113789"]/div[3]/div[12]/span[1]/h10/text()').extract()
['1']
>>> response.xpath('//*[@id="post-113789"]/div[3]/div[12]/span[1]/h10/text()').extract()[0]
'1'
>>> int(response.xpath('//*[@id="post-113789"]/div[3]/div[12]/span[1]/h10/text()').extract()[0])
1
#对于点赞数为0的文章，如：  http://blog.jobbole.com/69/
>>> response.xpath('//*[@id="69votetotal"]/text()').extract()
[]
#>>> response.xpath('//*[@id="69votetotal"]/text()').extract()[0]    #会报错
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
>>> response.xpath('//*[@id="post-113789"]/div[3]/div[12]/span[2]/text()')
[<Selector xpath='//*[@id="post-113789"]/div[3]/div[12]/span[2]/text()' data='  收藏'>]
>>> response.xpath('//*[@id="post-113789"]/div[3]/div[12]/span[2]/text()').extract()
['  收藏']
>>> response.xpath('//*[@id="post-113789"]/div[3]/div[12]/span[2]/text()').extract()[0]
'  收藏'
#为了去掉‘收藏’两个字，使用正则表达式re
#测试正则表达式
import re
try:
    match_re = re.match(r'.*?(\d+).*', ' 123 收藏')
    print(match_re.group(1))  #123
except:
    print(0)

try:
    match_re = re.match(r'.*?(\d+).*', '  收藏')
    print(match_re.group(1))
except:
    print(0)  #0
#测试正则表达式
import re
match_re = re.match(r'.*?(\d+).*', ' 123 收藏')
if match_re:
    print(match_re.group(1))  #123

match_re = re.match(r'.*?(\d+).*', '  收藏')
if match_re:
    print(match_re.group(1))  #

#提取  http://blog.jobbole.com/113789/  这篇文章的评论数
>>> response.xpath('//*[@id="post-113789"]/div[3]/div[12]/a/span/text()')
[<Selector xpath='//*[@id="post-113789"]/div[3]/div[12]/a/span/text()' data='  评论'>]
>>> response.xpath('//*[@id="post-113789"]/div[3]/div[12]/a/span/text()').extract()
['  评论']
>>> response.xpath('//*[@id="post-113789"]/div[3]/div[12]/a/span/text()').extract()[0]
'  评论'
#正则表达式

#提取  http://blog.jobbole.com/113789/  这篇文章的正文
>>> response.xpath('//*[@id="post-113789"]/div[3]').extract()[0]

#提取  http://blog.jobbole.com/113789/  这篇文章的文章标签
>>> response.xpath('//*[@id="post-113789"]/div[2]/p/a/text()').extract()
['IT技术', 'Redis', '数据库']

#如果要提取有评论的文章，如  http://blog.jobbole.com/112125/  这篇文章的文章标签
>>> response.xpath('//*[@id="post-112125"]/div[2]/p/a/text()').extract()
['职场', ' 1 评论 ', '工程师']
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
        pass

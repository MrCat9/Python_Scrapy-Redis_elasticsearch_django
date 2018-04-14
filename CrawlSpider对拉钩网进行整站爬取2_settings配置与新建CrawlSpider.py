# F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider\settings.py
# 在F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider\settings.py 下，设置F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider 为根目录
# 因为虽然在eclipse里已经将 F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider 添加到path里了，但在cmd下还未添加
import sys  #import os  在上面写过了
# sys.path.insert(0, "F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider")  #将F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider 添加到path
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  #F:\eclipse\···\···\test_scrapy_spider  工程路径
sys.path.insert(0, os.path.join(BASE_DIR, 'test_scrapy_spider'))  #将F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider 添加到path里
             #放在第0个，会优先在F:\eclipse\···\···\test_scrapy_spider\test_scrapy_spider里找需要import的module



# cmder 下
C:\Users\admin
λ workon scrapy_test
C:\Users\admin
(scrapy_test) λ f:

F:\cmder\vendor\git-for-windows
(scrapy_test) λ cd F:\eclipse\···\···\test_scrapy_spider  #进入工程目录

F:\eclipse\···\···\test_scrapy_spider
(scrapy_test) λ scrapy genspider --list  #查看可用的模板
Available templates:
  basic
  crawl
  csvfeed
  xmlfeed

F:\eclipse\···\···\test_scrapy_spider
(scrapy_test) λ scrapy genspider -t crawl lagou www.lagou.com  #用crawl模板创建名为lagou的spider
Created spider 'lagou' using template 'crawl' in module:
  test_scrapy_spider.spiders.lagou


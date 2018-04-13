'''  摘自https://baike.baidu.com/item/JSON/2462549?fr=aladdin
JSON(JavaScript Object Notation, JS 对象标记) 是一种轻量级的数据交换格式。
它基于 ECMAScript (w3c制定的js规范)的一个子集，采用完全独立于编程语言的文本格式来存储和表示数据。
简洁和清晰的层次结构使得 JSON 成为理想的数据交换语言。 
易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率。
'''



# 数据保存到json文件中



# pipelines.py
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs  #用codecs来完成文件的打开和写入
import json
from scrapy.exporters import JsonItemExporter  #将json文件输出


class TestJobbolePipeline(object):  #pipeline 主要用来做数据存储的   #这个pipeline的数字为300，大，后执行
    def process_item(self, item, spider):  #pipelines.py 会接受item  #要去settings.py中取消注释 ITEM_PIPELINES
        return item



class JsonWithEncodingPipeline(object):  #在setting.py里配置这个pipeline的数字为2
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf_8')
    
    def process_item(self, item, spider):  #pipelines.py 会接受item  在这里将item写入文件
        #调用process_item时要记得return item， 因为下一pipeline可能还需要处理item
        lines = json.dump(dict(item), ensure_ascii=False) + '\n'  #ensure_ascii=False 不设为False的话写入中文会出错，会直接写入Unicode
        self.file.write(lines)
        return item
    
    def spider_clsede(self, spider):  #当spider关闭时会调用这个函数
        self.file.close()
    
class JsonExporterPipeline(object):  #将json文件输出    #在setting.py里配置这个pipeline的数字为2，进行测试
    def __init__(self):
        #调用scrapy提供的json export导出json文件
        self.file = open('articleexporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf_8', ensure_ascii=False)  #用JsonItemExporter 做实例化
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        
    def process_item(self, item, spider):  #pipelines.py 会接受item  在这里将item写入文件
        #调用process_item时要记得return item， 因为下一pipeline可能还需要处理item
        self.exporter.export_item(item)
        return item



class ArticleImagePipeline(ImagesPipeline):  #定制化pipeline  ArticleImagePipeline  #这个pipeline的数字为1，小，先执行
    def item_completed(self, results, item, info):  #重载 item_completed
        for ok, value in results:
            image_file_path = value['path']  #保存图片的本地路径
        item['front_image_path'] = image_file_path  #保存图片的本地路径到items
        return item



# setting.py 下的 ITEM_PIPELINES
ITEM_PIPELINES = {
    'test_jobbole.pipelines.JsonExporterPipeline': 2,  #数字越小，越先处理
    #'scrapy.pipelines.images.ImagesPipeline': 1
    'test_jobbole.pipelines.ArticleImagePipeline': 1  #调用定制化的pipeline（ArticleImagePipeline）
}
IMAGES_URLS_FIELD = 'front_image_url'  #告诉images items中哪个是图片的url  #images需要接受一个数组
import os  #用于获取当前文件（setting.py）的路径
#os.path.dirname(__file__)  #获取当前文件的目录名称（test_jobbole）  #__file__是当前文件（setting.py）的名称
project_dir =  os.path.abspath(os.path.dirname(__file__))  #获取当前文件的目录的路径
IMAGES_STORE = os.path.join(project_dir, 'images')  #图片下载的保存路径  可以配置为绝对路径  要存在工程目录下，可以使用相对路径。在settings.py的同级目录下新建images
                                                    #图片储存在 project_dir目录下的images文件夹
                                                    #要下载图片需要PIL库
                                                    #下cmd下安装PIL库
                                                    #pip install -i https://pypi.douban.com/simple pillow
# IMAGES_MIN_HEIGHT = 100 #设置下载图片的最小高度  #过滤图片可以在settng.py中设置
# IMAGES_MIN_WIDTH = 100
# '''如果要实现自己的需求，也可以重载相应的函数达到需求，在pipelines中建立类，继承ImagesPipeline就可以了'''

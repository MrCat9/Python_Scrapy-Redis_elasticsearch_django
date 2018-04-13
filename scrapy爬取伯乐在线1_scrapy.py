#scrapy爬取伯乐在线的所有文章
#要过滤掉不是文章的url
#伯乐在线有个所有文章的url（http://blog.jobbole.com/all-posts/）
#可以直接应用



#安装scrapy
cmd下：
pip install -i https://pypi.douban.com/simple/ scrapy
或者：
cmd下：
workon scrapy_test  #进入虚拟环境
pip install -i https://pypi.douban.com/simple/ scrapy  #安装

#安装时报错
error: Microsoft Visual C++ 14.0 is required. Get it with 
       "Microsoft Visual C++ Build Tools": http://landinghub.visualstudio.com/visual-cpp-build-tools
解决办法：
https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
下载twisted对应版本的whl文件，cp后面是python版本，amd64代表64位。
然后在cmd下：
pip install C:\Users\admin\Downloads\Twisted-17.9.0-cp36-cp36m-win_amd64.whl
再次安装scrapy:
pip install -i https://pypi.douban.com/simple/ scrapy  #安装

#升级pip版本
cmd下：
python -m pip install -U pip

#新建scrapy工程
cmd下：
workon scrapy_test  #进入虚拟环境
f:  #切换到f盘  #选择保存工程的目录
cd F:\eclipse\admin\???  #选择保存工程的目录
scrapy startproject （工程名）  #新建scrapy工程
#创建完成后可以导入到eclipse中  #设置工程test_scrapy_spider 目录下的test_scrapy_spider文件：右键-->PyDev-->Set as Source Folder (add to PYTHONPATH)

#创建爬虫
cmd下：
workon scrapy_test  #进入虚拟环境
f:  #切换到f盘  #进入保存工程的目录
cd F:\eclipse\···\···\test_jobbole\  #选择保存工程的目录  #进入工程的目录
scrapy genspider jobbole_spider blog.jobbple.com  #建立一个名为jobbole_spider的爬虫，目标网站为blog.jobbple.com
                                                  #这个爬虫（jobbole_spider.py）会被放到工程的spider目录下

#scrapy启动某一个spider的命令：
cmd下：
workon scrapy_test  #进入虚拟环境
f:  #切换到f盘  #进入保存工程的目录
cd F:\eclipse\···\···\test_jobbole\  #选择保存工程的目录  #进入工程的目录
scrapy crawl jobbole_spider  #启动名为jobbole_spider的爬虫

#报错ModuleNotFoundError: No module named 'win32api'
#安装pypiwin32
pip install -i https://pypi.douban.com/simple pypiwin32



#运用scrapy写爬虫
#在工程test_jobbole 下新建一个文件main.py  使得可以在eclipse下完成scrapy的调试
#在main.py下：
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



#在settings.py下，将ROBOTSTXT_OBEY = True改为ROBOTSTXT_OBEY = False
#                   遵循ROBOTS协议                           关掉



#在jobbole_spider.py下：
# -*- coding: utf-8 -*-
import scrapy


class JobboleSpiderSpider(scrapy.Spider):
    name = 'jobbole_spider'
    allowed_domains = ['blog.jobbple.com']
    start_urls = ['http://blog.jobbple.com/']  #在这个list中我们可以放入需要爬取的url

    def parse(self, response):  #每一个url都会进入到这个函数
        pass

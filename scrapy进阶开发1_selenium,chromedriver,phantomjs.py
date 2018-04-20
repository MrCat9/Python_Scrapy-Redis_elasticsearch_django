# Selenium （浏览器自动化测试框架）  引用自百度百科 https://baike.baidu.com/item/Selenium/18266#viewPageContent
# Selenium 是一个用于Web应用程序测试的工具。Selenium测试直接运行在浏览器中，就像真正的用户在操作一样。
# 支持的浏览器包括IE（7, 8, 9, 10, 11），Mozilla Firefox，Safari，Google Chrome，Opera等。
# 这个工具的主要功能包括：测试与浏览器的兼容性——测试你的应用程序看是否能够很好得工作在不同浏览器和操作系统之上。
# 测试系统功能——创建回归测试检验软件功能和用户需求。支持自动录制动作和自动生成 .Net、Java、Perl等不同语言的测试脚本。

# selenium的构架图

# selenium是用来操纵浏览器的

# 如果要操作浏览器，还需要下载一个driver。

# 操控浏览器去请求网页



# 安装selenium
# cmder下
C:\Users\admin
λ pip install selenium



# selenium 文档 http://selenium-python.readthedocs.io/api.html

# 下载chrome的driver
# http://selenium-python.readthedocs.io/installation.html#drivers
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# http://chromedriver.storage.googleapis.com/index.html



# test_scrapy_spider\tools\selenium_spider.py
# -*- coding: utf-8 -*-

from selenium import webdriver
from scrapy.selector import Selector

# browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")  # chromedriver.exe 的路径
# 
# browser.get("https://item.taobao.com/item.htm?spm=a230r.1.14.1.5f285e0eeI6hSf&id=565917574046&ns=1&abbucket=4#detail")
# 
# print(browser.page_source)  # 天猫需要登陆，淘宝不需要  #可以获取到商品价格
# 
# # browser.find_element_by_css_selector(css_selector)  #browser有提供用于页面字段提取的函数
# # browser.find_element_by_xpath(xpath)
# 
# t_selector = Selector(text=browser.page_source)
# print(t_selector.css(".tb-promo-item-bd .tb-promo-price .tb-rmb-num::text").extract())  #
# 
# browser.quit()



# selenium 完成知乎模拟登录
# browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")  # chromedriver.exe 的路径
# 
# browser.get("https://www.zhihu.com/signup?next=%2F")
# 
# browser.find_element_by_css_selector(".SignContainer-switch span").click()  #点击进入登陆界面
# 
# browser.find_element_by_css_selector(".SignFlow-accountInput  input[name='username']").send_keys("···")  # 输入用户名
# browser.find_element_by_css_selector(".SignFlow-password input[name='password']").send_keys("···")  # 输入密码
# 
# browser.find_element_by_css_selector("button.SignFlow-submitButton").click()  # 点击登陆  # 找到class名为 SignFlow-submitButton 的button



# selenium 完成微博模拟登录
# 爬取微博可以参考微博开发平台  https://open.weibo.com/  http://open.weibo.com/wiki/%E9%A6%96%E9%A1%B5
# browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")  # chromedriver.exe 的路径
# browser.get("https://weibo.com/")
# import time
# time.sleep(10)  #延迟10s再执行下面的语句  #执行太快可能导致页面还没加载完毕，就执行selector，导致找不到 id="loginname"
# browser.find_element_by_css_selector("#loginname").send_keys("···")  #找到id名为loginname的
# time.sleep(3)  #输入太快会要求输入验证码
# browser.find_element_by_css_selector("input[node-type='password']").send_keys("···")  #找到node-type='password'的input
# browser.find_element_by_css_selector("a[tabindex='6'] span").click()  #找到一个tabindex='6'的a标签，之后在这个a标签下找span标签



# selenium 完成鼠标下滑
# browser.execute_script(script)  #执行js代码

# browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe")  # chromedriver.exe 的路径
# browser.get("https://www.oschina.net/blog")
# import time
# time.sleep(5)
# for i in range(3):  #下拉三次
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
#     time.sleep(3)  #下拉后停3秒钟



#设置chromedriver不加载图片
# chrome_opt = webdriver.ChromeOptions()  #生成实例
# prefs = {"profile.managed_default_content_settings.images":2}  # 2 就是不加载图片
# chrome_opt.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome(executable_path="F:/chromedriver_win32/chromedriver.exe", chrome_options=chrome_opt)
# browser.get("https://www.taobao.com")



# phantomjs, 无界面的浏览器， 多进程情况下phantomjs性能会下降很严重
# 下载 phantomjs  http://phantomjs.org/download.html
browser = webdriver.PhantomJS(executable_path="F:/phantomjs/phantomjs-2.1.1-windows/bin/phantomjs.exe")  # phantomjs.exe 的路径
browser.get("https://item.taobao.com/item.htm?id=561574212482&ali_refid=a3_420432_1006:1104574851:N:%E6%89%8B%E6%9C%BA%E5%A3%B3:7d5c2ecce43bcf1c59e2a395fa1e41d7&ali_trackid=1_7d5c2ecce43bcf1c59e2a395fa1e41d7&spm=a230r.1.14.6#detail")

print (browser.page_source)
browser.quit()








# 淘宝页面下
# 右键检查，右键查看网页源代码  看到的是不一样的  淘宝页面用了js动态填充
# 右键检查看到的是当前的，是浏览器运行过js之后的代码
# 右键查看网页源代码看到的是源码
# 所以右键检查看的到商品的价格，而右键查看网页源代码却看不到价格

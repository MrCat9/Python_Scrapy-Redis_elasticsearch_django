# chrome无界面运行
# 安装 pip install pyvirtualdisplay
# 不能在windows上运行  在linux上运行
# test_scrapy_spider\test_scrapy_spider\middlewares.py 下
# from pyvirtualdisplay import Display
# from selenium import webdriver
# display = Display(visible=0, size=(800, 600))  # visible=0 --> 不显示
# display.start()
#
# browser = webdriver.Chrome()
# browser.get()

# 可能遇到的问题：
# 错误：cmd=[‘xvfb’,’help’] 
# os error
#
# 解决方法：
# sudo apt-get install xvfb
# pip install xvfbwrapper



# 处理动态网站  chromedriver

# 处理动态网站  scrapy-splash  https://github.com/scrapy-plugins/scrapy-splash
# Splash是一个Javascript渲染服务。它是一个实现了HTTP API的轻量级浏览器，
# Splash是用Python实现的，同时使用Twisted和QT。Twisted（QT）用来让服务具有异步处理能力，以发挥webkit的并发能力。
# 可以在scrapy中处理ajax来抓取动态的数据，支持分布式，但没有chrome那么稳定。

# 处理动态网站 selenium grid 
# 支持分布式

# splinter   https://github.com/cobrateam/splinter
# 操控浏览器

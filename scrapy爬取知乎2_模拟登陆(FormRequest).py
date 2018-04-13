#常见httpcode
code    说明
200     请求被成功处理
301/302 永久性重定向/临时性重定向
403     没有权限访问
404     表示没有对应的资源
500     服务器错误
503     服务器停机或正在维护



# chrome下，转到  https://www.zhihu.com/signup?next=%2F  知乎
# F12进入调试-->network-->all
# ctrl+F5  强制刷新
# 可以看到每条请求和状态



# post请求

#怎么找post参数？
先找到登录的页面，F12进入调试-->network-->all，输入错误的账号和密码，观察post_url变换，从而确定参数。

#尝试用手机号码登陆
# post请求sign_in 的headers下的general有：
Request URL:https://www.zhihu.com/api/v3/oauth/sign_in
Request Method:POST
# post请求sign_in 的headers下的request payload 下有：
Content-Disposition: form-data; name="username"
+8613015664637  #登陆时输入的账号

Content-Disposition: form-data; name="password"
111111  #登陆时输入的密码



# _xsrf  登陆时生成的随机码，用来防御csrf攻击。没有_xsrf就访问时会返回403（无权限）



#尝试用邮箱登陆
# post请求sign_in 的headers下的general有：
Request URL:https://www.zhihu.com/api/v3/oauth/sign_in
Request Method:POST
# post请求sign_in 的headers下的request payload 下有：
Content-Disposition: form-data; name="username"
13015664637@qq.com  #登陆时输入的账号

Content-Disposition: form-data; name="password"
111111  #登陆时输入的密码



#分析知
#登陆（做post）需要账号、密码、_xsrf   _xsrf可以通过re或者scrapy的css选择器获取
#登陆之后要保存cookie  用于下次登陆



#安装request
#cmd下
pip install requests



# test_scrapy_spider\test_scrapy_spider\utils\zhihu_login_requests.py
# -*- coding: utf-8 -*-

import requests
# try:  #python2中叫做cookielib  3中叫做cookiejar  #这样写可以使一个代码兼容2，3
#     import cookielib
# except:
#     import http.cookiejar as cookielib
import http.cookiejar as cookielib
#import http.cookiejar as cookielib
import re

session = requests.session()  #session是某一次连接，这样就不用每次请求的时候都建立连接。不用requests，session效率高
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")  #实例化cookies，保存cookies
try:  #读取cookies                           #把cookie保存在cookies.txt里
    session.cookies.load(ignore_discard=True)
except:
    print ("cookie未能加载")

agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
#agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36
header = {  #不带头会返回错误500  #在浏览器的F12中可以找到头
    "HOST":"www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': agent
}

def is_login():
    #通过个人中心页面返回状态码来判断是否为登录状态
    inbox_url = "https://www.zhihu.com/inbox"  #通过检查是否可以进入私信页面来判断是否登陆
    #inbox_url = "https://www.zhihu.com/question/56250357/answer/148534773"  #不需要登陆也能看到回答或者问题（https://www.zhihu.com/question/56250357）
    response = session.get(inbox_url, headers=header, allow_redirects=False)  #allow_redirects=False 不设为False的话session在获取到302时会去自动获取跳转后的页面-->就会返回200
    #查看 response 的status_code 可以知道状态                #重定向
    if response.status_code != 200:
        return False
    else:
        return True

def get_xsrf():
    #获取xsrf code
    response = session.get("https://www.zhihu.com", headers=header)  #没有头会返回500 Server Error
    #print(response.text)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""

def get_index():  #检测是否用cookie登陆成功
    response = session.get("https://www.zhihu.com", headers=header)  
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf_8"))
    print ("ok")

def get_captcha():
    import time  #构建随机字符串
    t = str(int(time.time()*1000))  #构建随机字符串
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=header)  #这里只能用session，不能用requests  #因为session会带cookie等
    with open("captcha.jpg","wb") as f:
        f.write(t.content)  #t 是一个图片文件，所以写入content，而不是text
        f.close()
    #pass

    from PIL import Image  #用来打开图片  #pip install pillow
    try:
        im = Image.open('captcha.jpg')  #打开文件
        im.show()  #展示文件
        im.close()
    except:
        pass

    captcha = input("输入验证码\n>")  #人工输入验证码  #python2中用raw_input
    return captcha

def zhihu_login(account, password):
    #知乎登录
    if re.match("^1\d{10}",account):
        print ("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha":get_captcha()
        }
    else:
        if "@" in account:
            #判断用户名是否为邮箱
            print("邮箱方式登录")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),  #2018.4.5测试发现知乎现在不需要_xsrf
                "email": account,
                "password": password,
                "captcha":get_captcha()  #验证码
            }
    
    #response = requests.post(post_url, data=post_data, headers=header)
    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save()  #保存cookie

zhihu_login("@", "")
# get_xsrf()
# get_index()
is_login()
# get_captcha()

# \u767b\u5f55\u6210\u529f
# 登录成功
# 
# email \u5bf9\u5e94\u7684\u8d26\u6237\u4e0d\u5b58\u5728
# email对应的账户不存在
# 
# \u5e10\u53f7\u6216\u5bc6\u7801\u9519\u8bef
# 帐号或密码错误
#
# \u9a8c\u8bc1\u7801\u9519\u8bef
# 验证码错误
#
# \u8bf7\u586b\u5199\u9a8c\u8bc1\u7801
# 请填写验证码



# 新建知乎的spider
# cmd下
C:\Users\admin>workon scrapy_test
(scrapy_test) C:\Users\admin>f:
(scrapy_test) F:\>cd F:\eclipse\···\···\test_scrapy_spider
(scrapy_test) F:\eclipse\···\···\test_scrapy_spider>scrapy genspider zhihu www.zhihu.com



# test_scrapy_spider\test_scrapy_spider\spiders\zhihu.py
# -*- coding: utf-8 -*-
import re
import json
import datetime

# try:
#     import urlparse as parse
# except:
#     from urllib import parse
from urllib import parse

import scrapy
from scrapy.loader import ItemLoader
#from items import ZhihuQuestionItem, ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    #question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }  #'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"

    def parse(self, response):  #登陆成功的话，这里的response返回值为 HtmlResponse: <200 https://www.zhihu.com/>
        pass


    def start_requests(self):  #从登陆页面获取数据，然后调用login  #第一个执行的函数，准备登录
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)]
                            # 知乎登陆的url： https://www.zhihu.com/signup?next=%2F/   #scrapy基于Twist框架，所以Request是异步的，要设置回掉函数（callback=self.login），不设置的话会默认调用parse
        
    def login(self, response):
        response_text = response.text  #从登陆页面获取数据
#         # match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, response_text)
#         match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)  # re默认只匹配第一行，为了匹配全部内容-->加上re.DOTALL
#         xsrf = ''  #从登陆页面获取xsrf 
#         if match_obj:
#             xsrf = (match_obj.group(1))

        xsrf = '123456'  #2018.4.5测试发现知乎现在不需要_xsrf

        if xsrf:  #后面的步骤都需要在获取到xsrf的情况下继续
            #post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": xsrf,
                "email": "",
                "password": "",
                "captcha": ""
            }

            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data":post_data}, callback=self.login_after_captcha)
                                                                        #传递post_data

    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n>")

        post_data = response.meta.get("post_data", {})  #没有post_data,则返回空字典
        post_url = "https://www.zhihu.com/login/email"
        post_data["captcha"] = captcha  #传递验证码
        return [scrapy.FormRequest(  #FormRequest可以完成表的提交  #FormRequest的参数
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login  #验证是否登陆成功  #只能传递函数名称
        )]

    def check_login(self, response):
        #验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":  #因为知乎要在登陆成功后才能开始爬取
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)
                                           #不要做filter  #不设置回掉函数的话会默认调用parse



# test_scrapy_spider\main.py
# -*- coding: utf-8 -*-

from scrapy.cmdline import execute  #调用这个函数可以执行scrapy的脚本

# import sys
# sys.path.append('F:\eclipse\···\···\test_scrapy_spider')  #设置工程的目录  #复制工程test_scrapy_spider的路径

import sys
import os
# os.path.abspath(__file__)  #获取当前文件的路径
# os.path.dirname(os.path.abspath(__file__))  #获取当前文件的文件夹的路径
print(os.path.abspath(__file__))  #F:\eclipse\···\···\test_scrapy_spider\main.py
print(os.path.dirname(os.path.abspath(__file__)))  #F:\eclipse\···\···\test_scrapy_spider
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  #设置工程的目录

# execute(['scrapy', 'crawl', 'jobbole_spider'])  #调用execute函数，执行scrapy命令
execute(['scrapy', 'crawl', 'zhihu'])

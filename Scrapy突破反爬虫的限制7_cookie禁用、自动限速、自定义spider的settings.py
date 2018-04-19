# scrapy 文档      https://doc.scrapy.org/en/latest/
# scrapy 中文文档  http://scrapy-chs.readthedocs.io/zh_CN/latest/



# 如果用不到cookies的，就不要让对方知道你的cookies
# cookie 的禁用
# test_scrapy_spider\test_scrapy_spider\settings.py
COOKIES_ENABLED = False  #禁用cookie



# 限速
# test_scrapy_spider\test_scrapy_spider\settings.py
DOWNLOAD_DELAY = 10  #10秒下载一次
AUTOTHROTTLE_ENABLED = True  #自动控制下载速度



# 不同的spider配置不同的settings
# test_scrapy_spider\test_scrapy_spider\spiders\zhihu.py
# -*- coding: utf-8 -*-
import re
import json
import datetime

# try:
#     import urlparse as parse  #python2
# except:
#     from urllib import parse  #python3
from urllib import parse  #用于补全url

import scrapy
from scrapy.loader import ItemLoader
from items import ZhihuQuestionItem, ZhihuAnswerItem


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

    custom_settings = {
        "COOKIES_ENABLED": True  # 这样的话默认情况下的spider是读取settings.py里的 COOKIES_ENABLED = False  #禁用cookie
    }                            # 而知乎的这个spider是 "COOKIES_ENABLED": True  #启用cookie

    def parse(self, response):  #采取深度优先
        ······




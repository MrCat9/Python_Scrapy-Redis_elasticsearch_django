# scrapy �ĵ�      https://doc.scrapy.org/en/latest/
# scrapy �����ĵ�  http://scrapy-chs.readthedocs.io/zh_CN/latest/



# ����ò���cookies�ģ��Ͳ�Ҫ�öԷ�֪�����cookies
# cookie �Ľ���
# test_scrapy_spider\test_scrapy_spider\settings.py
COOKIES_ENABLED = False  #����cookie



# ����
# test_scrapy_spider\test_scrapy_spider\settings.py
DOWNLOAD_DELAY = 10  #10������һ��
AUTOTHROTTLE_ENABLED = True  #�Զ����������ٶ�



# ��ͬ��spider���ò�ͬ��settings
# test_scrapy_spider\test_scrapy_spider\spiders\zhihu.py
# -*- coding: utf-8 -*-
import re
import json
import datetime

# try:
#     import urlparse as parse  #python2
# except:
#     from urllib import parse  #python3
from urllib import parse  #���ڲ�ȫurl

import scrapy
from scrapy.loader import ItemLoader
from items import ZhihuQuestionItem, ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    #question�ĵ�һҳanswer������url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }  #'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"

    custom_settings = {
        "COOKIES_ENABLED": True  # �����Ļ�Ĭ������µ�spider�Ƕ�ȡsettings.py��� COOKIES_ENABLED = False  #����cookie
    }                            # ��֪�������spider�� "COOKIES_ENABLED": True  #����cookie

    def parse(self, response):  #��ȡ�������
        ������������




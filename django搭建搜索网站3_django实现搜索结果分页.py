# \LcvSearch\src\search\views.py
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render
from django.views.generic.base import View
from search.models import ArticleType
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from datetime import datetime
import redis

client = Elasticsearch(hosts=["127.0.0.1"])  #初始化es的连接
redis_cli = redis.StrictRedis()


class IndexView(View):
    #首页
    def get(self, request):
        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        return render(request, "index.html", {"topn_search":topn_search})

# Create your views here.
class SearchSuggest(View):  #处理搜索建议
    def get(self, request):
        key_words = request.GET.get('s','')  #输入的是s  #默认值为空''
        re_datas = []
        if key_words:
            suggestions = client.search(  # client.search 允许es语法
                index= "jobbole",
                body={
                    "suggest": {
                        "my_suggest": {
                            "text": key_words,
                            "completion": {
                                "field": "suggest",
                                "fuzzy": {
                                "fuzziness": 2
                                }
                            }
                        }
                    },
                        "_source": "title"
                }
            )
#             s = ArticleType.search()
#             s = s.suggest('my_suggest', key_words, completion={  #与es中格式类似
#                 "field":"suggest", "fuzzy":{
#                     "fuzziness":2
#                 },
#                 "size": 10  #返回10个
#             })
#             suggestions = s.execute_suggest()  #返回一个{}
            for match in suggestions["suggest"]["my_suggest"][0]["options"]:
                source = match["_source"]
                re_datas.append(source["title"])  #取title
        return HttpResponse(json.dumps(re_datas), content_type="application/json")  #将数据返回给前端


class SearchView(View):
    def get(self, request):
        key_words = request.GET.get("q","")  #搜索的词为q
        s_type = request.GET.get("s_type", "article")

        redis_cli.zincrby("search_keywords_set", key_words)

        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1

        jobbole_count = redis_cli.get("jobbole_count")
        start_time = datetime.now()
        response = client.search(  # client.search 允许es语法
            index= "jobbole",
            body={
                "query":{
                    "multi_match":{
                        "query":key_words,  #搜索的关键词
                        "fields":["tags", "title", "content"]  #要检索的字段
                    }
                },
                "from":(page-1)*10,  #分页
                "size":10,           #分页
                "highlight": {  #高亮
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "title": {},  #对title做高亮
                        "content": {},  #对content做高亮
                    }
                }
            }
        )

        end_time = datetime.now()
        last_seconds = (end_time-start_time).total_seconds()
        total_nums = response["hits"]["total"]  #总数量
        if (page%10) > 0:
            page_nums = int(total_nums/10) +1
        else:
            page_nums = int(total_nums/10)
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "title" in hit["highlight"]:  #取出title  #在highlight里取
                hit_dict["title"] = "".join(hit["highlight"]["title"])  #要join，要不然会显示成一个list
            else:
                hit_dict["title"] = hit["_source"]["title"]  #没有的话在_source 下取
            if "content" in hit["highlight"]:
                hit_dict["content"] = "".join(hit["highlight"]["content"])[:500]  #对content内容截断，因为可能很长
            else:
                hit_dict["content"] = hit["_source"]["content"][:500]

            hit_dict["create_date"] = hit["_source"]["create_date"]
            hit_dict["url"] = hit["_source"]["url"]  #用于跳转
            hit_dict["score"] = hit["_score"]  #得分

            hit_list.append(hit_dict)

        return render(request, "result.html", {"page":page,  #将数据放到html页面中
                                               "all_hits":hit_list,  #处理后的数据
                                               "key_words":key_words,
                                               "total_nums":total_nums,
                                               "page_nums":page_nums,
                                               "last_seconds":last_seconds,
                                               "jobbole_count":jobbole_count,
                                               "topn_search":topn_search})





# \LcvSearch\src\LcvSearch\urls.py
# -*- coding: utf-8 -*-

"""LcvSearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from search.views import SearchSuggest, SearchView, IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name="index"),

    url(r'^suggest/$', SearchSuggest.as_view(), name="suggest"),  #处理搜索建议  #在\LcvSearch\src\search\views.py 内处理

    url(r'^search/$', SearchView.as_view(), name="search"),  # search 接口  #在\LcvSearch\src\search\views.py 内定义SearchView
]






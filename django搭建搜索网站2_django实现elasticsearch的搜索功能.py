# \LcvSearch\src\LcvSearch\urls.py
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
from search.views import SearchSuggest, SearchView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(), name="index"),

    url(r'^suggest/$', SearchSuggest.as_view(), name="suggest"),  #处理搜索建议  #在\LcvSearch\src\search\views.py 内处理

    url(r'^search/$', SearchView.as_view(), name="search"),  # search 接口  #在\LcvSearch\src\search\views.py 内定义SearchView

]




# LcvSearch\src\search\views.py
import json
from django.shortcuts import render
from django.views.generic.base import View
from search.models import ArticleType
from django.http import HttpResponse
from elasticsearch import Elasticsearch


client = Elasticsearch(hosts=["127.0.0.1"])  #初始化es的连接


# Create your views here.
class SearchSuggest(View):  #处理搜索建议
    def get(self, request):
        key_words = request.GET.get('s','')  #输入的是s  #默认值为空''
        re_datas = []
        if key_words:
            s = ArticleType.search()
            s = s.suggest('my_suggest', key_words, completion={  #与es中格式类似
                "field":"suggest", "fuzzy":{
                    "fuzziness":2
                },
                "size": 10  #返回10个
            })
            suggestions = s.execute_suggest()  #返回一个{}
            for match in suggestions.my_suggest[0].options:
                source = match._source
                re_datas.append(source["title"])  #取title
        return HttpResponse(json.dumps(re_datas), content_type="application/json")  #将数据返回给前端


class SearchView(View):
    def get(self, request):
        key_words = request.GET.get("q","")  #搜索的词为q
        s_type = request.GET.get("s_type", "article")

        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1

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
                                               "page_nums":page_nums})
                                               
                                               
                                               



# \LcvSearch\src\templates\result.html 配置样式文件路径
{% load staticfiles %}

<link href="{% static 'css/style.css' %}" rel="stylesheet" type="text/css" />
<link href="{% static 'css/result.css' %}" rel="stylesheet" type="text/css" />

<script type="text/javascript" src="{% static 'js/jquery.js' %}"></script>
<script type="text/javascript" src="{% static 'js/global.js' %}"></script>
<script type="text/javascript" src="{% static 'js/pagination.js' %}"></script>



                    {% for hit in all_hits %}
                    <div class="resultItem">
                            <div class="itemHead">
                                <a href="{{ hit.url }}"  target="_blank" class="title">{% autoescape off %}{{ hit.title }}{% endautoescape %}</a>
                                <span class="divsion">-</span>
                                <span class="fileType">
                                    <span class="label">来源：</span>
                                    <span class="value">伯乐在线</span>
                                </span>
                                <span class="dependValue">
                                    <span class="label">得分：</span>
                                    <span class="value">{{ hit.score }}</span>
                                </span>
                            </div>
                            <div class="itemBody">
                                {% autoescape off %}{{ hit.content }}{% endautoescape %}
                            </div>
                            <div class="itemFoot">
                                <span class="info">
                                    <label>网站：</label>
                                    <span class="value">伯乐在线</span>
                                </span>
                                <span class="info">
                                    <label>发布时间：</label>
                                    <span class="value">2017-04-23</span>
                                </span>
                            </div>
                        </div>
                    {% endfor %}



                                <a href="{{ hit.url }}"  target="_blank" class="title">{% autoescape off %}{{ hit.title }}{% endautoescape %}</a>



                                {% autoescape off %}{{ hit.content }}{% endautoescape %}




        	<input type="text" class="searchInput" value="{{ key_words }}"/>



    var search_url = "{% url 'search' %}"





# \LcvSearch\src\templates\index.html 配置url
    var search_url = "{% url 'search' %}"



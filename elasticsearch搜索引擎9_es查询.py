# elasticserach 查询：

# 1. 基本查询:使用 elasticserach 内置的查询条件进行查询  #参与打分
# 2. 组合查询：把多个查询组合在一起进行复合查询          #参与打分
# 3. 过滤：查询同时，通过filter条件，在不影响打分的情况下筛选数据



# 添加映射
PUT lagou
{
  "mappings": {
    "job": {
      "properties": {
        "title": {
          "store": true, 
          "type": "text",
          "analyzer": "ik_max_word"  #用于处理汉字  #ik 文档  https://github.com/medcl/elasticsearch-analysis-ik
        },
        "company_name": {
          "store": true,
          "type": "keyword"
        },
        "desc": {
          "type": "text"
        },
        "comments": {
          "type": "integer"
        },
        "add_time": {
          "type": "date",
          "format": "yyyy-MM-dd"
        }
      }
    }
  }
}

POST lagou/job/
{
  "title": "python django 开发工程师",
  "company_name": "美团科技有限公司",
  "desc": "对 django的概念熟悉，熟悉python基础知识",
  "comments": 20,
  "add_time": "2017-4-1"
}

POST lagou/job/
{
  "title": "python scrapy redis 分布式爬虫",
  "company_name": "百度科技有限公司",
  "desc": "对 scrapy 的概念熟悉，熟悉 redis 的基础操作",
  "comments": 5,
  "add_time": "2017-4-15"
}

POST lagou/job/
{
  "title": "elasticserach 打造搜索引擎",
  "company_name": "阿里巴巴科技有限公司",
  "desc": "熟悉数据结构算法，熟悉python的基本开发",
  "comments": 15,
  "add_time": "2017-6-20"
}

POST lagou/job/
{
  "title": "python打造推荐引擎系统",
  "company_name": "阿里巴巴科技有限公司",
  "desc": "熟悉推荐引擎的原理及算法，掌握C语言",
  "comments": 60,
  "add_time": "2016-10-20"
}






# 简单查询

# match 查询
GET lagou/job/_search
{
  "query": {
    "match": {
      "title": "python"  #"title": "Python" 结果相同，因为match会做分词
    }  # 查询到3条信息  #关于python的都会提取出来，match查询会对内容进行分词，
  }                     #并且会自动对传入的关键词进行大小写转换，内置ik分词器会进行切分，
}                       #如python网站，只要搜到存在的任何一部分，都会返回

# match 查询
GET lagou/job/_search
{
  "query": {
    "match": {
      "title": "python网站"
    }  # 查询到3条信息  #因为分词成"python"和"网站" 只要有一个词匹配了，就会被查询出来
  }
}

# match 查询
GET lagou/job/_search
{
  "query": {
    "match": {
      "title": "爬取"  
    }  # 查询到1条信息  #虽然该条信息中没有出现爬取字段  #分词分成“爬”和“取”  #"title": "python scrapy redis 分布式爬虫"
  }
}

# match 查询
GET lagou/job/_search
{
  "query": {
    "match": {
      "title": "取"  
    }  # 查询到0条信息
  }
}



# term查询  # term查询不会对传入的值做处理  #可以理解为keyword  #只能查包含整个传入的内容的，一部分也不行，只能完全匹配
GET lagou/job/_search
{
  "query": {
    "term": {
      "title": "python爬虫"
    }  # 查询到0条信息  # term查询不会对传入的值做处理
  }
}

GET lagou/job/_search
{
  "query": {
    "match": {
      "title": "python爬虫"
    }  # 查询到3条信息
  }
}



GET lagou/job/_search
{
  "query": {
    "match": {
      "company_name": "百度"
    }  # 查询到0条信息  #因为company_name是keyword  #keyword是不会分析的  #只有完全匹配
  }
}


GET lagou/job/_search
{
  "query": {
    "term": {
      "company_name": "百度"
    }  # 查询到0条信息  #因为company_name是keyword  #keyword是不会分析的  #只有完全匹配
  }
}



# terms查询  # terms可以传入多个值,只要有一个匹配就会匹配
GET lagou/job/_search
{
  "query": {
    "terms": {
      "title": ["工程师", "django", "系统"]
    }  # 查询到2条信息
  }  #"title": "python django 开发工程师"  #"title": "python打造推荐引擎系统"
}



# 控制查询的返回数量  #可以用来做分页
GET lagou/job/_search
{
  "query": {
    "match": {
      "title": "python"
    }
  },
  "from": 1,   #从1开始    #第一条对应的是0
  "size": 2    #只取两个
}



# match_all  #返回所有 
GET lagou/_search  #没有写type  #搜索index lagou下的所有type
{
  "query": {
    "match_all": {}
  }  # 查询到4条信息
}



# match_phrase查询  #短语查询
GET lagou/job/_search
{
  "query": {
    "match_phrase": {
      "title": {
        "query": "python系统",  #分词成"python"和"系统"  #返回同时匹配"python"和"系统"的
        "slop": 6               # slop参数说明两个词条之间的距离小于等于6
      }  #查询到1条信息  #"title": "python打造推荐引擎系统"
    }
  }
}

GET lagou/job/_search
{
  "query": {
    "match_phrase": {
      "title": {
        "query": "python网站",
        "slop": 6
      }  #查询到0条信息  #能匹配到pyhotn 但匹配不到网站
    }
  }
}

GET lagou/job/_search
{
  "query": {
    "match_phrase": {
      "title": {
        "query": "python系统",
        "slop": 5
      }  #查询到0条信息  #距离太大
    }
  }
}



# multi_match查询
# 可以指定多个字段
# 如：查询title或desc这两个字段里面包含python关键词的文档
GET lagou/_search
{
  "query": {  
    "multi_match": {
      "query": "python",  #query为要查询的关键词 
      "fields": ["title","desc"]  # fileds表示在哪些字段里查询关键词
    }  # 查询到4条信息  #只要其中某个字段中出现了关键词，都会返回 
  }
}

GET lagou/_search
{
  "query": {  
    "multi_match": {
      "query": "python",  #query为要查询的关键词 
      "fields": ["title^3","desc"]  # fileds表示在哪些字段里查询关键词 #^3的意思为设置权重，在title中找到的权值为在desc字段中找到的权值的三倍
    }  # 查询到4条信息  #只要其中某个字段中出现了关键词，都会返回      #会影响score  排序
  }
}



# 指定返回字段
GET lagou/job/_search
{
  "stored_fields": ["title","company_name"],   #要返回的字段
  "query": {
    "match": {
      "title": "爬取"  
    }  #查询到3条信息
  }
}

GET lagou/job/_search
{
  "stored_fields": ["title","company_name","desc"],   #并不会返回desc，因为只能返回 store为true的。
  "query": {                                          #desc的store没指定，默认为false
    "match": {
      "title": "python"  
    }
  }
}



# 通过sort把结果排序
# sort是一个数组，里面是一个字典，字典的key就是要sort的字段，"order": "asc"  表示按升序排列
                                                          #  "order": "desc" 表示按降序排列
GET lagou/_search
{
  "query": {
    "match_all": {}  #先查询
  },
  "sort": [          #后排序
    {
      "comments": {
        "order": "desc"
      }
    }
  ]
}



# 查询范围  #range查询 
GET lagou/_search
{
  "query": {
    "range": {
      "comments": {  #指明要设置范围的字段
        "gte": 10,  #大于等于  #gt是大于
        "lte": 20,  #小于等于  #lt小于
        "boost": 2.0  #权重
      }
    }
  }
}

GET lagou/_search
{
  "query": {
    "range": {
      "add_time": {
        "gte": "2017-04-01", #对时间的范围查询，可以用字符串的形式传入
        "lte": "now"
      }
    }
  }
}



# wildcard模糊查询，可以使用通配符
GET lagou/_search
{
  "query": {
    "wildcard": {
      "title": {
        "value": "pyt*on",
        "boost": 2.0
      }  #查询到4条信息
    }
  }
}






# 组合查询

# 建立测试数据
POST lagou/testjob/_bulk
{"index":{"_id":1}}
{"salary":10, "title":"Python"}
{"index":{"_id":2}}
{"salary":20, "title":"Scrapy"}
{"index":{"_id":3}}
{"salary":30, "title":"Django"}
{"index":{"_id":4}}
{"salary":30, "title":"elasticserach"}

# bool查询
# bool查询包括了must should must_not filter来完成 
# filter可以用于过滤出需要的值，不参与打分
# must表示里面的所有查询都必须满足
# should表示里面的所有查询只要满足一个就行
# must_not表示里面的所有查询都必须不满足

# bool查询格式：
bool:{
    "filter":[],  #有多个用[{},{},{}]  #只有一个用{}
    "must":[],
    "should":[],
    "must_not":[],
}



# 通过bool查询，完成简单的过滤查询
# select * from testjob where salary=20
# 薪资为20的工作
GET lagou/testjob/_search
{
  "query": {  #请求体
    "bool": {
      "must": {  #不写must这块也行
        "match_all": {}
      },
      "filter": {
        "term": {  #用match也行，因为salary为int类型，int类型不会被分析
          "salary": 20
        }  #查询到1条信息
      }
    }
  }
}

# 薪资为10，20的工作  #指定多个值
GET lagou/testjob/_search
{
  "query": {
    "bool": {
      "must": {  #不写must这块也行
        "match_all": {}
      },
      "filter": {
        "terms": {
          "salary": [10,20]
        }  #查询到2条信息
      }
    }
  }
}



# select * from testjob where title="Python"
GET lagou/testjob/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "term": {
          "title": "Python"  #因为在存入的时候，Python被分词，以python的形式存入
        }  #查询到0条信息    #现在用term去查Python，当然查不到
      }
    }
  }
}

GET lagou/testjob/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "match": {
          "title": "Python"
        }  #查询到1条信息
      }
    }
  }
}

GET lagou/testjob/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "term": {
          "title": "python"
        }  #查询到1条信息
      }
    }
  }
}



# 查看分析器的解析结果
GET _analyze
{
  "analyzer": "ik_max_word",
  "text": "Python网络开发工程师"
}  # 分成了： python  网络  络  开发  发  工程师  工程  师


GET _analyze
{
  "analyzer": "ik_smart",
  "text": "Python网络开发工程师"
}  # 分成了： python  网络  开发  工程师



# bool过滤查询  #可以做组合过滤查询

# select * from testjob where (salary=20 OR title=Python) AND (salary != 30)
# 查询薪资等于20或者工作为python的工作，排除薪资为30和10的
GET lagou/testjob/_search
{
  "query": {
    "bool": {
      "should": [
        {"term": {"salary": 20}},
        {"term": {"title": "python"}}
      ],
      "must_not": [
        {"term": {"salary": 30}},
        {"term": {"salary": 10}}
      ]    # 查询到1条信息
    }
  }
}



# 嵌套查询
# select * from testjob where title="python" or (title="django" AND salary=30)
GET lagou/testjob/_search
{
  "query": {
    "bool": {
      "should": [
        {"term": {"title": "python"}},
        {
          "bool": {
            "must": [
              {"term": {"title": "django"}},
              {"term": {"salary": 30}}
            ]  #查询到2条信息
          }
        }
      ]
    }
  }
}



# 过滤空和非空
# 建立测试数据
POST lagou/testjob2/_bulk
{"index":{"_id":1}}
{"tags":["search"]}            # tags 传递了一个值
{"index":{"_id":2}}
{"tags":["search","python"]}   # tags 传递了2个值
{"index":{"_id":3}}
{"other_field":["some data"]}  #没有 tags
{"index":{"_id":4}}
{"tags":null}                  #有 tags ，但为null
{"index":{"_id":5}}
{"tags":["search",null]}       # tags 有 search 有null

# 处理null空值的方法
# select tags from testjob2 where tags is not Null 
GET lagou/testjob2/_search
{
  "query": {
    "bool": {
      "filter": {
        "exists": {
          "field": "tags"
        }  #查询到3条信息  "_id":5  "_id":2  "_id":1
      }
    }
  }
}

GET lagou/testjob2/_search
{
  "query": {
    "bool": {
      "must_not": {
        "exists": {
          "field": "tags"
        }  #查询到2条信息  "_id":4  "_id":3
      }
    }
  }
}

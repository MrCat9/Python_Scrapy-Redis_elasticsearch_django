# elasticserach的mapping映射：
# 创建索引时，可以预先定义字段的类型以及相关属性，每个字段定义一种类型，
# 属性比mysql里面丰富，前面没有传入，因为elasticsearch会根据json源数据的基础类型来猜测你想要的字段映射。
# 将输入的数据转变成可搜索的索引项。
# mapping就是我们自己定义的字段的数据类型，同时告诉elasticsearch如何索引数据以及是否可以被搜索。 
# 作用：会让索引建立的更加细致和完善，对于大多数是不需要我们自己定义
# 类型：静态映射，动态映射

内置类型
String类型： 两种text keyword。text会对内部的内容进行分析，索引，进行倒排索引等。设置为keyword则会当成字符串，不会被分析，只能完全匹配才能找到。（String类型在es5已经被弃用了）
数字类型:long, integer, short, byte, double, float
日期类型：date 以及datetime等
bool类型: boolean
binary类型:binary
复杂类型：object, nested
geo类型：geo-point(地理位置，通过经纬度来标志位置), geo-shape（地理位置，通过多点标志一个点线区）
专业类型：ip, competion  （competion用来做搜索建议）

object ：json里面内置的还有下层{}的对象

nested：把对象放到数组[{},{},{}]里，就是nested了



# 内置类型支持设置的参数
属性			描述							适合类型
store  			值为yes表示存储，				all
				为no表示不存储，默认为no  
				
				yes 表示分析，
index			no 表示不分析，					string    （分析text，不分析keyword）
				默认值为true  

				如果字段为空，
null_value		可以设置一个默认值，			all
				比如"NA"

analyzer  		可以设置索引和					all
				搜索时用的分析器，
				默认使用的是standard分析器，
				还可以使whitespace,simple,
				english

include_in_all	默认es为每个文档定义			all
				一个特殊域_all,它的作用
				是让每个字段被搜索到，
				如果不想某个字段被搜索到，
				可以设置为false

format			时间格式字符串的模式			date



# Elasticsearch 文档
# https://www.elastic.co/guide/cn/elasticsearch/guide/current/index.html



# 给一个文档建立mappings

# 创建索引(index)
PUT lagou
{
  "mappings": {
    "job": {    # type
      "properties": {
        "title": {  #值
          "type": "text"    # 设置好类型后，将不能修改
        },
        "salary_min": {
          "type": "integer"
        },
        "city": {
          "type": "keyword"
        },
        "company": {    #对于 object
          "properties": {  #要嵌套properties
            "name": {
              "type": "text"
            },
            "company_addr": {
              "type": "text"
            },
            "employee_count": {
              "type": "integer"
            }
          }
        },
        "publish_date": {
          "type": "date",
          "format": "yyyy-MM-dd"
        },
        "comments": {
          "type": "integer"
        }
      }
    }
  }
}

# 放入数据
PUT lagou/job/1
{
  "title": "python分布式爬虫开发",
  "salary_min": 15000,    # "salary_min": "15000",  #不会报错，因为会尝试转换  #  #"salary_min": abc,  #会报错
  "city": "北京",
  "company": {
    "name": "百度",
    "company_addr": "北京市软件园",
    "employee_count": 50
  },
  "publish_date": "2017-4-18",
  "comments": 15
}

# 获取index下的所有mapping
GET lagou/_mapping

# 获取index下的type的mapping
GET lagou/_mapping/job

# 获取集群中的所有mapping
GET _all/_mapping

# 获取job的mapping
GET _all/_mapping/job


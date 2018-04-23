# http://127.0.0.1:5601    dev tools 下



# es的文档、索引的CRUD操作

# 索引初始化操作
# 指定分片和副本的数量
# shards一旦设置不能修改，副本数量可以修改
PUT lagou    # lagou为索引的名称
{
  "settings": {
    "index": {
      "number_of_shards":5,  #分片的数量，默认为5
      "number_of_replicas":1 #副本的数量，默认为1
    }
  }
}

# 运行结果如下
{
  "acknowledged": true,
  "shards_acknowledged": true
}

# 在head中刷新，可以看到lagou

# 在head中，索引下，也可以新建索引

GET lagou/_settings          # 获取lagou的settings
GET .kibana,lagou/_settings  # 获取.kibana和lagou的settings
GET  _all/_settings          # 获取所有索引的settings
GET _settings                # 获取所有索引的settings

# 修改settings
PUT lagou/_settings
{
  "number_of_replicas": 2
}

# 获取所有的索引信息
GET _all

# 获取lagou的索引信息
GET lagou

# 保存信息到索引中
PUT lagou/man/1  #索引/type/id
{

  "name": "小明",

  "country": "China",

  "age": 3,

  "date": "1987-03-07 12:12:12"

}  #可以在head  数据浏览  lagou中看到插入的数据

POST lagou/man/    # 不指明id自动生成uuid
{

  "name": "小红",

  "country": "China",

  "age": 2,

  "date": "1999-09-09 12:12:12"

}

# 获取文档
GET lagou/man/1
GET lagou/man/1?_source=name
GET lagou/man/1?_source=name,age
GET lagou/man/1?_source

# 修改信息
PUT lagou/man/1  #覆盖式的，这样将没有country信息
{

  "name": "小刚",

  "age": 1,

  "date": "1987-03-07 12:12:12"

}

# 修改部分字段
POST lagou/man/1/_update
{
  "doc":{  #里面放要修改的内容
    "age":2,
    "country":"China"
  }
}

# 删除
DELETE lagou/man/1
DELETE lagou

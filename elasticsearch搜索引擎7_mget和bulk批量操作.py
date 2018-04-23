# mget  #批量查询

PUT testdb/job1/1
{

  "title": "job1_1"
  
}

PUT testdb/job1/2
{

  "title": "job1_2"
  
}

PUT testdb/job2/1
{

  "title": "job2_1"
  
}

PUT testdb/job2/2
{

  "title": "job2_2"
  
}

GET _mget  #批量查询  #查询index为testdb下的job1表的id为1和job2表的id为2的数据
{
  "docs":[
    {
      "_index":"testdb",
      "_type":"job1",
      "_id":1                 # job1_1
    },
    {
      "_index":"testdb",
      "_type":"job2",
      "_id":2                 # job2_2
    }
    ]
}

GET testdb/_mget  #批量查询  #可以不用每个都写index
{
  "docs":[
    {
      "_type":"job1",
      "_id":1                 # job1_1
    },
    {
      "_type":"job2",
      "_id":2                 # job2_2
    }
    ]
}

GET testdb/job1/_mget  #批量查询  #可以不用每个都写index和type  #查询index和type一样，只有id不一样
{
  "docs":[
    {
      "_id":1                 # job1_1
    },
    {
      "_id":2                 # job1_2
    }
    ]
}

GET testdb/job1/_mget
{
  "ids":[1,2]              # job1_1  job1_2
}






# bulk批量操作
可以合并多个操作，比如index，delete，update，create等等，包括从一个索引导入到另一个索引
action_and_meta_data\n
option_source\n
action_and_meta_data\n
option_source\n
….
action_and_meta_data\n
option_source\n
注意:每个操作都是由两行构成(delete除外)，
其他的命令比如index和create都是由元信息行和数据行组成，
update比较特殊，它的数据行可能是doc也可能是upsert或者script，
注意数据不能美化，即只能是两行的形式，而不能是经过解析的标准的json排列形式，否则会报错

POST _bulk
{ "index":{"_index":"test","_type":"type1","_id":"1"} }
{ "field1":"value1" }
···
···
{ "delete" : {"_index" : "test", "_type" : "type1", "_id" : "2"} }  #delete操作只有一行
···
···
{ "create":{"_index" : "test", "_type" : "type1", "_id":"3"} }
{ "field1":"value3" }
···
···
{ "update":{"_id":"1", "_type" : "type1", "_index" : "index1"} }
{ "doc" : {"field2" : "value2"} }

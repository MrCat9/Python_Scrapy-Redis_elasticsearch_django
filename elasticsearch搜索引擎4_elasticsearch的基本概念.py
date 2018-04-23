# elasticsearch基础概念：
# 1.集群：一个或多个节点组织在一起
# 2.节点：一个集群中的一台服务器，由一个名字来标识，默认是一个随机的漫画角色的名字
# 3.分片：索引划分为多份的能力，允许水平分割，扩展容量，多个分片响应请求，提高性能和吞吐量
# 4.副本：创建分片的一份或多分的能力，一个节点失败，其他节点顶上



elasticsearch	对应	mysql
index					数据库 
type					表 
document				行
fields					列



http 方法：
GET, POST, HEAD, OPTIONS, PUT, DELETE, TRACE, CONNECT

集合搜索和保存：增加了五种方法： 
OPTIONS, PUT, DELETE, TRACE, CONNECT

方法		描述
GET			请求指定的页面信息，并返回实体主体。
POST		向指定资源提交数据进行处理请求。数据被包含在请求体中。POST 请求可能会导致新的资源的建立和/或已有资源的修改。
PUT			向服务器传送的数据取代指定的文档的内容。
DELETE		请求服务器删除指定的页面。


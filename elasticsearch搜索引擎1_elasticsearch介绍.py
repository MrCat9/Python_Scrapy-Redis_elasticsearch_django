# 自己搭建的网站或者程序，添加搜索功能比较困难:
# 1.所以我们希望搜索解决方案要高效 
# 2.零配置并且免费 
# 3.能够简单的通过json和http与搜索引擎交互 
# 4.希望搜索服务很稳定 
# 5.简单的将一台服务器扩展到多台服务器

# elasticsearch介绍：
# 一个基于lucene的搜索服务器，  # elasticsearch对Lucene进行了封装，既能存储数据，又能分析数据，适合与做搜索引擎 
# 分布式多用户的全文搜索引擎 
# java开发的
# 基于restful web接口

# 很多大公司都用elasticsearch 戴尔 Facebook 微软等等

# 关系数据搜索缺点： 
# 1.无法对搜素结果进行打分排序 
# 2.没有分布式，搜索麻烦，对程序员的要求比较高 
# 3.无法解析搜索请求，对搜索的内容无法进行解析，如分词等 
# 4.数据多了，效率低 
# 5.需要分词，把汉字分成一个一个的有意义的词

# 所以需要搜索引擎

# nosql数据库：  (not only sql)  （如：mongodb, redis, elasticsearch）  （elasticsearch既可以做数据的分析，也可以做数据的存储）
# 文档数据库，不用与关系数据库  json代码，在关系数据库中数据存储，需要存到多个表，内部有多对多等关系，需要涉及到多个表才能将json里面的内容存下来，nosql直接将一个json的内容存起来，作为一个文档存档到数据库。 

# 全文搜索引擎：solr, sphinx, elasticsearch

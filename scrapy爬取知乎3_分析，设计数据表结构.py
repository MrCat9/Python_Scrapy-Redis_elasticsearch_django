#
C:\Users\admin>workon scrapy_test
(scrapy_test) C:\Users\admin>scrapy shell https://www.zhihu.com/question/271074839/answer/360407925
>>> response.text
'<html><body><h1>500 Server Error</h1>\nAn internal server error occured.\n</body></html>\n'
#直接访问会返回500 Internal Server Error  #要加上User-Agent
(scrapy_test) C:\Users\admin>scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0" https://www.zhihu.com/question/271074839/answer/360407925



#在未登录的情况下是可以访问问题（https://www.zhihu.com/question/271074839/）和回答（https://www.zhihu.com/question/271074839/answer/360407925）的



#把数据放到桌面
>>> with open("C:/Users/admin/Desktop/zhihu.html","wb") as f:
...     f.write(response.text.encode("utf8"))
...
50220    #返回数字，说明写入成功



#分析url请求结构
#点下知乎回答（https://www.zhihu.com/question/271074839/answer/360407925）下方的查看全部XXX个回答
#url会变成问题（https://www.zhihu.com/question/271074839）
#滚轮向下滚的时候观察network，注意answers请求
https://www.zhihu.com/api/v4/questions/271074839/answers?（···一堆···）Dbest_answerer%29%5D.topics&limit=5&offset=8
https://www.zhihu.com/api/v4/questions/271074839/answers?（···一堆···）Dbest_answerer%29%5D.topics&limit=5&offset=13&sort_by=default
# limit是这次获得的回答条数  #offset像是指针，从第8条开始+5    # 8+5=13



#访问 https://www.zhihu.com/api/v4/questions/271074839/answers?（···一堆···）Dbest_answerer%29%5D.topics&limit=5&offset=8
#进行分析



# 在数据库article_spider的tables下，新建表 zhihu_question
Field Name              Datatype        Len         Default     PK?     Not Null
zhihu_id                bigint          20                       √         √
topics                  varchar         255
url                     varchar         300                                √
title                   varchar         200                                √
content                 longtext                                           √
create_time             datetime
update_time             datetime
answer_num              int             11            0                    √
comments_num            int             11            0                    √
watch_user_num          int             11            0                    √
click_num               int             11            0                    √
crawl_time              datetime                                           √
crawl_update_time       datetime

# 在数据库article_spider的tables下，新建表 zhihu_answer
Field Name              Datatype        Len         Default     PK?     Not Null
zhihu_id                bigint          20                       √         √
url                     varchar         300                                √
question_id             bigint          20                                 √
author_id               varchar         100                                             #可能为匿名回答，所以可以为null
content                 longtext                                           √
parise_num              int             11            0                    √
comments_num            int             11            0                    √
create_time             datetime                                           √
update_time             datetime                                           √
crawl_time              datetime                                           √
crawl_update_time       datetime

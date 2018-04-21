# 在F:\eclipse\···\···\test_scrapy_spider下新建文件夹job_info
# 用于存放spider的状态，这样才能暂停  
# 不同的spider不能共用一个目录  #同一个spider在第二次启动暂停的时候也不能共用一个目录
# scrapy的爬虫结束信号接收ctrl+c命令

# 在cmder下
C:\Users\admin
(scrapy_test) λ f:

F:\cmder\vendor\git-for-windows
(scrapy_test) λ cd F:\eclipse\···\···\test_scrapy_spider

F:\eclipse\···\···\test_scrapy_spider
(scrapy_test) λ scrapy crawl lagou -s JOBDIR=job_info/001  
#也可以在settings.py中设置 JOBDIR = "job_info/001"  #也可以以custom_settings，把"JOBDIR" : "job_info/001" 写到spider里

# 一次ctrl+c暂停  两次ctrl+c强制退出，相当于kill

F:\eclipse\···\···\test_scrapy_spider
(scrapy_test) λ scrapy crawl lagou -s JOBDIR=job_info/001  #从上次暂停的地方继续运行

# 两次ctrl+c强制退出，相当于kill

F:\eclipse\···\···\test_scrapy_spider
(scrapy_test) λ scrapy crawl lagou -s JOBDIR=job_info/002  #重新开始运行



# test_scrapy_spider\job_info\001\requests.seen      #保存已经访问过的url
# test_scrapy_spider\job_info\001\spider.state       #保存spider的状态信息
# test_scrapy_spider\job_info\001\requests.queue\p0  #保存待处理的url

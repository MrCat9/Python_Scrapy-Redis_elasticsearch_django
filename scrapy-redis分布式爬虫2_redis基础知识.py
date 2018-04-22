# redis的安装（windows 64位）  https://github.com/MicrosoftArchive/redis/releases



# Redis文档
# http://www.runoob.com/redis/redis-tutorial.html
# http://redisdoc.com/



# 测试redis

# 打开一个cmder 窗口，使用cd命令切换目录到自己解压后文件夹的目录中（F:\Redis-x64-3.2.100），

# 运行 redis-server.exe redis.windows.conf
C:\Users\admin
λ cd F:\Redis-x64-3.2.100

C:\Users\admin
λ f:

F:\Redis-x64-3.2.100
λ redis-server.exe redis.windows.conf

# 这时候另启一个cmd窗口，原来的cmd窗口不可关闭，不然Redis服务端就关闭了，就无法访问了。

# 切换到redis目录下（F:\Redis-x64-3.2.100）

# 运行redis-cli.exe -h 127.0.0.1 -p 6379
C:\Users\admin
λ f:

F:\cmder\vendor\git-for-windows
λ cd F:\Redis-x64-3.2.100

F:\Redis-x64-3.2.100
λ redis-cli.exe -h 127.0.0.1 -p 6379
127.0.0.1:6379>    #启动成功



# Redis的数据类型
# 1.字符串
# 2.散列/哈希
# 3.列表
# 4.集合
# 5.可排序集合



# 字符串命令
# set mykey "123"   创建变量
# get mykey   查看变量
# getrange mykey start end   获取字符串，如:get name 1 6 #获取name1~6的字符串
# strlen mykey   获取长度
# incr/decr mykey    加一减一，类型是int
# append mykey ''com''   添加字符串，添加到末尾

127.0.0.1:6379> set mykey 123
OK
127.0.0.1:6379> get mykey
"123"

127.0.0.1:6379> set name helloWorld
OK
127.0.0.1:6379> strlen name
(integer) 10
127.0.0.1:6379> getrange name 1 6
"elloWo"

127.0.0.1:6379> incr mykey
(integer) 124
127.0.0.1:6379> decr mykey
(integer) 123

127.0.0.1:6379> append mykey 00
(integer) 5
127.0.0.1:6379> get mykey
"12300"
127.0.0.1:6379> append mykey "abc"
(integer) 8
127.0.0.1:6379> get mykey
"12300abc"



# 哈希命令
# hset myhash name "123abc"   创建变量，myhash类似于变量名，name类似于key，"123abc"类似于values
# hgetall myhash   得到key和values两者
# hget myhash  name  得到values
# hexists myhash name  检查是否存在这个哈希字段(name)
# hdel myhash name   删除这个key
# hkeys myhash   查看key
# hvals myhash   查看values

127.0.0.1:6379> hset myhash name 123abc  #用于为哈希表中的字段赋值 。 
(integer) 1     #如果哈希表不存在，一个新的哈希表被创建并进行 HSET 操作。 如果字段已经存在于哈希表中，旧值将被覆盖。
127.0.0.1:6379> hget myhash name
"123abc"
127.0.0.1:6379> hgetall myhash    #返回哈希表中，所有的字段和值。 
1) "name"        #在返回值里，紧跟每个字段名(field name)之后是字段的值(value)，
2) "123abc"      #所以返回值的长度是哈希表大小的两倍。
127.0.0.1:6379> hexists myhash name
(integer) 1         #回复整数，1或0。  #如果哈希包含字段-->1    #如果哈希不包含字段，或key不存在-->0
127.0.0.1:6379> hdel myhash name
(integer) 1         #删除成功返回1  失败返回0
127.0.0.1:6379> hkeys myhash    #用于查找所有符合给定模式 pattern 的 key 。。
(empty list or set)
127.0.0.1:6379> hvals myhash    #返回哈希表所有字段的值
(empty list or set)
127.0.0.1:6379>
127.0.0.1:6379> hset myhash name "xiaoming"
(integer) 1
127.0.0.1:6379> hkeys myhash
1) "name"
127.0.0.1:6379> hvals myhash
1) "xiaoming"
127.0.0.1:6379>
127.0.0.1:6379> hset myhash name2 "xiaohong"
(integer) 1
127.0.0.1:6379> hset myhash name3 "xiaodong"
(integer) 1
127.0.0.1:6379> hgetall myhash
1) "name"
2) "xiaoming"
3) "name2"
4) "xiaohong"
5) "name3"
6) "xiaodong"
127.0.0.1:6379> hkeys myhash
1) "name"
2) "name2"
3) "name3"
127.0.0.1:6379> hvals myhash
1) "xiaoming"
2) "xiaohong"
3) "xiaodong"



# 列表命令
# lpush/rpush mylist "list123"  左添加/右添加值
# lrange mylist 0 10   查看列表0~10的值
# blpop/brpop key1[key2] timeout   左删除/右删除一个，timeout是如果没有key，等待设置的时间后结束。
# lpop/rpop key   左删除/右删除，没有等待时间。
# llen key  获得长度
# lindex key index    取第index元素，index是从0开始的

# 命令				说明
# lpop/rpop			左删除/右删除
# llen mtianyan		长度
# lindex mtianyan 3	第几个元素
# sadd				集合做减法
# siner				交集
# spop				随机删除
# srandmember			随机选择多个元素
# smembers			获取set所有元素
# srandmember			随机选择多个元素
# zadd				每个数有分数
# zcount key 0 100	0-100分数据量统计

127.0.0.1:6379> lpush courses "scrapy"
(integer) 1
127.0.0.1:6379> lpush courses "django"
(integer) 2
127.0.0.1:6379> lrange courses 0 10
1) "django"    # lpush是左添加，添加在了表头
2) "scrapy"
127.0.0.1:6379> rpush courses "scrapy-redis"
(integer) 3
127.0.0.1:6379> lrange courses 0 10
1) "django"
2) "scrapy"
3) "scrapy-redis"
127.0.0.1:6379> blpop courses123 3  # timeout3s
(nil)
(3.04s)
127.0.0.1:6379> blpop courses 3  #左删除
1) "courses"
2) "django"
127.0.0.1:6379> lrange courses 0 10
1) "scrapy"
2) "scrapy-redis"
127.0.0.1:6379> rpop courses    # lpop/rpop 没有timeout参数，它不会等待
"scrapy-redis"
127.0.0.1:6379> lrange courses 0 10
1) "scrapy"
127.0.0.1:6379> llen courses
(integer) 1
127.0.0.1:6379>
127.0.0.1:6379> rpush courses abc1
(integer) 2
127.0.0.1:6379> rpush courses abc2
(integer) 3
127.0.0.1:6379> rpush courses abc3
(integer) 4
127.0.0.1:6379> lrange courses 0 10
1) "scrapy"
2) "abc1"
3) "abc2"
4) "abc3"
127.0.0.1:6379> lindex courses 1    # index从0开始
"abc1"



# 集合命令（集合-->不重复的list）
# sadd myset "abc123"   添加内容，返回1表示set中不存在该member，添加成功。返回0表示已存在该member，添加失败。
# scard key  查看set中member的个数
# sdiff key1 [key2]   2个set做减法，其实就是减去了交集部分
# sinter key1 [key2]    2个set做加法，其实就是留下了两者的交集
# spop key   随机删除值  返回删除的值
# srandmember key [count]  随机获取count个值  不写count默认取出一个
# smembers key   获取全部的元素

127.0.0.1:6379> sadd course_set "django"
(integer) 1  #添加成功
127.0.0.1:6379> sadd course_set "django"
(integer) 0  #添加失败
127.0.0.1:6379> scard course_set
(integer) 1
127.0.0.1:6379> sadd course_set "scrapy"
(integer) 1
127.0.0.1:6379> scard course_set
(integer) 2
127.0.0.1:6379>
127.0.0.1:6379> sadd course_set2 "scrapy"
(integer) 1
127.0.0.1:6379> sadd course_set2 "redis"
(integer) 1
127.0.0.1:6379> sdiff course_set course_set2  #course_set减去与course_set2的交集（scrapy），剩下django  #course_set中的member没被删除
1) "django"
127.0.0.1:6379> sdiff course_set2 course_set
1) "redis"
127.0.0.1:6379> sinter course_set course_set2  #取交集
1) "scrapy"
127.0.0.1:6379> scard course_set
(integer) 2
127.0.0.1:6379> spop course_set  #随机删除一个
"django"
127.0.0.1:6379> scard course_set
(integer) 1
127.0.0.1:6379> srandmember course_set2 1
1) "redis"
127.0.0.1:6379> srandmember course_set2 1
1) "redis"
127.0.0.1:6379> srandmember course_set2 1
1) "scrapy"
127.0.0.1:6379> srandmember course_set2 2
1) "scrapy"
2) "redis"
127.0.0.1:6379> smembers course_set2
1) "redis"
2) "scrapy"



# 可排序集合命令
# zadd key [NX|XX] [CH] [INCR] score member [score member ...]   添加集合元素
# zrangebyscore key 0 100   选取分数在0~100的元素
# zcount key min max   选取分数在min~max的元素的个数

127.0.0.1:6379> zadd zcourses_set 0 "django" 5 "scrapy" 10 "scrapy-redis"
(integer) 3
127.0.0.1:6379> zrangebyscore zcourses_set 6 10
1) "scrapy-redis"
127.0.0.1:6379> zcount zcourses_set 6 10
(integer) 1



127.0.0.1:6379> keys *  #查看redis中的所有变量
1) "name"
2) "mykey"
3) "course_set2"
4) "zcourses_set"
5) "myhash"
6) "courses"
7) "course_set"
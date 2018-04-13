爬虫去重策略-->跳出，防止陷入死循环
1. 将访问过的url保存到数据库中
  （效率低，每一个都要查一下，但最简单）
2. 将访问过的url保存到set中（保存在内存中），只要o(1)【这是常数阶时间复杂度】的代价就可以查询url  （速度快，基本上不需要做查询，但内存占用会越来越大）
  （100000000*2byte*50个字符/1024/1024/1024≈9G ）
  （一亿条url，一个字符两个byte（Unicode编码）,一条50字符）（保守估计，一亿条url需要9G内存）
3. url经过md5等方法哈希后保存到set中（比较常用）  （scarpy）
  （将任意长度的url压缩到同样长度的MD5字符串）（将url的字符缩减到固定的长度（较短），使得内存占用减少）
4. 用bitmap方法，将访问过的url通过hash函数映射到某一位（一个bit）
  （但hash可能把不同的url映射到同一个位上，这就发生了冲突）（可以继续向下寻址，来解决hash的冲突问题）
5. bloomfilter方法对bitmap进行改进，多重hash函数降低冲突
   （既有bitmap减少内存的作用，又减少了冲突）
   （100000000/8/1024/1024≈12M）

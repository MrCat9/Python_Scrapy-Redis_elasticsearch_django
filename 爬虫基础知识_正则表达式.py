正则表达式
1. 特殊字符
    1)  ^  $  *  ?  +  {2}  {2,}  {2,5}  |
    2)  []  [^]  [a-z]  .
    3)  \s  \S  \w  \W
    4)  [\u4E00-\u9FA5]  ()  \d


#coding:gb18030
import re
#  ^  $
str1 = 'abc123'
if re.match(r'^a.*3$', str1):  #匹配以a开头3结尾的字符串
    print('yes')  #yes
else:
    print('no')

#  ?
str2 = 'abbcc112233a2aa3a'
regex_str = '.*(a.*a).*'
match_obj = re.match(regex_str, str2)
if match_obj:
    print(match_obj.group(1))  #a3a  #说明是从str2末尾开始匹配的

#若要匹配abbcc112233a， 可以加上？ 变成非贪婪匹配模式，从左边开始匹配。默认的匹配模式是贪婪的，从右边开始
str2 = 'abbcc112233a2aa3a'
regex_str = '.*?(a.*a).*'
match_obj = re.match(regex_str, str2)
if match_obj:
    print(match_obj.group(1))  #abbcc112233a2aa3a  #前面一个a非贪婪了，但后面一个还是贪婪的  #前一个a从左往右，后一个a从右往左

str2 = 'abbcc112233a2aa3a'
regex_str = '.*?(a.*?a).*'
match_obj = re.match(regex_str, str2)
if match_obj:
    print(match_obj.group(1))  #abbcc112233a

#+
str3 = 'abc123aaabc'
regex_str = '.*(a.*a).*'
match_obj = re.match(regex_str, str3)
if match_obj:
    print(match_obj.group(1))  #aa

str3 = 'abc123aaabc'
regex_str = '.*(a.+a).*'
match_obj = re.match(regex_str, str3)
if match_obj:
    print(match_obj.group(1))  #aaa

str3 = 'abc123aa456abc'
regex_str = '.*(a.+a).*'
match_obj = re.match(regex_str, str3)
if match_obj:
    print(match_obj.group(1))  #a456a

#{2}  {2,}  {2,5}
str4 = 'abc123abca1aa22aa333a'
regex_str = '.*(a.{2}a).*'
match_obj = re.match(regex_str, str4)
if match_obj:
    print(match_obj.group(1))  #a22a

str4 = 'abc123abca1aa22aa333a'
regex_str = '.*(a.{3,}a).*'
match_obj = re.match(regex_str, str4)
if match_obj:
    print(match_obj.group(1))  #a333a

str4 = 'abc123abca1aa22aa333a'
regex_str = '.*(a.{4,}a).*'
match_obj = re.match(regex_str, str4)
if match_obj:
    print(match_obj.group(1))  #aa333a

str4 = 'abc123abca1aa22a'
regex_str = '.*(a.{2,5}a).*'
match_obj = re.match(regex_str, str4)
if match_obj:
    print(match_obj.group(1))  #a22a

str4 = 'abc123abca1aa666666a'
regex_str = '.*(a.{2,5}a).*'
match_obj = re.match(regex_str, str4)
if match_obj:
    print(match_obj.group(1))  #a1aa

#  |
str5 = 'abc123'
regex_str = '(abc|abc123)'
match_obj = re.match(regex_str, str5)
if match_obj:
    print(match_obj.group(1))  #abc

str5 = 'abc123'
regex_str = '(abc123|abc)'
match_obj = re.match(regex_str, str5)
if match_obj:
    print(match_obj.group(1))  #abc123

str5 = 'abc'
regex_str = '(abc123|abc)'
match_obj = re.match(regex_str, str5)
if match_obj:
    print(match_obj.group(1))  #abc

str5 = 'aabc123'
regex_str = '(abc|aabc)123'
match_obj = re.match(regex_str, str5)
if match_obj:
    print(match_obj.group(1))  #aabc
    print(match_obj)  #<_sre.SRE_Match object; span=(0, 7), match='aabc123'>

str5 = 'aabc123'
regex_str = '((abc|aabc)123)'
match_obj = re.match(regex_str, str5)
if match_obj:
    print(match_obj.group(1))  #aabc123
    print(match_obj.group(2))  #aabc

#  []
str6 = 'abc123'
regex_str = '([abcd]bc123)'
match_obj = re.match(regex_str, str6)
if match_obj:
    print(match_obj.group(1))  #abc123

str6 = '13112345678'  #匹配电话号码
regex_str = '(1[356789][0-9]{9})'
match_obj = re.match(regex_str, str6)
if match_obj:
    print(match_obj.group(1))  #13112345678

str6 = '13abcdefghi'
regex_str = '(1[356789][^1]{9})'  #[^1] mean not 1  #[.*]匹配 . 或者 *
match_obj = re.match(regex_str, str6)
if match_obj:
    print(match_obj.group(1))  #13abcdefghi

#  /s  /S
str7 = 'hello world'
regex_str = '(hello\sworld)'
match_obj = re.match(regex_str, str7)
if match_obj:
    print(match_obj.group(1))  #hello world
    
str7 = 'helloAworld'
regex_str = '(hello\sworld)'
match_obj = re.match(regex_str, str7)
if match_obj:
    print(match_obj.group(1))  #
    
str7 = 'hello1world'
regex_str = '(hello\Sworld)'
match_obj = re.match(regex_str, str7)
if match_obj:
    print(match_obj.group(1))  #hello1world
 
str7 = 'hello12world'
regex_str = '(hello\Sworld)'
match_obj = re.match(regex_str, str7)
if match_obj:
    print(match_obj.group(1))  #

str7 = 'hello12world'
regex_str = '(hello\S+world)'
match_obj = re.match(regex_str, str7)
if match_obj:
    print(match_obj.group(1))  #hello12world

#  \w  \W  #\w == [A-Za-z0-9_]
str8 = 'hello_world'
regex_str = '(hello\wworld)'
match_obj = re.match(regex_str, str8)
if match_obj:
    print(match_obj.group(1))  #hello_world

str8 = 'hello world'
regex_str = '(hello\Wworld)'
match_obj = re.match(regex_str, str8)
if match_obj:
    print(match_obj.group(1))  #hello world

str8 = 'hello`world'
regex_str = '(hello\Wworld)'
match_obj = re.match(regex_str, str8)
if match_obj:
    print(match_obj.group(1))  #hello`world

#  [\u4E00-\u9FA5]  #匹配汉字
str9 = '你好abc123'
regex_str = '([\u4E00-\u9FA5]+)'
match_obj = re.match(regex_str, str9)
if match_obj:
    print(match_obj.group(1))  #你好

str9 = 'study in 北京大学'  #提取大学名称
regex_str = '.*?([\u4E00-\u9FA5]+大学)'
match_obj = re.match(regex_str, str9)
if match_obj:
    print(match_obj.group(1))  #北京大学

#  \d
str10 = 'xxx is 100 years old'
regex_str = '.*?(\d+) years old'
match_obj = re.match(regex_str, str10)
if match_obj:
    print(match_obj.group(1))  #100



#提取出生年月日
#coding:gb18030
import re

str = ['xxx出生于2012年6月25日', 
       'xxx出生于2012年6月',
       'xxx出生于2012/6/25', 
       'xxx出生于2012-6-25', 
       'xxx出生于2012-06-25', 
       'xxx出生于2012-6']
regex_str = '.*出生于(\d{4}[年/-]\d{1,2}([月/-]\d{1,2}(日|$)|[月/-]$|$))'
for str1 in str:
    match_obj = re.match(regex_str, str1)
    if match_obj:
        print(match_obj.group(1))
#2012年6月25日
#2012年6月
#2012/6/25
#2012-6-25
#2012-06-25
#2012-6

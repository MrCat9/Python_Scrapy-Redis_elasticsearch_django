字符串编码
1. 计算机只能识别数字，文本转换为数字才能处理。计算机中8个bit作为一个字节，所以一个字节能表示最大的数字就是255.
2. 计算机是美国人发明的，所以一个字节可以表示所有字符了，所以ASCII（一个字节）编码就成为美国人标准编码。
3. 但是ASCII处理中文明显是不够的，中文不止255个汉字，所以中国制定了GB2312编码，用两个字节表示一个汉字。
   GB2312还把ASCII包含进去了，同理，日文，韩文等等上百个国家为了解决这个问题就都发展了一套字节的编码，
   标准就越来越多，如果出现多种语言混合就一定会出现乱码。
4. 于是unicode出现了，将所有语言统一到一套编码里。
5. ASCII和unicode编码：
（1）字母A用ASCII编码十进制65，二进制01000001
（2）汉字‘中’已超多ASCII编码的范围，用unicode编码是20013，二进制01001110 00101101
（3）A用unicode编码中只需要前面补0，二进制是 00000000 01000001
6. 乱码问题解决可，但是如果内容全是英文，unicode编码比ASCII需要多一倍的存储空间，同时如果传输需要多一倍的传输。
7. 所以出现了可变长的编码“utf-8”，把英文变长一个字节，汉字3个字节。特别生僻的变成4-6字节。如果传输大量的英文，utf-8作用就很明显。

                    储存或传输时：转换为utf-8编码
Unicode编码（内存）<----------------------------->utf-8编码（文件）
                      读取时：转换为Unicode编码



python的字符串在内存中是用Unicode编码的

decode：其他编码-->Unicode编码
decode('gb18030')  的作用： gb18030-->Unicode编码

import sys
print(sys.getdefaultencoding())  #utf-8  #查看默认编码

encode(encoding='utf8')方法是先decode成Unicode，再encode成utf8
                            这就需要被encode的对象最好是一个Unicode编码
                            如果encode的对象不是Unicode，就会先decode
                            又因为decode需要指明是哪种编码decode成unicode
                            而在没指明的情况下将会用默认编码进行decode
                            所以它在执行decode的时候就可能会报错

.decode('gb18030').encode('utf-8')



python2的话最好在文件开头加上#coding:utf8
不然python通过解释器读文件时，里面的中文会识别不了，会报错

python3不需要，都识别为Unicode，支持中文
所以python3可以直接encode

#
# -*- coding: utf-8 -*-
import datetime

time = 1234567
print(time)  #1234567
print(time.__class__)  #<class 'int'>

time1 = datetime.datetime.fromtimestamp(time)
print(time1)  #1970-01-15 14:56:07
print(time1.__class__)  #<class 'datetime.datetime'>

time2 = datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")  #1970-01-15 14:56:07
print(time2)
print(time2.__class__)  #<class 'str'>




#coding=utf-8
#聚合数据，采样点间隔10分钟
#注意：scheduled_flt_time和actual_flt_time 两列使用国际航空的标准时间：格林威治时间
#其余为北京时间
import time
import datetime
import csv

s = "2016-09-14-14-28-01"
t = datetime.datetime.strptime(s, "%Y-%m-%d-%H-%M-%S")
mt = time.mktime(t.timetuple())


'''
    t = datetime.datetime.strptime(timeStamp, "%Y-%m-%d-%H-%M-%S")
    mt = time.mktime(t.timetuple())
'''

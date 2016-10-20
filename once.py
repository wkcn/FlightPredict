#coding=utf-8
import MySQLdb
import time
import datetime
import matplotlib.pyplot as plt
import re
import csv

db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 

year = 2016
month = 9
day = 24
name = "E1-1A-1<E1-1-01>"

sql = "select timestamp, count from wifi where wifitag = '%s' and timestamp like '%d-%.2d-%.2d%%'" % (name ,year, month, day)

cursor.execute(sql)

results = cursor.fetchall()
ts = []
counts = []
for timestamp, count in results:
    t = datetime.datetime.strptime(timestamp, "%Y-%m-%d-%H-%M-%S")
    #mt = time.mktime(t.timetuple())
    #ts.append(mt)
    e = t.hour * 60 + t.minute
    ts.append(e)
    counts.append(count)
  

fs = []
sql = "select scheduled_flt_time, actual_flt_time from flights natural join gates where BGATE_AREA = '%s' and scheduled_flt_time like '%d/%d/%d %%' " % (name.split('-')[0], year, month, day)
print sql
cursor.execute(sql)
results = cursor.fetchall()
for scheduled_flt_time, actual_flt_time in results:
    timestamp = scheduled_flt_time
    if actual_flt_time:
        timestamp = scheduled_flt_time
    t = datetime.datetime.strptime(timestamp, "%Y/%m/%d %H:%M:%S")
    e = (t.hour+8) * 60 + t.minute
    fs.append(e)

print fs


plt.plot(ts,counts, 'b.')
zs = [10 for _ in range(len(fs))]
plt.plot(fs,zs,'r.', lineWidth = 5)
plt.show()

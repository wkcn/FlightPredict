#coding=utf-8
import MySQLdb
import time
import datetime
import matplotlib.pyplot as plt

db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 

def GetCount(name, day, hour, minute):
    ti = "2016-09-%.2d-%.2d-%d" % (day, hour, minute)
    bti = "2016-09-%.2d %d:%d" % (day, hour, minute)
    sql = "select avg(pcount) from wifi where wifitag = '%s' and timestamp like '%s%%'" % (name,ti)
    cursor.execute(sql)
    results = cursor.fetchall()
    for r in results:
        if r[0]:
            sql = "insert wifi_count(wifitag,pcount,timestamp) values ('%s',%lf, '%s')" % (name, r[0], bti)
            cursor.execute(sql)

def get_wifi_name():
    sql = "select distinct wifitag from wifi" 
    cursor.execute(sql)
    results = cursor.fetchall()
    wifi_name = []
    for r in results:
        wifi_name.append(r[0])
    return wifi_name

name = "E1-1A-1<E1-1-01>"
day = 10
hour = 0
minute = 5

wifis = get_wifi_name()
fo = file("wfs_new.txt", "w")
for w in wifis:
    fo.write(w + '\n')
fo.close()
#GetCount(name,day, hour, minute)
#db.commit()
for i in range(len(wifis)):
    for day in range(10, 25+1):
        for hour in range(0, 24):
            for minute in range(6):
                GetCount(wifis[i], day, hour, minute)
    db.commit()
    print (i, len(wifis))

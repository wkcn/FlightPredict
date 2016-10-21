#coding=utf-8
import MySQLdb
import time
import datetime
import matplotlib.pyplot as plt

db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 

def GetCount(day, hour, minute):
    ti = "2016-09-%.2d %d:%d" % (day, hour, minute)
    sql = "select flight_ID, count(*) from security_check where security_time like '%s%%' group by flight_ID" % ti
    cursor.execute(sql)
    results = cursor.fetchall()
    for r in results:
        sql = "insert security_count(time, flight_ID, count) values ('%s','%s', %d)" % (ti, r[0], r[1])
        cursor.execute(sql)

day = 10
hour = 4
minute = 2

#GetCount(day, hour, minute)
for day in range(10, 25+1):
    for hour in range(0, 24):
        print (day, hour)
        for minute in range(6):
            GetCount(day, hour, minute)
    db.commit()

#coding=utf-8
import MySQLdb
import time
import datetime
import matplotlib.pyplot as plt

db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 

for day in range(10, 25+1):
    se = set()
    sql = "select count(*),flight_ID from flights where scheduled_flt_time like '2016/9/%d%%' group by flight_ID" % day
    cursor.execute(sql)
    results = cursor.fetchall()
    for r,flight_ID in results:
        if r > 1:
            print "hahaha", flight_ID, r, day

print "over"

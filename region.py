#coding=utf-8
import MySQLdb
import time
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 

def viewRegion(name):
    sql = "select time, pcount from person_count where BGATE_AREA = '%s'" % (name)
    cursor.execute(sql)
    results = cursor.fetchall()
    ts = []
    pc = []
    for ti, pcount in results:
        t = datetime.datetime.strptime(ti + '0', "%Y-%m-%d %H:%M")
        y = t.day * 24 * 60 + t.hour * 60 + t.minute
        ts.append(y)
        pc.append(pcount)
    dta = pd.Series(pc)
    diff1 = dta.diff(100)
    plt.plot(diff1)
    plt.show()



def get_wifi(name):
    sql = "select timestamp, pcount from wifi_count where wifitag = '%s';" % name

    cursor.execute(sql)
    results = cursor.fetchall()
    ts = []
    counts = []
    for timestamp, count in results:
        t = datetime.datetime.strptime(timestamp + '0', "%Y-%m-%d %H:%M")
        y = t.day * 24 * 60 + t.hour * 60 + t.minute
        #mt = time.mktime(t.timetuple())
        ts.append(y)
        counts.append(count)
    plt.plot(ts, counts, 'b.')


def get_wifis(name):
    sql = "select timestamp, pcount from wifi_count where wifitag like '%s%%';" % name

    cursor.execute(sql)
    results = cursor.fetchall()
    print len(results)
    ts = []
    counts = []
    data = {}
    for timestamp, count in results:
        t = datetime.datetime.strptime(timestamp + '0', "%Y-%m-%d %H:%M")
        y = t.day * 24 * 60 + t.hour * 60 + t.minute
        #mt = time.mktime(t.timetuple())
        #ts.append(y)
        #counts.append(count)
        if y not in data:
            data[y] = 0
        data[y] += count
    for t in sorted(data.keys()):
        ts.append(t)
        counts.append(data[t])
    plt.plot(ts, counts, 'b.')


viewRegion("E1")
#get_wifis("E1-1A-1<E1-1-01>")
#get_wifis("E1")
#plt.show()

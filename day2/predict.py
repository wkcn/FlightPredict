#coding=utf-8
import MySQLdb
import time
import datetime
import matplotlib.pyplot as plt
import re
import csv

from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import *
from pybrain.supervised import *
import numpy as np


db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 
 
def get_wifi_name():
    sql = "select distinct wifitag from wifi" 
    cursor.execute(sql)
    results = cursor.fetchall()
    wifi_name = []
    for r in results:
        wifi_name.append(r[0])
    return wifi_name

def get_wifi(name):
    sql = "select timestamp, count from wifi where wifitag = '%s';" % name

    cursor.execute(sql)
    results = cursor.fetchall()
    ts = []
    counts = []
    for timestamp, count in results:
        t = datetime.datetime.strptime(timestamp, "%Y-%m-%d-%H-%M-%S")
        mt = time.mktime(t.timetuple())
        ts.append(mt)
        counts.append(count)
    return ts,counts

def CompareALL():
    ts,counts = get_wifi("E1-1A-1<E1-1-01>")
    print (len(ts))
    plt.plot(ts,counts, 'b')
    '''
    ts,counts = get_wifi("E1-1A-2<E1-1-02>")
    plt.plot(ts,counts, 'r')
    ts,counts = get_wifi("E1-1A-3<E1-1-03>")
    plt.plot(ts,counts, 'g')
    '''
    ts,counts = get_wifi("E1-1A-2<E1-1-02>")
    print (len(ts))
    plt.plot(ts,counts, 'g')
    plt.show()

def CompareDay(name):
    sql = "select timestamp, count from wifi where wifitag = '%s';" % name

    cursor.execute(sql)
    results = cursor.fetchall()
    dat = "2016-09-10"
    ldat = len(dat)
    ts = []
    counts = []
    pattern = re.compile("\d+")
    for timestamp,count in results: 
        #t = datetime.datetime.strptime(timestamp[ldat+1:], "%H-%M-%S")
        #mt = time.mktime(t.timetuple())
        p = pattern.findall(timestamp)
        hour = int(p[3])
        minute = int(p[4])
        mt = (hour * 60 + minute)
        ts.append(mt)
        counts.append(count)
    return ts, counts




def predict(name):
    ts, counts = CompareDay(name)

    cc = {} # 样本数量, 连接人数
    for i in range(len(ts)):
        t = ts[i]
        c = counts[i]
        if t not in cc:
            cc[t] = (0,0)
        cc[t] = (cc[t][0]+1, cc[t][1]+c)
    out = []
    for hour in range(15, 19):
        for minute in range(0, 6):
            sample = 0.0
            count = 0.0
            for m in range(0, 10):
                t = hour * 60 + minute * 10 + m
                if t in cc:
                    sample += cc[t][0]
                    count += cc[t][1]
            co = count * 1.0 / sample
            out.append((round(co, 3), name, "2016-09-25-%.2d-%d" % (hour, minute) )) 
    return out


#wifi_file = open("wf.txt")
#wifis = []
#for line in wifi_file.readlines():
#    wifis.append(line.strip())
wifis = get_wifi_name()

csvfile = file("result.csv", "wb")
writer = csv.writer(csvfile)
writer.writerow(["passengerCount", "WIFIAPTag", "slice10min"])
le = len(wifis)
for i in range(len(wifis)):
    print ("%d/%d" % (i, le))
    name = wifis[i]
    try:
        p = predict(name)
        writer.writerows(p)
    except:
        pass

print ("over")

import MySQLdb
import time
import datetime
import matplotlib.pyplot as plt
import re

from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import *
from pybrain.supervised import *
import numpy as np


db = MySQLdb.connect("localhost", "root", "wk", "flight1")
cursor = db.cursor() 
 
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


ts, counts = CompareDay("E1-1A-2<E1-1-02>")


#plt.subplot(2,2,1)
plt.plot(ts, counts, 'g.')

cc = {}
for i in range(len(ts)):
    t = ts[i]
    c = counts[i]
    if t not in cc:
        cc[t] = (0,0)
    cc[t] = (cc[t][0]+1, cc[t][1]+c)
out = []
for i in range(len(ts)):
    t = ts[i]
    out.append(cc[t][1] / cc[t][0]) 

plt.plot(ts, out, 'r.')

err = 0.
for i in range(len(ts)):
    t = ts[i]
    c = counts[i]
    y = out[i]
    err += (c-y) ** 2

print "Error: %lf" % err
#plt.subplot(2,2,2)
#CompareDay("E1-1A-2<E1-1-02>")
#plt.subplot(2,2,3)
#CompareDay("E1-1A-3<E1-1-03>")
#plt.subplot(2,2,4)
#CompareDay("E1-1A-4<E1-1-04>")
plt.show()



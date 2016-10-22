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
import pandas as pd
import statsmodels.api as sm


db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 

def get_wifi(name):
    sql = "select timestamp, pcount from wifi where wifitag = '%s';" % name

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

ts,counts = get_wifi("E1-1A-1<E1-1-01>")
#plt.plot(ts, counts, 'b')
#plt.show()

'''
dta = pd.Series(counts)
plt.subplot(2,2,1)
plt.plot(counts)
diff1 = dta.diff(1)
plt.subplot(2,2,2)
plt.plot(diff1)
plt.subplot(2,2,3)
diff2 = dta.diff(2)
plt.plot(diff2)
plt.subplot(2,2,4)
diff3 = dta.diff(3)
plt.plot(diff3)
plt.show()
'''
counts = range(10000)
dta = pd.Series(counts)

#dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001','2090'))

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta,lags=100,ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta,lags=100,ax=ax2)

plt.show()

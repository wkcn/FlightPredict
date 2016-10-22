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
import Queue as queue
import copy


db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 

def wifi(name):
    sql = "select timestamp, pcount from wifi_count where wifitag = '%s'" % name
    cursor.execute(sql)
    results = cursor.fetchall()
    datas = []
    for timestamp, count in results:
        t = datetime.datetime.strptime(timestamp + '0', "%Y-%m-%d %H:%M")
        datas.append((t, count)) 
    return datas

def get_history_avg(name, t):
    sql = "select avg(pcount) from wifi_count where wifitag = '%s' and timestamp like '%%%d:%d'" % (name, t.hour, t.minute // 10)
    cursor.execute(sql)
    results = cursor.fetchone()
    return results[0]

name = "E1-1A-1<E1-1-01>"
t = datetime.datetime(2016,9,25,15,0)
#print get_history_avg(name, t)
datas = wifi(name)

#10 minutes
#4 hour * 6
#7 个特征向量
#4 hour = 1 part
buf = []
partSize = 4 * 60 / 10 
partNum = 6
partP = partSize * partNum
ds = SupervisedDataSet(1 + partNum, 1)
for t,count in datas: 
    buf.append(count)
    if len(buf) > partP:
        del buf[0]
    if len(buf) == partP:
        x = [0.0 for _ in range(1 + partNum)]
        x[0] = get_history_avg(name, t)
        for i in range(1, partNum + 1):
            st = -1 - (i-1) * partSize
            su = 0.0
            for j in range(st, st-partSize, -1):
                su += buf[j]
            su /= partSize
            x[i] = su
        y = count
        #x = [y for _ in range(1+partNum)]
        #y = 10
        ds.addSample(x, y)

fnn = buildNetwork(1 + partNum,6, 4, 1, bias = True)
trainer = BackpropTrainer(fnn, ds, verbose=True)
print ("Start Training")
trainer.trainEpochs(epochs=1000)

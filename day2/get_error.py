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
days = range(10, 25+1)
 
def get_wifi_name():
    sql = "select distinct wifitag from wifi" 
    cursor.execute(sql)
    results = cursor.fetchall()
    wifi_name = []
    for r in results:
        wifi_name.append(r[0])
    return wifi_name

def get_wifi(name):
    sql = "select timestamp, pcount from wifi where wifitag = '%s';" % name

    cursor.execute(sql)
    results = cursor.fetchall()
    pattern = re.compile("\d+")
    rec = {}
    for timestamp, count in results:
        t = datetime.datetime.strptime(timestamp, "%Y-%m-%d-%H-%M-%S")
        if t.day not in rec:
            rec[t.day] = [[(0,0) for _ in range(6)] for _ in range(24)]
            #(num, sum of counts)
        p = rec[t.day][t.hour][t.minute // 10]
        rec[t.day][t.hour][t.minute // 10] = (p[0] + 1, p[1] + count) 
    return rec

def get_total_avg(data):
    av = [[0 for _ in range(6)] for _ in range(24)]
    for hour in range(24):
        for minute in range(6):
            sample = 0
            count = 0
            for d in days:
                sample += data[d][hour][minute][0]
                count += data[d][hour][minute][1]
            u = 0
            if sample > 0:
                u = count * 1.0 / sample
            av[hour][minute] = u
    return av

def get_day_avg(data):
    av = {}#[[0 for _ in range(6)] for _ in range(24)]
    for d in days:
        av[d] = [[0 for _ in range(6)] for _ in range(24)]
        for hour in range(24):
            for minute in range(6):
                p = data[d][hour][minute]
                u = 0
                if p[0] > 0:
                    u = p[1] * 1.0 / p[0]
                av[d][hour][minute] = u
    return av

def get_error(source, pre):
    err = 0.0
    for d in days:
        for hour in range(24):
            for minute in range(6):
                e = source[d][hour][minute] - pre[d][hour][minute]
                err += e ** 2
    return err

def predict(data, name):
    #error: 151179.674143
    av = get_total_avg(data)
    pre = {}
    for d in days:
        pre[d] = av
    return pre

def predict2(data, name):
    davg = get_day_avg(data)
    av = get_total_avg(data)
    frontNum = davg[days[0]][0][0]
    le = len(days) * 24 * 6
    X = np.matrix(np.zeros((le, 2)))
    y = np.matrix(np.zeros((le, 1)))
    i = 0
    for d in days:
        for hour in range(24):
            for minute in range(6):
                X[i, 0] = av[hour][minute]#davg[d][hour][minute]
                X[i, 1] = frontNum
                y[i, 0] = davg[d][hour][minute]
                frontNum = davg[d][hour][minute]
                i += 1

    '''
    fnn = buildNetwork(2, 2, 1, bias = True)
    ds = SupervisedDataSet(2, 1)
    for i in range(len(X)):
        ds.addSample(X[i], y[i])

    trainer = BackpropTrainer(fnn, ds, momentum=0.1, verbose=True, weightdecay=0.01)
    print ("start training")
    trainer.trainEpochs(epochs=50)

    pre = {}
    frontNum = av[0][0]
    for d in days:
        pre[d] = [[(0,0) for _ in range(6)] for _ in range(24)]
        for hour in range(24):
            for minute in range(6):
                out = SupervisedDataSet(2, 1)
                X = np.zeros((1,2))
                X[0][0] = av[hour][minute]
                X[0][1] = frontNum
                out.addSample(X, 0)
                out = fnn.activateOnDataset(out)
                frontNum = out[0][0]
                pre[d][hour][minute] = frontNum
    '''
    pre = {}
    i = (X.T * X)
    x = i.I * (X.T * y)


    #'''
    frontNum = av[0][0]
    for d in days:
        pre[d] = [[(0,0) for _ in range(6)] for _ in range(24)]
        for hour in range(24):
            for minute in range(6):
                X = np.matrix(np.zeros((1,2)))
                X[0, 0] = av[hour][minute]
                X[0, 1] = frontNum
                out = X * x
                frontNum = out[0, 0]
                u = 10
                pre[d][hour][minute] = (av[hour][minute]*u + frontNum) / (u+1)
                pre[d][hour][minute] = av[hour][minute]
   
    return pre
    #'''
    frontNum = av[15][0]
    rut = []
    for hour in range(15, 19):
        for minute in range(0, 6):
            X = np.matrix(np.zeros((1,2)))
            X[0, 0] = av[hour][minute]
            X[0, 1] = frontNum
            out = X * x
            frontNum = out[0, 0]
            u = 10
            co = (av[hour][minute]*u + frontNum) / (u+1)
    
            rut.append((round(co, 1), name, "2016-09-25-%.2d-%d" % (hour, minute) )) 
    return rut




name = "E1-1A-1<E1-1-01>"
data = get_wifi(name)
pre = predict(data, name)
tavg = get_day_avg(data)
ds = []
ps = []
for d in days:
    for hour in range(24):
        for minute in range(6):
            ds.append(tavg[d][hour][minute])
            ps.append(pre[d][hour][minute])
print get_error(tavg, pre)
plt.plot(ds, 'r')
plt.plot(ps, 'b')
plt.show()

'''
wifis = get_wifi_name()
le = len(wifis)
csvfile = file("airport_gz_passenger_predict.csv", "wb")
writer = csv.writer(csvfile)
writer.writerow(["passengerCount", "WIFIAPTag", "slice10min"])
for i in range(len(wifis)):
    print ("%d/%d" % (i, le))
    name = wifis[i]
    try:
        data = get_wifi(name)
        p = predict2(data, name)
        writer.writerows(p)
    except:
        pass

'''

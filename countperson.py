#coding=utf-8
import MySQLdb
import time
import datetime
import matplotlib.pyplot as plt
import Queue as queue

db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 

# 安检十五分钟后, 飞机起飞二十分钟前, 认为人在某个区域中

def GO(area, data):
    person = 0
    q = queue.PriorityQueue()
    for d in data:
        q.put(d)
    lastTime = None
    rec = {}
    while not q.empty():
        #print (area, q.qsize())
        time, actual_flt_time, pcount, kind = q.get()
        #print area, time, actual_flt_time, pcount, kind, person
        #raw_input()
        '''
        if lastTime != time and lastTime != None:
            tstr = "2016-09-%.2d %d:%d" % (lastTime.day, lastTime.hour, lastTime.minute // 10)
            sql = "insert person_count(BGATE_AREA, time, pcount) values ('%s', '%s', %d)" % (area, tstr, person)
            try:
                cursor.execute(sql)
            except:
                pass
        lastTime = time
        '''
        if kind == 1:
            person += pcount
            q.put((actual_flt_time, actual_flt_time, pcount, -1))
        elif kind == -1:
            person -= pcount

        rec[time] = person
    '''
    if lastTime:
        tstr = "2016-09-%.2d %d:%d" % (lastTime.day, lastTime.hour, lastTime.minute // 10)
        sql = "insert person_count(BGATE_AREA, time, pcount) values ('%s', '%s', %d)" % (area, tstr, person)
        cursor.execute(sql)
    '''
    for t in sorted(rec.keys()):
        p = rec[t]
        tstr = "2016-09-%.2d %d:%d" % (t.day, t.hour, t.minute // 10)
        sql = "insert person_count(BGATE_AREA, time, pcount) values ('%s', '%s', %d)" % (area, tstr, p)
        cursor.execute(sql)



sql = "select BGATE_AREA, time, actual_flt_time, pcount from region_count"
cursor.execute(sql)
results = cursor.fetchall()

gates = {}

for BGATE_AREA, time, actual_flt_time, pcount in results:
    if BGATE_AREA not in gates:
        gates[BGATE_AREA] = []
    ti = datetime.datetime.strptime(time + '0', "%Y-%m-%d %H:%M")

    act = datetime.datetime.strptime(actual_flt_time + '0', "%Y-%m-%d %H:%M")

    ti += datetime.timedelta(minutes = 20) 
    act -= datetime.timedelta(minutes = 20) 
    gates[BGATE_AREA].append((ti, act, pcount, 1))

for area in gates.keys():
    GO(area, gates[area])
    db.commit()
print ("over")

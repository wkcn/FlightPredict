#coding=utf-8
import MySQLdb
import time
import datetime
import matplotlib.pyplot as plt

db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 

'''
ti = "2016/9/11 13:50:00"
ti2 = "2016/9/10 13:50:00"

t = datetime.datetime.strptime(ti, "%Y/%m/%d %H:%M:%S")
t2 = datetime.datetime.strptime(ti2, "%Y/%m/%d %H:%M:%S")
print (t - t2).total_seconds() # timedelta
'''

def write_data():
    sql = "select flight_time, checkin_time from departure"
    cursor.execute(sql)
    results = cursor.fetchall()
    data = []
    for flight_time, checkin_time in results:
        try:
            ft = datetime.datetime.strptime(flight_time, "%Y/%m/%d %H:%M:%S")
            ct = datetime.datetime.strptime(checkin_time, "%Y/%m/%d %H:%M:%S")
            escape = (ft - ct).total_seconds()
            if escape > 3000 * 60:
                print flight_time, checkin_time
                break
            data.append(escape)
        except:
            pass

    plt.hist(data)
    plt.show()

    '''
    fi = open("wait.txt", "wb")
    for i in data:
        fi.write(str(i) + ",")
    '''

def draw_data():
    fi = open("wait.txt", "r")
    w = fi.read()
    sp = w.split(',')[:-1]
    miss = 0
    data = []
    for d in sp:
        minute = round(float(d) / 60)
        if minute > 8 * 60:
            miss += 1
            continue
        data.append(minute)
    print (len(data), "miss: %d" % miss)
    plt.hist(data, 1000)
    plt.show()
#write_data()
draw_data()

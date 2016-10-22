#coding=utf-8
import MySQLdb
import time
import datetime
import matplotlib.pyplot as plt

db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 

def GetAreas():
    sql = "select BGATE_ID, BGATE_AREA from gates"
    cursor.execute(sql)
    results = cursor.fetchall()
    res = {}
    for eid,area in results:
       res[eid] = area
    return res

err = 0

def GetAF(year, month, day, hour, minute):
    rt = datetime.datetime(year, month, day, hour, minute)
    ti = "%d-%.2d-%.2d %d:%d" % (year, month, day, hour, minute)
    sql = "select flight_ID, pcount from security_count where time = '%s'" % (ti)
    cursor.execute(sql)
    results = cursor.fetchall()
    for flight_ID, pcount in results:
        #t2 and t3 is Green time

        t2 = datetime.datetime(year, month, day, hour) + datetime.timedelta(hours = -8)
        ti2 = "%d/%d/%d" % (t2.year, t2.month, t2.day) #格林威治
        sql2 = "select BGATE_ID, scheduled_flt_time, actual_flt_time from flights where flight_ID = '%s' and scheduled_flt_time like '%s%%'" % (flight_ID, ti2)
        cursor.execute(sql2)
        res2 = cursor.fetchall()

        t3 = t2 + datetime.timedelta(days = 1)
        ti3 = "%d/%d/%d" % (t3.year, t3.month, t3.day) #格林威治
        sql3 = "select BGATE_ID, scheduled_flt_time, actual_flt_time from flights where flight_ID = '%s' and scheduled_flt_time like '%s%%'" % (flight_ID, ti3)
        cursor.execute(sql3)
        res3 = cursor.fetchall()

        rrr = []
        tt = 24 * 60 * 60 * 7 
        for BGATE_ID, scheduled_flt_time, actual_flt_time in res2 + res3:
            flt_time = scheduled_flt_time
            if actual_flt_time:
                flt_time = actual_flt_time
            try:
                st = datetime.datetime.strptime(flt_time, "%Y/%m/%d %H:%M:%S") + datetime.timedelta(hours = 8)
                escape = (st - rt).total_seconds()
                if escape > 0 and escape < tt:
                    tt = escape
                    rrr = [BGATE_ID, scheduled_flt_time, actual_flt_time]
            except:
                pass



        if len(rrr):
            BGATE_ID, scheduled_flt_time, actual_flt_time = rrr
            if BGATE_ID in areas:
                ae = areas[BGATE_ID]
                if len(actual_flt_time) == 0:
                    actual_flt_time = scheduled_flt_time
                #BGATE_AERA, scheduled_flt_time, actual_flt_time, pcount
                #print ae, scheduled_flt_time, actual_flt_time, pcount
                sst = ""
                aat = ""
                try:
                    st = datetime.datetime.strptime(scheduled_flt_time, "%Y/%m/%d %H:%M:%S") + datetime.timedelta(hours = 8)
                    sst = "2016-09-%.2d %d:%d" % (st.day, st.hour, st.minute // 10)
                except:
                    pass
                try:
                    at = datetime.datetime.strptime(actual_flt_time, "%Y/%m/%d %H:%M:%S") + datetime.timedelta(hours = 8)
                    aat = "2016-09-%.2d %d:%d" % (at.day, at.hour, at.minute // 10)
                except:
                    pass
                sqli = "insert region_count(BGATE_AREA, time, scheduled_flt_time, actual_flt_time, pcount) values ('%s','%s','%s','%s',%d)" % (ae,ti, sst, aat,pcount)
                try:
                    cursor.execute(sqli)
                except:
                    pass


areas = GetAreas()

year = 2016
month = 9
day = 14
hour = 9
minute  = 1

for day in range(10, 25+1):
    for hour in range(0, 24):
        print (day, hour)
        for minute in range(6):
            GetAF(year, month, day, hour, minute)
    db.commit()


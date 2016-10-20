import time
import datetime

ti = "2016/9/11 13:50:00"
ti2 = "2016/9/11 13:51:00"

t = datetime.datetime.strptime(ti, "%Y/%m/%d %H:%M:%S")
t2 = datetime.datetime.strptime(ti2, "%Y/%m/%d %H:%M:%S")

print (t2 - t).total_seconds()

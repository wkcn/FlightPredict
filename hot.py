#coding=utf-8
import MySQLdb
import time
import datetime
import matplotlib.pyplot as plt
import re
import csv

db = MySQLdb.connect("localhost", "root", "wk", "flight2")
cursor = db.cursor() 

'''
sql = "select security_time, scheduled_flt_time, actural_flt_time, BGATE_AREA from security_check natural join flights natural join gates"
cursor.execute(sql)
results = cursor.fetchall()
print len(results)
'''

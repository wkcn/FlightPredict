#coding=utf-8
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

dta=[10930,10318,10595,10972,7706,6756,9092,10551,9722,10913,11151,8186,6422,
        6337,11649,11652,10310,12043,7937,6476,9662,9570,9981,9331,9449,6773,6304,9355,
        10477,10148,10395,11261,8713,7299,10424,10795,11069,11602,11427,9095,7707,10767,
        12136,12812,12006,12528,10329,7818,11719,11683,12603,11495,13670,11337,10232,
        13261,13230,15535,16837,19598,14823,11622,19391,18177,19994,14723,15694,13248,
        9543,12872,13101,15053,12619,13749,10228,9725,14729,12518,14564,15085,14722,
        11999,9390,13481,14795,15845,15271,14686,11054,10395]
dta = pd.Series(dta)
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001','2090'))
dta.plot(figsize=(12,8))

#diff1= dta.diff(1)#我们已经知道要使用一阶差分的时间序列，之前判断差分的程序可以注释掉 //原文有错误应该是diff1= dta.diff(1)，而非dta= dta.diff(1)
fig = plt.figure(figsize=(12,8))
ax1=fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta,lags=40,ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta,lags=40,ax=ax2)
plt.show()

# 按照保洁的原始数据点画出行动轨迹。
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import traceTools as tt
from dateutil.parser import parse
from matplotlib import font_manager
import yinweilai

# 各参数设置
filename='~/Documents/2023-01-06_9038.xlsx'
date=pd.to_datetime('2023-01-06')
name=input('请输入需要查询的保洁姓名：')

df=pd.read_excel(filename, sheet_name=name)
t0=date+pd.to_timedelta('7:30:00')
t1=date+pd.to_timedelta('11:30:00')
t2=date+pd.to_timedelta('12:30:00')
t3=date+pd.to_timedelta('16:30:00')

dff=tt.dataNormalize(df, t0, t1, t2, t3)
# jump=tt.checkBlockJump(dff)
print(tt.workArea(name))
tt.workCover(dff, name)

# dff.to_excel('~/Documents/test1.xlsx')


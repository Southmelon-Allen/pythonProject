# 按照保洁的原始数据点画出行动轨迹。
import seaborn as sns
import pandas as pd
import traceTools as rt
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from dateutil.parser import parse
from matplotlib import font_manager

# 各参数设置
filename="~/datasets/pressure_data/唐和玉_20221213.xlsx"
df = pd.read_excel(filename)

ts=df['deviceTimestamp'].values
ts=[pd.to_datetime(i) for i in ts]

# 设置中午下班(t0)/上班(t1)时间
yy=ts[0].year
mm=ts[0].month
dd=ts[0].day
t0=datetime(yy, mm, dd, 8, 20)
t1=datetime(yy, mm, dd, 11, 30)
t2=datetime(yy, mm, dd, 12, 30)
t3=datetime(yy, mm, dd, 16, 30)

dff=rt.dataNormalize(df, t0, t1, t2, t3)
print(dff)

# jumps=rt.checkBlockJump(dff)
#
# print(jumps)
#
# rt.checkDataNum(ts)
# rt.checkDataGap(ts,2)

#
# gap=[(int(ts[i+1])-int(ts[i]))/1000 for i in range(len(ts)-1)]
# plt.plot(gap)
# plt.show()



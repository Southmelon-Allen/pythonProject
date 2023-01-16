# 保洁作业轨迹，按照5分钟一组，10个数据点进行投票。

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time

#def locVote(locs):

df = pd.read_excel("~/datasets/5772.xlsx")
rows=len(df.index)
cols=len(df.columns)-2

timeList=[]
floorList=[]

# 数据清洗
for i in range(rows):
    tt = df.loc[i, "updateTime"] + pd.to_timedelta("8:00:00")  # 换算到北京时间。
    timeList.append(tt)
    if (df.loc[i, "building"]=="14栋")&(df.loc[i, "unit"]=="1单元"):
        if "层" in df.loc[i, "floor"]:
            #t=str(df.loc[i, "updateTime"])
            #print(t)
            #tt=t[11:19]
            #tt=df.loc[i, "updateTime"]+pd.to_timedelta("8:00:00") #换算到北京时间。
            #timeList.append(tt)
            str1=str(df.loc[i, "floor"])
            loc=str1.find("层")
            floorNum=int(str1[0:loc])
            floorList.append(floorNum)
    else: floorList.append(0)

#数据点投票
floorList1=[]
timeList1=[]

for i in range(int(rows/5)):
    timeList1.append(timeList[i*5])
    floors=floorList[i*5:i*5+5]
    floorList1.append(np.argmax(np.bincount(floors)))


title="Cleaner Trace"
#sns.set_style("whitegrid")
#sns.set(rc={'figure.figsize':(11.7,6.27)})

fig=sns.scatterplot(x=timeList1, y=floorList1, color="blue", y_jitter=5)
fig.set_title(title)
plt.grid(axis="y")
plt.show()
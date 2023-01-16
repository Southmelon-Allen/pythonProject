# 按照保洁的原始数据点画出行动轨迹。
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel("~/Desktop/zxl1001.xlsx")
rows=len(df.index)
cols=len(df.columns)-2

keyword=["时间", "楼栋", "单元", "楼层", "步数"]
timeList=[]
floorList=[]
workArea=[["4栋", "1单元"], ["4栋", "2单元"]]#, ["19栋", "2单元"], ["4栋", "1单元"]]
workSteps=0
workStepCount=0
voidTime=pd.to_timedelta("0:00:00")
steps=0

#判断当前数据点是否在工作区域内
def inArea(area):
    if area in workArea: return True
    else: return False

#限幅滤波法
def ampFilter(floors, limit=5):
    for i in range(len(floors)-1):
        if abs(floors[i]-floors[i+1])>=limit:
            floors[i+1]=floors[i]
    return floors

def medFilter(floors, period=5):
    for i in range(int(len(floors)/period)):
        value=np.median(floors[i*period: (i+1)*period])
        for j in range(period):
            floors[i*period+j]=value
    return floors

#筛选出楼层的数据点
for i in range(rows):
    tt = df.loc[i, keyword[0]] + pd.to_timedelta("8:00:00")  # 换算到北京时间。
    timeList.append(tt)
    area=["",""]
    area[0]=df.loc[i, keyword[1]]
    area[1]=df.loc[i, keyword[2]]

    if inArea(area):
        if "层" in df.loc[i, keyword[3]]:
            str1=str(df.loc[i, keyword[3]])
            loc=str1.find("层")
            floorNum=int(str1[0:loc])
            floorList.append(floorNum)
        else: floorList.append(0)
        #计算步数差
        if i<rows-1: steps=df.loc[i+1, keyword[4]]-df.loc[i, keyword[4]]
        workSteps+=steps
        #计算有步数的数据点
        if steps>0: workStepCount+=1
        steps=0
    else:
        floorList.append(0)

print("当天工作区域内总步数: ", workSteps)
print("当天工作区域内有步数的时长：", workStepCount/2, "分钟")
print("作业效率: ", workSteps*2/workStepCount)

floorList=medFilter(floorList, 10)
#计算10个点的移动平均

floorList1=[]
timeList1=[]

for i in range(len(timeList)-10):
    sma10=sum(floorList[i:i+10])/10
    floorList1.append(int(sma10))
    timeList1.append(timeList[i])

title="Cleaner Trace"

#尝试滤波算法
timeList2=[]
floorList2=[]

#floorlist2=jf.SlidingAverage(np.array(floorList).T, 10)

#print(floorlist2)
#print(timeList[0:len(floorList2)])

#sns.set_style("whitegrid")
#sns.set(rc={'figure.figsize':(11.7,6.27)})

fig=sns.barplot(x=timeList, y=floorList, color="blue")
fig.set_title(title)
plt.grid(axis="y")
plt.show()
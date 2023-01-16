# 按照保洁的原始数据点画出行动轨迹。
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import jitterFilter as jf
import numpy as np
import datetime
from dateutil.parser import parse
from matplotlib import font_manager

#配置数据
workerName="钱叶芝"
enName="Qian Yezhi"
areaName="Building 5"
filename="~/datasets/yinweilai-workers/"+workerName+".xlsx"
keyword=["时间", "楼栋", "单元", "楼层", "步数"]
noon="12:00:00"
workArea=[["5栋", "1单元"], ["5栋", "2单元"]]#, ["19栋", "2单元"], ["4栋", "1单元"]]

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


dff = pd.read_excel(filename, sheet_name=None)
sheets=list(dff.keys())

metrics=pd.DataFrame(index=sheets, columns=["steps", "morning steps", "afternoon steps", "work time", "morning time","afternoon time", "efficiency"])
metrics["steps"]=np.zeros(len(sheets))
metrics["morning steps"]=np.zeros(len(sheets))
metrics["afternoon steps"]=np.zeros(len(sheets))
metrics["work time"]=np.zeros(len(sheets))
metrics["morning time"]=np.zeros(len(sheets))
metrics["afternoon time"]=np.zeros(len(sheets))
metrics["efficiency"]=np.zeros(len(sheets))



for s in sheets:
    #数据初始化
    timeList = []
    floorList = []
    moveList=[]
    workSteps = 0
    workStepCount = 0
    steps = 0
    morningSteps=0
    afternoonSteps=0
    morningStepCount=0
    afternoonStepCount=0

    df=dff[s]

    location = pd.DataFrame(index=df.index, columns=["timestamp", "floor"])

    rows=len(df.index)
    cols=len(df.columns)-2

    #筛选出楼层的数据点
    for i in range(rows):


        tt = df.loc[i, keyword[0]]# + pd.to_timedelta("8:00:00")  # 换算到北京时间。
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
            if steps>0:
                moveList.append("moving")
                workStepCount+=1
                if df.loc[i, keyword[0]]<noon:
                    morningSteps+=steps
                    morningStepCount+=1
                else:
                    afternoonSteps+=steps
                    afternoonStepCount+=1
            else: moveList.append("not moving")
            steps=0
        else:
            floorList.append(-3)
            moveList.append("not moving")

    metrics.loc[s, "steps"]=workSteps
    metrics.loc[s, "work time"] = int(workStepCount/2)
    metrics.loc[s, "morning steps"] = morningSteps
    metrics.loc[s, "afternoon steps"] = afternoonSteps
    metrics.loc[s, "morning time"] = int(morningStepCount / 2)
    metrics.loc[s, "afternoon time"] = int(afternoonStepCount / 2)
    if workStepCount!=0: metrics.loc[s, "efficiency"]= int(workSteps*2/workStepCount)
    else:metrics.loc[s, "efficiency"]= 0

    print(s)

    #print("当天工作区域内有步数的时长：", workStepCount/2, "分钟")
    #print("作业效率: ", workSteps*2/workStepCount)

    floorList=medFilter(floorList, 10)
    timeList1=list(map(parse, timeList))

    location["timestamp"]=timeList
    location["floor"]=floorList

    title=s+ workerName+" in "+areaName
    #remark="steps:"+str(workSteps)+", total time:"+str(int(workStepCount/2))+", efficiency:"+str(int(workSteps*2/workStepCount))
    #floorlist2=jf.SlidingAverage(np.array(floorList).T, 10)

    #print(floorlist2)
    #print(timeList[0:len(floorList2)])

    #sns.set_style("whitegrid")
    #sns.set(rc={'figure.figsize':(11.7,6.27)})
    df["时间"]=np.array(timeList1)
    df["楼层"]=np.array(floorList)
    #df.plot.bar(y="楼层", x="时间")


    # plt.bar(x=timeList1, y=floorList)
    # plt.show()

    # fig=sns.scatterplot(x=timeList1, y=floorList, hue=moveList, marker="+")
    # fig.set_title(title)
    # plt.grid(axis="y")
    # #plt.text('0:0:0', 22, remark)
    # plt.show()
    # fname=s+enName+".jpg"
    #plt.savefig(fname)
    #plt.clf()


    # fig = plt.figure(figsize=(5, 3), dpi=100)
    # plt.bar(df.index, floorList, width=0.5, label="楼层")


    #设定中文字体
    #mac系统中查询中文字体：fc-list :lang=zh

    # my_font=font_manager.FontProperties(fname="/System/Library/AssetsV2/com_apple_MobileAsset_Font7/e2d3f9277678ccbf64020abef4c0eb9a1de1bed3.asset/AssetData/Lantinghei.ttc")
    #
    #
    # x=[x for x in df.index[::100]]
    # _x=["{}时".format(x) for x in timeList[::100]]
    # plt.xticks(x, _x, rotation=45, fontproperties=my_font)
    # plt.yticks(range(-3, 24))
    # plt.xlabel("时间", fontproperties=my_font, fontsize="small")
    # plt.ylabel("楼层", fontproperties=my_font)
    # plt.title(title, fontproperties=my_font)
    # plt.grid(alpha=0.5)
    # plt.legend(loc="best", prop=my_font )
    # plt.show()
    # break

# metrics.to_excel("~/Documents/"+enName+".xlsx")


with pd.ExcelWriter("~/Documents/test.xlsx") as ewriter:
    df.to_excel(ewriter, sheet_name="sheetA")
    metrics.to_excel(ewriter, sheet_name="sheetB")
# 生成印未来人员的效能分析表
# 指标维度见：

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import jitterFilter as jf
import numpy as np

# dff = pd.read_excel(filename, sheet_name=None)
# sheets=list(dff.keys())

metrics=pd.DataFrame(index=sheets, columns=["steps",
                                            "morning steps",
                                            "afternoon steps",
                                            "work time",
                                            "morning time",
                                            "afternoon time",
                                            "efficiency"])



# metrics["steps"]=np.zeros(len(sheets))
# metrics["morning steps"]=np.zeros(len(sheets))
# metrics["afternoon steps"]=np.zeros(len(sheets))
# metrics["work time"]=np.zeros(len(sheets))
# metrics["morning time"]=np.zeros(len(sheets))
# metrics["afternoon time"]=np.zeros(len(sheets))
# metrics["efficiency"]=np.zeros(len(sheets))
#
# for s in sheets:
#     #数据初始化
#     timeList = []
#     floorList = []
#     workSteps = 0
#     workStepCount = 0
#     steps = 0
#     morningSteps=0
#     afternoonSteps=0
#     morningStepCount=0
#     afternoonStepCount=0
#
#     df=dff[s]
#
#     rows=len(df.index)
#     cols=len(df.columns)-2
#
#     #筛选出楼层的数据点
#     for i in range(rows):
#
#
#         tt = df.loc[i, keyword[0]]# + pd.to_timedelta("8:00:00")  # 换算到北京时间。
#         timeList.append(tt)
#         area=["",""]
#         area[0]=df.loc[i, keyword[1]]
#         area[1]=df.loc[i, keyword[2]]
#
#         if inArea(area):
#             if "层" in df.loc[i, keyword[3]]:
#                 str1=str(df.loc[i, keyword[3]])
#                 loc=str1.find("层")
#                 floorNum=int(str1[0:loc])
#                 floorList.append(floorNum)
#             else: floorList.append(0)
#             #计算步数差
#             if i<rows-1: steps=df.loc[i+1, keyword[4]]-df.loc[i, keyword[4]]
#             workSteps+=steps
#
#             #计算有步数的数据点
#             if steps>0:
#                 workStepCount+=1
#                 if df.loc[i, keyword[0]]<noon:
#                     morningSteps+=steps
#                     morningStepCount+=1
#                 else:
#                     afternoonSteps+=steps
#                     afternoonStepCount+=1
#             steps=0
#         else:
#             floorList.append(0)
#
#     metrics.loc[s, "steps"]=workSteps
#     metrics.loc[s, "work time"] = int(workStepCount/2)
#     metrics.loc[s, "morning steps"] = morningSteps
#     metrics.loc[s, "afternoon steps"] = afternoonSteps
#     metrics.loc[s, "morning time"] = int(morningStepCount / 2)
#     metrics.loc[s, "afternoon time"] = int(afternoonStepCount / 2)
#     if workStepCount!=0: metrics.loc[s, "efficiency"]= int(workSteps*2/workStepCount)
#     else:metrics.loc[s, "efficiency"]= 0
#
#     print(s)
#
#     floorList=medFilter(floorList, 10)
#
#     title=s+enName+" in "+areaName


    #plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    #plt.rcParams['axes.unicode_minus'] = False    # 解决无法显示符号的问题
    #sns.set(font='SimHei', font_scale=0.8)        # 解决Seaborn中文显示问题

    # fig=sns.barplot(x=timeList, y=floorList, color="blue")
    # fig.set_title(title)
    # plt.grid(axis="y")
    # #plt.text('0:0:0', 22, remark)
    # plt.show()
    # fname=s+enName+".jpg"
    # plt.savefig(fname)
    # plt.clf()

metrics.to_excel("~/Documents/"+enName+".xlsx")
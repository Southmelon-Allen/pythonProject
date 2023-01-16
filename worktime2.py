# 计算从运营平台时长统计导出的数据，进行格式转换
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import datetime


df = pd.read_excel("~/Desktop/西海岸人员数据.xlsx")
rows=len(df.index)
cols=len(df.columns)-2

for row in range(rows):
    for col in range(3):
        str1 = str(df.iloc[row, col + 4])
        #print(str1)
        hs = "0"
        ms = "0"
        #print(str1)
        if str1.find("h")>-1:
            hs=str1[0:str1.find("h")]
            ms=str1[str1.find("h")+1:len(str1)]
            if ms=="": ms="0"
        else:
            ms=int(str1)  #没有"h" 只有分钟数

        worktime=int(hs)*60+int(ms)
        #print(hs, ms)
        df.iloc[row, col+4]=worktime

df.to_excel("~/Desktop/xihaian_output.xlsx")

#title="Staying Time"
#sns.set_style("whitegrid")
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
# plt.rcParams['axes.unicode_minus'] = False    # 解决无法显示符号的问题
# sns.set(font='SimHei', font_scale=0.8)        # 解决Seaborn中文显示问题

#sns.set(rc={'figure.figsize':(11.7,6.27)})

#floorTime=df["2022-09-20"]
#floorList=df.index.values

#fig=sns.barplot(x=floorList, y=floorTime, color="grey")
#fig.set_title(title)
#plt.show()
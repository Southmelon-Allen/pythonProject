import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager


def notCover(a, m=2, n=34):
    b=[]
    for i in range(m, n+1):
        if i not in a: b.append(i)
    return b

filename="~/Desktop/yajule-data.xlsx"

dff = pd.read_excel(filename, sheet_name=None)
sheets=list(dff.keys())
floors=pd.DataFrame(index=range(2, 36), columns=sheets)

for s in sheets:

    print("Worker", s)
    floors[s]=np.zeros(34)

    df=dff[s]
    dd=df[df["层数"]!=0]
    coverList=list(dd["覆盖层数"].values)

    noCoverList=[]

    for l in coverList:
        if pd.isna(l): continue

        ll=l[l.find("[")+1: l.find("]")]
        ll=ll.split(",")
        if ll==['']: continue
        lll=[int(x) for x in ll]
        noCoverList.append(notCover(lll))

    for r in floors.index:
        for col in noCoverList:
            if r in col: floors.loc[r, s]+=1
    floors.loc[35, s]=len(noCoverList)

    #设定中文字体
    #mac系统中查询中文字体：fc-list :lang=zh

    my_font=font_manager.FontProperties(fname="/System/Library/AssetsV2/com_apple_MobileAsset_Font7/e2d3f9277678ccbf64020abef4c0eb9a1de1bed3.asset/AssetData/Lantinghei.ttc")
    title=s
    fig = plt.figure(figsize=(10, 6))
    plt.bar(floors.index, floors[s], width=0.5, label="未覆盖天数")

    # x=[x for x in df.index[::100]]
    # _x=["{}时".format(x) for x in timeList[::100]]
    plt.xticks(range(2, 36))
    plt.yticks(range(1, 31))
    plt.xlabel("楼层", fontproperties=my_font)
    plt.ylabel("未覆盖天数", fontproperties=my_font)
    plt.title(title, fontproperties=my_font)
    plt.grid(alpha=0.5)
    # plt.legend(loc="best", prop=my_font )
    plt.savefig(s+".jpg")
    plt.clf()
    # plt.show()
    # break



floors.to_excel("~/Documents/notCover.xlsx")
# 按照保洁的原始数据点画出行动轨迹。
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

filename="~/Downloads/徐朝之1.xlsx"

df = pd.read_excel(filename)
dff = df[:72]
# 设定中文字体
# mac系统中查询中文字体：fc-list :lang=zh


my_font=font_manager.FontProperties(fname="/System/Library/AssetsV2/com_apple_MobileAsset_Font7/e2d3f9277678ccbf64020abef4c0eb9a1de1bed3.asset/AssetData/Lantinghei.ttc")

y1=dff['气压定位'].values
y2=dff['wifi定位'].values
xx=dff['上报时间'].values
# yy=df['pressureHeight'].values
yt=list(range(-2, 24))
del yt[2]

y1=[int(i[4:]) for i in y1]
y2=[int(i[4:]) for i in y2]
xx=[i[-8:-3] for i in xx]


fig = plt.figure()
# ax1 = fig.add_subplot(1,2,1)
# ax2 = fig.add_subplot(1,2,2)


# plt.plot(list(range(len(xx))), y2, color='orange')
plt.plot(list(range(len(xx))), y1, color='blue')



xl=[i for i in xx[::5]]
x=list(range(len(xx)))[::5]

plt.title("印未来超保-徐朝之 3幢2单元轨迹 2022-12-6", fontproperties=my_font)
plt.xticks(x, xl, rotation=45)
plt.yticks(yt)
plt.ylabel('楼层', fontproperties=my_font)
plt.grid(alpha=0.5)

# ax1.set_xticks(x)
# ax2.set_xticks(x)
#
# ax1.set_xticklabels(xl, rotation=90)
# ax2.set_xticklabels(xl, rotation=90)
#
# ax1.set_yticks(yt)
# ax2.set_yticks(range(-2, 75, 3))

# ax1.set_xlabel("时间", fontproperties=my_font)
# ax2.set_xlabel("时间", fontproperties=my_font)

# ax1.set_ylabel("楼层", fontproperties=my_font)
# ax2.set_ylabel("高度（米）", fontproperties=my_font)
#
# ax1.set_title("东原印未来2幢2单元楼层定位 2022-12-5", fontproperties=my_font)
# ax2.set_title("东原印未来2幢2单元高度定位 2022-12-5", fontproperties=my_font)
#
# ax1.grid(alpha=0.5)
# ax2.grid(alpha=0.5)

# ax1.legend(loc="best", prop=my_font )
# ax2.legend(loc="best", prop=my_font )


plt.show()
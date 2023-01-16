# 按照保洁的原始数据点画出行动轨迹。
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

filename="~/Downloads/dongyuan1205-1.xlsx"

df = pd.read_excel(filename)

# 设定中文字体
# mac系统中查询中文字体：fc-list :lang=zh


my_font=font_manager.FontProperties(fname="/System/Library/AssetsV2/com_apple_MobileAsset_Font7/e2d3f9277678ccbf64020abef4c0eb9a1de1bed3.asset/AssetData/Lantinghei.ttc")

y=df['楼层定位'].values
xx=df['数据时间'].values
yy=df['pressureHeight'].values
yt=list(range(-1, 24))
del yt[1]

fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

ax1.plot(xx, y, color='blue')
ax2.plot(xx, yy, color='orange')

x=[i for i in range(len(xx))[::10]]
xl=[i[-8:-3] for i in xx[::10]]

ax1.set_xticks(x)
ax2.set_xticks(x)

ax1.set_xticklabels(xl, rotation=90)
ax2.set_xticklabels(xl, rotation=90)

ax1.set_yticks(yt)
ax2.set_yticks(range(-2, 75, 3))

# ax1.set_xlabel("时间", fontproperties=my_font)
# ax2.set_xlabel("时间", fontproperties=my_font)

ax1.set_ylabel("楼层", fontproperties=my_font)
ax2.set_ylabel("高度（米）", fontproperties=my_font)

ax1.set_title("东原印未来2幢2单元楼层定位 2022-12-5", fontproperties=my_font)
ax2.set_title("东原印未来2幢2单元高度定位 2022-12-5", fontproperties=my_font)

ax1.grid(alpha=0.5)
ax2.grid(alpha=0.5)

# ax1.legend(loc="best", prop=my_font )
# ax2.legend(loc="best", prop=my_font )


plt.show()


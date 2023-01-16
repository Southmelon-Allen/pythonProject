# 按照保洁的原始数据点画出行动轨迹。
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from dateutil.parser import parse
from matplotlib import font_manager

# 各参数设置
filename="~/Downloads/洪金英1208.xlsx"
step=20
yt=list(range(-2, 23))
time_limit=2   # 至少多长时间（分钟）算是一次作业
bu=['2-1', '2-2', '5-2']  #负责的楼栋单元范围
del yt[2]

df = pd.read_excel(filename)
my_font=font_manager.FontProperties(fname="/System/Library/AssetsV2/com_apple_MobileAsset_Font7/e2d3f9277678ccbf64020abef4c0eb9a1de1bed3.asset/AssetData/Lantinghei.ttc")

# 拆分楼栋、单元、楼层
locs=df['block'].values
b_u=[i[0:3] for i in locs]
# unit=[int(i[2]) for i in locs]
# floors=[int(i[4:]) for i in locs]

# 计算完成度结果
# 算出总体的点位数，生成所有点位的集合。

pts=[]
for b in bu:
    for f in yt:
        pts.append('{0}-{1}'.format(b, f))
pts0=pts
pts=set(pts)
# 计算出所有去过点位的集合
locs=set(locs)

# 对比，打印完成度结果
print('======作业完成度数据======')
print('今日应作业点位数： ', len(pts))
print('今日实际作业点位数： ', len(pts & locs))
print('今日点位覆盖率：{:.2f} '.format(len(pts & locs)/len(pts)))
print('今日未覆盖点位： ', set.difference(pts, (pts & locs)))
print('=======================')

# 计算点位的频次
# 把作业轨迹，按照点位-停留时间的流水拉成一个两列的矩阵。
trace=[]
con=1

for i in range(len(df.index)-1):
    loc_now=df.loc[i, 'block']
    loc_next=df.loc[i+1, 'block']
    if loc_now not in pts: continue  #如果不在工作区域内，不算
    if loc_now==loc_next:
        con+=1
    else:
        trace.append([loc_now, con/2])
        con=1

# df0: 每个点位的轨迹和停留时间
df0 = pd.DataFrame(trace, columns=['point','time'])

# df1: 该保洁人员当天在所有点位的总停留时间和打卡频次
df1 = pd.DataFrame(np.zeros((len(pts), 2)), index=pts0, columns=['time_total', 'freq'])

for p in df1.index:
    dd=df0[df0['point']==p]
    df1.loc[p, 'freq']=len(dd)
    df1.loc[p, 'time_total']=sum(dd['time'].values)

# 创建一个dataframe，index为所有点位，列为'频度'和'总停留时间'
# 统计每个点位的频度（小于2分钟不统计）
# 统计每个点位的停留时间

# 输出excel结果
# 参考代码 >>> with pd.ExcelWriter('output.xlsx') as writer:  # doctest: +SKIP
#     ...
#     df1.to_excel(writer, sheet_name='Sheet_name_1')
#     ...
#     df2.to_excel(writer, sheet_name='Sheet_name_2')
#
#     >>> with pd.ExcelWriter('output.xlsx',
#                              ...                     mode='a') as writer:  # doctest: +SKIP
#         ...
#         df.to_excel(writer, sheet_name='Sheet_name_3')
with pd.ExcelWriter('~/Downloads/人效统计.xlsx') as writer:
    df0.to_excel(writer, sheet_name='作业轨迹')
    df1.to_excel(writer, sheet_name='点位时长和频度')

# 以下为轨迹画图
y1=df['block'].values
xx=df['时间'].values


y1=[int(i[4:]) for i in y1]
xx=[i[-8:-3] for i in xx]

fig = plt.figure()
plt.plot(list(range(len(xx))), y1, color='blue')

xl=[i for i in xx[::step]]
x=list(range(len(xx)))[::step]

plt.title("印未来超保-徐朝之 3幢2单元轨迹 2022-12-6", fontproperties=my_font)
plt.xticks(x, xl, rotation=45)
plt.yticks(yt)
plt.ylabel('楼层', fontproperties=my_font)
plt.grid(alpha=0.5)

plt.show()
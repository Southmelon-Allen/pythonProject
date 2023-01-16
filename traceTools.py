import numpy as np
from datetime import datetime
import pandas as pd


workers =  {'唐和玉': 'b1efa913d201871018b978db00f6303e',
            '洪金英': '65a7410a8244a0b91e390af0f30cadae',
            '徐朝之': '24e2893a693e01a5fe31ed0afef2dfd7',
            '熊江秀': '942c34f986dab2bfec9e900bb756cd5e',
            '关小艳': '92cefd3b2f1cc0a13d8f3ee771fc7e6e',
            '沈建根': '3b6af61f753161c8e34bb22015b0bde5'
            }

areas =  {'唐和玉': ['1-1', '1-2'],
            '洪金英': ['2-1', '2-2', '5-2'],
            '徐朝之': ['3-1', '3-2'],
            '熊江秀': ['4-1', '4-2'],
            '关小艳': ['6-1', '7-1', '5-1'],
            '沈建根': ['8-1', '8-2']
            }

floorSet = {'1-1': [-2, 23, 0],
            '1-2': [-2, 23, 0],
            '2-1': [-2, 23, 0],
            '2-2': [-2, 23, 0],
            '3-1': [-2, 23, 0],
            '3-2': [-2, 23, 0],
            '4-1': [-2, 23, 0],
            '4-2': [-2, 23, 0],
            '5-1': [-2, 23, 0],
            '5-2': [-2, 23, 0],
            '6-1': [-2, 23, 0, -1],
            '7-1': [-2, 23, 0, -1],
            '8-1': [-2, 23, 0],
            '8-2': [-2, 23, 0]}

# 检查一段数据中，数据点是否有遗漏
# 参数：ts-每条数据的timestamp（datetime格式）列表。t0-中午下班时间，t1-下午上班时间。
def checkDataNum(ts):
    ts_start=ts[0]
    ts_end=ts[-1]
    ts_delta=ts_end-ts_start
    num0=int(ts_delta.seconds/30)
    num1=len(ts)
    print('起始时间：', ts[0])
    print('结束时间：', ts[-1])
    print('整体时长：', int(ts_delta.seconds/60), '分钟')
    print('应有数据点个数：', num0)
    print('实有数据点个数：', num1)
    print('数据完整率：', num1/num0)
    return

# 检查一段数据中，在哪些时间跨度上存在漏点
# 参数：ts-每条数据的timestamp（datetime格式）列表。ms-时间跨度，默认5分钟

def checkDataGap(ts, ms=5):
    gaps=0
    d=pd.to_timedelta(0)
    for i in range(len(ts)-1):
        delta=ts[i+1]-ts[i]
        if delta.seconds>=ms*60:
            print('起始：', ts[i], '结束：', ts[i+1])
            gaps+=1
            d+=delta
    print('总共漏点的时间段数量为：', gaps)
    print('总共漏算时长为：',int(d.seconds/60),'分钟')
    return

# 识别跨楼栋，单元漂移。
# 识别逻辑：前后两个数据点，如果楼层是连续的（前后两个数据点，数据的时间戳相差小于45秒，楼层数字都大于1，相差不超过1层），楼栋单元不一致，算做一次漂移。
# 参数：df-轨迹的原始数据

def checkBlockJump(df):
    dff=pd.DataFrame(columns=['Start_time', 'End_time', 'From', 'To'])
    cnt=0
    for i in range(len(df.index)-1):
        t_from=df.loc[i, 'time']
        t_to=df.loc[i+1, 'time']
        bd_from=df.loc[i, 'building']
        bd_to=df.loc[i+1, 'building']
        ut_from=df.loc[i, 'unit']
        ut_to=df.loc[i+1, 'unit']
        fl_from=df.loc[i, 'floor']
        fl_to=df.loc[i+1, 'floor']
        bk_from=df.loc[i, 'block']
        bk_to=df.loc[i+1, 'block']
        # print(t_from, t_to, bd_from, bd_to, ut_from,ut_to, fl_from, fl_to)
        if (t_to-t_from).seconds<45 \
                and abs(fl_from-fl_to)<2 \
                and ((bd_from!=bd_to) or (ut_from!=ut_to)) \
                and fl_from>1 \
                and fl_to>1 :
            dff.loc[cnt]=[t_from, t_to, bk_from, bk_to]
            cnt+=1
    return dff

# 导入数据规范化，
# 1. 将时间戳转化为timestamp格式。
# 2. 将楼栋、单元、楼层数据数字化。
# 3. 计算出'天台'对应的楼层数字（比数字最高层高一层）
# 4. 过滤掉非上班时间的数据点。t0,t1,t2,t3分别为上午上下班时间和下午上下班时间。
# 5. 过滤掉'block'字段第一个字符不是数字的。

def dataNormalize(df, t0, t1, t2, t3):
    df=df.loc[(df['createTime']>=t0) & (df['createTime']<=t3)]
    df=df.loc[(df['createTime']<=t1) | (df['createTime']>=t2)]
    dff=pd.DataFrame(columns=['time','building', 'unit', 'floor', 'block'])
    for i in df.index:
        t=pd.to_datetime(df.loc[i, 'createTime'])
        # if t<t0 or t1<t<t2 or t>t3: continue # 如果不在工作时间段内，该数据点不计入。
        if not df.loc[i, 'block'][0].isnumeric(): continue #不是楼栋区域的过滤掉。
        dff.loc[i, 'time']=t
        dff.loc[i, 'building']=df.loc[i, 'building'][:-1]
        dff.loc[i, 'unit'] = df.loc[i, 'unit'][:-2]
        dff.loc[i, 'block']=df.loc[i, 'block']
        block=df.loc[i, 'block']
        block1=block[block.find('-')+1:] #分两段截取字符串，求得楼层数字
        floor=int(block1[block1.find('-')+1:])
        dff.loc[i, 'floor'] = floor
    dff.index=range(len(dff))
    time_total=int(((t1-t0)+(t3-t2)).seconds/60)
    cnt1=list(df['block'].values).count('Out Of Range')
    cnt2=list(df['unit'].values).count('Unknown')
    print(f'数据转换完毕，上班时间共{time_total}分钟, 应有{int(time_total*2)}个数据点')
    print(f'楼栋可定位区域内数据点个数为：{len(dff)}，对应时间{len(dff)//120}小时{(len(dff)%120)//2}分钟')
    print(f'无信号-Out of range的数据点个数为：{cnt1}')
    print(f'车库-Unknown的数据点个数为：{cnt2}')

    return dff

# 计算工作区域的block集合
# 入参：name-保洁人员的姓名
def workArea(name):
    area=set()
    for a in areas[name]:
        b=floorSet[a]
        blist=list(range(b[0], b[1]+1))
        for r in b[2:]: blist.remove(r)
        for fs in blist:
            area.add(a+'-'+str(fs))
    return area

# 计算工作的覆盖度
# 覆盖度=工作时间内到过的工作点位数/总的工作点位数
# 入参：df-轨迹原始数据， name-保洁人员姓名
# 将原始数据的block数据和areas取交集即可计算

def workCover(df, name):
    area=workArea(name)
    to_area=set(df['block'].values) & area
    cover=len(to_area)/len(area)
    print(f'保洁人员{name}当天的作业区域覆盖率为：{cover}')
    # print(df['block'].values)
    # print(to_area)
    return cover

# def dataNormalize_back(df, t0, t1, t2, t3):
#     dff=pd.DataFrame(columns=['time','building', 'unit', 'floor', 'block'])
#     for i in df.index:
#         t=pd.to_datetime(df.loc[i, 'createTime'])
#         if t<t0 or t1<t<t2 or t>t3: continue # 如果不在工作时间段内，该数据点不计入。
#         if not df.loc[i, 'block'][0].isnumeric(): continue #不是楼栋区域的过滤掉。
#         dff.loc[i, 'time']=t
#         dff.loc[i, 'building']=df.loc[i, 'building'][:-1]
#         dff.loc[i, 'unit'] = df.loc[i, 'unit'][:-2]
#         dff.loc[i, 'block']=df.loc[i, 'block']
#         floor=df.loc[i, 'floor'][:-1]
#         if floor!='天':
#             dff.loc[i, 'floor'] = int(floor)
#         else:
#             dff.loc[i, 'floor'] = -18
#     #print(dff)
#     #计算天台的楼层
#     top=dff['floor'].values.max()+1
#     #将所有的天台赋值为top
#     for i in dff.index:
#         if dff.loc[i, 'floor']==-18:
#             dff.loc[i, 'floor']=top
#     dff.index=range(len(dff))
#     return dff

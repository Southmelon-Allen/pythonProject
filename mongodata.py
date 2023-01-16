import pymongo as pm
from datetime import datetime
from dateutil import parser
import pandas as pd
import numpy as np
import os

# 初始化要查询的人员姓名和工牌(印未来/雅居乐)

workers =  {'唐和玉': 'c50f63c74bd2fa739357b8b48e07df66',
            '洪金英': '2c9befe53b9740175edf325533fc3714',
            '徐朝之': '24e2893a693e01a5fe31ed0afef2dfd7',
            '熊江秀': '942c34f986dab2bfec9e900bb756cd5e',
            '关小艳': '85978481fc6a2048507fca49e2c93423',
            '沈建根': 'f66478f37f174132c789db7c707d5fa8',
            '王凤英': 'f4437de4f0582eae8c26b86084001d6a',
            '何碧珍': '864b3d588ac2a8c9428d776ebafdc3dc',
            '何克秀': '9e125b747def3d10c743055514ef9395',
            '吴冬香': 'b9c611e2b5b36c2d3497cac3050b8ec2',
            '方丹体': '4078aa3d6569b8e6d37cec29aac692e2',
            '胡显兰': 'd9ade3f972463eee96e600deaacdd9bb'
            }

# 初始化数据库连接
time_key='createTime'
client = pm.MongoClient(host='dds-bp13277a14a229e41951-pub.mongodb.rds.aliyuncs.com',
                        port=3717,
                        username='lbs_app',
                        password='RmfHPDpbw0KY8UVk')
db=client.lbs
collection=db.combined_location

# 输入要查询数据的日期
dateinput=input('请输入要查询数据的日期（YYYY-MM-DD）：')
output_file='~/Documents/'+dateinput+'_'+str(np.random.randint(10000))+'.xlsx'

# 设置要过滤的列名
drop_cols=['_class', 'blockId', '_id', 'fpCreditLevel',
           'deviceTimestamp', 'updateTime']


start_time=parser.parse(dateinput+' 00:00:00')-pd.to_timedelta('8:0:0')
end_time=parser.parse(dateinput+' 23:59:59')-pd.to_timedelta('8:0:0')

result=collection.find_one({'iotId':workers['关小艳']})


dfs={}
for k in workers.keys():
    print(f'开始导出{k}的数据')
    df = pd.DataFrame(columns=result.keys())
    results=collection.find({'iotId':workers[k],
                             time_key: {'$gte': start_time, '$lte': end_time}})
    cnt=0
    for i in results:
        i[time_key]=pd.to_datetime(i[time_key])+pd.to_timedelta('8:0:0')
        df.loc[cnt]=i
        cnt+=1

    df = df.drop(columns=drop_cols)
    # df = df[(df[time_key] > start_time) & (df[time_key] < end_time)]
    df=df.reindex(range(len(df)))

    dfs[k]=df
print('数据读取完毕')


with pd.ExcelWriter(output_file) as writer:  # doctest: +SKIP
    for k in dfs.keys():
        dfs[k].to_excel(writer, sheet_name=k)

# results=collection.find({'iotId':'92cefd3b2f1cc0a13d8f3ee771fc7e6e'})
# for i in results:
#     i['uploadTime']=pd.to_datetime(i['uploadTime'])
#     df.loc[cnt]=i
#     #print(i)
#     cnt+=1
#
# df=df[(df['uploadTime']>start_time)&(df['uploadTime']<end_time)]
# df.to_excel('~/Documents/0868120295486903.xlsx')



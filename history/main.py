# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

#import matplotlib.pyplot as plt

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import serial
import pyserial

pyserial.


np.random.seed(0)
sns.set()
#uniform_data = np.random.rand(3, 3)
#print(uniform_data)
#heatmap = sns.heatmap(uniform_data)
#flights = pd.read_excel("flights.xlsx")
#print(flights)
#print(sns.get_dataset_names())
#df=sns.load_dataset('brain_networks')
#print(df)

'''
sets=sns.get_dataset_names()
for s in sets:
    print("读取数据集", s)
    df=sns.load_dataset(s)
    filename="/Users/allenli/"+s+".xlsx"
    df.to_excel(filename)
    print("正在保存", filename)
'''
'''
df=pd.read_excel("~/datasets/tips.xlsx")
sns.catplot(kind="box", data=df)
plt.show()
plt.savefig("1.png")
'''

#data = pd.read_excel("~/datasets/dongyuan.xlsx")
#print(data.head())

a=[1048, 448, 330, 209, 900, 358, 106, 641, 30, 277]
b=np.array(a)
aa=np.array([91,420,868,616,1455,838,629,166,811,30,242,149])
m=aa.mean()
s=aa.std()
print(m, s, m-3*s, m+3*s)



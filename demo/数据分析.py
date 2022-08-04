import pandas as pd
import re

df = pd.read_csv('data.csv')

data1 = df['正面（一级标签+二级标签）']
data2 = df['负面（一级标签+二级标签）']


list1 = []
for d in data1:
    if 'nan' not in str(d):
        name = re.compile('【(.*?)】')
        type1 = name.findall(d)
        for t in type1:
            # t = t.replace('玩法内容', '内容玩法').replace('平台版本', '版本问题').replace('平台/版本', '版本问题').replace('遗留问题', '常规bug').replace('版本问题', '常规bug')
            # t = t.replace('系统机制', '操作体验').replace('建议/期望', '建议/期待').replace('操作体验', '性能表现/网络表现')
            list1.append(t)
    else:
        pass

list2 = []
for d in data2:
    if 'nan' not in str(d):
        name = re.compile('【(.*?)】')
        type1 = name.findall(d)
        for t in type1:
            t = t.replace('玩法内容','内容玩法').replace('平台版本','版本问题').replace('平台/版本','版本问题')
            t = t.replace('遗留问题', '常规bug').replace('版本问题', '常规bug').replace('品质对比', '常规bug')
            t = t.replace('美术呈现', '其他').replace('运营表现', '其他').replace('建议/期望', '其他')
            list2.append(t)
    else:
        pass

sum3 = int(len(list1)) + int(len(list2))
print('正面占比:',(len(list1) / sum3))
print('负面占比:',(len(list2) / sum3))
d1 = {}
for l in list1:
    d1[l] = d1.get(l,0)+1

key1 = []
values1 = []
for key,values in d1.items():
    key1.append(key)
    values1.append(values)

sum1 = sum(values1)
dd1 = {}
for k,v in zip(key1,values1):
    bfb = '%0.2lf' %(v/sum1)
    bfb1 = str(float(bfb) * 100) + "%"
    dd1[k] = bfb1

d2 = {}
for l in list2:
    d2[l] = d2.get(l,0)+1

key2 = []
values2 = []
for key,values in d2.items():
    key2.append(key)
    values2.append(values)

sum2 = sum(values2)
dd2 = {}
for k,v in zip(key2,values2):
    bfb = '%0.2lf' %(v/sum2)
    bfb1 = str(float(bfb) * 100) + "%"
    dd2[k] = bfb1

df2 = pd.DataFrame(dd1,index=[0]).T
df2.to_csv('正面标签.csv',encoding='utf-8-sig')

df3 = pd.DataFrame(dd2,index=[0]).T
df3.to_csv('负面标签.csv',encoding='utf-8-sig')
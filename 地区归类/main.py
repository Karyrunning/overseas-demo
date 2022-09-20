import pandas as pd

df = pd.read_excel('地区.xlsx')
list_1 = []
list_2 = []
for j,k in zip(df['国家'],df['地区']):
    l = str(j).split('、')
    for i in l:
        list_1.append(i)
        list_2.append(k)

df2 = pd.DataFrame()
df2['国家'] = list_1
df2['地区'] = list_2
df2.to_csv('3.csv',encoding='utf-8-sig')
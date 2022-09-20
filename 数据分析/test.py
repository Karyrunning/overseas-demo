with open('class-fenci.txt','r',encoding='utf-8') as f:
    content = f.readlines()

import pandas as pd

d = {}
for c in content:
    c = c.split(' ')
    for i in c:
        d[i] = d.get(i,0)+1

list1 = list(d.items())
x_data = []
y_data = []
df = pd.DataFrame(list1)
df.to_csv('高频词.csv',encoding='utf-8-sig')

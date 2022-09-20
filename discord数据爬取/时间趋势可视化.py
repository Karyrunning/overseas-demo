import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('./output/阿拉伯11-22.csv', encoding="utf-8-sig")
df['数量'] = 1
name = '阿拉伯'

def time_split(x):
    x = str(x).split(':')
    return x[0]

df['时间'] = df['发文原始时间'].apply(time_split)
new_df = df['时间'].value_counts()
new_df.sort_index(inplace=True)
x_data = list(new_df.index)
y_data = list(new_df.values)
new_df.to_csv('./output/{}-时间表格.csv'.format(name), encoding="utf-8-sig")
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(20, 12), dpi=300)
plt.plot(x_data, y_data, color='#b82410')
plt.title("{}-时间热度趋势".format(name))
plt.xlabel("时间")
plt.ylabel("发帖数量")
plt.xticks(rotation=90)
plt.savefig('./output/{}-发帖热度时间趋势图.png'.format(name))
plt.show()
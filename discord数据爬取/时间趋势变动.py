import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(suppress=True)
# pd.set_option("display.float_format", lambda x: "%.2f" % x)
df1 = pd.read_csv('input/原始数据1.csv', encoding="utf-8-sig", parse_dates=True, index_col='发文时间')
df2 = pd.read_csv('input/原始数据2.csv', encoding="utf-8-sig", parse_dates=True, index_col='发文时间')
df3 = pd.concat([df1,df2],axis=0)

df = df3.tz_convert('Asia/Shanghai')
df = df['2022-07-21 10':'2022-08-01 12']
df = df.drop_duplicates(keep='first')
x_data = [str(n).split(".")[0] for n in df.index]
x_data1 = [str(n).split(" ")[0] for n in x_data]
x_data2 = [str(n).split(" ")[1] for n in x_data]
list_id = []
for i in df['发布者id']:
    l = str(i) + "\t"
    list_id.append(l)
new_df = pd.DataFrame()
new_df['发文原始时间'] = x_data
new_df['发文日期'] = x_data1
new_df['发文时间 HH:MM:SS'] = x_data2
# new_df['发布者id'] = list_id
new_df['发布者名字'] = list(df['发布者名字'])
new_df['内容信息'] = list(df['内容信息'])
new_df['机翻内容'] = ' '
new_df['被提及人'] = list(df['被提及人'])
new_df['频道'] = list(df['频道'])
new_df.to_csv('./output/清洗过后的数据.csv',encoding='utf-8-sig',index=False)



# df['数量'] = 1
# new_df = df['数量'].resample('H').sum()
#
# x_data = [str(n).split("+")[0] for n in new_df.index]
# y_data = list(new_df.values)
#
# df1 = pd.DataFrame()
# df1['时间'] = x_data
# df1['数量'] = y_data
# df1.to_csv('./output/时间趋势数据.csv',encoding="utf-8-sig")
#
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.figure(figsize=(16, 12), dpi=300)
# plt.plot(x_data, y_data, color='#b82410')
# plt.title("时间热度趋势")
# plt.xlabel("时间")
# plt.ylabel("发帖数量")
# plt.xticks(rotation=45)
# plt.savefig('./output/发帖热度时间趋势图.png')
# plt.show()
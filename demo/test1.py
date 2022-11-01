import pandas as pd
from matplotlib import pyplot as plt
df1 = pd.read_csv('咩咩启示录 - Oct 12, 2022 - 3 20 36 PM.csv',encoding="UTF-16",sep='\t',parse_dates=['Date'], index_col ="Date")
df2 = pd.read_csv('咩咩启示录 - Oct 12, 2022 - 3 20 36 PM.csv',encoding="UTF-16",sep='\t')
df1['数量'] = 1


list1 = []
for i in list(df1.index):
    i = str(i)
    p = pd.Period(i,freq='W')
    p1 = str(p).split('/')
    p2 = p1[1]
    list1.append(p2)


# df2['时间周期'] = list1
#
# df2 = df2.drop_duplicates(subset=['时间周期'], keep='first')
# print(df2)
# df2.to_csv('data.csv',encoding='utf-8-sig')
# df2.index = pd.to_datetime(list1)
# new_df1 = df2['2022-08-11':]
# new_df1.to_csv('阶段三.csv',encoding='utf-8-sig')
new_df = df1['Reach'].resample('2W').mean()
# new_df1 = new_df['2022-08-14':'2022-10-02']
print(new_df)
new_df.to_csv('data.csv',encoding='utf-8-sig')

# plt.figure(figsize=(12,9),dpi=300)
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.plot(new_df, color='#3498DB', label='发布推文')
# plt.legend()
# plt.title('近段时间内-发布推文')
# plt.xlabel('时间')
# plt.ylabel('发布推文')
# plt.grid()
# plt.savefig('发布推文.png')
# plt.show()
import pandas as pd

df = pd.read_excel('YTB&Twitch标签讨论1.xlsx')
df['时间'] = pd.to_datetime(df['发布日期'],format='%Y年%m月%d日')
df.index = df['时间']
df = df['2021-12-12':'2022-07-01']


def main1(x):
    x = str(x)
    if 'K' in x:
        x1 = x.replace('K','')
        x1 = int(float(x1) * 1000)
        return int(x1)
    elif 'M' in x:
        x1 = x.replace('M', '')
        x1 = int(float(x1) * 1000000)
        return int(x1)
    else:
        return float(x)


def main2(x):
    x = str(x).split('-')
    x1 = str(x[0]) + '-' + str(x[1])
    return x1

df['点赞次数'] = df['点赞次数'].apply(main1)
df['粉丝数量'] = df['粉丝数量'].apply(main1)
df['时间1'] = df['时间'].apply(main2)
df.to_csv('data.csv',encoding='utf-8-sig',index=False)
# new_df = df.groupby('时间1').agg("sum")
# new_df.to_csv('1.csv',encoding='utf-8-sig')
# import datetime
# from dateutil.relativedelta import relativedelta
# df = pd.read_excel('原始数据表.xlsx')
# df['时间'] = pd.to_datetime(df['YYDD（UTC-5）'])
#
# df['时间']=df['时间'].dt.week
# list1 = []
# for i in df['时间']:
#     date = datetime.date(2022, 1, 1) + relativedelta(weeks=+i)
#     print(date)
#     date = str(date)
#     if '2022-12' in date:
#         date = date.replace('2022-12','2021-12')
#         list1.append(date)
#     else:
#         list1.append(date)

# df['时间1'] = list1
# df.to_csv('1.csv',encoding='utf-8-sig')
# print(df['时间'])
# df.index = df['时间']
# df['时间1'] = df['时间']
# df['时间1'] = df['时间1'].resample('W')
# print(df['时间1'])
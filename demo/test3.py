import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_excel('YTB&Twitch标签讨论1.xlsx')


def main1(x):
    x1 = str(x)
    if 'K' in x1:
        x1 = x1.replace('K','')
        x1 = int(float(x1) * 1000)
        return x1
    elif 'M' in x1:
        x1 = x1.replace('M', '')
        x1 = int(float(x1) * 1000000)
        return x1
    else:
        return int(x1)

df['点赞次数'] = df['点赞次数'].apply(main1)
df['粉丝数量'] = df['粉丝数量'].apply(main1)


data = df[['观看次数','点赞次数','评论总数']]
ss = StandardScaler()
data_x = ss.fit_transform(data)

list1 = []
for i in data_x:
    sum1 = i[0] + i[1] + i[2]
    list1.append(sum1)
df['权重计算'] = list1
df.to_csv('YTB&Twitch标签讨论.csv',encoding='utf-8-sig',index=False)


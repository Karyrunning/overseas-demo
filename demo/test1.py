import pandas as pd

df1 = pd.read_excel('tarkov Tweets.xlsx')
df2 = pd.read_excel('塔科夫官推-内容简单标签v1.xlsx')


def t_id(x):
    x = str(x)
    x1 = x.replace("'","")
    return int(x1)


df2['Tweet Id'] = df2['Tweet Id'].apply(t_id)

d1 = {}
d2 = {}
d3 = {}

for j,k,l,h in zip(df1['Tweet Id'],df1['Replies'],df1['Retweets'],df1['Likes']):
    d1[j] = k
    d2[j] = l
    d3[j] = h

list1 = []
list2 = []
list3 = []
for i in df2['Tweet Id']:
    try:
        number1 = d1[i]
        list1.append(number1)
    except:
        list1.append(' ')

    try:
        number2 = d2[i]
        list2.append(number2)
    except:
        list2.append(' ')

    try:
        number3 = d3[i]
        list3.append(number3)
    except:
        list3.append(' ')

df2['Replies'] = list1
df2['Retweets'] = list2
df2['Likes'] = list3
df2.pop('Replies')  # 删除备注列
df2.pop('Retweets')  # 删除备注列
df2.pop('Likes')  # 删除备注列
df2.insert(22, 'Replies', list1)  # 插入备注列
df2.insert(23, 'Retweets', list2)  # 插入备注列
df2.insert(24, 'Likes', list3)  # 插入备注列
df2.to_csv('塔科夫.csv',encoding='utf-8-sig',index=False)

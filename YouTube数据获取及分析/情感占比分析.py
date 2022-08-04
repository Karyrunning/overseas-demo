import pandas as pd

df = pd.read_csv('./output/emotion_BP-评论数据.csv')




def comp_score_total(x):
    df1 = x
    comp = df1['comp_score'].value_counts()

    x_data = list(comp.index)
    y_data = list(comp.values)
    d = {}
    for x,y in zip(x_data,y_data):
        d[x] = y

    feifu = (d['pos'] + d['neu']) / sum(y_data) * 100
    feifu = '{:.2f}'.format(feifu) + "%"

    return d,feifu

new_df = df.groupby('视频链接').apply(comp_score_total)

neu = []
neg = []
pos = []
list2 = []

for n in new_df.values:
    neu.append(n[0]['neu'])
    neg.append(n[0]['neg'])
    pos.append(n[0]['pos'])
    list2.append(n[1])

df2 = pd.DataFrame()
df2['视频链接'] = list(new_df.index)
df2['正向'] = pos
df2['中立'] = neu
df2['负向'] = neg
df2['非负占比'] = list2
df2.to_csv('./output/bp情感分析.csv',encoding='utf-8-sig')

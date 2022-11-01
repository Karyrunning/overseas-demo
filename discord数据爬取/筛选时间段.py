import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from googletrans import Translator
from tqdm import tqdm
import time
import random
translator = Translator()
a = random.uniform(0.1,0.5)

df1 = pd.read_csv('input/菲律宾新数据.csv', encoding="utf-8-sig", parse_dates=True, index_col='发文时间')
# df2 = pd.read_csv('input/巴西11-13新数据.csv', encoding="utf-8-sig", parse_dates=True, index_col='发文时间')
# df3 = pd.read_csv('input/巴西14-22旧数据.csv', encoding="utf-8-sig", parse_dates=True, index_col='发文时间')
# df4 = pd.read_csv('input/巴西14-22新数据.csv', encoding="utf-8-sig", parse_dates=True, index_col='发文时间')
data = pd.concat([df1],axis=0)

df = data.tz_convert('Asia/Shanghai')
df = df['2022-10-27 12':'2022-10-28 12']
df = df.drop_duplicates(keep='first')
df = df.sort_values(by=['发文时间'],ascending=True)

# list_trans = []
# for d in tqdm(df['内容信息']):
#     try:
#         translations = translator.translate(d, dest='en')
#         list_trans.append(translations.text)
#         time.sleep(a)
#     except:
#         list_trans.append('')
#         continue

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
new_df['机翻内容'] = ''
new_df['被提及人'] = list(df['被提及人'])
new_df['频道'] = list(df['频道'])
new_df.to_csv('./output/菲律宾.csv',encoding='utf-8-sig',index=False)

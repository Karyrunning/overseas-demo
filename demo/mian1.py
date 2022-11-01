import requests
import re
import pandas as pd


df = pd.read_excel('Assignment 2 - Freshdirect data.xlsx')

new_df = df[df['GEOGRAPHY'] == 'Queens']


def mian1(x):
    x1 = str(x).split(' ')
    x1 = x1[0]
    x2 = str(x1).split('-')
    x2 = x2[0]
    return x2


def mian2(x):
    x1 = str(x).split(' ')
    x1 = x1[0]
    x2 = str(x1).split('-')
    x2 = x2[1]
    return x2


new_df['number'] = 1
new_df['ACQUIRED_year'] = new_df['ACQUIRED_DATE'].apply(mian1)
new_df['ACQUIRED_meath'] = new_df['ACQUIRED_DATE'].apply(mian2)

data = pd.DataFrame()
data['订单数'] = new_df['number']
data['年'] = new_df['ACQUIRED_year']
data['月'] = new_df['ACQUIRED_meath']
data['日'] = new_df['ACQUIRED_DATE']
data = data.reset_index(drop=True)


new_df1 = data.groupby(['年', '月']).agg('sum')
new_df2 = data.groupby(['年', '日']).agg('sum')
new_df1.to_csv('data1.csv',encoding='utf-8-sig')
new_df2.to_csv('data2.csv',encoding='utf-8-sig')
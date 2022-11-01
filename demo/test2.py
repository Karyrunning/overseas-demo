from lxml import etree
import pandas as pd

df = pd.read_csv('explore-csv.csv',sep=',')

def main1(x):
    x1 = int(x)
    if x1 <= 10000:
        return 1
    elif 10000 < x1 <= 100000:
        return 2
    else:
        return 3

df['type'] = df['Reach'].apply(main1)
df.to_csv('data.csv',encoding='utf-8-sig')

import requests
import re
# from lxml import etree
# import pandas as pd
# with open('逃离塔科夫 - 主题 - YouTube.html','r',encoding='utf-8-sig')as f:
#     content = f.read()
#
# soup = etree.HTML(content)
# href = soup.xpath('//div[@id="meta"]/h3[@class="style-scope ytd-grid-video-renderer"]/a/@href')
# df = pd.DataFrame()
# df['url'] = href
# df.to_csv('链接.csv')
import pandas as pd

df = pd.read_excel('原始数据表.xlsx')
df['周时间'] = df['周时间'].astype('str')

def main1(x):
    x = str(x)
    x1 = " " + x + " "
    return x1
df['周时间'] = df['周时间'].apply(main1)
df.to_csv('demo.csv',encoding='utf-8-sig')
# def main1(x):
#     df1 = x
#     new_df1 = df1['一级标签'].value_counts()
#     return new_df1
#
#
# new_df = df.groupby('周时间').apply(main1)
#
# new_df.to_csv('demo.csv',encoding='utf-8-sig')

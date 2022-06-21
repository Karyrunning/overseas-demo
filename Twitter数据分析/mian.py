import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
df = pd.read_excel('PUBGMOBILE Tweets.xlsx',sheet_name='有回复的Tweets和官方的回帖')

data = df[['Replies','Retweets','Likes']]
ss = StandardScaler()
data_x = ss.fit_transform(data)

def zanbi(x,y,l):
    try:
        z = x + y + l
        return float(z)
    except:
        return np.nan

list_zb = []

for j,k,o in data_x:
    z = zanbi(j,k,o)
    list_zb.append(z)

df['zanbi'] = list_zb

new_df = df.sort_values(by=['zanbi'],ascending=False)
new_df.to_csv('1.csv')
id = new_df['Tweet Id'][:10]
str1 = ''
for i in id:
    str1 += 'twitterThread: {} or '.format(i)

str2 = "(" + str1 + ")" + " not (POSTTYPE: rp or qt)"
str2 = str2.replace('or )',')')
with open('1.txt','w',encoding='utf-8-sig')as f:
    f.write(str2)
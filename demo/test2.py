import pandas as pd

df = pd.read_csv('data.csv')

def main1(x):
    x = int(x)
    if x <= 100000:
        return '1'
    elif 100000 < x <= 500000:
        return '2'
    elif 500000 < x <= 1000000:
        return '3'
    else:
        return '4'

def main2(x):
    df1 = x
    new_df1 = df1['内容二级标签'].value_counts()
    return new_df1

df['粉丝数量'] = df['粉丝数量'].apply(main1)
new_df = df.groupby('内容一级标签').apply(main2)
new_df.to_csv('1.csv',encoding='utf-8-sig')


# new_df = df['粉丝数量'].value_counts()
# new_df.to_csv('1.csv',encoding='utf-8-sig')
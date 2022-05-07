import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


def hbzz(x):
    x = float(x)
    x = x * 100
    x = '%0.3lf' %x + "%"
    return x

df = pd.read_csv('./input/Youtube.csv', encoding="UTF-16",sep='\t',parse_dates=['Date'], index_col ="Date")
new_df = df['youtube_view'].resample('D').sum()
new_df1 = df['youtube_view']["2022-04-07"].resample('1H').sum()
df = pd.read_csv('./output/new_youtube.csv')
new_df2 = df.dropna(how='any',axis=0)
new_df2['commment_number'] = 1
new_df2['comment_date'] = pd.to_datetime(new_df2['comment_date'])
new_df2.index = new_df2['comment_date']
new_df3 = new_df2['commment_number'].resample('D').sum()



#总体播放量增长趋势
def line1():
    x_data = list(new_df.index)
    y_data = list(new_df.values)
    print(np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(x_data))
    print(y_data)
    plt.figure(figsize=(12,9),dpi=300)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(x_data, y_data, color='#3498DB', label='总体播放量')
    plt.legend()
    plt.title('近段时间内-总体播放量')
    plt.xlabel('时间')
    plt.ylabel('播放量')
    plt.grid()
    plt.savefig('./output/总体播放量.png')
    plt.show()

    data1 = pd.DataFrame()
    data1['date'] = x_data
    data1['youtube_view'] = y_data
    data1['huanbi'] = data1['youtube_view'].pct_change()
    data1.fillna(0, inplace=True)
    data1['huanbi'] = data1['huanbi'].apply(hbzz)
    data1.to_csv('./output/原始数据/总时间播放量.csv')


#当天播放量增长趋势
def line2():
    x_data = list(new_df1.index)
    y_data = list(new_df1.values)

    print(np.vectorize(lambda s: s.strftime('%Y-%m-%d %H:%M:%S'))(x_data))
    print(y_data)
    plt.figure(figsize=(12,9),dpi=300)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(x_data, y_data, color='#3498DB', label='当天播放量')
    plt.legend()
    plt.title('当天播放量总体趋势')
    plt.xlabel('时间')
    plt.ylabel('播放量')
    plt.grid()
    plt.savefig('./output/当天播放.png')
    plt.show()

    data1 = pd.DataFrame()
    data1['date'] = x_data
    data1['youtube_view'] = y_data
    data1['huanbi'] = data1['youtube_view'].pct_change()
    data1.fillna(0, inplace=True)
    # data1['huanbi'] = data1['huanbi'].apply(hbzz)
    data1.to_csv('./output/原始数据/当天播放量.csv')

#总体评论趋势增长
def line3():
    x_data = list(new_df3.index)
    y_data = list(new_df3.values)
    print(np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(x_data))
    print(y_data)
    plt.figure(figsize=(12, 9), dpi=300)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(x_data, y_data, color='#3498DB', label='总体评论量')
    plt.legend()
    plt.title('近段时间内-总体评论量')
    plt.xlabel('时间')
    plt.ylabel('评论量')
    plt.grid()
    plt.savefig('./output/总体评论量.png')
    plt.show()

    data1 = pd.DataFrame()
    data1['date'] = x_data
    data1['youtube_view'] = y_data
    data1['huanbi'] = data1['youtube_view'].pct_change()
    data1.fillna(0, inplace=True)
    data1['huanbi'] = data1['huanbi'].apply(hbzz)
    data1.to_csv('./output/原始数据/总时间评论量.csv')

if __name__ == '__main__':
    line1()
    line2()
    line3()
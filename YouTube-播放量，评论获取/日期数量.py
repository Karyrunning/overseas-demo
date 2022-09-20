import pandas as pd


def data_screen():
    df = pd.read_csv('./input/{}'.format(input_filename), encoding="UTF-16",sep='\t')
    # csv内容筛选，选出全是YouTube的内容行
    # df1 = df[df['Source'] == 'Youtube']
    # df1 = df1[df1['Engagement'] >= 1000]
    new_df = df.drop_duplicates(subset=['URL'], keep='first')

    data = data_screen1(data_screen1(new_df))
    new_df = data['Alternate Date Format'].value_counts()
    new_df.sort_index(ascending=True, inplace=True)
    new_df.to_csv('./output/YouTube日期.csv',encoding='utf-8-sig')
    print(new_df)

def data_screen3():
    df = pd.read_csv('./input/{}'.format(input_filename), encoding="UTF-16", sep='\t')
    new_df = df.drop_duplicates(subset=['URL'], keep='first')
    data = data_screen1(data_screen1(new_df))
    def main1(x):
        data1 = x
        data1 = data1['Sentiment'].value_counts()
        x_data = [d for d in data1.index]
        y_data = [d for d in data1.values]
        d = {}
        for j,k in zip(x_data,y_data):
            d[j] = k
        try:
            Positive = d['Positive']
        except:
            Positive = 0
        try:
            Neutral = d['Neutral']
        except:
            Neutral = 0
        ffl = (int(Positive)+int(Neutral)) / sum(y_data)
        return ffl
    new_df = data.groupby('Alternate Date Format').apply(main1)
    new_df.sort_index(ascending=True, inplace=True)
    new_df.to_csv('./output/YouTube日期.csv', encoding='utf-8-sig')
    print(new_df)


def data_screen1(data):
    df = data
    keyword1 = ''
    keyword2 = ''
    new_df = df[((df['Headline'].str.contains('{}'.format(keyword1), case=False)) | (df['Hit Sentence'].str.contains('{}'.format(keyword1), case=False))) & ((df['Headline'].str.contains('{}'.format(keyword2), case=False)) | (df['Hit Sentence'].str.contains('{}'.format(keyword2), case=False)))]
    return new_df

def data_screen2():
    df = pd.read_csv('./output/Youtube.csv')
    new_df = df.groupby('发布日期').agg('sum')
    print(new_df)

if __name__ == '__main__':
    input_filename = 'division_mobile - Aug 11, 2022 - 2 58 03 PM.csv'
    # 数据筛选
    data_screen()
    print('*' * 60)
    # data_screen2()
    # data_screen3()

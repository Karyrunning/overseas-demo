import pandas as pd


def data_screen():
    df = pd.read_csv('./input/{}'.format(input_filename), encoding="UTF-16",sep='\t')
    # csv内容筛选，选出全是YouTube的内容行
    df1 = df[df['Source'] == 'Youtube']
    # df1 = df1[df1['Engagement'] >= 1000]
    new_df = df1.drop_duplicates(subset=['URL'], keep='first')

    data = data_screen1(data_screen1(new_df))
    print(data)
    new_df = data['Alternate Date Format'].value_counts()
    new_df.sort_index(ascending=True, inplace=True)
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
    input_filename = 'Diablo_Immortal_Mobile - Jun 6, 2022 - 12 52 35 PM.csv'
    # 数据筛选
    data_screen()
    print('*' * 60)
    data_screen2()

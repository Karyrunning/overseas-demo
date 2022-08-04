import pandas as pd


def main1():
    df1 = pd.read_csv('./data2/Sensor_Tower_App_Intel_Reviews_1492005122__2022-05-30_to_2022-06-05.csv',encoding='utf-16',sep='\t')
    df2 = pd.read_csv('./data2/Sensor_Tower_App_Intel_Reviews_com.blizzard.diablo.immortal__2022-05-30_to_2022-06-05.csv',encoding='utf-16',sep='\t')

    df3 = pd.concat([df1,df2],axis=0)

    df1 = pd.read_excel('工具表单持续更新--地区、自研.xlsx', sheet_name='地区列表-20210514')
    d1 = {}
    for j, k in zip(df1['国家简称(ST)'], df1['中文']):
        d1[j] = k
    country_data = df3['Country'].value_counts()
    x_data = list(country_data.index)[:5]
    y_data = list(country_data.values)[:5]
    country = []
    for x in x_data:
        name = d1[x]
        country.append(name)
    print('前5个国家分别是:', country)
    print("前5个国家评论数:", y_data)

    def total(x):
        df = x
        rating_data = df['Rating'].value_counts()

        d = {}
        sum_count = 0
        for key, value in zip(rating_data.index, rating_data.values):
            d[key] = value
            sum_count += value

        return d[1],d[2],d[3],d[4],d[5]


    df4 = df3.groupby('Date').apply(total)
    date = list(df4.index)
    y_data = list(df4.values)
    one_number = []
    two_number = []
    three_number = []
    four_number = []
    five_number = []
    for y in y_data:
        one_number.append(y[0])
        two_number.append(y[1])
        three_number.append(y[2])
        four_number.append(y[3])
        five_number.append(y[4])

    df5 = pd.DataFrame()
    df5['Date'] = date
    df5['一星'] = one_number
    df5['二星'] = two_number
    df5['三星'] = three_number
    df5['四星'] = four_number
    df5['五星'] = five_number
    df5.to_csv('暗黑不朽.csv', encoding='utf-8-sig')


def main2():
    df1 = pd.read_csv('./data2/Sensor_Tower_App_Intel_Reviews_com.miHoYo.GenshinImpact__2020-09-28_to_2020-10-02.csv', encoding='utf-16',
                      sep='\t')
    df2 = pd.read_csv('./data2/Sensor_Tower_App_Intel_Reviews_1517783697__2020-09-28_to_2020-10-02.csv',
                      encoding='utf-16', sep='\t')

    df3 = pd.concat([df1, df2], axis=0)
    df1 = pd.read_excel('工具表单持续更新--地区、自研.xlsx', sheet_name='地区列表-20210514')
    d1 = {}
    for j, k in zip(df1['国家简称(ST)'], df1['中文']):
        d1[j] = k
    country_data = df3['Country'].value_counts()
    x_data = list(country_data.index)[:5]
    y_data = list(country_data.values)[:5]
    country = []
    for x in x_data:
        name = d1[x]
        country.append(name)
    print('前5个国家分别是:', country)
    print("前5个国家评论数:", y_data)

    def total(x):
        df = x
        rating_data = df['Rating'].value_counts()
        d = {}
        sum_count = 0
        for key, value in zip(rating_data.index, rating_data.values):
            d[key] = value
            sum_count += value
        return d[1], d[2], d[3], d[4], d[5]

    df4 = df3.groupby('Date').apply(total)
    date = list(df4.index)
    y_data = list(df4.values)
    one_number = []
    two_number = []
    three_number = []
    four_number = []
    five_number = []
    for y in y_data:
        one_number.append(y[0])
        two_number.append(y[1])
        three_number.append(y[2])
        four_number.append(y[3])
        five_number.append(y[4])

    df5 = pd.DataFrame()
    df5['Date'] = date
    df5['一星'] = one_number
    df5['二星'] = two_number
    df5['三星'] = three_number
    df5['四星'] = four_number
    df5['五星'] = five_number
    df5.to_csv('原神.csv', encoding='utf-8-sig')


if __name__ == '__main__':
    main1()
    main2()
import pandas as pd


def main_ios(name):
    df = pd.read_csv('{}'.format(name),encoding='utf-16',sep='\t')
    df1 = pd.read_excel('工具表单持续更新--地区、自研.xlsx', sheet_name='地区列表-20210514')
    d1 = {}
    for j, k in zip(df1['国家简称(ST)'], df1['中文']):
        d1[j] = k

    d2 = {}
    for j, k in zip(df1['国家简称(ST)'], df1['区域（截至2021年2月刊）']):
        d2[j] = k



    rating_data = df['Rating'].value_counts()
    country_data = df['Country'].value_counts()

    diqu = []
    for x in list(country_data.index):
        name = d2[x]
        diqu.append(name)
    df3 = pd.DataFrame()
    df3['简称'] = list(country_data.index)
    df3['地区'] = diqu
    df3['频次'] = list(country_data.values)
    df4 = df3.groupby('地区').agg('sum')
    df4.sort_values(by=['频次'],ascending=False,inplace=True)

    x_data2 = list(df4.index)[:5]
    y_data2 = list(df4['频次'])[:5]

    x_data = list(country_data.index)[:5]
    y_data = list(country_data.values)[:5]

    country = []
    for x in x_data:
        name = d1[x]
        country.append(name)
    d = {}
    sum_count = 0
    for key,value in zip(rating_data.index,rating_data.values):
        d[key] = value
        sum_count += value


    good_rating = '%0.3lf' % ((d[5] + d[4] + d[3]) / sum_count)
    bad_rating = '%0.3lf' % ((d[1] + d[2]) / sum_count)
    fire_rating = '%0.3lf' % (d[5] / sum_count)
    four_rating = '%0.3lf' % (d[4] / sum_count)
    three_rating = '%0.3lf' % (d[3] / sum_count)
    two_rating = '%0.3lf' % (d[2] / sum_count)
    one_rating = '%0.3lf' % (d[1] / sum_count)
    print("*" * 20, 'ios', "*" * 20)
    print('前5个国家分别是:', country)
    print("前5个国家评论数:", y_data)
    print('前5个地区分别是:', x_data2)
    print("前5个地区评论数:", y_data2)
    print('总评论的数量:', sum_count)
    print('好评占比:', float(float(good_rating) * 100), "---", '好评总数为:', int(d[5] + d[4] + d[3]))
    print('五星占比:', float(float(fire_rating) * 100), "---", '五星评论数为:', d[5])
    print('四星占比:', float(float(four_rating) * 100), "---", '四星评论数为:', d[4])
    print('差评占比:', float(float(bad_rating) * 100), "---", '差评总数为:', int(d[2] + d[1]))
    print('二星占比:', float(float(two_rating) * 100), "---", '二星评论数为:', d[2])
    print('一星占比:', float(float(one_rating) * 100), "---", '一星评论数为:', d[1])

    def state_proportion(x):
        df1 = df[df['Country'] == x]
        rating_data = df1['Rating'].value_counts()
        name = d1[x]
        d = {}
        sum_count1 = 0
        for key, value in zip(rating_data.index, rating_data.values):
            d[key] = value
            sum_count1 += value

        zhanbi = '%0.3lf' % (sum_count1 / sum_count)
        one_rating = d[1]
        two_rating = d[2]
        three_rating = d[3]
        free_rating = d[4]
        five_rating = d[5]

        return name,sum_count1,zhanbi,five_rating,free_rating,three_rating,two_rating,one_rating
    df2 = pd.DataFrame()
    df2['国家'] = ['国家']
    df2['评论数量'] = ['评论数量']
    df2['占比'] = ['占比']
    df2['一星'] = ['一星']
    df2['二星'] = ['二星']
    df2['三星'] = ['三星']
    df2['四星'] = ['四星']
    df2['五星'] = ['五星']

    df2.to_csv('ios排名前五国家星级占比.csv',encoding='utf-8-sig',header=None,index=None,mode='w')
    for x in x_data:
        name,sum_count1,zhanbi,five_rating,free_rating,three_rating,two_rating,one_rating = state_proportion(x)
        df2['国家'] = [name]
        df2['评论数量'] = [sum_count1]
        df2['占比'] = [zhanbi]
        df2['一星'] = [one_rating]
        df2['二星'] = [two_rating]
        df2['三星'] = [three_rating]
        df2['四星'] = [free_rating]
        df2['五星'] = [five_rating]
        df2.to_csv('ios排名前五国家星级占比.csv', encoding='utf-8-sig', header=None, index=None, mode='a+')


def main_android(name):
    df = pd.read_csv('{}'.format(name), encoding='utf-16',
                     sep='\t')
    df1 = pd.read_excel('工具表单持续更新--地区、自研.xlsx', sheet_name='地区列表-20210514')
    d1 = {}
    for j, k in zip(df1['国家简称(ST)'], df1['中文']):
        d1[j] = k
    d2 = {}
    for j, k in zip(df1['国家简称(ST)'], df1['区域（截至2021年2月刊）']):
        d2[j] = k

    rating_data = df['Rating'].value_counts()
    country_data = df['Country'].value_counts()
    diqu = []
    for x in list(country_data.index):
        name = d2[x]
        diqu.append(name)
    df3 = pd.DataFrame()
    df3['简称'] = list(country_data.index)
    df3['地区'] = diqu
    df3['频次'] = list(country_data.values)
    df4 = df3.groupby('地区').agg('sum')
    df4.sort_values(by=['频次'], ascending=False, inplace=True)

    x_data2 = list(df4.index)[:5]
    y_data2 = list(df4['频次'])[:5]

    x_data = list(country_data.index)[:5]
    y_data = list(country_data.values)[:5]
    country = []
    for x in x_data:
        name = d1[x]
        country.append(name)
    d = {}
    sum_count = 0
    for key, value in zip(rating_data.index, rating_data.values):
        d[key] = value
        sum_count += value

    good_rating = '%0.3lf' % ((d[5] + d[4] + d[3]) / sum_count)
    bad_rating = '%0.3lf' % ((d[1] + d[2]) / sum_count)
    fire_rating = '%0.3lf' % (d[5] / sum_count)
    four_rating = '%0.3lf' % (d[4] / sum_count)
    three_rating = '%0.3lf' % (d[3] / sum_count)
    two_rating = '%0.3lf' % (d[2] / sum_count)
    one_rating = '%0.3lf' % (d[1] / sum_count)
    print("*" * 20, 'android', "*" * 20)
    print('前5个国家分别是:', country)
    print("前5个国家评论数:", y_data)
    print('前5个地区分别是:', x_data2)
    print("前5个地区评论数:", y_data2)
    print('总评论的数量:', sum_count)
    print('好评占比:', float(float(good_rating) * 100),"---",'好评总数为:',int(d[5] + d[4] + d[3]))
    print('五星占比:', float(float(fire_rating) * 100),"---",'五星评论数为:',d[5])
    print('四星占比:', float(float(four_rating) * 100),"---",'四星评论数为:',d[4])
    print('差评占比:', float(float(bad_rating) * 100),"---",'差评总数为:',int(d[2] + d[1]))
    print('二星占比:', float(float(two_rating) * 100), "---", '二星评论数为:', d[2])
    print('一星占比:', float(float(one_rating) * 100), "---", '一星评论数为:', d[1])
    def state_proportion(x):
        df1 = df[df['Country'] == x]
        rating_data = df1['Rating'].value_counts()
        name = d1[x]
        d = {}
        sum_count1 = 0
        for key, value in zip(rating_data.index, rating_data.values):
            d[key] = value
            sum_count1 += value

        zhanbi = '%0.3lf' % (sum_count1 / sum_count)
        one_rating = d[1]
        two_rating = d[2]
        three_rating = d[3]
        free_rating = d[4]
        five_rating = d[5]

        return name, sum_count1, zhanbi, five_rating, free_rating, three_rating, two_rating, one_rating

    df2 = pd.DataFrame()
    df2['国家'] = ['国家']
    df2['评论数量'] = ['评论数量']
    df2['占比'] = ['占比']
    df2['一星'] = ['一星']
    df2['二星'] = ['二星']
    df2['三星'] = ['三星']
    df2['四星'] = ['四星']
    df2['五星'] = ['五星']
    df2.to_csv('android排名前五国家星级占比.csv', encoding='utf-8-sig', header=None, index=None, mode='w')
    for x in x_data:
        name, sum_count1, zhanbi, five_rating, free_rating, three_rating, two_rating, one_rating = state_proportion(x)
        df2['国家'] = [name]
        df2['评论数量'] = [sum_count1]
        df2['占比'] = [zhanbi]
        df2['一星'] = [one_rating]
        df2['二星'] = [two_rating]
        df2['三星'] = [three_rating]
        df2['四星'] = [free_rating]
        df2['五星'] = [five_rating]
        df2.to_csv('android排名前五国家星级占比.csv', encoding='utf-8-sig', header=None, index=None, mode='a+')


if __name__ == '__main__':
    ios_name = './data1/Sensor_Tower_App_Intel_Reviews_1492005122__2022-05-30_to_2022-06-05.csv'
    android_name = './data1/Sensor_Tower_App_Intel_Reviews_com.blizzard.diablo.immortal__2022-05-30_to_2022-06-05.csv'
    main_ios(ios_name)
    main_android(android_name)
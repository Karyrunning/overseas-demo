import pandas as pd


def main_ios(name):
    df = pd.read_csv('{}'.format(name),encoding='utf-16',sep='\t')
    df1 = pd.read_excel('工具表单持续更新--地区、自研.xlsx', sheet_name='地区列表-20210514')
    d1 = {}
    for j, k in zip(df1['国家简称(ST)'], df1['中文']):
        d1[j] = k


    rating_data = df['Rating'].value_counts()
    country_data = df['Country'].value_counts()
    x_data = list(country_data.index)[:5]
    country = []
    for x in x_data:
        name = d1[x]
        country.append(name)
    d = {}
    sum_count = 0
    for key,value in zip(rating_data.index,rating_data.values):
        d[key] = value
        sum_count += value

    good_rating = '%0.2lf' %((d[5]+d[4]+d[3]) / sum_count)
    bad_rating = '%0.2lf' %((d[1]+d[2]) / sum_count)
    print("*" * 20, 'ios', "*" * 20)
    print('前5个国家分别是:',country)
    print('总评论的数量:',sum_count)
    print('好评占比:',good_rating)
    print('差评占比',bad_rating)

    def state_proportion(x):
        df1 = df[df['Country'] == x]
        rating_data = df1['Rating'].value_counts()
        name = d1[x]
        d = {}
        sum_count = 0
        for key, value in zip(rating_data.index, rating_data.values):
            d[key] = value
            sum_count += value
        one_rating = '%0.2lf' % (d[1] / sum_count)
        two_rating = '%0.2lf' % (d[2] / sum_count)
        three_rating = '%0.2lf' % (d[3] / sum_count)
        free_rating = '%0.2lf' % (d[4] / sum_count)
        five_rating = '%0.2lf' % (d[5] / sum_count)

        return name,sum_count,five_rating,free_rating,three_rating,two_rating,one_rating
    df2 = pd.DataFrame()
    df2['国家'] = ['国家']
    df2['评论数量'] = ['评论数量']
    df2['五星'] = ['五星']
    df2['四星'] = ['四星']
    df2['三星'] = ['三星']
    df2['二星'] = ['二星']
    df2['一星'] = ['一星']
    df2.to_csv('ios排名前五国家星级占比.csv',encoding='utf-8-sig',header=None,index=None,mode='w')
    for x in x_data:
        name, sum_count, five_rating, free_rating, three_rating, two_rating, one_rating = state_proportion(x)
        df2['国家'] = [name]
        df2['评论数量'] = [sum_count]
        df2['五星'] = [five_rating]
        df2['四星'] = [free_rating]
        df2['三星'] = [three_rating]
        df2['二星'] = [two_rating]
        df2['一星'] = [one_rating]
        df2.to_csv('ios排名前五国家星级占比.csv', encoding='utf-8-sig', header=None, index=None, mode='a+')


def main_android(name):
    df = pd.read_csv('{}'.format(name), encoding='utf-16',
                     sep='\t')
    df1 = pd.read_excel('工具表单持续更新--地区、自研.xlsx', sheet_name='地区列表-20210514')
    d1 = {}
    for j, k in zip(df1['国家简称(ST)'], df1['中文']):
        d1[j] = k

    rating_data = df['Rating'].value_counts()
    country_data = df['Country'].value_counts()
    x_data = list(country_data.index)[:5]
    country = []
    for x in x_data:
        name = d1[x]
        country.append(name)
    d = {}
    sum_count = 0
    for key, value in zip(rating_data.index, rating_data.values):
        d[key] = value
        sum_count += value

    good_rating = '%0.2lf' % ((d[5] + d[4] + d[3]) / sum_count)
    bad_rating = '%0.2lf' % ((d[1] + d[2]) / sum_count)
    print("*"*20,'android',"*"*20)
    print('前5个国家分别是:', country)
    print('总评论的数量:', sum_count)
    print('好评占比:', good_rating)
    print('差评占比', bad_rating)

    def state_proportion(x):
        df1 = df[df['Country'] == x]
        rating_data = df1['Rating'].value_counts()
        name = d1[x]
        d = {}
        sum_count = 0
        for key, value in zip(rating_data.index, rating_data.values):
            d[key] = value
            sum_count += value
        one_rating = '%0.2lf' % (d[1] / sum_count)
        two_rating = '%0.2lf' % (d[2] / sum_count)
        three_rating = '%0.2lf' % (d[3] / sum_count)
        free_rating = '%0.2lf' % (d[4] / sum_count)
        five_rating = '%0.2lf' % (d[5] / sum_count)

        return name, sum_count, five_rating, free_rating, three_rating, two_rating, one_rating

    df2 = pd.DataFrame()
    df2['国家'] = ['国家']
    df2['评论数量'] = ['评论数量']
    df2['五星'] = ['五星']
    df2['四星'] = ['四星']
    df2['三星'] = ['三星']
    df2['二星'] = ['二星']
    df2['一星'] = ['一星']
    df2.to_csv('android排名前五国家星级占比.csv', encoding='utf-8-sig', header=None, index=None, mode='w')
    for x in x_data:
        name, sum_count, five_rating, free_rating, three_rating, two_rating, one_rating = state_proportion(x)
        df2['国家'] = [name]
        df2['评论数量'] = [sum_count]
        df2['五星'] = [five_rating]
        df2['四星'] = [free_rating]
        df2['三星'] = [three_rating]
        df2['二星'] = [two_rating]
        df2['一星'] = [one_rating]
        df2.to_csv('android排名前五国家星级占比.csv', encoding='utf-8-sig', header=None, index=None, mode='a+')


if __name__ == '__main__':
    ios_name = 'Sensor_Tower_App_Intel_Reviews_1543991460__2022-05-17_to_2022-05-24.csv'
    android_name = 'Sensor_Tower_App_Intel_Reviews_1543991460__2022-05-17_to_2022-05-24.csv'
    main_ios(ios_name)
    main_android(android_name)
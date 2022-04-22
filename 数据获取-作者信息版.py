import time
import pandas as pd
import os
import requests




def data_screen():
    df = pd.read_csv('./input/{}'.format(filename1), encoding="UTF-16",sep='\t')
    df['youtube_view'] = df['youtube_view'].astype(int)
    df1 = df.sort_values(by=['youtube_view'],ascending=False)
    list_author_url = []
    list_author_name = []
    list_video_url = []
    for u,i,ul in zip(df1['User Profile Url'][0:10],df1['Influencer'][0:10],df1['URL'][0:10]):
        list_author_url.append(u)
        list_author_name.append(i)
        list_video_url.append(ul)
    return list_author_url, list_author_name,list_video_url


def data_screen1():
    df = pd.read_csv('./output/{}'.format(filename2))
    new_df = df.dropna(how='any', axis=0)

    def qx(x):
        x = str(x)
        if 'K' in x:
            x = x.replace('K','000')
            return x
        elif 'M' in x:
            x = x.replace('M', '0000')
            return x
        else:
            return x

    new_df['comment_vote'] = new_df['comment_vote'].apply(qx)
    new_df['comment_vote'] = new_df['comment_vote'].astype(int)
    df1 = new_df.sort_values(by=['comment_vote'], ascending=False)

    list_author_url = []
    list_author_name = []
    list_video_url = []
    for u,i,ul in zip(df1['comment_author'][0:10],df1['comment_channel'][0:10],df1['video_url'][0:10]):
        list_author_url.append(i)
        list_author_name.append(u)
        list_video_url.append(ul)
    return list_author_url,list_author_name,list_video_url

#获取每个作者的视频数量，视频播放量，和订阅人数
def channel_number(id):
    url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={}&key={}'.format(id,key)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    response = requests.get(url=url,headers=headers)
    content = response.json()
    time.sleep(0.1)
    item = content['items'][0]
    viewcount = item['statistics']['viewCount']
    videoCount = item['statistics']['videoCount']
    hiddenSubscriberCount = item['statistics']['hiddenSubscriberCount']
    if hiddenSubscriberCount == False:
        subscriberCount = item['statistics']['subscriberCount']
    else:
        subscriberCount  = 'hidden'

    return viewcount,videoCount,hiddenSubscriberCount,subscriberCount


def new_data():
    list1, list2, list6 = data_screen()
    list3, list4, list7 = data_screen1()
    list5 = []
    viewcount_list1 = []
    viewcount_list2 = []
    videoCount_list1 = []
    videoCount_list2 = []
    subscriberCount_list1 = []
    subscriberCount_list2 = []
    for l in list1:
        l = str(l).split('/')
        l = l[-1]
        result = channel_number(l)
        viewcount_list1.append(result[0])
        videoCount_list1.append(result[1])
        subscriberCount_list1.append(result[3])
    for l in list3:
        href = 'https://www.youtube.com/channel/' + l
        list5.append(href)
        result = channel_number(l)
        viewcount_list2.append(result[0])
        videoCount_list2.append(result[1])
        subscriberCount_list2.append(result[3])

    df = pd.DataFrame()
    df['author_url'] = list1
    df['author_name'] = list2
    df['video_url'] = list6
    df['view_count'] = viewcount_list1
    df['video_count'] = videoCount_list1
    df['subscriber_count'] = subscriberCount_list1

    df1 = pd.DataFrame()
    df1['author_url'] = list5
    df1['author_name'] = list4
    df1['video_url'] = list7
    df1['view_count'] = viewcount_list2
    df1['video_count'] = videoCount_list2
    df1['subscriber_count'] = subscriberCount_list2

    writer = pd.ExcelWriter(os.path.join(os.getcwd(), './output/top10作者和评论者相关信息.xlsx'))
    df.to_excel(writer, sheet_name='视频发布者信息')
    df1.to_excel(writer, sheet_name='评论者信息')
    writer.save()

if __name__ == '__main__':
    filename1 = 'Youtube.csv'
    filename2 = 'new_youtube.csv'
    key = '@@@@@@@@@@@@'
    # #数据筛选
    new_data()

import pandas as pd
from pyyoutube import Api
import subprocess
import concurrent.futures
import json
import requests
import re
import time


#获取每个视频的播放量
def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        'cookie': 'VISITOR_INFO1_LIVE=RKzCsolgDCo; PREF=tz=Asia.Shanghai; __Secure-3PSID=IggCDOfkt0_YvrRDH-9lGSQbor6o0VHQhsijgQ4gSv7__3n2Rs0EYtZeb1R4fwClxR3K0Q.; __Secure-3PAPISID=bjI6sYyXBcWou2TC/ANlPiGPXDtZw2_zCf; LOGIN_INFO=AFmmF2swRQIgUOkIEPy88ifEtDyB0dnwxxfJt76mIVSAk3b12prs34QCIQD41kthQYAp3YpI6KqMpbtSkik2DyNKhwIbkEk_F-o00A:QUQ3MjNmd3BVZmExUDZ2WmZGN3I0V0dHOVo0QkN0eW9TU3U0ZmVCSC0xSlJWczB0cXdGS2E3ejVrNWNnOUpUUWRQdS1Qcm9nMTNnLU5lbkE0Q1p0TEZaZ1RIOXJIdlRiTE0tZjRXYWVEd2V0SDBOanBnWXhGaGtfVjF6RFlqVjcyZnpKdWxTb29fem9Xck4zaENyeDQwbE1QZXl4MEZkSnBR; YSC=81TJ3_NWjT4; CONSISTENCY=AGDxDeP7498HbtzACaaXCZmEVo5IfvYWPFZHoNj_dc8snXp0-n3tTq1tEoOXp6Dfp3jKfSkiUhgpP70Kf0XvE6gMj3comTlnB7Z0JzxTKiHOfdy9OKp31k1FCz4A3p9M5oO6wCfHI5-4eb-9wqhXKVtn; __Secure-3PSIDCC=AJi4QfH3eAzxlsYFUG-MxtfTavjOM8Um9U6WuyXPjK7Rbz4isixrCiJBjIS9_A-62PH7r5PMHQ',
    }
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        content = html.text
        view = re.compile('"allowRatings":.*?,"viewCount":"(\d+)","author"')
        views = view.findall(content)
        try:
            views = views[0]
        except:
            views = 0
        time.sleep(0.2)
        return views
    else:
        time.sleep(0.2)
        print(html.status_code)


def data_screen():
    df = pd.read_csv('./input/{}'.format(input_filename), encoding="UTF-16",sep='\t')
    # csv内容筛选，选出全是YouTube的内容行
    df1 = df[df['Source'] == 'Youtube']

    new_df = df1.drop_duplicates(subset=['URL'], keep='first')

    data = data_screen1(data_screen1(new_df))

    data['youtube_view'] = data['URL'].apply(get_html)

    data.to_csv('./input/{}'.format(create_filename), encoding="UTF-16", sep='\t')

def data_screen1(data):
    df = data
    new_df = df[((df['Headline'].str.contains('{}'.format(keyword1), case=False)) | (df['Hit Sentence'].str.contains('{}'.format(keyword1), case=False))) & ((df['Headline'].str.contains('{}'.format(keyword2), case=False)) | (df['Hit Sentence'].str.contains('{}'.format(keyword2), case=False)))]
    return new_df


#获取每个评论下面的回复数量内容
def reply_number(cid):
    api = Api(api_key=key)
    channel_by_id = api.get_comments(parent_id=cid)
    return len(channel_by_id.items)


#获取YouTube每个视频连接下面的评论内容
def get_data(url):
    name = str(url).split('v=')[1]
    status, result = subprocess.getstatusoutput("youtube-comment-downloader --url {} --output ./input/data/{}.json".format(url,name))
    return result


#整合好一个新的CSV文件
def new_data():
    df = pd.read_csv('./input/{}'.format(create_filename), encoding="UTF-16", sep='\t')

    count = 0
    for d,h,se,u,uu,yv in zip(df['Date'],df['Headline'],df['Hit Sentence'],df['URL'],df['User Profile Url'],df['youtube_view']):
        count += 1
        name = str(u).split('v=')[1]
        with open('./input/data/{}.json'.format(name),'r',encoding='utf-8')as f:
            content = f.readlines()
        if len(content) != 0:
            for c in content:
                c = c.strip('\n')
                c = json.loads(c)
                author = c['author']
                time_parsed = pd.to_datetime(c['time_parsed'],unit='s')
                text = c['text']
                cid = c['cid']
                channel = c['channel']
                votes = c['votes']
                new_df = pd.DataFrame()
                new_df['video_date'] = [d]
                new_df['video_head'] = [h]
                new_df['video_sentence'] = [se]
                new_df['video_url'] = [u]
                new_df['author_url'] = [uu]
                new_df['video_views'] = [yv]
                new_df['comment_date'] = [time_parsed]
                new_df['comment_text'] = [text]
                new_df['comment_cid'] = [cid]
                new_df['comment_channel'] = [channel]
                new_df['comment_author'] = [author]
                new_df['comment_vote'] = [votes]
                new_df.to_csv('./output/{}'.format(new_filename), mode="a+", encoding="utf-8-sig", index=False, header=False)
                print('正在处理第{}个视频内容,还剩余{}个视频未处理'.format(count,int(len(df['URL'])-count)))
        else:
            new_df = pd.DataFrame()
            new_df['video_date'] = [d]
            new_df['video_head'] = [h]
            new_df['video_sentence'] = [se]
            new_df['video_url'] = [u]
            new_df['author_url'] = [uu]
            new_df['video_views'] = [yv]
            new_df['comment_date'] = ['']
            new_df['comment_text'] = ['']
            new_df['comment_cid'] = ['']
            new_df['comment_channel'] = ['']
            new_df['comment_author'] = ['']
            new_df['comment_vote'] = ['']
            new_df.to_csv('./output/{}'.format(new_filename), mode="a+", encoding="utf-8-sig", index=False, header=False)
            print('正在处理第{}个视频内容,还剩余{}个视频未处理'.format(count,int(len(df['URL'])-count)))


#应用多进程的方法把全部评论内容获取下来
def run():
    df = pd.read_csv('./input/{}'.format(create_filename), encoding="UTF-16", sep='\t')
    # 多进程
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as e:
        futuers = [e.submit(get_data, url) for url in df['URL']]
        for futuer in concurrent.futures.as_completed(futuers):
            print(futuer.result())


if __name__ == '__main__':
    input_filename = 'Valorant_Mobile_Closed_Beta_in_China_海外监控 - Apr 18, 2022 - 5 01 14 PM.csv'
    keyword1 = 'Valorant'
    keyword2 = 'mobile'
    create_filename = 'Youtube.csv'

    new_filename = 'new_youtube.csv'
    key = '@@@@@@@@@@@@'
    new_df = pd.DataFrame()
    new_df['video_date'] = ['video_date']
    new_df['video_head'] = ['video_head']
    new_df['video_sentence'] = ['video_sentence']
    new_df['video_url'] = ['video_url']
    new_df['author_url'] = ['author_url']
    new_df['video_views'] = ['video_views']
    new_df['comment_date'] = ['comment_date']
    new_df['comment_text'] = ['comment_text']
    new_df['comment_cid'] = ['comment_cid']
    new_df['comment_channel'] = ['comment_channel']
    new_df['comment_author'] = ['comment_author']
    new_df['comment_vote'] = ['comment_vote']
    new_df.to_csv('./output/{}'.format(new_filename),mode="w", encoding="utf-8-sig", index=False, header=False)
    # 数据筛选
    data_screen()
    # # #多进程评论获取
    run()
    #获取其余内容并且合并为一个新表
    new_data()

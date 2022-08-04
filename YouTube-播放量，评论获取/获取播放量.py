import pandas as pd
import concurrent.futures
import requests
import re
import time
from tqdm import tqdm
import concurrent.futures

#获取每个视频的播放量
def get_html(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        'cookie': 'VISITOR_INFO1_LIVE=RKzCsolgDCo; PREF=tz=Asia.Shanghai; __Secure-3PSID=IggCDOfkt0_YvrRDH-9lGSQbor6o0VHQhsijgQ4gSv7__3n2Rs0EYtZeb1R4fwClxR3K0Q.; __Secure-3PAPISID=bjI6sYyXBcWou2TC/ANlPiGPXDtZw2_zCf; LOGIN_INFO=AFmmF2swRQIgUOkIEPy88ifEtDyB0dnwxxfJt76mIVSAk3b12prs34QCIQD41kthQYAp3YpI6KqMpbtSkik2DyNKhwIbkEk_F-o00A:QUQ3MjNmd3BVZmExUDZ2WmZGN3I0V0dHOVo0QkN0eW9TU3U0ZmVCSC0xSlJWczB0cXdGS2E3ejVrNWNnOUpUUWRQdS1Qcm9nMTNnLU5lbkE0Q1p0TEZaZ1RIOXJIdlRiTE0tZjRXYWVEd2V0SDBOanBnWXhGaGtfVjF6RFlqVjcyZnpKdWxTb29fem9Xck4zaENyeDQwbE1QZXl4MEZkSnBR; YSC=81TJ3_NWjT4; CONSISTENCY=AGDxDeP7498HbtzACaaXCZmEVo5IfvYWPFZHoNj_dc8snXp0-n3tTq1tEoOXp6Dfp3jKfSkiUhgpP70Kf0XvE6gMj3comTlnB7Z0JzxTKiHOfdy9OKp31k1FCz4A3p9M5oO6wCfHI5-4eb-9wqhXKVtn; __Secure-3PSIDCC=AJi4QfH3eAzxlsYFUG-MxtfTavjOM8Um9U6WuyXPjK7Rbz4isixrCiJBjIS9_A-62PH7r5PMHQ',
    }

    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        content = html.text
        #获取观看数量
        view = re.compile('"allowRatings":.*?,"viewCount":"(\d+)","author"')
        views = view.findall(content)
        try:
            views = views[0]
        except:
            views = 0
        #获取点赞人数
        accept = re.compile('"defaultText":\{"accessibility":\{"accessibilityData":\{"label":".*\d+ 人表示喜歡"\}\},"simpleText":"(.*\d+)"\},"toggledText"')
        accepts = accept.findall(content)
        try:
            accepts = accepts[0]

        except:
            accepts = 0
        #获取评论人数
        comment = re.compile('"commentCount":{"simpleText":"(\d+)"},')
        comments = comment.findall(content)
        try:
            comments = comments[0]
        except:
            comments = 0
        #获取粉丝数量
        fan = re.compile('\{"accessibility":\{"accessibilityData":\{"label":".*? 位訂閱者"\}\},"simpleText":"(.*?) 位訂閱者"}')
        fans = fan.findall(content)

        try:
            fans = fans[0]
        except:
            fans = 0
        # 标题
        title = re.compile('{"videoPrimaryInfoRenderer":{"title":{"runs":\[{"text":"(.*?)".*?')
        titles = title.findall(content)

        try:
            titles = titles[0]
        except:
            titles = 0

        # 发布时间
        timedate = re.compile('"dateText":\{"simpleText":"(.*?)"\}\}\},')
        timedates = timedate.findall(content)

        try:
            timedates = timedates[0]
        except:
            timedates = 0

        # 发布者 iXBT games
        name = re.compile('"shortBylineText":{"runs":\[{"text":"(.*?)","navigationEndpoint".*?')
        names = name.findall(content)

        try:
            names = names[0]
        except:
            names = 0
        time.sleep(0.1)
        return timedates,url,views,accepts,comments,fans,titles,names
    else:
        print(html.status_code)


def data_screen():
    df = pd.read_csv('./input/{}'.format(input_filename),encoding='utf-16',sep='\t')
    # csv内容筛选，选出全是YouTube的内容行
    df1 = df[df['Source'] == 'Youtube']
    # df1 = df1[df1['Engagement'] >= 1000]
    new_df = df.drop_duplicates(subset=['URL'], keep='first')
    data = data_screen1(data_screen1(new_df))
    list_date = []
    list_view = []
    list_url = []
    list_fan = []
    list_comment = []
    list_accept = []
    list_title = []
    list_name = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
        # 调用这个函数，用一个列表的形式把这个函数给保存下来
        futuers = [e.submit(get_html, item) for item in data['URL']]
        # 用叠带把这个函数的内容一个个打印出来
        for futuer in tqdm(concurrent.futures.as_completed(futuers)):
            timedates,url,views,accepts,comments,fans,titles,names = futuer.result()
            list_date.append(timedates)
            list_url.append(url)
            list_view.append(views)
            list_accept.append(accepts)
            list_comment.append(comments)
            list_fan.append(fans)
            list_title.append(titles)
            list_name.append(names)


    new_data = pd.DataFrame()
    new_data['视频链接'] = list_url
    new_data['发布日期'] = list_date
    new_data['视频标题'] = list_title
    new_data['观看次数'] = list_view
    new_data['点赞次数'] = list_accept
    new_data['评论总数'] = list_comment
    new_data['作者名称'] = list_name
    new_data['粉丝数量'] = list_fan
    new_data.to_csv('./output/Youtube.csv',encoding='utf-8-sig',sep=',',index=None)


def data_screen1(data):
    df = data
    keyword1 = ''
    keyword2 = ''
    new_df = df[((df['Headline'].str.contains('{}'.format(keyword1), case=False)) | (df['Hit Sentence'].str.contains('{}'.format(keyword1), case=False))) & ((df['Headline'].str.contains('{}'.format(keyword2), case=False)) | (df['Hit Sentence'].str.contains('{}'.format(keyword2), case=False)))]
    return new_df


if __name__ == '__main__':
    input_filename = 'Monster_Hunter_Mobile - Aug 2, 2022 - 5 15 10 PM.csv'
    # 数据筛选
    data_screen()


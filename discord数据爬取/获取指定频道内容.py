import requests
import time
from tqdm import tqdm
import pandas as pd
import numpy as np
import re
import random


user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

#这里可能也要修改
headers = {
    "authorization": "OTU4MTk3NzMzNTY5NzQ5MDAy.GHqIIi.DFkwYshaqYTFsqqnfzaLe0JbtK9numsQ7YWMOM",
    "cookie": "__dcfduid=33e576e0af0b11ecacf421044cb0b85c; __sdcfduid=33e576e1af0b11ecacf421044cb0b85c3b11a81671047def08f144a9c4fea5e370d50311a16a60c0a9b852455c597243; _ga=GA1.2.746746656.1648522323; _gid=GA1.2.1084155933.1659600218; OptanonConsent=isIABGlobal=false&datestamp=Thu+Aug+04+2022+16%3A03%3A38+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.33.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1&AwaitingReconsent=false; __cf_bm=3oA99UHQ32vwhpSIZvbqiVVj8yMwVUJkqYAOErRfK64-1659600230-0-AWLsn5/PLYYaSFHi478cEkSkY7FoCqPTRt3iM1nQ5WR+WU/n3sZgPmx8GFmrsNVE27cG42MWqBiosRSIzjtsB4VDH31KQDNWDxQ+itEeiQRwLkc6I3E1FzkSBYtOLFIpeg==",
    "referer": "https://discord.com/channels/948237510914486303/948257420327657502",
    "sec-ch-ua": 'Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": random.choice(user_agent),
    "x-debug-options": "bugReporterEnabled",
    "x-discord-locale": "zh-CN",
    "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InpoLUNOIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAzLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5nb29nbGUuY29tLmhrLyIsInJlZmVycmluZ19kb21haW4iOiJ3d3cuZ29vZ2xlLmNvbS5oayIsInNlYXJjaF9lbmdpbmUiOiJnb29nbGUiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTM3NTA2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
}

def check_status(url):
    html = requests.get(url,headers=headers)
    if html.status_code == 200:
        content = html.json()
        messages = content['total_results']
        return messages
    else:
        print(html.status_code)


def get_html():
    a = random.uniform(1.0, 1.5)
    number = int(total / 25) +1
    list_number = [(j * 25) for j in range(0,number+1)]
    list_number = list_number[fw1:fw2]
    # #阿拉伯
    # list_channel = ['986607131644035108']
    # channel_name = ['general']
    # 拉美
    # list_channel = ['991791247624781854', '991792315461025872', '994889246127161424']
    # channel_name = ['chat-general-espanol', 'reporta-un-bug', 'sugerencias']
    #巴西
    list_channel = ['1004863310115651595', '986011017194663987', '986011017697959936','986007094908055573']
    channel_name = ['report-bugs', 'sugestoes-e-feedbacks', 'duvidas','chat-aberto']
    # #土耳其
    # list_channel = []
    # channel_name = []
    d = {}
    for l,n in zip(list_channel,channel_name):
        d[l] = n
    for i in tqdm(list_number):
        href = url + "&offset={}".format(i)
        try:
            html = requests.get(url=href, headers=headers)
            content = html.json()
            messages = content['messages']
        except:
            time.sleep(300)
            html = requests.get(url=href, headers=headers)
            content = html.json()
            messages = content['messages']

        for m in messages:
            try:
                comment = m[0]['content'].strip('\n\n').replace('\n','')
            except:
                comment = np.NAN
            try:
                timedeate = m[0]['timestamp']
            except:
                timedeate = np.NAN
            try:
                username = m[0]['author']['username']
            except:
                username = np.NAN
            try:
                author_id = m[0]['author']['id']
            except:
                author_id = np.NAN
            try:
                mentions = m[0]['mentions'][0]['username']
            except:
                mentions = np.NAN
            try:
                channel_id = m[0]['channel_id']
            except:
                channel_id = np.NAN

            if channel_id in list_channel:
                if len(comment) != 0:
                    strinfo = re.compile('\<.*?\>')
                    comment = strinfo.sub(' ', comment)
                df = pd.DataFrame()
                df['发文时间'] = [timedeate]
                df['发布者id'] = [author_id]
                df['发布者名字'] = [username]
                df['内容信息'] = [comment]
                df['被提及人'] = [mentions]
                df['频道'] = [d[channel_id]]
                df.to_csv('./input/{}.csv'.format(name), mode='a+', header=False, index=False,encoding='utf-8-sig')
            else:
                pass
        time.sleep(a)


if __name__ == '__main__':
    #这里是要修改的
    #&max_id=1001881652428800000
    fw1 = 0
    fw2 = 200
    name = '巴西14-22新数据'
    #desc 最新数据 asc 最旧数据
    url = 'https://discord.com/api/v9/guilds/978655279157747712/messages/search?min_id=1008042246144000000&max_id=1011303736934400000&sort_by=timestamp&sort_order=desc'
    total = check_status(url)
    #频道ID
    df = pd.DataFrame()
    df['发文时间'] = ['发文时间']
    df['发布者id'] = ['发布者id']
    df['发布者名字'] = ['发布者名字']
    df['内容信息'] = ['内容信息']
    df['被提及人'] = ['被提及人']
    df['频道'] = ['频道']
    df.to_csv('./input/{}.csv'.format(name), mode='w', header=False, index=False,encoding='utf-8-sig')

    get_html()


import requests
import time
from tqdm import tqdm
import pandas as pd
import numpy as np
import re


#这里可能也要修改
headers = {
    "authorization": "OTU4MTk3NzMzNTY5NzQ5MDAy.GaVp0R.qhzqiza_ITnKxTC0r5swkja3GTWmw2MMuWIrg4",
    "cookie": "__dcfduid=33e576e0af0b11ecacf421044cb0b85c; __sdcfduid=33e576e1af0b11ecacf421044cb0b85c3b11a81671047def08f144a9c4fea5e370d50311a16a60c0a9b852455c597243; _ga=GA1.2.746746656.1648522323; OptanonConsent=isIABGlobal=false&datestamp=Mon+Jun+27+2022+11%3A23%3A11+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.33.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1&AwaitingReconsent=false; __cfruid=be19e182bdc8d426a43ce4ad83538f56f5cae9ff-1656639137; __cf_bm=xUn4JLmUDj91S5Xn5IQ0avYB89bArxmkdQzYPLHYORw-1656640114-0-AS0tz6VkIjJBJODi+yYvJGliidb7NBCp/TC1F5PnaWX7Pvg/3ZFPbTnRs83gWlV0ScFXJkLYnyJuLQ0HRsiJGaIYPz7PYCC6NUKZc371sbpEXa7CsXGwZo79pl2CSpTReQ==",
    "referer": "https://discord.com/channels/948237510914486303/948259165783085107",
    "sec-ch-ua": 'Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
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
    number = int(total / 25) +1
    list_number = [(j * 25) for j in range(0,number+1)]
    list_channel = ['948259361497694278','948259127925284915','948259165783085107','948259093745909781']
    channel_name = ['other-division-games','ask-the-team','feedback-and-bugs','general-chat']
    count = 0
    d = {}
    for l,n in zip(list_channel,channel_name):
        d[l] = n
    for i in tqdm(list_number):
        count += 1
        if count > 50:
            time.sleep(300)
            count = 0
        else:
            href = url + "&offset={}".format(i)
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

                    df.to_csv('./input/原始数据.csv', mode='a+', header=None, index=None,encoding='utf-8-sig')
                else:
                    pass
            time.sleep(2)


if __name__ == '__main__':
    #这里是要修改的
    #&max_id=1001881652428800000
    url = 'https://discord.com/api/v9/guilds/948237510914486303/messages/search?min_id=999344937369600000&max_id=1003693591756800000'
    total = check_status(url)
    #频道ID
    df = pd.DataFrame()
    df['发文时间'] = ['发文时间']
    df['发布者id'] = ['发布者id']
    df['发布者名字'] = ['发布者名字']
    df['内容信息'] = ['内容信息']
    df['被提及人'] = ['被提及人']
    df['频道'] = ['频道']
    df.to_csv('./input/原始数据.csv', mode='w', header=None, index=None,encoding='utf-8-sig')

    get_html()


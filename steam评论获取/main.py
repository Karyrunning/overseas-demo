import requests
from lxml import etree
import pandas as pd
import time
import random
from tqdm import tqdm

headers = {
    "Cookie": "recentlyVisitedAppHubs=1313140; timezoneOffset=28800,0; _ga=GA1.2.1229393990.1663222089; browserid=2747781448323163218; sessionid=d9beb64391c13468e5860f65; steamCountry=US%7C71ebbd05f4ea8efdba333092eca59b34; steamLoginSecure=76561198863766772%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTRGRV8yMTREMzREMF8xRkQ0NiIsICJzdWIiOiAiNzY1NjExOTg4NjM3NjY3NzIiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY2NDI2MDUzMSwgIm5iZiI6IDE2NjQxNzMyMDUsICJpYXQiOiAxNjY0MTczMjE1LCAianRpIjogIjBCQTFfMjE1M0YxN0VfRDFBQkQiLCAib2F0IjogMTY2MzU1MjcwMiwgInJ0X2V4cCI6IDE2ODEzNTI4MzQsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICI0My4xMzIuOTguMzEiLCAiaXBfY29uZmlybWVyIjogIjQzLjEzMi45OC4zMSIgfQ.JIdVqHczMPngRmJtka3-ImarmdaDGPoVWzgHVlWlHJuX2Kc2KnGqBbLhToQav6vkCH_QGG1qd3XSnN7Qm3xJAQ; _gid=GA1.2.187597089.1664173217; app_impressions=1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100003_|1313140@2_9_100003_|1313140@2_9_100003_|1313140@2_9_100003_|1313140@2_9_100003_|1313140@2_9_100010_|1313140@2_9_100003_|1313140@2_9_100003_|1313140@2_9_100003_|1313140@2_9_100003_|1313140@2_9_100003_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_|1313140@2_9_100010_",
    "Host": "steamcommunity.com",
    "Referer": "https://steamcommunity.com/app/1313140/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=all",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


def get_status_code(url):
    html = requests.get(url,headers=headers)
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)


def get_html(html):
    content = html.text
    soup = etree.HTML(content)
    timedate = soup.xpath('//div[@class="hours"]/text()')
    title = soup.xpath('//div[@class="title"]/text()')
    hours = soup.xpath('//div[@class="hours"]/text()')
    list_comment = []

    div1 = soup.xpath('//div[@class="apphub_UserReviewCardContent"]')
    for d in div1:
        comment = d.xpath('./div[@class="apphub_CardTextContent"]/text()')
        comment = ' '.join(comment)
        comment = comment.replace('\r\n\t\t\t\t','').replace('\t','').replace('\r','').replace('\n','').strip(' ')
        list_comment.append(comment)

    df = pd.DataFrame()
    df['发布时间'] = timedate
    df['状态'] = title
    df['游戏时长'] = hours
    df['评论'] = list_comment
    df.to_csv('数据.csv', encoding='utf-8-sig', index=False, header=False, mode='a+')
    a = random.uniform(1.0, 1.5)
    time.sleep(a)


if __name__ == '__main__':
    df = pd.DataFrame()
    df['发布时间'] = ['发布时间']
    df['状态'] = ['状态']
    df['游戏时长'] = ['游戏时长']
    df['评论'] = ['评论']
    df.to_csv('数据.csv',encoding='utf-8-sig',index=False,header=False,mode='w')
    for j in tqdm(range(1,200,1)):
        url = "https://steamcommunity.com/app/1313140/homecontent/?userreviewscursor=AoIIP3N9UnSt%2Fc8D&userreviewsoffset=10&p={}&workshopitemspage={}&readytouseitemspage={}&mtxitemspage={}&itemspage={}&screenshotspage={}&videospage={}&artpage={}&allguidepage={}&webguidepage={}&integratedguidepage={}&discussionspage={}&numperpage=10&browsefilter=toprated&browsefilter=toprated&l=schinese&appHubSubSection=10&filterLanguage=all&searchText=&maxInappropriateScore=50".format(j,j,j,j,j,j,j,j,j,j,j,j)
        get_status_code(url)
import requests
import random
import pandas as pd
from tqdm import tqdm
import concurrent.futures
from lxml import etree

df = pd.read_csv('./input/Apex_Mobile - May 26, 2022 - 8 02 02 PM.csv',encoding='utf-16',sep='\t')


def chuli_url(x):
    x = str(x).split("?sort")
    x = x[0]
    return x


df['URL'] = df['URL'].apply(chuli_url)
df.drop_duplicates(subset=['URL'], keep='first', inplace=True)

def main_ur(i):
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
    headers = {
        'user-agent': random.choice(user_agent),
        'cookie': 'loid=0000000000l9fveu25.2.1648523470673.Z0FBQUFBQmlRbmpPNWFuZEtXMjktOXc5MXJLZFBDQ0xHVml1ZkoyVHYwU09rYnJMLXJ6TGU0QlpMNE0wZk1aY09rZXNEYkxzMnpONllDVDBCQlFRR1RJMExrUDgtdU9rOGtxSWZuckxvajAzODVzbzBpVlRmWk5yNVZ3ck5vVmRTUnhHenRodmdIRnk; csv=2; edgebucket=d6qBld9Xk55c8mFjI3; g_state={"i_l":0}; reddit_session=1666198239917%2C2022-03-29T03%3A12%3A30%2Caa2666b5c3d5b749bb61016a4d6e89ece5f29e6e; recent_srs=t5_2qh03%2Ct5_2qh1i%2Ct5_2sc2s%2Ct5_2xvvr%2Ct5_266pd9%2Ct5_2tn4t%2Ct5_wbjtq%2Ct5_rgzzt%2Ct5_2qhwp%2Ct5_2ud8h; token_v2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTM2MjA2NzgsInN1YiI6IjE2NjYxOTgyMzk5MTctZWljcmIzLTY5ZERFUWJhZklHWDQ0WkhZRUN0ZXZnIiwibG9nZ2VkSW4iOnRydWUsInNjb3BlcyI6WyIqIiwiZW1haWwiLCJwaWkiXX0.qDN0amqLHAQeERgLVH_MZMThTHP86RX_SXNcJh5E4EY; yuhaozeng_recentclicks2=t3_urhepd%2Ct3_us6aut%2Ct3_uvyce0%2Ct3_uvvrk1%2Ct3_uxuwne; session_tracker=ragdrajqcndpfkqgbo.0.1653566024594.Z0FBQUFBQmlqMnBJaEhJcWdOYktfLUp1clNtN0pqMDFMaGRPdnN0LWJUSUcwZ19tNGhyN0lXemxfd0RSemw0aEVHRDgyZ2NkOEc1a2QxNHBrY2pla29sdWVaRFlsc0VUUFNSajhfT0JjRjlHQ2FTcF9zQndqYzZ3YnNyZUNLc1BZVk5BNWE0REwtVFA',
    }

    html = requests.get(i,headers=headers)
    content = html.text
    soup = etree.HTML(content)
    try:
        votes = soup.xpath('//div[@class="_1E9mcoVn4MYnuBQSVDt1gC"]/div/text()')[0]
        if 'k' in votes:
            votes = votes.replace('k','').replace('.','')
            votes = int(votes) * 100
    except:
        votes = 0
    try:
        comments = soup.xpath('//div[@class="_3-miAEojrCvx_4FQ8x3P-s"]/div[1]/span/text()')[0]
        comments = str(comments).split(" ")[0]
        comments = int(comments)
    except:
        comments = 0

    return votes,comments,i


list_votes = []
list_comments = []
list_url = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
    # 调用这个函数，用一个列表的形式把这个函数给保存下来
    futuers = [e.submit(main_ur, item) for item in df['URL']]
    # 用叠带把这个函数的内容一个个打印出来
    for futuer in tqdm(concurrent.futures.as_completed(futuers)):
        votes, comments,url = futuer.result()
        list_votes.append(votes)
        list_comments.append(comments)
        list_url.append(url)

df1 = pd.DataFrame()
df1['论坛链接'] = list_url
df1['点赞数量'] = list_votes
df1['评论数量'] = list_comments
df1.to_csv('./output/reddit帖子具体信息.csv',encoding='utf-8-sig',sep=',')
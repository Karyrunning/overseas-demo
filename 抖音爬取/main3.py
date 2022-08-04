import requests
from lxml import etree
import numpy as np
import pandas as pd
from tqdm import tqdm
import re
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "cookie": "douyin.com; ttwid=1%7Cje-FuTyRYZ2yeqLWIV-0UaJEKjgK3Z-ZwtC3IhXScaw%7C1658216712%7C3227fede5ab1c3e7796e9e01a1166b22f8915ed7123525e02c0874731477031b; s_v_web_id=verify_l5rvf33z_uNyyjTAj_BSbG_4HL1_BrNR_4CwNLKogevXK; passport_csrf_token=b35ee8266eeef2fd6e0f064e53880e4f; passport_csrf_token_default=b35ee8266eeef2fd6e0f064e53880e4f; d_ticket=b92a7ad752d8dd10cdf34ffc70d1c0c2f8696; n_mh=tAEuoAg1La9sYtHwxmG5tufR23dc2gronxORACD3EAs; passport_auth_status=76871744b9b2e2ece1027b2593f1f20c%2C; passport_auth_status_ss=76871744b9b2e2ece1027b2593f1f20c%2C; sso_auth_status=89c0a659dc3c1520adb1d8f2abae8cc0; sso_auth_status_ss=89c0a659dc3c1520adb1d8f2abae8cc0; sso_uid_tt=f4476075bf10eefc6a4b62234f24e89c; sso_uid_tt_ss=f4476075bf10eefc6a4b62234f24e89c; toutiao_sso_user=5b6abf7a1df603c4d9488e7127618604; toutiao_sso_user_ss=5b6abf7a1df603c4d9488e7127618604; sid_ucp_sso_v1=1.0.0-KDI0ZTk5MjhmNGZkMzQyNmFmNmFlYzIzNGMwMjA5NmRhMTA4ZDliODQKHwi-m7Dh1ozxBxCmwtmWBhjvMSAMMMqE25IGOAJA8QcaAmhsIiA1YjZhYmY3YTFkZjYwM2M0ZDk0ODhlNzEyNzYxODYwNA; ssid_ucp_sso_v1=1.0.0-KDI0ZTk5MjhmNGZkMzQyNmFmNmFlYzIzNGMwMjA5NmRhMTA4ZDliODQKHwi-m7Dh1ozxBxCmwtmWBhjvMSAMMMqE25IGOAJA8QcaAmhsIiA1YjZhYmY3YTFkZjYwM2M0ZDk0ODhlNzEyNzYxODYwNA; odin_tt=4d81d4ff73e847c4396091c906dc54bdbc0f2bb56e89be4f13a70328dbcd4fd29f8e0e88a3c9d208fcd1424c2cae970e8958d4ca30b86da5d75ef07160b95fb9; sid_guard=5b6abf7a1df603c4d9488e7127618604%7C1658216743%7C5184000%7CSat%2C+17-Sep-2022+07%3A45%3A43+GMT; uid_tt=f4476075bf10eefc6a4b62234f24e89c; uid_tt_ss=f4476075bf10eefc6a4b62234f24e89c; sid_tt=5b6abf7a1df603c4d9488e7127618604; sessionid=5b6abf7a1df603c4d9488e7127618604; sessionid_ss=5b6abf7a1df603c4d9488e7127618604; sid_ucp_v1=1.0.0-KDJkZjliYjYxZWNmNmY0YTNmOWUzNzE3ZTI5NzRkZjM5ZGIyYzIyOGEKHwi-m7Dh1ozxBxCnwtmWBhjvMSAMMMqE25IGOAJA8QcaAmxmIiA1YjZhYmY3YTFkZjYwM2M0ZDk0ODhlNzEyNzYxODYwNA; ssid_ucp_v1=1.0.0-KDJkZjliYjYxZWNmNmY0YTNmOWUzNzE3ZTI5NzRkZjM5ZGIyYzIyOGEKHwi-m7Dh1ozxBxCnwtmWBhjvMSAMMMqE25IGOAJA8QcaAmxmIiA1YjZhYmY3YTFkZjYwM2M0ZDk0ODhlNzEyNzYxODYwNA; THEME_STAY_TIME=%22299833%22; IS_HIDE_THEME_CHANGE=%221%22; douyin.com; strategyABtestKey=1658997193.124; __ac_nonce=062e249cd00cba713a8be; __ac_signature=_02B4Z6wo00f01kO-ZkQAAIDCw7ycBIxrJFpDnmLAAPIcErWTLD307p7uX13DLChl.sbdfrW4dvf5FfUY8RRt5xVXAi9GM74duVR1VI8cI6XazPvdl3mLX08U6.x1rKEkRIT0hzCwGwsqkM2I0d; msToken=pSonkjyhuE6K8eOoEz8HHELu2ton2jzynTTKQ8TobP4dcMKS8yiLE6VHuk6qVuIL6mvaT7zWrkemCAzp1hgNI_n8jow4E-qe0PQI026y-v5nvlizGowGzBI=; msToken=qIz4PwWRrdvfjMbB9cJ3OXh96UEJAN0qvw-J0ev3wqA4zkRCvBNQGHrshGFIMu4LA0-6PyE4GDXlv1-n3V_CSfrQURQBKVftU4aPpqw4mH7N9hTExR7kgLE=; home_can_add_dy_2_desktop=%221%22; tt_scid=W9rIXQVsDQ4PINpOd4bR2dgrfqZGTKE1OrPOJsKfKV6gNoqlIRU9etq-88ZEGwho0aac; download_guide=%224%2F20220728%22",
}


def check_status(url):
    html = requests.get(url,headers=headers)
    if html.status_code == 200:
        get_html(html,url)
    else:
        print(html.status_code)


def get_html(html,url):
    soup = etree.HTML(html.text)
    try:
        data = soup.xpath('//div[@class="kr4MM4DQ"]/span/text()')
        like = data[0]
        pinglun = data[1]
        shoucan = data[2]
    except:
        like = np.NAN
        pinglun = np.NAN
        shoucan = np.NAN

    try:
        title = re.compile('name="description" content="(.*?)"')
        title1 = title.findall(html.text)
        title1 = str(title1).split('-')[0].replace("['","")
        if '来抖音，记录美好生活！' in title1:
            title1 = np.NAN
    except:
        title1 =np.NAN

    try:
        timedate = soup.xpath('//div[@class="JvhAw4hP"]/span/text()')
        timedate = timedate[-1]
    except:
        timedate = np.NAN

    # try:
    #     biaoqian = soup.xpath('//h1[@class="z8_VexPf"]/span[@class="Nu66P_ba"]/span[2]/a/span/text()')
    #     biaoqian = ','.join(biaoqian)
    # except:
    #     biaoqian = np.NAN

    df = pd.DataFrame()
    df['链接'] = [url]
    df['标题+标签'] = [title1]
    df['发布时间'] = [timedate]
    # df['标签'] = [biaoqian]
    df['点赞'] = [like]
    df['评论数'] = [pinglun]
    df['收藏'] = [shoucan]
    df.to_csv('数据.csv', encoding='utf-8-sig', mode='a+', index=None, header=None)

# def note_html(html,url):
#     content = html.text
#     pinglun = re.compile('<div class="yCJWkVDx">(.*?)</div>')
#     pinglun1 = pinglun.findall(content)
#     try:
#         pinglun1 = pinglun1[0]
#     except:
#         pinglun1 =np.NAN
#
#     like = re.compile('<span class="htnqqoaP">(\d+)</span>')
#     like1 = like.findall(content)
#     try:
#         like1 = like1[0]
#     except:
#         like1 = np.NAN


if __name__ == '__main__':
    df = pd.DataFrame()
    df['链接'] = ['链接']
    df['标题'] = ['标题']
    df['发布时间'] = ['发布时间']
    # df['标签'] = ['标签']
    df['点赞'] = ['点赞']
    df['评论数'] = ['评论数']
    df['收藏'] = ['收藏']
    df.to_csv('数据.csv',encoding='utf-8-sig',mode='w',index=None,header=None)
    data = pd.read_excel('抖音快手小红书0728.xlsx')
    data = data[data['站点名称'] == '抖音app'].iloc[0:50]
    for u in tqdm(data['文章地址']):
        if '?schema_type=37' not in u:
            check_status(u)
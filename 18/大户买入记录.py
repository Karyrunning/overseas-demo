import pandas as pd
import requests
from tqdm import tqdm
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "user-token": "1032d37c749846fd6859840e64c9d97c",
    "Origin": "https://www.shipan.hechao.art",
    "Referer": "https://www.shipan.hechao.art/",
    "Host": "api.codeleven.cn",
}

session = requests.session()
session.headers = headers


def get_data():
    url = 'https://api.codeleven.cn/nft-live/server/market-api/index?pageNum=1&pageSize=100&onlyShowHot=true&orderBy=HOT_DESC&platformId=20'
    html = session.get(url)
    content = html.json()
    data = content['data']['records']
    list_id = []
    for c in data:
        list_id.append(c['albumId'])
    get_buy(list_id)


def get_buy(list_id):
    df = pd.DataFrame()
    a = random.uniform(0.5, 1.0)
    for i in tqdm(list_id):
        for j in range(1,3):
            url = 'https://api.codeleven.cn/nft-live/server/market-api/transactionList?platformId=20&pageNum={}&pageSize=20&albumId={}&onlyTop1000=true'.format(j,i)
            html = session.get(url)
            content = html.json()
            data = content['data']['records']
            for d in data:
                buyTime = d['buyTime']
                userWalletId = d['userWalletId']
                itemName = d['itemName']
                df['买入时间'] = [buyTime]
                df['买入id'] = [userWalletId]
                df['物品名称'] = [itemName]
                df.to_csv('购物清单.csv', mode='a+', encoding='utf-8-sig', index=False, header=False)
            time.sleep(a)

if __name__ == '__main__':
    df = pd.DataFrame()
    df['买入时间'] = ['买入时间']
    df['买入id'] = ['买入id']
    df['物品名称'] = ['物品名称']
    df.to_csv('购物清单.csv',mode='w',encoding='utf-8-sig',index=False,header=False)
    get_data()



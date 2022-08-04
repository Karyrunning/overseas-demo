import requests
from lxml import etree
import time
import random
import pandas as pd
import numpy as np
from tqdm import tqdm

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
    "user-agent": random.choice(user_agent),
    'cookie': '_cb=C-f2DWN3ORbBJpyYS; _pubcid=4c4aa4b6-532d-40de-afbd-a63e7c89796e; chsn_cnsnt=www.metacritic.com%3AC0001%2CC0002%2CC0003%2CC0004; tglr_anon_id=ecfc42bb-b748-4dad-86a9-ef3d45614d6b; tglr_tenant_id=src_1kZD6ZLXVCIj0d2XTZb7WONLbaA; s_ecid=MCMID%7C33408398269421397814085829049771396338; cohsn_xs_id=ba0a21be-9b9c-4171-ac99-3ca044ee1053; __utmz=15671338.1656054547.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ctk=NjJiNTYzMTU2OGY5YWRlNDk1NWY2NjFiNzVkNQ%3D%3D; _v__chartbeat3=B1Q8yPpfHZTBVESu1; mc_s_s=a_4; _BB.bs=d|1; __utmc=15671338; __utma=15671338.1121991455.1655198874.1656059184.1659425121.4; _cb_svref=null; _pbjs_userid_consent_data=3524755945110770; AMCVS_3C66570E5FE1A4AB0A495FFC%40AdobeOrg=1; s_cc=true; tglr_sess_id=16b5fe39-6385-4524-af21-ee45901cf46e; tglr_req=https://www.metacritic.com/game/playstation-4/monster-hunter-world; tglr_sess_count=4; aam_uuid=26475820525479062053625628707786644458; _BB.enr=aud_282IAlTMAxCmk8MOYMhEkSR5Nhs%2Caud_2Aqtp0KNJaAjUATKJKFOtBA8WOU%2Caud_287h0BkcvFJEBbYvd1vtTQkRpif%2Caud_27lJRPKUSUzt3PqKf1nGCI2Ng8q%2Caud_27DbjyG2ctvCYDu2rsIRXMgb8fE; dw-tag=main_content; tglr_ref=null; tmpid=1659425302519271; prevPageType=user_reviews; AMCV_3C66570E5FE1A4AB0A495FFC%40AdobeOrg=1585540135%7CMCIDTS%7C19207%7CMCMID%7C33408398269421397814085829049771396338%7CMCAAMLH-1660030103%7C3%7CMCAAMB-1660030103%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1659432503s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; OptanonConsent=isIABGlobal=false&datestamp=Tue+Aug+02+2022+15%3A28%3A52+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.20.0&hosts=&consentId=7b9d0c9a-33c5-4783-b692-4b65855d9d43&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=HK%3BHCW; OptanonAlertBoxClosed=2022-08-02T07:28:52.396Z; _chartbeat2=.1655198874031.1659425332437.0000000000000001.BGZlJWgfGfBCAP_WoDBAZvvDgSS8Z.12; __utmb=15671338.12.10.1659425121; metapv=12; _BB.d=|||12; s_sq=%5B%5BB%5D%5D; utag_main=v_id:0181618a792b00163765d1af6a380506f003406700bd0$_sn:4$_ss:0$_st:1659427133193$vapi_domain:metacritic.com$_pn:12%3Bexp-session$ses_id:1659425121441%3Bexp-session; cto_bundle=rtcaqF9rS1I1bVclMkZZUlpORExaSHk0SW5MZWhLOG9zejUlMkI5V0d5QnFFaCUyRmN3WkQ4TDZlTXN5ak1Kczg0d2R0eHhmdlZPem9xSk4lMkI5Q1BlNmFMS2VudmdaY0UwMzV6NXM1QVJ1cVFNJTJGRkxSTTJQcDJXTzNlOFM0T0dGVVB5ZCUyRnFyWTVJT05yRkdiaVhENTRFN044b2k5M2hIb3clM0QlM0Q; RT="z=1&dm=metacritic.com&si=eced0f9c-5baf-4ae6-8899-12662faf3d5f&ss=l6buvcqy&sl=9&tt=j28&bcn=%2F%2F684d0d47.akstat.io%2F&obo=2&ul=d7u0"',
}


def get_status(url):
    html = requests.get(url,headers=headers)
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)


def get_html(html):
    content = html.text
    soup = etree.HTML(content)
    data = soup.xpath('//div[@class="review_section"]')
    print(len(data))
    for d in data[:-3]:
        try:
            name = d.xpath('./div/div/div/a/text()')
            name = name[0]
        except:
            name = np.NAN
        try:
            timedate = d.xpath('./div/div/div[2]/text()')
            timedate = timedate[0]
        except:
            timedate = np.NAN
        try:
            pingfeng = d.xpath('./div/div[2]/div/text()')
            pingfeng = pingfeng[0]
        except:
            pingfeng = np.NAN
        try:
            comtent1 = d.xpath('./div[2]/span/span/text()')
            comtent2 = d.xpath('./div[@class="review_body"]/span/text()')
            comtent3 = comtent1+comtent2
            comtent4 = ' '.join(comtent3)
            comtent4 = comtent4.replace('\r','').replace('\n','')
        except:
            comtent4 = np.NAN
        # try:
        #     comtent1 = d.xpath('./div[@class="review_body"]/text()')
        #     # comtent2 = d.xpath('./div[@class="review_body"]/span/text()')
        #     # comtent3 = comtent1+comtent2
        #     comtent4 = ' '.join(comtent1)
        #     comtent4 = comtent4.replace('\r','').replace('\n','').strip(' ')
        #     print(comtent4)
        # except:
        #     comtent4 = np.NAN

        df = pd.DataFrame()
        df['发布时间'] = [timedate]
        df['发布作者'] = [name]
        df['评分'] = [pingfeng]
        df['发布内容'] = [comtent4]
        df.to_csv('{}_user_reviews.csv'.format(number), encoding='utf-8-sig', mode='a+', header=False, index=False)

    time.sleep(1)


if __name__ == '__main__':
    df = pd.DataFrame()
    df['发布时间'] = ['发布时间']
    df['发布作者'] = ['发布作者']
    df['评分'] = ['评分']
    df['发布内容'] = ['发布内容']
    number = 3
    df.to_csv('{}_user_reviews.csv'.format(number),encoding='utf-8-sig',mode='w',header=False,index=False)
    for i in tqdm(range(0,5)):
        url = 'https://www.metacritic.com/game/xbox-one/monster-hunter-world/user-reviews?sort-by=date&num_items=100&page={}'.format(i)
        get_status(url)
    # url = 'https://www.metacritic.com/game/playstation-4/monster-hunter-world/critic-reviews'
    # get_status(url)
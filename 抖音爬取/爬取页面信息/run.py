import requests
import execjs

def dy_sign(method,kw=None):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.douyin.com/",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "cookie":cookies
    }
    # TODO 先获取一个有效的 s_v_web_id，替换到 headers的 cookie中，即可进行采集
    # TODO 手动复制的s_v_web_id不可用！  slide_cookie.py文件可以生成s_v_web_id。
    # TODO 有问题就看文章更新，实在找不到就留言、私信或者加群咨询
    if method=='user_info':
        url = f'https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={kw}'
        d = requests.get(url,headers={'User-Agent':headers.get('User-Agent')}).text
        print(url)
        return d

    if method =='comment':
        headers_comment = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookies + '; ttwid=1%7CgrmzurD-QWrAfpvHumhgYZ2ta-b7RVbyedy_qCcyGwE%7C1649930727%7Cd3da0563d05919d66b2224b2189b3992769898e7d9e1d0d2a012f0c4c413e28d',
            'pragma': 'no-cache',
            'referer': 'https://www.douyin.com/discover?modal_id=7084774393322179840',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        url = f'https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={kw}&cursor=0&count=20&item_type=0&rcFT=AAQffZzBg&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=99.0.4844.51&browser_online=true&engine_name=Blink&engine_version=99.0.4844.51&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7086293446633686565'

        return requests.get(url, headers=headers_comment).text

    with open('signature.js','r',encoding='utf-8') as f:
        b = f.read()
    c = execjs.compile(b)
    # sort_type,publish_time = '0','0'
    # offset = 0
    d = c.call(method,kw)
    print(d)
    e = requests.get(d, headers=headers)
    return e.text

#https://www.douyin.com/aweme/v1/web/search/item/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_video_web&sort_type=0&publish_time=0&keyword=%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80&search_source=normal_search&query_correct_type=1&is_filter_search=0&offset=0&count=15&version_code=160100&version_name=16.1.0&cookie_enabled=true&screen_width=1280&screen_height=720&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F91.0.4472.164+Safari%2F537.36&browser_online=true&_signature=_02B4Z6wo00f013h-hDgAAIDAyI9o8JBGuZN4fsCAALzM04
#https://www.douyin.com/aweme/v1/web/search/item/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_video_web&sort_type=2&publish_time=1&keyword=%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80&search_source=normal_search&query_correct_type=1&is_filter_search=0&offset=50&count=15&version_code=160100&version_name=16.1.0&cookie_enabled=true&screen_width=1280&screen_height=720&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F91.0.4472.164+Safari%2F537.36&browser_online=true&_signature=_02B4Z6wo00f019zRU-gAAIDAbCC.IR3Gbrfc0RdAAJX09e

if __name__ == '__main__':
    import json
    cookies = 'THEME_STAY_TIME=%222511%22; __ac_signature=_02B4Z6wo00f01jzVC6wAAIDDF19QaSeU29I89S8AAO34d8; home_can_add_dy_2_desktop=%220%22; ttwid=1%7CdI-0B0iZLpqthlJlPJEblevlqGs-vQPmYbFfQPpg4OE%7C1658801299%7C4025277e460be7bb14f537c3725ddbf0c09e47c7a5b30a2daee777640ff297c0; msToken=OzDUdFVmhEF4PUmReFfG2JrlcD3OsE59FaAiQuHEbIidRnUQ5geS-2u0gaRmzD7j8nAf-7gJz1T2lFTMu4DmeVCH9ZYBUbiFrtsiHUs4TOpF; __ac_nonce=062df4c92004f0e944ce2;'


    # 首页推荐视频
    #print(dy_sign(method='feed'))
    # 搜索视频
    print(dy_sign(method='search_item',kw='王者荣耀'))

    # # 评论  (评论除了s_v_web_id，还可能需要在 headers_comment 中加上ttwid，随便复制一个即可)
    # print(dy_sign(method='comment',kw='6979814126004604192'))

    # 作品
    #print(dy_sign(method='aweme_post',kw='MS4wLjABAAAAIWFmTfNJmRajbViR_rK6iGgQMIq0lAWdFmQ5z6iU9Vd4uo9KXOgcJE0o5Dn0JAmW'))
    # 搜素用户
    #print(dy_sign(method='search_user',kw='北京'))
    # 用户主页
    #print(dy_sign(method='user_info',kw='MS4wLjABAAAAIWFmTfNJmRajbViR_rK6iGgQMIq0lAWdFmQ5z6iU9Vd4uo9KXOgcJE0o5Dn0JAmW'))
    ...

import requests
import json

data = {
    "device_platform": "webapp",
    "aid": 6383,
    "channel": "channel_pc_web",
    "search_channel": "aweme_video_web",
    "sort_type": 2,
    "publish_time": 1,
    "keyword": "王者荣耀",
    "search_source": "tab_search",
    "query_correct_type": 1,
    "is_filter_search": 1,
    "from_group_id": 7118731493156998432,
    "offset": 30,
    "count": 10,
    "search_id": "202207261010380101511962210D67F17D",
    "version_code": 170400,
    "version_name": "17.4.0",
    "cookie_enabled": True,
    "screen_width": 1920,
    "screen_height": 1080,
    "browser_language": "zh-CN",
    "browser_platform": "Win32",
    "browser_name": "Chrome",
    "browser_version": "103.0.0.0",
    "browser_online": True,
    "engine_name": "Blink",
    "engine_version": "103.0.0.0",
    "os_name": "Windows",
    "os_version": 10,
    "cpu_core_num": 8,
    "device_memory": 8,
    "platform": "PC",
    "downlink": 10,
    "effective_type": "4g",
    "round_trip_time": 50,
    "webid": 7121986523742438945,
    "msToken": "yjqUcVxzabLkNoqDpuf0EkMq4KnlS6pGG0GTa_a8iH6KRq4XE-DU8lHQauI6Dil0TUfsrtD0diWyfmvnzBR0uLw2l9WJsdyCOVMhNyHO-zhNhBAKlpbrJzA=",
    "X-Bogus": "DFSzswVujviANHl7SImsWM9WX7je",
    "_signature": "_02B4Z6wo00001SKrP5wAAIDBoqnF3DCBkTUiqzsAACp47RYfqw2B01exp.JS-ExcXLlO2tADs86mNaIf0fZbg5MMVI8Zut.xjkvrZTpoCu5-KbvhmAkd1pJJd6QlLRQN254jBguTDTbuxW8Fa9",
}

cookies = 'THEME_STAY_TIME=%222511%22; __ac_signature=_02B4Z6wo00f01jzVC6wAAIDDF19QaSeU29I89S8AAO34d8; home_can_add_dy_2_desktop=%220%22; ttwid=1%7CdI-0B0iZLpqthlJlPJEblevlqGs-vQPmYbFfQPpg4OE%7C1658801299%7C4025277e460be7bb14f537c3725ddbf0c09e47c7a5b30a2daee777640ff297c0; msToken=OzDUdFVmhEF4PUmReFfG2JrlcD3OsE59FaAiQuHEbIidRnUQ5geS-2u0gaRmzD7j8nAf-7gJz1T2lFTMu4DmeVCH9ZYBUbiFrtsiHUs4TOpF; __ac_nonce=062df4c92004f0e944ce2;'

headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookies + '; ttwid=1%7CgrmzurD-QWrAfpvHumhgYZ2ta-b7RVbyedy_qCcyGwE%7C1649930727%7Cd3da0563d05919d66b2224b2189b3992769898e7d9e1d0d2a012f0c4c413e28d',
            'pragma': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }

url = 'https://www.douyin.com/aweme/v1/web/search/item/'
html = requests.get(url,headers=headers,data=json.dumps(data))
print(html.text)

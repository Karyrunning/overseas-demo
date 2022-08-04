import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "x-algolia-api-key": "aca0d7082e4e63af5ba5917d5e96bed0",
    "x-algolia-application-id": "NKTZZ4AIZU",
}

data = {
    "x-algolia-agent":"Algolia%20for%20JavaScript%20(4.1.0)%3B%20Browser"
}


def check_status(url):
    html = requests.post(url,headers=headers,data=json.dumps(data))
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)


def get_html(html):
    content = html.text
    print(content)


if __name__ == '__main__':
    url = 'https://nktzz4aizu-dsn.algolia.net/1/indexes/prod_discoverable_guilds/query?'
    check_status(url)
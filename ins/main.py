import requests
from lxml import etree

headers ={

    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
}

url = 'https://www.instagram.com/dislyte_official/'
html = requests.get(url,headers=headers)
soup = etree.HTML(html.text)
href = soup.xpath('//div[@class="_aabd _aa8k _aanf"]/a/@href')
print(href)
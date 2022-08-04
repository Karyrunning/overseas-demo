import requests
import pandas as pd


#建立列表，存数据
lst1=[] 
lst2=[]
lst3=[]

#关键字 gaming 、movies 、videos 、aww
key1 = input('请输入第一个关键字:\n')
key2 = input('请输入第二个关键字:\n')
key3 = input('请输入第三个关键字:\n')

proxies = {'http':'127.0.0.1:10809'} #添加代理

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50',
         'Accept': 'application/json, text/javascript, */*; q=0.01',
         'referer': 'https://frontpagemetrics.com/r/gaming'
         }
url='https://frontpagemetrics.com/ajax/compare.reddits'

#josn 参数，自定义输入关键字跟上面的input对应,如果是差2个自己改下data参数即可
data={
      'reddit0':key1,
      'reddit1':key2,
      'reddit2':key3,
      'reddit3':'',
      'reddit4':''
      }

html=requests.post(url=url,headers=headers,data=data,proxies=proxies) #代理

growth=html.json()['message']['growth']['data']

#print(growth)

for a in growth:
    dic1={}
    dic1['y']=a['y']
    dic1['a']=a['a']
    dic1['b']=a['b']
    dic1['c']=a['c']
    lst1.append(dic1)
    
df1=pd.DataFrame(lst1)


total=html.json()['message']['total']['data']

for b in total:
    dic2={}
    dic2['y']=b['y']
    dic2['a']=b['a']
    dic2['b']=b['b']
    dic2['c']=b['c']
    lst2.append(dic2)
    
df2=pd.DataFrame(lst2)

ranks=html.json()['message']['ranks']['data']

for c in ranks:
    dic3={}
    dic3['y']=c['y']
    dic3['a']=c['a']
    dic3['b']=c['b']
    dic3['c']=c['c']
    lst3.append(dic3)
    
df3=pd.DataFrame(lst3)
    
    
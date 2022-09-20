from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# 设置浏览器
options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values' :
        {'notifications' : 2}#禁止谷歌浏览器弹出通知消息
}
options.add_experimental_option('prefs',prefs)

browser = webdriver.Chrome(options=options,executable_path='chromedriver.exe')
browser.maximize_window()#浏览器窗口最大化
browser.implicitly_wait(10)#隐形等待10秒
# 访问facebook网页
try:
    browser.get('https://www.facebook.com/?stype=lo&jlou=Afdn3hJmaqOi6flOLMb1evBGPfT9J9MEBcuV-DZavdZNlhPS2qo-kJFC5CBrd-xE7LVghiIYV6uHO5wAJL0YPReaiEbHNeAmzwpKUCf5HyhAXA&smuh=28702&lh=Ac9qtmp2oSGUyS6o6mo')
    time.sleep(2)
#如果打开facebook页面失败，则尝试重新加载
except:
    browser.find_element_by_id('reload-button').click()
    print('重新刷新页面~')
time.sleep(2)

# 输入账户密码
browser.find_element_by_id('email').clear()
browser.find_element_by_id('email').send_keys('+8613060923171')
browser.find_element_by_id('pass').clear()
browser.find_element_by_id('pass').send_keys('snice960751327')

# 模拟点击登录按钮，两种不同的点击方法
browser.find_element_by_xpath('//button[@name="login"]').send_keys(Keys.ENTER)
time.sleep(3)

#进入到主页面里面
url = 'https://www.facebook.com/search/posts/?q=dislyte&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D'
browser.get(url)#访问用户主页
time.sleep(5)

check_height = browser.execute_script("return document.body.scrollHeight;")
for r in range(20):
    time.sleep(2)
    browser.execute_script("window.scrollBy(0,1500)")


# #下拉滑动条至底部，加载出所有帖子信息
# t = True
# while t:
#     check_height = browser.execute_script("return document.body.scrollHeight;")
#     for r in range(20):
#         time.sleep(2)
#         browser.execute_script("window.scrollBy(0,1500)")
#     check_height1 = browser.execute_script("return document.body.scrollHeight;")
#     if check_height == check_height1:
#         t = False
# time.sleep(20)


# #定位发布日期，找到每篇帖子的超链接
# post_urls = []
# for link in browser.find_elements_by_xpath("//span[starts-with(@id,'jsc_c')]/span[2]/span/a"):
#     url = str(link.get_attribute('href')).split('?')[0]
#     print(url)
#     #注意！！！link.get_attribute('href')返回的一个结果为：
#     #https://www.facebook.com/fan.alice.31/posts/1574509182705311?__cft__[0]=AZWWrKVCLX2teHSF7weZfTtfpdLvUhCwTwZj9eGyviXSYa1OWmlH0MOMt8XeEo0Q0U1LaK2eSor1TEuL5QluW1f8RQPdd0omdAZM8PccCmEoLO-iY9goWjfXZxpnNO4XguQAXRifjmy-U6YZYp6baUxNfnep0cFscw6pczE2NJ72Aw&__tn__=%2CO%2CP-R
#     #其中，只有？前面部分为用户帖子对应的链接，因此，使用了split进行字符串分割
#     post_urls.append(url)
#
# #删除 'https://www.facebook.com/photo/'这类链接
# post_urls = list(set(post_urls))
# for url in post_urls:
#     if url == 'https://www.facebook.com/photo/':
#         post_urls.remove(url)
# print(len(post_urls))

# #依次点击post_urls中的链接，进入用户帖子爬取帖子内容
# post_time = []
# contents = []
# work_url = []
# for url in post_urls:
#     try:
#         browser.get(url)#访问用户帖子
#         ptime = browser.find_element_by_xpath("//span[2]/span/a/span").text
#         content = browser.find_element_by_xpath("//div[@data-ad-preview='message']/div/div/span/div[1]").text
#         if content:
#             post_time.append(ptime)
#             contents.append(content)
#             work_url.append(url)
#     except:
#           print('跳过该链接~')
#     time.sleep(6)
#
# #将获得到的信息写入本地文档
# df=pd.DataFrame({'post_time':post_time,'content':contents,'post_url':work_url})
# df.to_csv('3.csv',encoding='utf-8-sig')
# print('Done!')
# -*- coding: utf-8 -*-
# @UpdataTime : 2022/6/1 16:00
# @Author  : lx

from selenium import webdriver


class Browser():
    def __init__(self, **kwargs, ):
        # TODO： update your executablePath
        executablePath = r"chromedriver.exe"
        self.executablePath = kwargs.get("executablePath", executablePath)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.options = {
            "headless": True,
            "handleSIGINT": True,
            "handleSIGTERM": True,
            "handleSIGHUP": True,
        }
        if self.executablePath is not None:
            self.options["executablePath"] = self.executablePath

        self.browser = webdriver.Chrome(executable_path=self.executablePath, chrome_options=options)
        self.browser.get('https://www.douyin.com')

    def search_item(self, keyword):
        doc = self.browser.execute_script('''
            function queryData(url) {
               var p = new Promise(function(resolve,reject) {
                   var e={
                           "url":"https://www.douyin.com/search/%s?publish_time=1&sort_type=2&source=tab_search&type=video",
                           "method":"GET"
                         };
                    var h = new XMLHttpRequest;
                    h.open(e.method, e.url, true);
                    h.setRequestHeader("accept","application/json, text/plain, */*");  
                    h.setRequestHeader("salute-by","lx");  
                    h.setRequestHeader("content-type","application/json;charset=UTF-8");
                    h.onreadystatechange =function() {
                         if(h.readyState === 4 && h.status  ===200) {
                             resolve(h.responseText);
                         } else {}
                    };
                    h.send(null);
                    });
                    return p;
                }
            var p1 = queryData('lx');
            res = Promise.all([p1]).then(function(result){
                    return result
            })
            return res
        ''' % (keyword))
        return doc

    def close(self):
        self.browser.close()
        self.browser.quit()


# 把URL换成自己的
browser = Browser()
print(browser.search_item('王者荣耀'))
# print(browser.search_item('RPC'))
# print(browser.search_item('案例'))
# print(browser.search_item('教程'))
browser.close()

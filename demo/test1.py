import json
#函数名必须这样写 这是mitmdump规则
def response(flow):
    #下面这个网址是通过fiddler获取到的 但是有些数据我们无法解密，所以需要用mitmdump捕获数据包然后做分析\

    if 'aweme.snssdk.com/aweme/v1/user/profile/other/?' in flow.request.url:
        result=json.loads(flow.response.text)
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print("******************************************************************************")
        print(" ")
        print(result)
        print(" ")
        print("******************************************************************************")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")

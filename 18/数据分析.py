import pandas as pd
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import sys

df = pd.read_csv('购物清单.csv', encoding="utf-8-sig", parse_dates=True, index_col='买入时间')


def before_Hours(hours):
    hours = int(hours)
    t = time.time() - hours*60*60
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
    return t


def main1(x):
    x1 = str(x).split('#')
    return x1[0]


df['物品名称'] = df['物品名称'].apply(main1)
df['买入数量'] = 1

now_time = str(before_Hours(0))
first_3_hours = str(before_Hours(2))

print(now_time)
print(first_3_hours)
df = df[first_3_hours:now_time]
new_df = df.groupby('物品名称').agg('sum')
new_df.sort_values(by='买入数量',inplace=True,ascending=False)
new_df = new_df.drop(['买入id'],axis=1)
new_df = new_df[new_df['买入数量'] > 3]


def text_to_html():
    if len(new_df) > 0:
        #把列表写成HTML语句用于后面发送邮件
        trigger_html_str = ''
        for i,v in zip(list(new_df.index),list(new_df.values)):
            tail_html_str = '''<tr>
                            <td>{}</td>
                            <td>{}</td>               
                            </tr>'''.format(i, v[0])
            trigger_html_str = trigger_html_str + tail_html_str
        return trigger_html_str
    else:
        trigger_html_str = ''
        return trigger_html_str


def send_mail(receiver):
    host_server = 'smtp.qq.com'  # QQ邮箱的SMTP服务器
    sender_qq = '960751327'  # 发件人的QQ号码
    pwd = 'fdrrjmiqqnaubdcj'  # QQ邮箱的授权码
    sender_qq_mail = '960751327@qq.com'  # 发件人邮箱地址

    mail_title = '18大户交易记录'  # 设置邮件标题

    msg = MIMEMultipart('related')
    msg["Subject"] = Header(mail_title, 'utf-8')  # 填写邮件标题
    msg["From"] = sender_qq_mail  # 发送者邮箱地址
    msg["To"] = receiver  # 接收者邮件地址

    table_html_code = '''
        <table width="90%" border="1" cellspacing="0" cellpadding="4"  class="tabtop13">
                    <tr>
                    <th bgcolor="#6633FF" colspan="6" class="btbg titfont" style="color:#fff; font-weight: bold; ">18大户交易记录
                    </tr>
                    <tr class="btbg titfont">
                        <th style='background:#E74C3C'>藏品名称</th>
                        <th style='background:#E74C3C'>购买数量</th>
                    </tr>
                <!-- host -->
            </table>
            <br>'''

    mail_html = open("table.html", "r", encoding="utf-8").read()
    #添加HTML文本内容
    mail_html = mail_html.replace('<!-- imgstart -->', table_html_code)
    #在里面添加表格形式，以表格的形式发送出来
    mail_html = mail_html.replace('<!-- host -->', text_to_html())

    content = MIMEText(mail_html, 'html', 'utf-8')
    msg.attach(content)

    smtp = SMTP_SSL(host_server)  # SSL 登录
    smtp.set_debuglevel(0)  # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.ehlo(host_server)  # 连接服务器
    smtp.login(sender_qq, pwd)  # 邮箱登录

    try:
        smtp.sendmail(sender_qq_mail, receiver, msg.as_string())  # 发送邮件函数
        smtp.quit()  # 发送邮件结束
        print("Successfully Send！")  # 输出成功标志
    except Exception as e:
        print("The sever is busy,please continue later.",e)


if __name__ == '__main__':
    try:
        receiver = sys.argv[1]
    except:
        receiver = '960751327@qq.com'  # 收件人邮箱地址
    try:
        send_mail(receiver)  # 调用函数，发送邮件
    except:
        send_mail(receiver)  # 调用函数，发送邮件



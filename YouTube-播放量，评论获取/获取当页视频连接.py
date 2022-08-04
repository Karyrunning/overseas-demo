import requests
from lxml import etree

url = 'https://www.youtube.com/c/Ubisoft/videos?view=0&sort=dd&flow=grid'


headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        'cookie': 'VISITOR_INFO1_LIVE=RKzCsolgDCo; PREF=tz=Asia.Shanghai; __Secure-3PSID=IggCDOfkt0_YvrRDH-9lGSQbor6o0VHQhsijgQ4gSv7__3n2Rs0EYtZeb1R4fwClxR3K0Q.; __Secure-3PAPISID=bjI6sYyXBcWou2TC/ANlPiGPXDtZw2_zCf; LOGIN_INFO=AFmmF2swRQIgUOkIEPy88ifEtDyB0dnwxxfJt76mIVSAk3b12prs34QCIQD41kthQYAp3YpI6KqMpbtSkik2DyNKhwIbkEk_F-o00A:QUQ3MjNmd3BVZmExUDZ2WmZGN3I0V0dHOVo0QkN0eW9TU3U0ZmVCSC0xSlJWczB0cXdGS2E3ejVrNWNnOUpUUWRQdS1Qcm9nMTNnLU5lbkE0Q1p0TEZaZ1RIOXJIdlRiTE0tZjRXYWVEd2V0SDBOanBnWXhGaGtfVjF6RFlqVjcyZnpKdWxTb29fem9Xck4zaENyeDQwbE1QZXl4MEZkSnBR; YSC=81TJ3_NWjT4; CONSISTENCY=AGDxDeP7498HbtzACaaXCZmEVo5IfvYWPFZHoNj_dc8snXp0-n3tTq1tEoOXp6Dfp3jKfSkiUhgpP70Kf0XvE6gMj3comTlnB7Z0JzxTKiHOfdy9OKp31k1FCz4A3p9M5oO6wCfHI5-4eb-9wqhXKVtn; __Secure-3PSIDCC=AJi4QfH3eAzxlsYFUG-MxtfTavjOM8Um9U6WuyXPjK7Rbz4isixrCiJBjIS9_A-62PH7r5PMHQ',
    }

html = requests.get(url,headers=headers)
print(html.text)

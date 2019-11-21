from bs4 import BeautifulSoup



# with open('test.html') as f:
#     soup = BeautifulSoup(f, features="html.parser")
#     # print(soup.prettify())
#     # print(soup.find_all(find_li_with_getreward))
#     all_li = soup.find_all(attrs={'data-type': 'getreward'})
#     for li in all_li:
#         print(li['data-usertaskid'])
#

import requests

url = 'https://app.qianfanedu.cn/mag/user/v1'
headers = {
    'Referer': 'https://app.qianfanedu.cn/mag/addon/v1/sign/signView?needlogin=1&themecolor=38AEF5',
    'Accept-Language': 'zh-cn',
    'X-Requested-With':	'XMLHttpRequest',
    'Content-Type':	'application/x-www-form-urlencoded',
    'Accept-Encoding':	'br, gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MAGAPPX|4.6.7-4.6.8-19|iOS 12.3.1 iPhone XR|',
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*'
    }

# 登录拿token
r = requests.post(url=url + '/user/login', headers=headers, data={'account': 'dynamite', 'password': 'pgonline', 'auth': ''})
token = (r.json()['data']['token'])
print('领取前积分: ' + str(r.json()['data']['total_score']))

headers['User-Agent'] = headers['User-Agent'] + 'qianfanedu|7EADFE8E-98B7-4A15-922D-888936AA0F2D|63260804096cf9731c345fb92dfe7be9|b7a2090d8d064f4d5e6c2fb445507380|' + token
r2 = requests.get(url=url + '/user/myCenter',headers=headers)
print('最新积分: ' + str(r2.json()['data']['score']))
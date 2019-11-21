import requests
from bs4 import BeautifulSoup

url = 'https://app.qianfanedu.cn/mag/user/v1'
headers = {
    'Referer': 'https://app.qianfanedu.cn/mag/addon/v1/sign/signView?needlogin=1&themecolor=38AEF5',
    'Accept-Language': 'zh-cn',
    'X-Requested-With':	'XMLHttpRequest',
    'Content-Type':	'application/x-www-form-urlencoded',
    'Accept-Encoding':	'br, gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MAGAPPX|4.6.7-4.6.8-19|iOS 13.1.2 iPhone XS|',
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*'
    }

# 登录拿token并显示金币数
r = requests.post(url=url + '/user/login', headers=headers, data={'account': 'dynamite', 'password': 'pgonline', 'auth': ''})
token = (r.json()['data']['token'])
print('领取前积分: ' + str(r.json()['data']['total_score']))

# 获得任务页面
headers['User-Agent'] = headers['User-Agent'] + 'qianfanedu|7EADFE8E-98B7-4A15-922D-888936AA0F2D|63260804096cf9731c345fb92dfe7be9|b7a2090d8d064f4d5e6c2fb445507380|' + token
r1 = requests.get(url=url+'/user/task?needlogin=1&themecolor=38AEF5', headers=headers)

# 取得 usertaskid
soup = BeautifulSoup(r1.text, features="html.parser")
tasks_completed = soup.find_all(attrs={'data-type': 'getreward'})
for li in tasks_completed:
    print(li['data-usertaskid'])

# 领奖
headers['authority'] = 'app.qianfanedu.cn'
headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
if len(tasks_completed) > 0:
    for li in tasks_completed:
        try:
            requests.get(url=url + '/GradeScore/getScoreTaskReward?id=' + str(li['data-usertaskid']), headers=headers)
        except: print('failed to collect coin')
else:
    print('no task completed')

# 显示最新金币数
r2 = requests.get(url=url + '/user/myCenter', headers=headers)
print('最新积分: ' + str(r2.json()['data']['score']))

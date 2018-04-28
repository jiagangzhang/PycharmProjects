import requests
import sys
from send_email import email

url = 'https://api.mymm.cn/api/v1b/search/style'
params = {'cc': 'CHS',
          'pagesize': 200,
          'merchantid': 4250,
          'pageno': 1
          }
address = {
    'jz': 'jiagangzhang@mymm.com',
    'enoch': 'enochzheng@mymm.com'
    }
tmp = {}
output = []

res = requests.get(url, params=params)
if res.status_code != 200:
    print('!!!!!!Error when trying to get response!!!!!!')
    print(res.text)
    sys.exit(0)

# print(r.text)
print('pagesize = %d'%params['pagesize'])
print('total style: ' + str(res.json()['HitsTotal']))
print('total pages: ' + str(res.json()['PageTotal']))
page_num = res.json()['PageTotal']


def check_sku(pagenumber, merchant_id=None):
    """
    go through the result /api/search/style of selected merchant, 
    check if a skuid can be found in different styles
    :param pagenumber: int
    :param merchant_id: int, default is 4250 (strawberry), can input any merchant id
    :return: None
    """
    params['pageno'] = pagenumber
    print('Retrieving page %d' % pagenumber)
    if merchant_id is not None:
        params['merchantid'] = merchant_id
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print('!!!!!!Error when trying to get response for page %d !!!!!!' % pagenumber)
        print(r.text)
        sys.exit(0)

    page_data = r.json()['PageData']
    for style in page_data:
        style_code = style['StyleCode']
        for sku in style['SkuList']:
            sku_id = sku['SkuId']
            if sku_id not in tmp:
                tmp[sku_id] = style_code
            else:
                output.append({sku_id: (tmp[sku_id], style_code)})


def name_to_email(names):
    """
    :param names: a list of short names contained in the address.keys(), non-existing name will be ignored
    :return: a list of email addresses corresponding to the names given
    """
    # emails = []
    # for name in names:
    #     if name in address.keys():
    #         emails.append(address[name])
    #     else:
    #         print('%s is not in the address lists, email won\'t be sent to this user' % name)
    # return emails
    return [address[name] for name in names if name in address.keys()] # list comprehension

for page in range(page_num):
    check_sku(page+1)

# print(tmp)
if len(output) > 0:
    print(output)
    recipients = name_to_email(['jz'])
    email(subject='!! Duplicate sku found !!', recipients=recipients, body='Please check logs')
else:
    print('Congratulations, no duplicate sku!')
    recipients = name_to_email(['jz'])
    email(subject='No duplicate sku', recipients=recipients, body='Congratulations, no duplicate sku!')

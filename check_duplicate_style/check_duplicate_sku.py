import requests
import sys

url = 'https://api.mymm.cn/api/v1b/search/style'
params = {'cc': 'CHS',
          'pagesize': 200,
          'merchantid': 4250,
          'pageno': 1
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


def check_sku(pagenumber):
    params['pageno'] = pagenumber
    print('Retrieving page %d' % pagenumber)
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

for page in range(page_num):
    check_sku(page+1)

# print(tmp)
if len(output) > 0:
    print(output)
else:
    print('Congratulations, no duplicate sku!')

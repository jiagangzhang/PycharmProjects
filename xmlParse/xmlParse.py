import bs4

xml = 'sohoAccount.xml'
with open(xml) as fhand:
    soup = bs4.BeautifulSoup(fhand, 'xml')

# a = soup.find_all('User')
for User in soup.find_all('User'):
    try:
        print(User['Name'] + '\t' + 'Beast' + '\t' + User['FullName'])
    except:
        continue
# print(a[0]['Name'])
# print(len(a))
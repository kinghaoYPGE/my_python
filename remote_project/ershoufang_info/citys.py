import csv
from urllib import request

from bs4 import BeautifulSoup

url = 'https://www.lianjia.com'

# 获取 html
html = request.urlopen(url).read()

bs = BeautifulSoup(html, 'html5lib')

city_tags = bs.find('div', {'class': 'fc-main clear'}).findChildren('a')

with open('citys.csv', 'w') as f:
    writer = csv.writer(f)
    for city_tag in city_tags:
        city_url = u'%s' % city_tag.get('href')
        city_name = u'%s' % city_tag.get_text()

        writer.writerow([city_name, city_url])
        print(city_name, city_url)

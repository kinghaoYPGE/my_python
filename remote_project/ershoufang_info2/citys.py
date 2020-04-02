from urllib import request
from bs4 import BeautifulSoup
import csv


home_url = 'https://www.lianjia.com'

html = request.urlopen(home_url).read()
bs = BeautifulSoup(html, 'html5lib')

citys_tag = bs.find('div', {'class': 'fc-main clear'}).findChildren('a')

#m = map(lambda city_tag: [city_tag.get_text(), city_tag.get('href')], citys_tag)

#d = {tag.get_text(): tag.get('href') for tag in citys_tag}

with open('citys.csv', 'w') as f:
    writer = csv.writer(f)

    for tag in citys_tag:
        writer.writerow((tag.get_text(), tag.get('href')))

    print('done.')

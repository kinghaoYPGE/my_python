import csv
from bs4 import BeautifulSoup
from urllib import request
import re

def gethtml_bs(url):
    html = request.urlopen(url).read()
    if html:
        bs = BeautifulSoup(html, 'html5lib')
    return html, bs

def get_house_dict(house_tag):
    info = house_tag.find('div', {'class': 'houseInfo'}).get_text().split('|')
    title = house_tag.find('div', {'class': 'title'}).get_text()
    #取整数
    price = re.findall(r'\d+', house_tag.find('div', {'class': 'totalPrice'}).span.get_text())[0]
    size = re.findall(r'\d+', info[2].strip())[0]
    block = info[0].strip()
    type = info[1].strip()
    floor_year_info = house_tag.find('div', {'class': 'positionInfo'}).get_text().split('-')[0]
    offset = floor_year_info.index(')')
    floor = floor_year_info[:offset+1]
    year = floor_year_info[offset+1:]
    return {'title': title,
            'price': price,
            'size': size,
            'block': block,
            'type': type,
            'floor': floor,
            'year': year}

def get_house_list(url, page):
    house_page_url = (url + 'pg{0}/').format(page)
    print('===fetch %s...'%house_page_url )
    html, bs = gethtml_bs(house_page_url)
    house_tags = bs.find_all('li', {'class': 'clear'})
    return [get_house_dict(tag) for tag in house_tags]



def house_generator(url):
    """
    由于数据多，用列表会导致内存过大
    """
    page = 1
    while True:
        house_list = get_house_list(url, page)
        if page >= 20:
            break
        yield house_list
        page += 1

    
def house(url):
    gen_obj = house_generator(url)
    if gen_obj:
        print('writing to houses.csv...')
        with open('houses.csv','w') as f:
            writer = csv.writer(f, delimiter='|')
            header = ['title', 'price', 'size', 'block', 'type', 'floor', 'year']
            writer.writerow(header)
            for house_infos in gen_obj:
                """title = house_info.get('title')
                price = house_info.get('price')
                size = house_info.get('size')
                block = house_info.get('block')
                house_type = house_info.get('type')
                writer.writerows([title, price, size, block, house_type])"""
                writer.writerows([[house_info[k] for k in header] for house_info in house_infos])
        print('writing to houses.csv...Done!')




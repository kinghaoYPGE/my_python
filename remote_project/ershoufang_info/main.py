import sys
import csv
from urllib import request
from bs4 import BeautifulSoup
from house_info import house

def get_city_dict():
    """
    获取城市信息
    """
    city_dict = {}

    with open('citys.csv', 'r') as f:
        reader = csv.reader(f)
        for city in reader:
            city_dict[city[0]] = city[1]
    return city_dict

def get_district_dict(url):
    district_dict = {}
    html = request.urlopen(url).read()
    bsobj = BeautifulSoup(html, 'html5lib')
    roles = bsobj.find('div', {'data-role':'ershoufang'}).findChildren('a')

    for role in roles:
        district_url = u'%s'%role.get('href')
        district_name = u'%s'%role.get_text()
        district_dict[district_name] = district_url
    return district_dict

def run():
    city_dict = get_city_dict()

    for city_name in city_dict.keys():
        print(city_name, end=', ')
    print()

    input_city_name = input('请输入城市: ')

    city_url = city_dict.get(input_city_name)
    if city_url:
        print(input_city_name, city_url)
        ershoufang_city_url = city_url+'ershoufang'
        district_dict = get_district_dict(ershoufang_city_url)
        for district in district_dict.keys():
            print(district, end=', ')
        print()
        input_district = input('请输入地区： ')
        district_url = district_dict.get(input_district)
        if not district_url:
            print('请输入正确的地区名！')
            sys.exit()
        house_info_url = city_url + district_url[1:]
        print(house_info_url)
        house(house_info_url)
    else:
        print("请输入正确的城市名！")
        sys.exit()

if __name__ == '__main__':
    run()


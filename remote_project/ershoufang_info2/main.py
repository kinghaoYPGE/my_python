import csv
from urllib import request
from bs4 import BeautifulSoup
from house_info import house, gethtml_bs


def get_city_dict():
    with open ('citys.csv') as f:
        reader = csv.reader(f)
        #print(dict(reader))
        return dict(reader)

def get_area_dict(url):
    html, bs = gethtml_bs(url)
    areas_tag = bs.find('div', {'data-role': 'ershoufang'}).findChildren('a')
    return {tag.get_text(): url[0:-12] + tag.get('href') for tag in areas_tag}

def get_ershoufang_url(url):
    """并不是所有的城市都有二手房功能"""
    html, bs = gethtml_bs(url)
    ershoufang_url = url+'ershoufang/'
    return ershoufang_url if bs.find('a', {'href': ershoufang_url}) else None

def run():
    citys = get_city_dict()
    print(', '.join(citys.keys()))
    print('请输入城市： ')
    input_name = input()
  
    try:
        city_url = citys[input_name]
        print(input_name, city_url)
       
        ershoufang_url = get_ershoufang_url(city_url)
        print(ershoufang_url)
        if ershoufang_url:
            areas = get_area_dict(ershoufang_url)
            print(', '.join(areas.keys()))
            print('请输入地区： ')
            input_area = input()
            area_url = areas[input_area]
            print(input_area, area_url)
            #得到房屋所需信息, 放到houses.csv文件中
            house(area_url)

        else:
            print('该城市尚未开通二手房功能，敬请期待！')

    except KeyError as k:
        print("输入有误！")
        run()
    except:
        raise

if __name__ == '__main__':
    run()
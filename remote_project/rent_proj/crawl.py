from bs4 import BeautifulSoup
import requests
import csv

url = 'http://sh.58.com/pinpaigongyu/pn/{page}/?minprice=2000_3000'

# 已完成的页数
page = 0

# 打开房源文件
csv_file = open('rent.csv', 'w')

csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print('fetch: ', url.format(page=page))
    response = requests.get(url.format(page=page))
    
    html = BeautifulSoup(response.text, 'html.parser')
    house_list = html.select(".list > li")
    

    # 当house_list没有值时结束
    if not house_list:
        break

    for house in house_list:
        house_title = house.select('h2')[0].string
        house_url = 'http://sh.58.com%s'%(house.select('a')[0]['href'])
        house_info_list = house_title.split()
        house_location = house_info_list[1] 
        house_money = house.select('.money > span > b')[0].string

        csv_writer.writerow([house_title, house_location, house_money, house_url])

csv_file.close()

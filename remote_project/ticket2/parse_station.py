import re
import requests

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9058'

resp = requests.get(url, verify=False)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', resp.text)
print(dict(stations))
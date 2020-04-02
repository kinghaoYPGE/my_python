# coding: utf-8
"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2018-07-07
    tickets -dg 成都 南京 2018-07-07

"""
from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable
from colorama import init, Fore

class TrainsCollection:
    header = '车次 车站 时间 历时 一等 二等 高级软卧 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_tranis, available_place, options):
        self.available_tranis = available_tranis
        self.available_place = available_place
        self.options = options

    @property
    def trains(self):
        for raw_train in self.available_tranis:
            raw_train_list = raw_train.split('|')
            train_no = raw_train_list[3]
            initial = train_no[0].lower()
            duration = raw_train_list[10]
            if not self.options or initial in self.options:
                train = [
                    train_no,# train number
                    '\n'.join([Fore.GREEN + self.available_place[raw_train_list[6]] + Fore.RESET,#始发站
                               Fore.RED + self.available_place[raw_train_list[7]] + Fore.RESET]),#终点站
                    '\n'.join([Fore.GREEN + raw_train_list[8] + Fore.RESET,# 发车时间
                               Fore.RED + raw_train_list[9] + Fore.RESET]),# 到站时间
                    duration,#时长
                    raw_train_list[-6] if raw_train_list[-6] else '--',# 一等 
                    raw_train_list[-7] if raw_train_list[-7] else '--',# 二等 
                    raw_train_list[-15] if raw_train_list[-15] else '--',# 高级软卧
                    raw_train_list[-8] if raw_train_list[-8] else '--',#  软卧
                    raw_train_list[-14] if raw_train_list[-14] else '--',#硬卧
                    raw_train_list[-11] if raw_train_list[-11] else '--',#硬座
                    raw_train_list[-9] if raw_train_list[-9] else '--',#无座
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


def cli():
    """command line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']

    url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
    'leftTicketDTO.train_date={0}&leftTicketDTO.from_station={1}'
    '&leftTicketDTO.to_station={2}&purpose_codes=ADULT').format(
        date, from_station, to_station)
    r = requests.get(url, verify=False)
    available_tranis =  r.json()['data']['result']
    available_place = r.json()['data']['map']
    options = ''.join([key for key, value in arguments.items() if value is True])
    TrainsCollection(available_tranis, available_place, options).pretty_print()

if __name__ == '__main__':
    cli()
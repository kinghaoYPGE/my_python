# coding utf-8
"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h, --help 显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2018-01-01
    tickets -d 上海 北京 2018-01-01
"""
from docopt import docopt
from stations import stations, urls
import requests, prettytable
from colorama import init, Fore

class TrainsCollection:
    header = '车次 车站 时间 历时 一等 二等 高级软卧 软卧 硬卧 硬座 无座'.split()

    def __init__(self, trains, place, opts):
        self.trains = trains
        self.place = place
        self.opts = opts

    @property
    def parse_trains(self):
        for train in self.trains:
            train_info = train.split('|')
            train_no = train_info[3]
            #过滤-gdzk选项
            if not self.opts or train_no[0].lower() in self.opts:
                show_info =[
                    train_no,
                    '\n'.join([Fore.BLUE+self.place[train_info[6]]+Fore.RESET, 
                    Fore.GREEN+self.place[train_info[7]]+Fore.RESET]),
                    '\n'.join([Fore.BLUE+train_info[8]+Fore.RESET, 
                    Fore.GREEN+train_info[9]+Fore.RESET]),
                    train_info[10],
                    train_info[-6] if train_info[-6] else '--',
                    train_info[-7] if train_info[-7] else '--',
                    train_info[-15] if train_info[-15] else '--',
                    train_info[-8] if train_info[-8] else '--',
                    train_info[-14] if train_info[-14] else '--',
                    train_info[-11] if train_info[-11] else '--',
                    train_info[-9] if train_info[-9] else '--',
                ]
                yield show_info

    def pretty_print(self):
        pt = prettytable.PrettyTable()
        #pt.__set_field_names(self.header)
        pt._set_field_names(self.header)
        for row in self.parse_trains:
            pt.add_row(row)
        print(pt)

def client():
    """command-line interface"""
    argvs = docopt(__doc__)
    #print(client.__doc__)
    #print(argvs)
    from_station = stations.get(argvs['<from>'])
    to_station = stations.get(argvs['<to>'])
    date = argvs['<date>']
    start_url = urls[0].format(date, from_station, to_station)
    tickets_info = requests.get(start_url).json(encoding='utf-8')
    trains = [u'%s'%i for i in tickets_info['data']['result']]
    #解析trains
    TrainsCollection(trains, {v:k for k,v in stations.items()}, 
    ''.join([k for k, v in argvs.items() if v is True])).pretty_print()
   

if __name__ == '__main__':
    client()
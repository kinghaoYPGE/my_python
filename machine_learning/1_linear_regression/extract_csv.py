import pandas as pd
import re

"""
数据预处理，生成training set
"""


def run():
    df = pd.read_csv('houses.csv', delimiter='|', usecols=([1, 2, 4, 5, 6]))
    df['type'] = df['type'].apply(
        lambda x: int(re.findall('\d+', x)[0]) + int(re.findall('\d+', x)[1]))
    df['floor'] = df['floor'].apply(lambda x: find_number('\d+', x))
    df['year'] = df['year'].apply(lambda x: find_number('\d+', x))
    df.to_csv('training.csv', sep='|')


def find_number(reg, str):
    result = re.findall(reg, str)
    if result:
        return result[0]
    return ''


if __name__ == '__main__':
    run()

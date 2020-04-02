from functools import reduce
from random import choice

from flask import Flask, g, render_template, request
import MySQLdb

# import json

app = Flask(__name__)
app.config.from_pyfile('settings.py')


def connect_db():
    """得到mysql数据库连接"""
    return MySQLdb.connect(app.config['MYSQL_URL'],
                           app.config['MYSQL_USERNAME'],
                           app.config['MYSQL_PASSWORD'],
                           app.config['MYSQL_DATABASE'])


@app.route('/')
def index():
    cursor = g.db.cursor()
    sql = 'select * from user'
    cursor.execute(sql)
    user_table = cursor.fetchall()
    sql = 'select * from anime'
    cursor.execute(sql)
    anime_table = cursor.fetchall()
    sql = 'select * from anime_style'
    cursor.execute(sql)
    anime_style_table = cursor.fetchall()
    sql = 'select * from user_anime'
    cursor.execute(sql)
    user_anime_table = cursor.fetchall()
    all_data = dict(user=user_table,
                    anime=anime_table,
                    anime_style=anime_style_table,
                    user_anime=user_anime_table)

    return render_template('index.html', all_data=all_data)


@app.route('/search')
def search():
    user = request.args.get('user')
    recommend_dict = recommend(user)
    return render_template('search.html', recommend_data=recommend_dict)


# @app.route('/recommend/<user>')
def recommend(user):
    """
    用于实现简单推荐算法
        1. 找到用户喜爱的anime-在user_anime表中
        2. 分析这些anime的类别-在anime_style表中
        3. 找到前三个标签， 从数据库中找到这三个标签下的anime
        4. 展示推荐的anime name, brief
    """
    cur = g.db.cursor()
    sql = 'select anime_id from user_anime where user_id = %s' % user
    cur.execute(sql)
    # 得到user喜欢的anime id 列表
    love_list = [str(row[0]) for row in cur.fetchall()]
    sql = '''select style_id,count(*) 
             from anime_style 
             where anime_id in (%s) 
             group by style_id 
             order by count(*) desc limit 3''' % ','.join(love_list)
    cur.execute(sql)
    style_list = [str(row[0]) for row in cur.fetchall()]

    anime_dict = {}
    for style_id in style_list:
        sql = 'select anime_id from anime_style where style_id = %s' % style_id
        cur.execute(sql)
        anime_list = cur.fetchall()
        anime_dict[style_id] = list(map(lambda row: str(row[0]), anime_list))

    # 对anime_dict的value取交集和去重
    anime_set = set(reduce(lambda x, y: x & y, [set(v) for k, v in anime_dict.items()]))

    recommend_list = list(anime_set)
    while True:
        recommend_anime = choice(recommend_list)
        if recommend_anime not in love_list:
            break

    sql = 'select name, brief from anime where id = %s' % recommend_anime
    cur.execute(sql)
    recommend_anime_info = cur.fetchall()

    return dict(name=recommend_anime_info[0][0], brief=recommend_anime_info[0][1])


@app.before_request
def get_connect():
    g.db = connect_db()


@app.teardown_request
def close_connect(exception):
    g.db.close()
    return exception


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8089')

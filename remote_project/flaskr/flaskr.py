from flask import Flask, g, render_template, session, request, abort, flash, redirect, url_for
import sqlite3
from contextlib import closing  # 可用来初始化sqlite3

# DATABASE = './flaskr.db'
# DEBUG = True
# SECRET_KEY = 'secret key'
# USERNAME = 'admin'
# PASSWORD = 'default'

app = Flask(__name__)

# from_object()方法会把改模块下所有的大写变量加载到flask的config中
# app.config.from_object(__name__)
app.config.from_pyfile('settings.py')


@app.route('/')
def show_blogs():
    """时间倒序"""
    show_sql = 'select title, text from sample_blog order by id desc'
    cur = g.db.execute(show_sql)
    blog_list = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('blog_list.html', blog_list=blog_list)


@app.route('/add', methods=['POST'])
def add_blog():
    """登录用户可以添加条目"""
    if not session.get('logged_in'):
        abort(401)  # 中断请求
    add_sql = 'insert into sample_blog (title, text) VALUES (?, ?)'
    g.db.execute(add_sql, [request.form['title'], request.form['text']])
    g.db.commit()

    # 闪现消息到blog_list.html
    flash('New item was successfully posted!')
    return redirect(url_for('show_blogs'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_blogs'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_blogs'))


def connect_db():
    """连接sqlite3数据库"""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """初始化数据库"""
    with closing(connect_db()) as db:
        # 将sql脚本导入到sqlite3数据库中
        with open('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    """每次请求前连接数据库，并把连接保存在特殊对象'g'中，'g'只能保存一次请求的信息"""
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """请求结束后， 关闭数据库连接"""
    g.db.close()


@app.errorhandler(401)
def handle_401(error):
    return render_template('401.html', error=error), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')

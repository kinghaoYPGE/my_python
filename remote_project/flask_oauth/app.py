import datetime
import os
import random
import time

from flask import Flask, render_template, request, redirect, session, url_for
from flask_pymongo import PyMongo
from settings import MongoConfig
from settings import GitHubConfig as gh
from requests_oauthlib import OAuth2Session

app = Flask(__name__)
app.config.from_object(MongoConfig)
mongo = PyMongo(app)


def get_github_wisdom(page=1, count=10):
    """分页查询"""
    return mongo.db.wilsom.find({}) \
        .sort([('timestamp', -1)]) \
        .skip(count * (page - 1)).limit(count)


def get_page_count(count=10):
    """统计页数"""
    return mongo.db.wilsom.find({}).count() // count + 1


def github_say():
    """拿到token后, 得到相关用户信息"""
    github = OAuth2Session(client_id=gh.client_id, token=session['oauth_token'])
    profile = github.get(gh.user_url).json()
    """拿到用户信息并和留言存入到mongodb中"""
    wisdom_dict = {
        "username": profile["name"],
        "avatar_url": profile["avatar_url"],
        "html_url": profile["html_url"],
        "geek_wisdom": session["geek_wisdom"],
        "datetime": datetime.datetime.today().strftime("%Y/%-m/%d %H:%M"),
        "timestamp": time.time()
    }
    del session['geek_wisdom']
    mongo.db.wilsom.insert(wisdom_dict)


@app.route('/', methods=['POST', 'GET'])
@app.route('/page/<int:page>', methods=['POST', 'GET'])
def index(page=1):
    """
    如果POST请求，进行第三方登陆留言，得到留言列表
    如果GET请求，得到留言列表
    :param page:
    :return:
    """
    if request.method == 'POST':
        # 由于重定向请求，保存留言到session中
        session['geek_wisdom'] = request.form['geek_wisdom']
        try:
            """尝试直接进行留言，没有授权则进行授权操作"""
            github_say()
        except KeyError:
            """进行授权操作"""
            github = OAuth2Session(gh.client_id)
            print('github...')
            authorization_url, state = github.authorization_url(gh.authorization_base_url)
            session['oauth_state'] = state
            return redirect(authorization_url)
    wisdom_list = get_github_wisdom(page=page)
    return render_template('index.html', page=page,
                           wisdom_list=wisdom_list, page_count=get_page_count())


@app.route('/callback')
def callback():
    """得到github的token"""
    github = OAuth2Session(client_id=gh.client_id, state=session['oauth_state'])
    # 得到token
    token = github.fetch_token(gh.token_url, client_secret=gh.client_secret,
                               authorization_response=request.url)
    session['oauth_token'] = token
    github_say()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    # 支持https
    app.run(port=8089, debug=True, ssl_context=('ssl.crt', 'ssl.key',), threaded=True)
    # app.run(port=8089, debug=True)

import datetime
from flask import Flask, session, redirect, url_for, render_template, request, flash, Response
import redis

DEBUG = True
SECRET_KEY = 'secret key'

app = Flask(__name__)
app.config.from_object(__name__)

r = redis.StrictRedis()


@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', user=session['user'])


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['user']:
            session['user'] = request.form['user']
        else:
            flash('Invalid user', message='error')
        return redirect(url_for('home'))
    return '<form action="" method="post">user: <input name="user"></form>'


def event_stream():
    """
    消息生成器
    :return:
    """
    pubsub = r.pubsub()
    # 监听频道
    pubsub.subscribe('chat')
    for message in pubsub.listen():
        print(message['data'])
        # yield 'data: %s\n\n' % str(b'%s' % bytes(message['data']), encoding='utf-8')
        yield 'data: %s\n\n' % bytes(message['data']).decode('utf-8')


@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype='text/event-stream')


@app.route('/post', methods=['POST'])
def post():
    message = request.form['message']
    user = session.get('user', 'anonymous')
    now = datetime.datetime.now().replace(microsecond=0).time()
    r.publish('chat', u'[%s] %s: %s' % (now.isoformat(), user, message))
    return Response(status=204)


if __name__ == '__main__':
    app.run(port=8089)

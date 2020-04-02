from flask import Flask, redirect, render_template, url_for, \
    abort, session, escape, request, make_response

app = Flask(__name__)

# 打开session密钥
app.secret_key = 'kinghao'


@app.route('/home')
def home():
    # return 'This is index'
    # 可以强制中断请求
    abort(404)
    return redirect(url_for('hello', name='Python3 flask'))


@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)


@app.route('/')
def index():
    if 'username' in session:
        return '''Logged in as %s<br>
        <a href="/logout">logout</a>''' % escape(session['username'])

    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录"""
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    """登出"""
    session.pop('username', None)
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    # return render_template('404.html', error=error), 404
    resp = make_response(render_template('404.html', error=error), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)

from flask import Flask, url_for, render_template, request, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello Flask!'


@app.route('/hello/<name>', methods=['GET', 'POST'])
def hello(name):
    # return '%s love Flask!' % name
    return render_template('hello.html', name=name)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return '%d' % post_id


@app.route('/url/<func_name>')
def get_url(func_name):
    return url_for(func_name)


@app.route('/url')
def show_url():
    return '\n'.join([url_for('index'),
                      url_for('hello', name='allen'),
                      url_for('show_post', post_id=23),
                      url_for('static', filename='style.css')])


@app.route('/sum/<int:a>/<int:b>')
def sum_ab(a, b):
    return str(a + b)


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    value = request.args.get('key', '')
    return request.method + username + value


@app.route('/file/upload', method='POST')
def file_upload():
    if request.method == 'GET':
        return None
    f = request.files['the_file']
    f.save('./uploads/'+f.filename)
    return 'success'


@app.route('/cookies/get')
def get_cookie():
    # 取cookie
    username = request.cookies.get('username')
    return username


@app.route('/cookies/put')
def put_cookie():
    # 存cookie
    resp = make_response(render_template('hello.html'))
    resp.set_cookie('username', 'kinghao')
    return resp


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8000', debug=True)

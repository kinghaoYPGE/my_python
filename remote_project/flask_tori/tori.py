import os

import json

import argparse
from flask import Flask, render_template, g, abort, request
import rethinkdb as r
from flask.json import jsonify

RDB_HOST = os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
TODO_DB = 'todoapp'
DEBUG = True


def db_setup():
    """
    连接rethinkDB数据库并初始化数据库
    :return:
    """
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(TODO_DB).run(connection)
        r.db(TODO_DB).table_create('todos').run(connection)
        print('Database setup completed. Now run the app without --setup.')
    except r.RqlRuntimeError:
        print('Database already exists. Now run the app without --setup.')
    finally:
        connection.close()


app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def get_db_conn():
    """
    请求之前得到RethinkDB的连接
    :return:
    """
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=TODO_DB)
    except r.RqlDriverError:
        abort(503, 'No database connection could be established.')


@app.teardown_request
def close_conn(exception):
    try:
        g.rdb_conn.close()
    except AttributeError as e:
        pass


@app.route('/todos')
def get_todos():
    """
    返回json格式的todo list
    :return:
    """
    todo_list = list(r.table('todos').run(g.rdb_conn))
    return json.dumps(todo_list)


@app.route('/todos', methods=['POST'])
def new_todo():
    """
    创建一个todo
    :return:
    """
    inserted = r.table('todos').insert(request.json).run(g.rdb_conn)
    return jsonify(id=inserted['generated_keys'][0])


@app.route('/todos/<todo_id>')
def get_todo(todo_id):
    """
    得到todo信息
    :param todo_id:
    :return:
    """
    todo = r.table('todos').get(todo_id).run(g.rdb_conn)
    return json.dumps(todo)


@app.route('/todos/<todo_id>', methods=['PUT', 'PATCH'])
def update_todo(todo_id):
    """
    修改todo
    :param todo_id:
    :return:
    """
    if request.method == 'PUT':
        """
        替换修改
        """
        return jsonify(r.table('todos').get(todo_id).replace(request.json).run(g.rdb_conn))
    if request.method == 'PATCH':
        """
        合并修改
        """
        return jsonify(r.table('todos').get(todo_id).update(request.json).run(g.rdb_conn))


@app.route('/todos/<todo_id>', methods=['DELETE'])
def del_todo(todo_id):
    return jsonify(r.table('todos').get(todo_id).delete().run(g.rdb.conn))


@app.route('/')
def index():
    return render_template('todo.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask todo app')
    parser.add_argument('--setup', dest='run_setup', action='store_true')
    args = parser.parse_args()
    if args.run_setup:
        db_setup()
    else:
        app.run(port=8089)

#! /usr/bin/env python
# encoding: utf-8
from flask import Blueprint, request, current_app, render_template, \
    url_for, jsonify, redirect
from flask_login import login_user, logout_user
from sqlalchemy import or_

from ..dbs import db
from ..user import User

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/signup', methods=['POST'])
def signup_user():
    try:
        user = User.query.filter(
            or_(User.name == request.form['name'], User.email == request.form['email'])).first()
        if user:
            return jsonify(status='error', info=u'已存在该用户')
        user = User()
        user.name = request.form['name']
        user.email = request.form['email']
        user.set_password(request.form['password'])

        # 存入到数据库
        db.session.add(user)
        db.session.commit()
        return jsonify(status='success', info=u'创建用户成功')
    except Exception as e:
        current_app.logger.error(e)
        return render_template(url_for('qa.index'))


@user.route('/login', methods=['POST'])
def login_users():
    try:
        user = User.query.filter(User.name == request.form['name']).first()
        if user:
            if user.verify_password(request.form['password']):
                login_user(user)
        return redirect(url_for('qa.index'))
    except Exception as e:
        current_app.logger.error(e)
        return redirect(url_for('qa.index'))


@user.route('/logout')
def logout_users():
    logout_user()
    return redirect(url_for('qa.index'))

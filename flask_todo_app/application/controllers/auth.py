from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user
from application.forms import *
import application.models as Models

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_by_email = Models.User.objects(email=form.email_or_username.data).first()
        user_by_name = Models.User.objects(username=form.email_or_username.data).first()

        if user_by_email and user_by_email.verify_password(form.password.data):
            login_user(user_by_email)
        elif user_by_name and user_by_name.verify_password(form.password.data):
            login_user(user_by_name)
        else:
            flash(message='Invalid Email/Username or Password!', category='error')
            return redirect(url_for('auth.login'))
        return redirect(url_for('todo.index'))
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 处理表单数据(面向对象方式)-flask_wtf: 处理表单
    form = RegisterForm()
    if form.validate_on_submit():
        user = Models.User(
            username=form.username.data,
            email=form.email.data
        ).save()
        user.password = form.password.data
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('todo.index'))

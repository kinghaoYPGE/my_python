#! /usr/bin/env python
# encoding: utf-8


class FlaskConfig(object):
    # session密钥
    SECRET_KEY = 'secret key'
    # 配置数据库,账号,密码，url,database
    SQLALCHEMY_DATABASE_URI = "mysql://qa:qa@localhost/qa"

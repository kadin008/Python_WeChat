# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-05
IDE: PyCharm
Introduction: 
"""
SERVER_PORT = 8099
DEBUG = False
SQLALCHEMY_ECHO = False
AUTH_COOKIE_NAME = 'mooc_food'

IGNORE_UERL = [
    '^/user/login'
]
IGNORE_CHECK_LOGIN_URLS = [
    '^/static',
    '^/favicon.ico'
]
PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    '1': '正常',
    '0': '已删除'
}



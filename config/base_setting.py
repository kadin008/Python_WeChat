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
    '^/user/login',
    '^/api'
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


MINA_APP = {
    'appid': 'wx24caabd564709caa',
    'appkey': '1420972ba3964031f59a646dd8b77eba'
}


UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}


APP = {
    # 'domain': 'http://192.168.2.99:8090'
    'domain': 'http://wx.aipic.net.cn:8090'
}



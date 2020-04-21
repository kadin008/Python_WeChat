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

IGNORE_URLS = [
    '^/user/login',
]

IGNORE_CHECK_LOGIN_URLS = [
    '^/static',
    '^/favicon.ico'
]

API_IGNORE_URLS = [
    '^/api'
]

PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    '1': '正常',
    '0': '已删除'
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0": "订单关闭",
    "1": "支付成功",
    "-8": "待支付",
    "-7": "待发货",
    "-6": "待确认",
    "-5": "待评价"
}

MINA_APP = {
    'app_id': 'wx24caabd564709caa',
    'app_key': '1420972ba3964031f59a646dd8b77eba',
    'pay_key': '',
    'mch_id': '',
    'callback_url': '/api/order/callback'
}


UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}






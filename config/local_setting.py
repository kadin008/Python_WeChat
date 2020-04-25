# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-05
IDE: PyCharm
Introduction: 
"""
db_username = 'kadin208'
db_password = 'A100s200'
db_server = 'rdsv148e9hymz8rj85wqo.mysql.rds.aliyuncs.com'
db_name = 'food_db'
DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://' + db_username + ':' + db_password + "@" + db_server + "/" + db_name
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = 'utf8mb4'

APP = {
    'domain': 'http://192.168.2.99:8090'
}

MINA_APP = {
    'app_id': 'wx24caabd564709caa',
    'app_key': '1420972ba3964031f59a646dd8b77eba',
    'pay_key': '',
    'mch_id': '',
    'callback_url': '/api/order/callback2'
}

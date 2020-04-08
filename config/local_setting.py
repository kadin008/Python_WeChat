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
SERVER_PORT = 8090
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://' + db_username + ':' + db_password + "@" + db_server + "/" + db_name
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = 'utf8mb4'


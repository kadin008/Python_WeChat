# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-06
IDE: PyCharm
Introduction: 
"""
from flask import Blueprint, send_from_directory
from application import app

route_static = Blueprint('static', __name__)


@route_static.route('/<path:filename>')
def index(filename):
    # app.logger.info(filename)
    return send_from_directory(app.root_path + '/web/static/', filename)







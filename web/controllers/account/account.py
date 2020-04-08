# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-06
IDE: PyCharm
Introduction: 
"""
from flask import Blueprint
from common.libs.helper import ops_render


route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def index():
    return ops_render('account/index.html')


@route_account.route('/info')
def info():
    return ops_render('account/info.html')


@route_account.route('/set')
def set():
    return ops_render('account/set.html')







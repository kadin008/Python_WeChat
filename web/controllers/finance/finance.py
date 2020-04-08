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

route_finance = Blueprint('finance_page', __name__)


@route_finance.route('/index')
def index():
    return ops_render('finance/index.html')


@route_finance.route('/pay-info')
def payInfo():
    return ops_render('finance/pay_info.html')


@route_finance.route('/account')
def account():
    return ops_render('finance/account.html')




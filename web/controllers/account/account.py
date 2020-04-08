# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-06
IDE: PyCharm
Introduction: 
"""
from application import app, db
from flask import Blueprint, request
from common.libs.helper import ops_render, iPagination
from common.models.user import User


route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def index():
    resp_data = {}
    req = request.values
    page = int(req['page']) if ('page' in req and req['page']) else 1
    query = User.query

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': '/account/index'
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    List = query.order_by(User.uid.desc()).all()[offset:limit]
    resp_data['list'] = List
    resp_data['pages'] = pages
    return ops_render('account/index.html', resp_data)


@route_account.route('/info')
def info():
    return ops_render('account/info.html')


@route_account.route('/set')
def set():
    return ops_render('account/set.html')







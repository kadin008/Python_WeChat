# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-06
IDE: PyCharm
Introduction: 
"""
from application import app, db
from flask import Blueprint, request, redirect, jsonify
from sqlalchemy import or_
from common.libs.helper import ops_render, iPagination, getCurrentDate
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.user import User
from common.models.log.app_access_log import AppAccessLog


route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = User.query

    if 'mix_kw' in req:
        rule = or_(
            User.nickname.like('%{0}%'.format(req['mix_kw'])),
            User.mobile.like('%{0}%'.format(req['mix_kw']))
        )
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace('&p={}'.format(page), '')
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    List = query.order_by(User.uid.desc()).all()[offset:limit]
    resp_data['list'] = List
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render('account/index.html', resp_data)


@route_account.route('/info')
def info():
    resp_data = {}
    req = request.args
    reback_url = UrlManager.buildUrl('/account/index')
    uid = int(req.get('id', 0))
    if uid < 1:
        return redirect(reback_url)

    info = User.query.filter_by(uid=uid).first()
    if not info:
        return redirect(reback_url)

    access_list = AppAccessLog.query.filter_by(uid=uid).order_by(AppAccessLog.id.desc()).limit(10).all()
    resp_data['info'] =info
    resp_data['access_list'] = access_list
    return ops_render('account/info.html', resp_data)


@route_account.route('/set', methods=['GET', 'POST'])
def set():
    default_pwd = '********'
    if request.method == 'GET':
        resp_data = {}
        req = request.args
        uid = int(req.get('id', 0))
        info = None
        if uid:
            info = User.query.filter_by(uid=uid).first()
        resp_data['info'] = info
        return ops_render('account/set.html', resp_data)

    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else None
    email = req['email'] if 'email' in req else None
    mobile = req['mobile'] if 'mobile' in req else None
    login_name = req['login_name'] if 'login_name' in req else None
    login_pwd = req['login_pwd'] if 'login_pwd' in req else None

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入昵称'
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入邮箱'
        return jsonify(resp)

    if mobile is None or len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入昵称'
        return jsonify(resp)

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入登录的用户名'
        return jsonify(resp)

    if login_pwd is None or len(login_pwd) < 8:
        resp['code'] = -1
        resp['msg'] = '请输入密码'
        return jsonify(resp)

    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = '用户已存在！'
        return jsonify(resp)

    User_info = User.query.filter_by(uid=id).first()
    if User_info:
        model_user = User_info
    else:
        model_user = User()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.geneSalt()

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    if login_pwd != default_pwd:
        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
    model_user.updated_time = getCurrentDate()

    db.session.add(model_user)
    db.session.commit()
    return jsonify(resp)


@route_account.route('/ops', methods=['POST'])
def ops():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = '操作失败！请联系关联员'
        return jsonify(resp)

    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = '操作失败！请联系关联员'
        return jsonify(resp)

    User_info = User.query.filter_by(uid=id).first()
    if not User_info:
        resp['code'] = -1
        resp['msg'] = '操作失败！请联系关联员'
        return jsonify(resp)

    if act == 'remove':
        User_info.status = 0
    elif act == 'recover':
        User_info.status = 1
    User_info.updated_time = getCurrentDate()
    db.session.add(User_info)
    db.session.commit()

    return jsonify(resp)







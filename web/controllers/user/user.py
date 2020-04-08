# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-06
IDE: PyCharm
Introduction: 
"""
import json
from flask import Blueprint, request, jsonify, make_response, redirect, g
from application import app
from common.models.user import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.libs.helper import ops_render

route_user = Blueprint('user_page', __name__)


@route_user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if g.current_user:
            return redirect(UrlManager.buildUrl("/"))
        return ops_render('user/login.html')

    resp = {'code': 200, 'msg': '登录成功', 'data': {}}
    req = request.values
    app.logger.info(req)
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '用户名不能为空！'
        return jsonify(resp)

    if login_pwd is None or len(login_pwd) < 1:
        resp['code'] = -1
        resp['msg'] = '密码不能为空！'
        return jsonify(resp)

    user_info = User.query.filter_by(login_name=login_name).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = '用名或密码不正确！'
        return jsonify(resp)

    if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = '用名或密码不正确！'
        return jsonify(resp)

    response = make_response(json.dumps(resp))
    response.set_cookie(
        app.config['AUTH_COOKIE_NAME'], '%s#%s' % (
            UserService.geneAuthCode(user_info), user_info.uid),  60 * 60 * 24 * 120
    )

    return response


@route_user.route('/edit')
def edit():
    return ops_render('user/edit.html')


@route_user.route('/reset-pwd')
def resetPwd():
    return ops_render('user/reset_pwd.html')


@route_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response


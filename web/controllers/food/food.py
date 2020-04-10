# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-06
IDE: PyCharm
Introduction: 
"""
from application import app, db
from flask import Blueprint, request, jsonify
from common.models.food.food_cat import FoodCat
from common.libs.helper import ops_render, getCurrentDate

route_food = Blueprint('food_page', __name__)


@route_food.route('/index')
def index():
    return ops_render('food/index.html')


@route_food.route('/info')
def info():
    return ops_render('food/info.html')


@route_food.route('/set')
def set():
    return ops_render('food/set.html')


@route_food.route('/cat')
def cat():
    resp_data = {}
    req = request.values
    query = FoodCat.query

    if 'status' in req and int(req['status']) > -1:
        query = query.fulter(FoodCat.status == int(req['status']))

    List = query.order_by(FoodCat.weight.desc(), FoodCat.id.desc()).all()
    resp_data['list'] = List
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'cat'
    return ops_render('food/cat.html', resp_data)


@route_food.route('/cat-set', methods=['GET', 'POST'])
def catSet():
    if request.method == 'GET':
        resp_data = {}
        req = request.args
        id = int(req.get('id', 0))
        info = None
        if id:
            info = FoodCat.query.filter_by(id=id).first()
        resp_data['info'] = info
        resp_data['current'] = 'cat'
        return ops_render('food/cat_set.html', resp_data)

    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    name = req['name'] if 'name' in req else ''
    weight = int(req['weight']) if ('weight' in req and int(req['weight']) > 0)else 1

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入邮箱'
        return jsonify(resp)

    food_cat_info = FoodCat.query.filter_by(id=id).first()
    if food_cat_info:
        model_food_cat = food_cat_info

    else:
        model_food_cat = FoodCat
        model_food_cat.created_time = getCurrentDate()

    model_food_cat.name = name
    model_food_cat.weight = weight
    model_food_cat.updated_time = getCurrentDate()
    db.session.add(model_food_cat)
    db.session.commit()
    return jsonify(resp)


@route_food.route('/cat-ops', methods=['POST'])
def catOps():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''

    if not id:
        resp['code'] = -1
        resp['msg'] = '为获取到ID'
        return jsonify(req)

    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = '操作有误，请重试'
        return jsonify(req)

    food_info = FoodCat.query.filter_by(id=id).first()
    if not food_info:
        resp['code'] = -1
        resp['msg'] = '未查询到该会员，请核实后在操作'
        return jsonify(req)

    if act == 'remove':
        food_info.status = 0
    elif act == 'recover':
        food_info.status = 1

    food_info.updated_time = getCurrentDate()
    db.session.add(food_info)
    db.session.commit()

    return jsonify(resp)






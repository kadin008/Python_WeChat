# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-13
IDE: PyCharm
Introduction: 
"""
from application import db
from flask import request, jsonify
from sqlalchemy import or_
from web.controllers.api import route_api
from common.models.food.food import Food
from common.models.food.food_cat import FoodCat
from common.libs.helper import getCurrentDate
from common.libs.member.MemberService import MemberService
from common.libs.UrlManager import UrlManager


@route_api.route('/food/index')
def FoodIndex():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    cat_list = FoodCat.query.filter_by(status=1).order_by(FoodCat.weight.desc()).all()
    data_cat_list = []
    data_cat_list.append({
        'id': 0,
        'name': '全部'
    })

    if cat_list:
        for item in cat_list:
            tmp_data = {
                'id': item.id,
                'name': item.name
            }
            data_cat_list.append(tmp_data)
    resp['data']['cat_list'] = data_cat_list

    food_list = Food.query.filter_by(status=1).order_by(Food.total_count.desc(), Food.id.desc()).limit(3).all()
    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)
    resp['data']['banner_list'] = data_food_list

    return jsonify(resp)


@route_api.route('/food/search')
def FoodSearch():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    cat_id = int(req['cat_id']) if 'cat_id' in req else 0
    mix_kw = str(req['mix_kw']) if 'mix_kw' in req else ''
    query = Food.query.filter_by(status=1)

    if cat_id > 0:
        query = query.filter(Food.cat_id == cat_id)

    if 'mix_kw' in req:
        rule = or_(Food.name.like('%{0}%'.format(mix_kw)), Food.tags.like('%{0}%'.format(mix_kw)))
        query = query.filter(rule)

    food_list = query.order_by(Food.total_count.desc(), Food.id.desc()).limit(10).all()

    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'name': item.name,
                'price': str(item.price),
                'min_price': str(item.price),
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)
    resp['data']['list'] = data_food_list
    return jsonify(resp)

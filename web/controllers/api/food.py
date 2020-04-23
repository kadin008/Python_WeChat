# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-13
IDE: PyCharm
Introduction: 
"""
from flask import request, jsonify, g
from sqlalchemy import or_
from web.controllers.api import route_api
from common.models.food.food import Food
from common.models.food.food_cat import FoodCat
from common.models.member.member import Member
from common.models.member.member_cart import MemberCart
from common.models.member.member_comments import MemberComment
from common.libs.UrlManager import UrlManager
from common.libs.helper import getDicFilterField, selectFilterObj


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
    p = int(req['p']) if 'p' in req else 1
    if p < 1:
        p = 1
    query = Food.query.filter_by(status=1)

    page_size = 10
    offset = (p - 1) * page_size
    if cat_id > 0:
        query = query.filter(Food.cat_id == cat_id)

    if mix_kw:
        rule = or_(Food.name.like('%{0}%'.format(mix_kw)), Food.tags.like('%{0}%'.format(mix_kw)))
        query = query.filter(rule)

    food_list = query.order_by(Food.total_count.desc(), Food.id.desc()).offset(offset).limit(page_size).all()

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
    resp['data']['has_more'] = 0 if len(data_food_list) < page_size else 1
    return jsonify(resp)


@route_api.route('/food/info')
def FoodInfo():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0
    food_info = Food.query.filter_by(id=id).first()
    if not food_info or not food_info.status:
        resp['code'] = -1
        resp['msg'] = '已下架'
        return jsonify(resp)

    member_info = g.member_info
    cart_number = 0
    if member_info:
        cart_number = MemberCart.query.filter_by(member_id=member_info.id).count()

    resp['data']['info'] = {
        'id': food_info.id,
        'name': food_info.name,
        'summary': food_info.summary,
        'total_count': food_info.total_count,
        'comment_count': food_info.comment_count,
        'stock': food_info.stock,
        'price': str(food_info.price),
        'main_image': UrlManager.buildImageUrl(food_info.main_image),
        'pics': [UrlManager.buildImageUrl(food_info.main_image), UrlManager.buildImageUrl(food_info.main_image)]
    }
    resp['data']['cart_number'] = cart_number
    return jsonify(resp)


@route_api.route('/food/comment', methods=['POST'])
def FoodComments():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0

    query = MemberComment.query.filter(MemberComment.food_ids.ilike(',{0},'.format(id)))
    List = query.order_by(MemberComment.id.desc()).limit(5).all()
    data_list = []
    if List:
        member_map = getDicFilterField(Member, Member.id, 'id', selectFilterObj(List, 'member_id'))
        for item in List:
            if item.member_id not in member_map:
                continue
            tmp_member_info = member_map[item.member_id]
            tmp_data = {
                'score': item.score_desc,
                'date': item.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                'content': item.content,
                'user': {
                    'nickname': tmp_member_info.nickname,
                    'avatar_url': tmp_member_info.avatar
                }
            }
            data_list.append(tmp_data)
    resp['data']['list'] = data_list
    resp['data']['count'] = query.count()

    return jsonify(resp)







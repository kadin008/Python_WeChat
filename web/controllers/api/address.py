# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-23
IDE: PyCharm
Introduction: 
"""
from application import app, db
from flask import g, jsonify, request
from web.controllers.api import route_api
from common.models.member.member_address import MemberAddress
from common.libs.helper import getCurrentDate


# 添加收获地址
@route_api.route('/my/address/set', methods=['POST'])
def myAddSet():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    member_info = g.member_info
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    address = req['address'] if 'address' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''

    province_id = int(req['province_id']) if ('province_id' in req and req['province_id']) else 0
    province_str = req['province_str'] if 'province_str' in req else ''

    city_id = int(req['city_id']) if ('city_id' in req and req['city_id']) else 0
    city_str = req['city_str'] if 'city_str' in req else ''

    district_id = int(req['district_id']) if ('district_id' in req and req['district_id']) else 0
    district_str = req['district_str'] if 'district_str' in req else ''

    if not nickname:
        resp['code'] = -1
        resp['msg'] = '请填写联系人姓名'
        return jsonify(resp)

    if not mobile:
        resp['code'] = -1
        resp['msg'] = '请填写联系人的手机号'
        return jsonify(resp)

    if not address:
        resp['code'] = -1
        resp['msg'] = '请输入详细地址'
        return jsonify(resp)

    if province_id < 1:
        resp['code'] = -1
        resp['msg'] = '请选择省份'
        return jsonify(resp)

    if city_id < 1:
        resp['code'] = -1
        resp['msg'] = '请选择省份'
        return jsonify(resp)

    if city_id < 1:
        district_str = ''

    default_address_count = MemberAddress.query.filter_by(is_default=1, member_id=member_info.id, status=1).count()
    model_address = MemberAddress()
    model_address.member_id = member_info.id
    model_address.is_default = 1 if default_address_count == 0 else 0
    model_address.created_time = getCurrentDate()
    model_address.nickname = nickname
    model_address.mobile = mobile
    model_address.address = address
    model_address.province_id = province_id
    model_address.province_str = province_str
    model_address.city_id = city_id
    model_address.city_str = city_str
    model_address.area_id = district_id
    model_address.area_str = district_str if district_str == '请选择' else ''
    model_address.updated_time = getCurrentDate()
    db.session.add(model_address)
    db.session.commit()
    return jsonify(resp)















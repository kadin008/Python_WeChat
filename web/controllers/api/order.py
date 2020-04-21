# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-19
IDE: PyCharm
Introduction: 
"""
import json, decimal
from application import app, db
from web.controllers.api import route_api
from flask import request, jsonify, g
from common.models.food.food import Food
from common.models.pay.pay_order import PayOrder
from common.models.member.oauth_member_bind import OauthMemberBind
from common.libs.UrlManager import UrlManager
from common.libs.pay.PayService import PayService
from common.libs.member.CartService import CartService
from common.libs.pay.WeChatService import WeChatSefvice
from common.libs.helper import getCurrentDate


@route_api.route('/order/info', methods=['POST'])
def orderInfo():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    params_goods = req['goods'] if 'goods' in req else None
    member_info = g.member_info
    params_goods_list = []
    if params_goods:
        params_goods_list = json.loads(params_goods)

    food_dic = {}
    for item in params_goods_list:
        food_dic[item['id']] = item['number']

    food_ids = food_dic.keys()
    food_list = Food.query.filter(Food.id.in_(food_ids)).all()

    data_food_list = []
    yun_price = pay_price = decimal.Decimal(0.00)
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'name': item.name,
                'price': str(item.price),
                'pic_url': UrlManager.buildImageUrl(item.main_image),
                'number': food_dic[item.id],
            }
            pay_price = pay_price + item.price * int(food_dic[item.id])
            data_food_list.append(tmp_data)

    default_address = {
        'name': "编程浪子",
        'mobile': "12345678901",
        'address': "上海市浦东新区XX",
    }

    resp['data']['food_list'] = data_food_list
    resp['data']['pay_price'] = str(pay_price)
    resp['data']['yun_price'] = str(yun_price)
    resp['data']['total_price'] = str(pay_price + yun_price)
    resp['data']['default_address'] = default_address

    return jsonify(resp)


@route_api.route('/order/create', methods=['POST'])
def orderCreate():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    type = req['type'] if 'type' in req else None
    params_goods = req['goods'] if 'goods' in req else None

    items = []
    if params_goods:
        items = json.loads(params_goods)

    if len(items) < 1:
        resp['code'] = -1
        resp['msg'] = '请选择商品'
        return jsonify(resp)

    member_info = g.member_info
    target = PayService()
    params = {}
    resp = target.createOrder(member_info.id, items, params)

    if resp['code'] == 200 and type == 'cart':
        CartService.deleteItem(member_info.id, items)

    return jsonify(resp)


@route_api.route('/order/pay', methods=['POST'])
def orderPay():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    member_info = g.member_info
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = '系统繁忙，请稍后再试'
        return jsonify(resp)

    oauth_bind_info = OauthMemberBind.query.filter_by(member_id=member_info.id).first()
    if not oauth_bind_info:
        resp['code'] = -1
        resp['msg'] = '系统繁忙，请稍后再试'
        return jsonify(resp)

    config_mina = app.config['MINA_APP']
    notify_url = app.config['APP']['domain'] + config_mina['callback_url']
    target_wechat = WeChatSefvice(merchant_key=config_mina['pay_key'])
    data = {
        'appid': config_mina['app_id'],
        'mch_id': config_mina['mch_id'],
        'nonce_srt': target_wechat.get_nonce_str(),
        'body': '订餐',
        'out_trade_no': pay_order_info.order_sn,
        'total_fee': int(pay_order_info.total_price * 100),
        'notify_url': notify_url,
        'trade_type': 'JSAPI',
        'openid': oauth_bind_info.openid
    }

    pay_info = target_wechat.get_pay_info(data)
    pay_order_info.prepay_id = pay_info['prepay_id']

    db.session.add(pay_order_info)
    db.session.commit()

    resp['data']['pay_info'] = pay_info

    return jsonify(resp)


@route_api.route('/order/callback', methods=['POST'])
def orderCallback():
    result_data = {
        'return_code': 'SUCCESS',
        'return_msg': 'OK'
    }

    header = {'Content-Type': 'application/xml'}

    config_mina = app.config['MINA_APP']
    target_weChat = WeChatSefvice(merchant_key=config_mina['paykey'])
    callback_data = target_weChat.xml_to_dict(request.data)
    app.logger.info(callback_data)
    sign = callback_data['sign']
    callback_data.pop('sign')
    gene_sign = target_weChat.create_sign(callback_data)
    app.logger.info(gene_sign)
    if sign != gene_sign:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_weChat.dict_to_xml(result_data), header

    order_sn = callback_data['out_trade_no']
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_weChat.dict_to_xml(result_data), header

    if int(pay_order_info.total_price * 100) != int(callback_data['total_fee']):
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_weChat.dict_to_xml(result_data), header

    if pay_order_info.status == 1:
        return target_weChat.dict_to_xml(result_data), header
    target_pay = PayService()
    target_pay.orderSuccess(pay_order_id=pay_order_info.id, params={'pay_sn': callback_data['transaction_id']})
    target_pay.addPayCallbackData(pay_order_id=pay_order_info.id, data=request.data)
    return target_weChat.dict_to_xml(result_data), header


@route_api.route('/order/ops')
def orderOps():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    member_info = g.member_info
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    act = req['act'] if 'act' in req else ''

    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn, member_id=member_info.id).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = '系统繁忙，请稍后再试'
        return jsonify(resp)

    if act == 'cancel':
        pass
    elif act == 'confirm':
        pay_order_info.express_status = 1
        pay_order_info.updated_time = getCurrentDate()
        db.session.add(pay_order_info)
        db.session.commit()
    return jsonify(resp)




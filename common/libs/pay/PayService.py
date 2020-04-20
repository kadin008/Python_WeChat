# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-20
IDE: PyCharm
Introduction: 
"""
import decimal, hashlib, time, random
from application import app, db
from common.models.food.food import Food
from common.models.pay.pay_order import PayOrder
from common.models.pay.pay_order_item import PayOrderItem
from common.models.pay.pay_order_callback_data import PayOrderCallbackDatum
from common.libs.helper import getCurrentDate
from common.libs.food.FoodService import FoodService


class PayService(object):
    def __init__(self):
        pass

    def createOrder(self, member_id, items=None, params=None):
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}

        pay_price = decimal.Decimal(0.00)
        continue_cnt = 0
        food_ids = []
        for item in items:
            if decimal.Decimal(item['price']) < 0:
                continue_cnt += 1
                continue
            pay_price = pay_price + decimal.Decimal(item['price']) * int(item['number'])
            food_ids.append(item['id'])

        if continue_cnt >= len(items):
            resp['code'] = -1
            resp['msg'] = '商品items为空~~'
            return resp

        yun_price = params['yun_price'] if params and 'yun_price' in params else 0
        note = params['note'] if params and 'note' in params else ''

        yun_price = decimal.Decimal(yun_price)
        total_price = pay_price + yun_price

        try:
            tmp_food_list = db.session.query(Food).filter(Food.id.in_(food_ids)).with_for_update().all()
            app.logger.info(tmp_food_list)
            tmp_food_stock_mapping = {}
            for tmp_item in tmp_food_list:
                tmp_food_stock_mapping[tmp_item.id] = tmp_item.stock

            model_pay_order = PayOrder()
            model_pay_order.order_sn = self.geneOrderSn()
            model_pay_order.member_id = member_id
            model_pay_order.total_price = total_price
            model_pay_order.yun_price = yun_price
            model_pay_order.pay_price = pay_price
            model_pay_order.note = note
            model_pay_order.status = -8
            model_pay_order.express_status = -8
            model_pay_order.updated_time = model_pay_order.created_time = getCurrentDate()

            db.session.add(model_pay_order)

            for item in items:
                tmp_left_stock = tmp_food_stock_mapping[item['id']]
                if decimal.Decimal(item['price']) < 0:
                    continue

                if int(item['number']) > int(tmp_left_stock):
                    raise Exception('您购买的这个美食太火爆了，剩余：%s, 你购买%s' % (tmp_left_stock, item['number']))

                tmp_ret = Food.query.filter_by(id=item['id']).update({
                    'stock': int(tmp_left_stock) - int(item['number'])
                })

                if not tmp_ret:
                    raise Exception('下单失败，请重新下单')

                tmp_pay_item = PayOrderItem()
                tmp_pay_item.pay_order_id = model_pay_order.id
                tmp_pay_item.quantity = item['number']
                tmp_pay_item.price = item['price']
                tmp_pay_item.food_id = item['id']
                tmp_pay_item.note = note
                tmp_pay_item.updated_time = tmp_pay_item.created_time = getCurrentDate()
                db.session.add(tmp_pay_item)
                FoodService.setStockChangeLog(item['id'], -item['number'], '在线购买')

            db.session.commit()
            resp['data'] = {
                'id': model_pay_order.id,
                'order_sn': model_pay_order.order_sn,
                'total_price': str(total_price)
            }
        except Exception as e:
            db.session.rollback()
            resp['code'] = -1
            resp['msg'] = '下单失败，请重新下单'
            resp['msg'] = str(e)

            return resp

        return resp

    def geneOrderSn(self):
        m = hashlib.md5()
        sn = None
        while True:
            str = '%s-%s' % (int(round(time.time()*1000)), random.randint(0, 9999999))
            m.update(str.encode("utf-8"))
            sn = m.hexdigest()
            if not PayOrder.query.filter_by(order_sn=sn).first():
                break

        return sn



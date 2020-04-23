# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-21
IDE: PyCharm
Introduction: 
"""
import json, requests, datetime
from application import app, db
from sqlalchemy import func
from common.libs.helper import getCurrentDate
from common.libs.pay.WeChatService import WeChatSefvice
from common.models.queue.queue_list import QueueList
from common.models.food.food import Food
from common.models.food.food_stock_change_log import FoodStockChangeLog
from common.models.member.oauth_member_bind import OauthMemberBind
from common.models.pay.pay_order import PayOrder
from common.models.pay.pay_order_item import PayOrderItem


'''
python manager.py runjob -m queue/index
'''


class JobTask(object):
    def __init__(self):
        pass

    def run(self, params):
        List = QueueList.query.filter_by(status=-1).order_by(QueueList.id.asc()).limit(1).all()
        for item in List:
            if item.queue_name == 'pay':
                self.handlePay(item)

            item.status = 1
            item.updated_time = getCurrentDate()
            db.session.add(item)
            db.session.commit()

    def handlePay(self, item):
        data = json.loads(item.data)
        if 'member_id' not in data or 'pay_order_id' not in data:
            return False

        oauth_bind_info = OauthMemberBind.query.filter_by(member_id=data['member_id']).first()
        if not oauth_bind_info:
            return False

        pay_order_info = PayOrder.query.filter_by(id=data['pay_order_id']).first()
        if not pay_order_info:
            return False

        # 更新销售总量
        pay_order_items = PayOrderItem.query.filter_by(payorder_id=pay_order_info.id).all()
        notice_content = []
        if pay_order_items:
            data_from = datetime.datetime.now().strftime('%Y-%m-01 00:00:00')
            data_to = datetime.datetime.now().strftime('%Y-%m-31 23:59:59')
            for item in pay_order_items:
                tmp_food_info = Food.query.filter_by(id=item.food_id).first()
                if not tmp_food_info:
                    continue

                notice_content.append('%s %s分' % (tmp_food_info, item.quantity))

                # 当月的销售
                tmp_stat_info = db.session.query(FoodStockChangeLog, func.sum(FoodStockChangeLog.quantity).label('total'))\
                    .filter(FoodStockChangeLog.food_id == item.food_id)\
                    .filter(FoodStockChangeLog.created_time >= data_from, FoodStockChangeLog.created_time <= data_to).first()

                tmp_month_count = tmp_stat_info[1] if tmp_stat_info[1] else 0

                tmp_food_info.total_count += 1
                tmp_food_info.month_count = tmp_month_count
                db.session.add(tmp_food_info)
                db.session.commit()

        if pay_order_info.prepay_id != '1':
            app.logger.info('skip notce')
            return

        # 发订阅消息
        keyword1_val = pay_order_info.order_number
        keyword2_val = '、'.join(notice_content)
        keyword3_val = "总价：" + str(pay_order_info.total_price)
        # keyword4_val = str(pay_order_info.order_number)
        # keyword5_val = ''
        if pay_order_info.express_info:
            express_info = json.loads(pay_order_info.express_info)
            keyword3_val += '快递信息：' + str(express_info['address'])

        target_weChat = WeChatSefvice()
        access_token = target_weChat.getAccessToken()
        headers = {'Content-Type': 'application/json'}
        url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/uniform_send?access_token=%s' % access_token
        params = {
            "touser": oauth_bind_info.openid,
            "weapp_template_msg": {
                "template_id": "XFtjbdJVpn0hsWB18HLXI2tHmxxCTqptgjKZfu_Bt3k",
                "page": "page/my/order_list",
                "form_id": pay_order_info.prepay_id,
                "data": {
                    "character_string1": {
                        "value": keyword1_val
                    },
                    "thing2": {
                        "value": keyword2_val
                    },
                    "amount4": {
                        "value": keyword3_val
                    },
                    "time6": {
                        "value": keyword3_val
                    },
                    'thing11': {
                        "value": keyword3_val
                    }
                }
            }
        }

        r = requests.post(url=url, data=json.dumps(params), headers=headers)
        r.encoding = 'utf-8'
        app.logger.info(r.text)
        return True













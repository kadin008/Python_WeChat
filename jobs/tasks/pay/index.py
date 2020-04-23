# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-23
IDE: PyCharm
Introduction: 
"""
import datetime
from application import app, db
from common.models.pay.pay_order import PayOrder
from common.libs.pay.PayService import PayService

'''
python manager.py runjob -m  pay/index
'''


class JobTask(object):
    def __init__(self):
        pass

    def run(self, params):

        now = datetime.datetime.now()
        date_before_30min = now + datetime.timedelta(minutes=-30)
        List = PayOrder.query.filter_by(status=-8)\
            .filter(PayOrder.created_time <= date_before_30min.strftime('%Y-%m-%d %H:%M:%S')).all()

        if not List:
            app.logger.info("not data")
            return

        pay_target = PayService()
        for item in List:
            pay_target.closeOrder(pay_order_id=item.id)

        app.logger.info('it \'s over')









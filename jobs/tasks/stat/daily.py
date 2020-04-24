# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-24
IDE: PyCharm
Introduction: 
"""
import random
from application import app, db
from sqlalchemy import func
from common.models.member.member import Member
from common.models.food.food_sale_change_log import FoodSaleChangeLog
from common.models.food.wx_share_history import WxShareHistory
from common.models.pay.pay_order import PayOrder
from common.models.stat.stat_daily_member import StatDailyMember
from common.models.stat.stat_daily_food import StatDailyFood
from common.models.stat.stat_daily_site import StatDailySite
from common.libs.helper import getFormatDate, getCurrentDate


'''
python manager.py runjob -m stat/daily -a member | food | site -p 2020-04-24
'''


class JobTask(object):
    def __init__(self):
        pass

    def run(self, params):
        act = params['act'] if 'act' in params else ''
        date = params['param'][0] if params['param'] and len(params['param']) else getFormatDate(format='%Y-%m-%d')
        app.logger.info(params)
        if not act:
            return

        date_from = date + ' 00:00:00'
        date_to = date + ' 23:59:59'
        func_params = {
            'act': act,
            'date': date,
            'date_from': date_from,
            'date_to': date_to
        }

        if act == 'member':
            self.statMember(func_params)
        elif act == 'food':
            self.statFood(func_params)
        elif act == 'site':
            self.statSite(func_params)
        elif act == 'test':
            self.test()

    # 会员数据统计
    def statMember(self, params):
        act = params['act']
        date = params['date']
        date_from = params['date_from']
        date_to = params['date_to']
        app.logger.info('act: {0}, date_from: {1}, date_to: {2}'.format(act, date_from, date_to))

        member_list = Member.query.all()
        if not member_list:
            app.logger.info('not member list')
            return

        for member_info in member_list:
            tmp_stat_member = StatDailyMember.query.filter_by(date=date, member_id=member_info.id).first()
            if tmp_stat_member:
                tmp_model_stat_member = tmp_stat_member
            else:
                tmp_model_stat_member = StatDailyMember()
                tmp_model_stat_member.member_id = member_info.id
                tmp_model_stat_member.date = date
                tmp_model_stat_member.created_time = getCurrentDate()

            tmp_stat_pay = db.session.query(func.sum(PayOrder.total_price).label('total_pay_money'))\
                .filter(PayOrder.member_id == member_info.id, PayOrder.status == 1)\
                .filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to).first()

            tmp_stat_share_count = WxShareHistory.query.filter(WxShareHistory.member_id == member_info.id)\
                .filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to).count()

            tmp_model_stat_member.total_pay_money = tmp_stat_pay[0] if tmp_stat_pay[0] else 0.00
            tmp_model_stat_member.total_shared_count = tmp_stat_share_count

            '''
            # 生成测试数据
            
            '''
            tmp_model_stat_member.total_pay_money = random.randint(50, 100)
            tmp_model_stat_member.total_shared_count = random.randint(100, 1600)

            tmp_model_stat_member.updated_time = getCurrentDate()
            db.session.add(tmp_model_stat_member)
            db.session.commit()
        return True

    # 商品数据统计
    def statFood(self, params):
        act = params['act']
        date = params['date']
        date_from = params['date_from']
        date_to = params['date_to']
        app.logger.info('act: {0}, date_from: {1}, date_to: {2}'.format(act, date_from, date_to))

        stat_food_list = db.session.\
            query(FoodSaleChangeLog.food_id, func.sum(FoodSaleChangeLog.quantity).label('total_count'),
                  func.sum(FoodSaleChangeLog.price).label('total_pay_money')).\
            filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to).\
            group_by(FoodSaleChangeLog.food_id).all()

        if not stat_food_list:
            app.logger.info('not data')
            return

        for item in stat_food_list:
            tmp_food_id = item[0]
            tmp_stat_food = StatDailyFood.query.filter_by(date=date, food_id=tmp_food_id).first()
            if tmp_stat_food:
                tmp_model_stat_food = tmp_stat_food
            else:
                tmp_model_stat_food = StatDailyFood()
                tmp_model_stat_food.date = date
                tmp_model_stat_food.food_id = tmp_food_id
                tmp_model_stat_food.created_time = getCurrentDate()

            tmp_model_stat_food.total_count = item[1]
            tmp_model_stat_food.total_pay_money = item[2]

            '''
            # 测试数据添加
            
            '''
            tmp_model_stat_food.total_count = random.randint(60, 100)
            tmp_model_stat_food.total_pay_money = random.randint(1500, 1600)

            tmp_model_stat_food.updated_time = getCurrentDate()
            db.session.add(tmp_model_stat_food)
            db.session.commit()
        return True

    # 全站数据统计
    def statSite(self, params):
        act = params['act']
        date = params['date']
        date_from = params['date_from']
        date_to = params['date_to']
        app.logger.info('act: {0}, date_from: {1}, date_to: {2}'.format(act, date_from, date_to))

        stat_pay = db.session.query(func.sum(PayOrder.total_price).label('total_pay_money')).\
            filter(PayOrder.status == 1).\
            filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to).first()

        stat_member_count = Member.query.count()
        stat_new_member_count = Member.query.\
            filter(Member.created_time >= date_from, Member.created_time <= date_to).count()

        stat_order_count = PayOrder.query.filter_by(status=1).\
            filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to).count()

        stat_share_count = WxShareHistory.query.\
            filter(WxShareHistory.created_time >= date_from, WxShareHistory.created_time <= date_to).count()

        tmp_stat_site = StatDailySite.query.filter_by(date=date).first()
        if tmp_stat_site:
            tmp_model_stat_site = tmp_stat_site
        else:
            tmp_model_stat_site = StatDailySite()
            tmp_model_stat_site.date = date
            tmp_model_stat_site.created_time = getCurrentDate()

        tmp_model_stat_site.total_pay_money = stat_pay[0] if stat_pay[0] else 0.00
        tmp_model_stat_site.total_new_member_count = stat_new_member_count
        tmp_model_stat_site.total_member_count = stat_member_count
        tmp_model_stat_site.total_order_count = stat_order_count
        tmp_model_stat_site.total_shared_count = stat_share_count

        '''
        # 制造测试数据
        '''
        tmp_model_stat_site.total_pay_money = random.randint(1000, 1100)
        tmp_model_stat_site.total_new_member_count = random.randint(100, 150)
        tmp_model_stat_site.total_member_count = random.randint(1000, 1800)
        tmp_model_stat_site.total_order_count = random.randint(100, 1600)
        tmp_model_stat_site.total_shared_count = random.randint(1500, 2500)

        tmp_model_stat_site.updated_time = getCurrentDate()
        db.session.add(tmp_model_stat_site)
        db.session.commit()
        return True

    def test(self):
        import datetime
        from common.libs.helper import getFormatDate
        now = datetime.datetime.now()
        for i in reversed(range(1, 30)):
            date_before = now + datetime.timedelta(days=-i)
            date = getFormatDate(date=date_before, format='%Y-%m-%d')
            tmp_params = {
                'act': 'test',
                'date': date,
                'date_from': date + ' 00:00:00',
                'date_to': date + ' 23:59:59'
            }

            self.statFood(tmp_params)
            self.statMember(tmp_params)
            self.statSite(tmp_params)











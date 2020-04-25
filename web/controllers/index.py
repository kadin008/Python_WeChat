# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-06
IDE: PyCharm
Introduction: 
"""
import datetime
from flask import Blueprint, g
from common.models.stat.stat_daily_site import StatDailySite
from common.libs.helper import ops_render, getFormatDate

route_index = Blueprint('index_page', __name__)


@route_index.route('/')
def index():
    resp_data = {
        'data': {
            'finance': {
                'today': 0,
                'month': 0
            },
            'member': {
                'total_new': 0,
                'month_mew': 0,
                'total': 0
            },
            'order': {
                'today': 0,
                'month': 0
            },
            'shared': {
                'today': 0,
                'month': 0
            }
        }
    }
    now = datetime.datetime.now()
    date_before_30day = now + datetime.timedelta(days = -30)
    date_from = getFormatDate(date=date_before_30day, format='%Y-%m-%d')
    date_to = getFormatDate(date=now, format='%Y-%m-%d')

    List = StatDailySite.query.filter(StatDailySite.date >= date_from).\
        filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()).all()

    data = resp_data['data']

    if List:
        for item in List:
            data['finance']['month'] += item.total_pay_money
            data['member']['month_mew'] += item.total_new_member_count
            data['member']['total'] = item.total_member_count
            data['order']['month'] += item.total_order_count
            data['shared']['month'] += item.total_shared_count

            if getFormatDate(date=item.date, format='%Y-%m-%d') == date_to:
                data['finance']['today'] += item.total_pay_money
                data['member']['total_new'] += item.total_new_member_count
                data['order']['today'] += item.total_order_count
                data['shared']['today'] += item.total_shared_count

    return ops_render('index/index.html', resp_data)



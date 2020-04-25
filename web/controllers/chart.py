# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-25
IDE: PyCharm
Introduction: 
"""
import datetime
from flask import Blueprint, jsonify
from common.models.stat.stat_daily_site import StatDailySite
from common.libs.helper import getFormatDate

route_chart = Blueprint('chart_page', __name__)


@route_chart.route('/dashboard')
def dashboard():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    now = datetime.datetime.now()
    date_before_30day = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30day, format='%Y-%m-%d')
    date_to = getFormatDate(date=now, format='%Y-%m-%d')

    List = StatDailySite.query.filter(StatDailySite.date >= date_from). \
        filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()).all()

    data = {
        'categories': [],
        'series': [
            {
                'name': '会员总数',
                'data': []
            },
            {
                'name': '订单总数',
                'data': []
            }
        ]
    }

    if List:
        for item in List:
            data['categories'].append(getFormatDate(date=item.date, format='%Y-%m-%d'))
            data['series'][0]['data'].append(item.total_member_count)
            data['series'][1]['data'].append(item.total_order_count)

    resp['data'] = data
    return jsonify(resp)


@route_chart.route('/finance')
def finance():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    now = datetime.datetime.now()
    date_before_30day = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30day, format='%Y-%m-%d')
    date_to = getFormatDate(date=now, format='%Y-%m-%d')

    List = StatDailySite.query.filter(StatDailySite.date >= date_from). \
        filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()).all()

    data = {
        'categories': [],
        'series': [
            {
                'name': '日营收报表',
                'data': []
            }
        ]
    }

    if List:
        for item in List:
            data['categories'].append(getFormatDate(date=item.date, format='%Y-%m-%d'))
            data['series'][0]['data'].append(float(item.total_pay_money))

    resp['data'] = data
    return jsonify(resp)


@route_chart.route('/share')
def share():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    now = datetime.datetime.now()
    date_before_30day = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30day, format='%Y-%m-%d')
    date_to = getFormatDate(date=now, format='%Y-%m-%d')

    List = StatDailySite.query.filter(StatDailySite.date >= date_from). \
        filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()).all()

    data = {
        'categories': [],
        'series': [
            {
                'name': '日营收报表',
                'data': []
            }
        ]
    }

    if List:
        for item in List:
            data['categories'].append(getFormatDate(date=item.date, format='%Y-%m-%d'))
            data['series'][0]['data'].append(float(item.total_shared_count))
    resp['data'] = data
    return jsonify(resp)



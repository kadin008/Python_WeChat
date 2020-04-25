# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-06
IDE: PyCharm
Introduction: 
"""
import datetime
from application import app
from flask import Blueprint, request
from common.models.food.food import Food
from common.models.member.member import Member
from common.models.stat.stat_daily_site import StatDailySite
from common.models.stat.stat_daily_food import StatDailyFood
from common.models.stat.stat_daily_member import StatDailyMember
from common.libs.helper import ops_render, getFormatDate, iPagination, getDicFilterField, selectFilterObj


route_stat = Blueprint('stat_page', __name__)


@route_stat.route('/index')
def index():
    now = datetime.datetime.now()
    date_before_30day = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30day, format='%Y-%m-%d')
    default_date_to = getFormatDate(date=now, format='%Y-%m-%d')

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to

    query = StatDailySite.query.filter(StatDailySite.date >= date_from).filter(StatDailySite.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace('&p={}'.format(page), '')
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    List = query.order_by(StatDailySite.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    resp_data['list'] = List
    resp_data['pages'] = pages
    resp_data['current'] = 'index'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }

    return ops_render('stat/index.html', resp_data)


@route_stat.route('/food')
def food():
    now = datetime.datetime.now()
    date_before_30day = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30day, format='%Y-%m-%d')
    default_date_to = getFormatDate(date=now, format='%Y-%m-%d')

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to

    query = StatDailyFood.query.filter(StatDailyFood.date >= date_from).filter(StatDailyFood.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace('&p={}'.format(page), '')
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    List = query.order_by(StatDailyFood.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    data_list = []
    if List:
        food_map = getDicFilterField(Food, Food.id, 'id', selectFilterObj(List, 'food_id'))
        for item in List:
            tmp_food_info = food_map[item.food_id] if item.food_id in food_map else {}
            tmp_data = {
                'date': item.date,
                'total_count': item.total_count,
                'total_pay_money': item.total_pay_money,
                'food_info': tmp_food_info
            }
            data_list.append(tmp_data)

    resp_data['list'] = data_list
    resp_data['pages'] = pages
    resp_data['current'] = 'food'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }

    return ops_render('stat/food.html', resp_data)


@route_stat.route('/member')
def member():
    now = datetime.datetime.now()
    date_before_30day = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30day, format='%Y-%m-%d')
    default_date_to = getFormatDate(date=now, format='%Y-%m-%d')

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to

    query = StatDailyMember.query.filter(StatDailyMember.date >= date_from).filter(StatDailyMember.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace('&p={}'.format(page), '')
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    List = query.order_by(StatDailyMember.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    data_list = []
    if List:
        member_map = getDicFilterField(Member, Member.id, 'id', selectFilterObj(List, 'member_id'))
        for item in List:
            tmp_member_info = member_map[item.member_id] if item.member_id in member_map else {}
            tmp_data = {
                'date': item.date,
                'total_pay_money': item.total_pay_money,
                'total_shared_count': item.total_shared_count,
                'member_info': tmp_member_info
            }
            data_list.append(tmp_data)

    resp_data['list'] = data_list
    resp_data['pages'] = pages
    resp_data['current'] = 'member'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render('stat/member.html', resp_data)


@route_stat.route('/share')
def share():
    now = datetime.datetime.now()
    date_before_30day = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30day, format='%Y-%m-%d')
    default_date_to = getFormatDate(date=now, format='%Y-%m-%d')

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to

    query = StatDailySite.query.filter(StatDailySite.date >= date_from).filter(StatDailySite.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace('&p={}'.format(page), '')
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    List = query.order_by(StatDailySite.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()

    resp_data['list'] = List
    resp_data['pages'] = pages
    resp_data['current'] = 'food'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render('stat/share.html', resp_data)











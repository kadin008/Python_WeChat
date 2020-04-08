# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-06
IDE: PyCharm
Introduction: 
"""
from flask import Blueprint, g
from common.libs.helper import ops_render

route_index = Blueprint('index_page', __name__)


@route_index.route('/')
def index():
    return ops_render('index/index.html')



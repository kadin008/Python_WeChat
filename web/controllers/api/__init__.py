# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-09
IDE: PyCharm
Introduction: 
"""
from flask import Blueprint


route_api = Blueprint('api_page', __name__)

from web.controllers.api.menber import *
from web.controllers.api.food import *
from web.controllers.api.cart import *
from web.controllers.api.order import *
from web.controllers.api.my import *


@route_api.route('/')
def index():
    return 'Mina Api V1.0'



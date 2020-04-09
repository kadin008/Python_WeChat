# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-09
IDE: PyCharm
Introduction: 
"""
import json
from application import app, db
from flask import request, g
from common.models.log.app_access_log import AppAccessLog
from common.models.log.app_error_log import AppErrorLog
from common.libs.helper import getCurrentDate


class LoginService(object):
    @staticmethod
    def addAccessLog():
        target = AppAccessLog()
        target.target_url = request.url
        target.referer_url = request.referrer
        target.ip = request.remote_addr
        target.query_params = json.dumps(request.values.to_dict())
        if 'current_user' in g and g.current_user is not None:
            target.uid = g.current_user.uid
        target.ua = request.headers.get('User-Agent')
        target.created_time = getCurrentDate()
        db.session.add(target)
        db.session.commit()
        return True

    @staticmethod
    def addErrorLog(content):
        target = AppErrorLog()
        target.target_url = request.url
        target.referer_url = request.referrer
        target.query_params = json.dumps(request.values.to_dict())
        target.content = content
        target.created_time = getCurrentDate()
        db.session.add(target)
        db.session.commit()
        return True




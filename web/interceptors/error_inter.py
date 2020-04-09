# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-09
IDE: PyCharm
Introduction: 
"""
from application import app
from common.libs.helper import ops_render
from common.libs.LogService import LoginService


@app.errorhandler(404)
def error_404(e):
    LoginService.addErrorLog(e)
    return ops_render('error/error.html', {'status': 404, 'msg': '很抱歉! 你访问的页面不存在!'})



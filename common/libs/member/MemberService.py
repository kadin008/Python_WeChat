# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-09
IDE: PyCharm
Introduction: 
"""
import json
import requests
import hashlib
import random
import string
from application import app


class MemberService(object):
    @staticmethod
    def geneAuthCode(member_info=None):
        m = hashlib.md5()
        str = '%s-%s-%s' % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return (''.join(keylist))

    @staticmethod
    def getWeChatOpenId(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code' \
            .format(app.config['MINA_APP']['app_id'], app.config['MINA_APP']['app_key'], code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid






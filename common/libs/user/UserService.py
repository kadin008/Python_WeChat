# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-07
IDE: PyCharm
Introduction: 
"""
import hashlib
import base64


class UserService(object):
    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        str = '%s-%s' % (base64.encodebytes(pwd.encode('utf-8')), salt)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def geneAuthCode(user_info):
        m = hashlib.md5()
        str = '%s-%s-%s-%s' % (user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(str.encode('utf-8'))
        return m.hexdigest()





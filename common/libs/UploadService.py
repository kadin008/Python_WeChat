# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-11
IDE: PyCharm
Introduction: 
"""
import os
import stat
import uuid
from application import app, db
from datetime import datetime
from werkzeug.utils import secure_filename
from common.libs.helper import getCurrentDate
from common.models.images import Image


class UploadService(object):
    @staticmethod
    def uploadByFile(file):
        config_upload = app.config['UPLOAD']
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1]
        if ext not in config_upload['ext']:
            resp['code'] = -1
            resp['msg'] = '暂不支持%s扩展类文件' % ext
            return resp

        root_path = app.root_path + config_upload['prefix_path']
        file_dir = datetime.now().strftime('%Y%m%d')
        save_dir = root_path + file_dir
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

        file_name = str(uuid.uuid4()).replace('-', '') + '.' + ext
        file.save('{0}/{1}'.format(save_dir, file_name))

        model_image = Image()
        model_image.file_key = file_dir + "/" + file_name
        model_image.created_time = getCurrentDate()
        db.session.add(model_image)
        db.session.commit()

        resp['data'] = {
            'file_key': model_image.file_key
        }

        return resp











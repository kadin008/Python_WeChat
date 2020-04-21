# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-21
IDE: PyCharm
Introduction: 
"""
import json
from application import app, db
from common.models.queue.queue_list import QueueList
from common.libs.helper import getCurrentDate


class QueueService(object):

    @staticmethod
    def addQueue(queue_name, data=None):
        model_queue = QueueList()
        model_queue.queue_name = queue_name
        if data:
            model_queue.data = json.dump(data)
        model_queue.created_time = model_queue.updated_time = getCurrentDate()

        db.session.add(model_queue)
        db.session.commit()

        return True








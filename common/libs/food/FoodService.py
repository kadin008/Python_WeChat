# _*_ coding: utf-8 _*_
"""
Project: ordering
Creotor: Patrick_Wang
Create time: 2020-04-11
IDE: PyCharm
Introduction: 
"""
from application import db
from common.models.food.food_stock_change_log import FoodStockChangeLog
from common.models.food.food import Food
from common.libs.helper import getCurrentDate


class FoodService(object):
    @staticmethod
    def setStockChangeLog(food_id=0, quantity=0, note=''):
        if food_id < 1:
            return False

        food_info = Food.query.filter_by(id=food_id).first()
        if not food_info:
            return False

        model_stock_change = FoodStockChangeLog()
        model_stock_change.food_id = food_id
        model_stock_change.unit = quantity
        model_stock_change.total_stock = food_info.stock
        model_stock_change.note = note
        model_stock_change.created_time = getCurrentDate()
        db.session.add(model_stock_change)
        db.session.commit()
        return True








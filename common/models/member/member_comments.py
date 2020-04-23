# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class MemberComment(db.Model):
    __tablename__ = 'member_comments'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='会员id')
    food_ids = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='商品ids')
    pay_order_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='订单id')
    score = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='评分')
    content = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='评论内容')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='插入时间')

    @property
    def score_desc(self):
        score_map = {
            '10': '好评',
            '6': '中评',
            '0': '差评'
        }
        return score_map[str(self.score)]


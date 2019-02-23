from application import db, app
from application.models import Base, NameMixIn

from flask_login import current_user
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import TSVECTOR

class Item(Base):

    lexeme = db.Column(TSVECTOR, nullable=False)
    users = db.relationship("UserItem", backref='Item', lazy=True)
    
    def __init__(self, lexeme):
        self.lexeme = lexeme

    @staticmethod
    def get_matching_item(user_item_name):
        stmt = text("SELECT item FROM item"
                    " WHERE to_tsvector('finnish', :user_item_name) = item.lexeme"
                    " GROUP BY item.id, item.lexeme").params(user_item_name=user_item_name)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            app.logger.info(row[0])
            parts = row[0].split(',')
            response.append({"id":parts[0][1:], "lexeme":parts[1][:-1]})

        return response[0]

    @staticmethod
    def name_to_lexeme(name):
        stmt = text("SELECT to_tsvector('finnish', :name)").params(name=name)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append(row[0])
        return response[0]

class UserItem(Base, NameMixIn):

    __tablename__ = 'user_item'

    best_before = db.Column(db.Date, nullable=True)
    used = db.Column(db.Boolean, nullable=False)
    expired = db.Column(db.Boolean, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                            nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self, name, best_before):
        self.name = name
        self.best_before = best_before
        self.used = False
        self.expired = False

    @staticmethod
    def list_users_items():
        stmt = text("SELECT user_item.id AS id, user_item.name AS name, user_item.best_before AS best_before FROM item, user_item"
                    " WHERE user_item.account_id = :user"
                    " AND user_item.used = false"
                    " AND user_item.expired = false"
                    " GROUP BY user_item.id"
                    " ORDER BY (CASE WHEN user_item.best_before IS NULL THEN 1 ELSE 0 END) ASC,"
                    "   user_item.best_before ASC").params(user=current_user.id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "best_before":row[2]})

        return response

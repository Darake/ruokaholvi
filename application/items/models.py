from application import db, app
from application.models import Base, NameMixIn

from flask_login import current_user
from sqlalchemy.sql import text

class Item(Base, NameMixIn):

    users = db.relationship("UserItem", backref='Item', lazy=True)
    
    def __init__(self, name):
        self.name = name

class UserItem(Base):

    __tablename__ = 'user_item'

    best_before = db.Column(db.Date, nullable=True)
    used = db.Column(db.Boolean, nullable=False)
    expired = db.Column(db.Boolean, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                            nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self, best_before):
        self.best_before = best_before
        self.used = False
        self.expired = False

    @staticmethod
    def list_users_items():
        stmt = text("SELECT user_item.id AS id, item.name AS name, user_item.best_before AS best_before FROM item, user_item"
                    " WHERE user_item.account_id = :user"
                    " AND item.id = user_item.item_id"
                    " AND user_item.used = false"
                    " AND user_item.expired = false"
                    " ORDER BY (CASE WHEN user_item.best_before IS NULL THEN 1 ELSE 0 END) ASC,"
                    "   user_item.best_before ASC").params(user=current_user.id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "best_before":row[2]})

        return response
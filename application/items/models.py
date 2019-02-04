from application import db
from application.models import BaseWithName

class Item(BaseWithName):
    
    best_before = db.Column(db.Date, nullable=True)
    used = db.Column(db.Boolean, nullable=False)
    expired = db.Column(db.Boolean, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                            nullable=False)

    def __init__(self, name, best_before):
        self.name = name
        self.best_before = best_before
        self.used = False
        self.expired = False

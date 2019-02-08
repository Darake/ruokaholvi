from application import db
from application.models import Base, DatestampMixIn, NameMixIn

class User(Base, DatestampMixIn, NameMixIn):

    __tablename__ = "account"

    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    items = db.relationship("UserItem", backref='account', lazy=True)
    recipes = db.relationship("Recipe", backref='account', lazy=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False   

    def is_authenticated(self):
        return True         
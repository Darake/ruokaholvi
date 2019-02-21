from flask_user import UserMixin, current_user
from sqlalchemy.sql import text

from application import db
from application.models import Base, DatestampMixIn, NameMixIn

class User(Base, DatestampMixIn, NameMixIn, UserMixin):

    __tablename__ = "account"

    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    items = db.relationship("UserItem", backref='account', lazy=True)
    recipes = db.relationship("Recipe", backref='account', lazy=True)

    roles = db.relationship('Role', secondary='user_roles')

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

    @staticmethod
    def get_role(userId):
        stmt = text("SELECT roles.name FROM roles, user_roles, account"
                    " WHERE account.id = :userId"
                    " AND user_roles.user_id = account.id"
                    " AND roles.id = user_roles.role_id").params(userId=userId)
        res = db.engine.execute(stmt)

        try:
            return res.first().name
        except:
            return ""

class Role(Base, NameMixIn):
    
    __tablename__ = 'roles'

class UserRoles(Base):

    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer(), db.ForeignKey('account.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
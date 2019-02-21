# flask-sovellus
from flask import Flask
app = Flask(__name__)

# asetuksia
import os
app.static_folder = 'static'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['USER_EMAIL_SENDER_EMAIL'] = 'noreply@example.com'
app.config.from_mapping(CLOUDINARY_URL=os.environ.get('CLOUDINARY_URL'))

from flask_babelex import Babel
babel = Babel(app)

# tietokanta
from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:salasana@localhost/food_vault"

db = SQLAlchemy(app)

# oman sovelluksen toiminnallisuudet
from application import views

from application.items import models
from application.items import views

from application.auth import models
from application.auth import views

from application.recipes import models
from application.recipes import views

# kirjautuminen
from application.auth.models import User, Role
from os import urandom
app.config["SECRET_KEY"] = os.environ.get("FV_SECRET_KEY", "")

from flask_login import LoginManager
from flask_user import UserManager
user_manager = UserManager(app, db, User)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# luodaan taulut tarvittaessa
try:
    db.create_all()
except:
    pass

# luodaan admin käyttäjä tarvittaessa
if not User.query.filter(User.username == 'admin').first():
    user = User(name='Administrator', username='admin',
                password=os.environ.get("ADMIN_PASSWORD"))
    user.roles.append(Role(name='admin'))
    db.session.add(user)
    db.session().commit()

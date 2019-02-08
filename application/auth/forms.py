from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError

from application.auth.models import User

def uniqueUsernameRequired(form, field):
    if User.query.filter_by(username=form.username.data).first():
        raise ValidationError("Username taken")

def validLogInRequired(form, field):
    if not User.query.filter_by(username=form.username.data,
                                password=form.password.data).first():
        raise ValidationError("Username or password invalid")

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.InputRequired()])
    password = PasswordField("Password", [validators.InputRequired(), validLogInRequired])

    class Meta:
        csrf = False

class RegistrationForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired()])
    username = StringField("Username", [validators.InputRequired(), uniqueUsernameRequired])
    password = PasswordField("Password", [validators.InputRequired()])

    class Meta:
        csrf = False
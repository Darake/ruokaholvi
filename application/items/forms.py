from flask_wtf import FlaskForm
from wtforms import StringField, DateField, validators, SelectField

class ItemForm(FlaskForm):
    name = StringField("Item name:", [validators.InputRequired()])
    best_before = DateField("Best before", [validators.Optional()])

    class Meta:
        csrf = False

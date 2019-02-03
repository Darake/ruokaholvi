from flask_wtf import FlaskForm
from wtforms import StringField, validators

class ItemForm(FlaskForm):
    name = StringField("Item name:", [validators.InputRequired()])
    bestBefore = StringField("Best before:")

    class Meta:
        csrf = False

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, validators

class IngredientForm(FlaskForm):
    ingredient = StringField("Ingredient:", [validators.InputRequired()])

    class Meta:
        csrf = False

class RecipeForm(FlaskForm):
    name = StringField("Recipe name:", [validators.InputRequired()])
    instructions = TextAreaField("Instructions:", [validators.InputRequired()])
    image = FileField("Image:", [validators.Optional()])

    class Meta:
        csrf = False

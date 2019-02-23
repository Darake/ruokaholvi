from application import app

from flask import request
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, TextAreaField, validators, ValidationError

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def get_size(file):
    if file.content_length:
        return file.content_length

    try:
        pos = file.tell()
        file.seek(0, 2)
        size = file.tell()
        file.seek(pos)
        return size
    except (AttributeError, IOError):
        pass

    return 0

def SmallSizeRequired(form, field):
    try:
        file = request.files[form.image.name]
    except:
        return

    if get_size(file) > 10 * 1024 * 1024:
        raise ValidationError('Upload a smaller picture. Max size 10MB')

    
def ImageRequired(form, field):
    try:
        filename = request.files[form.image.name].filename
    except:
        return
    if not ('.' in filename and \
            filename.split('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']) \
            and filename != '':
        raise ValidationError('Only jpg, jpeg or png files allowed')

class IngredientForm(FlaskForm):
    amount = StringField("Ingredient:", [validators.Optional()])
    name = StringField("Ingredient:", [validators.InputRequired()])

    class Meta:
        csrf = False

class RecipeForm(FlaskForm):
    name = StringField("Recipe name:", [validators.InputRequired()])
    instructions = TextAreaField("Instructions:", [validators.InputRequired()])
    image = FileField("Image:", [ImageRequired, SmallSizeRequired])

    class Meta:
        csrf = False

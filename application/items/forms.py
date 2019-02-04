from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField

class ItemForm(FlaskForm):
    name = StringField("Item name:", [validators.InputRequired()]) 
    day = SelectField("Best before:", coerce=int,
        choices=[(0,''), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), 
            (8,8), (9,9), (10,10), (11,11), (12,12), (13,13), 
            (14,14), (15,15), (16,16), (17,17), (18,18), (19,19),
            (20,20), (21,21), (22,22), (23,23), (24,24), (25,25),
            (26,26), (27,27), (28,28), (29,29), (30,30), (31,31)])
    month = SelectField(coerce=int,
            choices=[(0,''), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7),
                (8,8), (9,9), (10,10), (11,11), (12,12)])
    year = SelectField(coerce=int,
            choices=[(2019,2019), (2020, 2020), (2021, 2021)])

    class Meta:
        csrf = False

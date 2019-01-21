from application import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(144), nullable=False)
    used = db.Column(db.Boolean, nullable=False)

    def __init__(self, name):
        self.name = name
        self.used = False

from application import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(144), nullable=False)
    best_before = db.Column(db.String(144), nullable=True)
    used = db.Column(db.Boolean, nullable=False)
    expired = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, best_before):
        self.name = name
        self.best_before = best_before
        self.used = False
        self.expired = False

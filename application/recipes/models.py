from application import db, app
from application.models import Base, NameMixIn, DatestampMixIn

from flask_login import current_user
from sqlalchemy.sql import text

class Ingredient(Base):
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'),
                            nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self, recipe_id, item_id):
        self.recipe_id = recipe_id
        self.item_id = item_id

    @staticmethod
    def list_recipes_ingredients(recipeId):
        stmt = text("SELECT item.name FROM item, ingredient, recipe"
                    " WHERE item.id = ingredient.item_id"
                    " AND ingredient.recipe_id = :recipeId"
                    " GROUP BY item.name").params(recipeId=recipeId)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append(row[0])

        return response

class Recipe(Base, DatestampMixIn, NameMixIn):

    instructions = db.Column(db.String(2000), nullable=False)
    image = db.Column(db.String(144), nullable=True)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                            nullable=False)

    ingredients = db.relationship("Ingredient", backref='Recipe', lazy=True)
    

    def __init__(self, name, instructions, image):
        self.name = name
        self.instructions =instructions
        self.image = image
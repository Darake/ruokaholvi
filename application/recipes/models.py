from application import db, app
from application.models import Base, NameMixIn, DatestampMixIn

from flask_login import current_user
from sqlalchemy.sql import text

class Ingredient(Base):
    amount = db.Column(db.String(144), nullable=True)
    name = db.Column(db.String(144), nullable=False)
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', 
                            ondelete='CASCADE'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self, amount, name, recipe_id, item_id):
        self.amount = amount
        self.name = name
        self.recipe_id = recipe_id
        self.item_id = item_id

    

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

    @staticmethod
    def list_recipes_ingredients(recipeId):
        stmt = text("SELECT ingredient.name, ingredient.id, ingredient.amount FROM ingredient, recipe"
                    " WHERE ingredient.recipe_id = :recipeId"
                    " GROUP BY ingredient.name, ingredient.id, ingredient.amount").params(recipeId=recipeId)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"name":row[0], "id":row[1], "amount":row[2]})
            

        return response

    @staticmethod
    def list_recipes_by_user_ingredients(userId):
        stmt = text("SELECT recipe.id, recipe.name, recipe.image, COUNT(DISTINCT ingredient.id)"
                    " FROM item CROSS JOIN user_item CROSS JOIN account CROSS JOIN recipe"
                    " LEFT JOIN ingredient"
                    " ON ingredient.recipe_id = recipe.id"
                    " AND ingredient.item_id = item.id"
                    " AND item.id = user_item.item_id"
                    " AND user_item.expired = false"
                    " AND user_item.used = false"
                    " AND user_item.account_id = :userId"
                    " GROUP BY recipe.id, recipe.name, recipe.image"
                    " ORDER BY COUNT(ingredient.id) DESC").params(userId=userId)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append(
                {
                "id": row[0],
                "name": row[1],
                "image": row[2],
                "userIngredient": row[3]
                }
            )
        
        return response

    @staticmethod
    def list_recipes_by_user_item(userId, user_itemId):
        stmt = text("SELECT recipe.id, recipe.name, recipe.image, COUNT(DISTINCT ingredient.id)"
                    " FROM item CROSS JOIN user_item CROSS JOIN account CROSS JOIN recipe"
                    " LEFT JOIN ingredient ON recipe.id = ingredient.recipe_id"
                    " AND ingredient.item_id = item.id"
                    " AND item.id = user_item.item_id"
                    " AND user_item.expired = false"
                    " AND user_item.used = false"
                    " AND user_item.account_id = :userId"
                    " WHERE recipe.id IN ("
                    "  SELECT recipe.id FROM recipe, ingredient, user_item, item"
                    "  WHERE recipe.id = ingredient.recipe_id"
                    "  AND ingredient.item_id = item.id"
                    "  AND item.id = user_item.item_id"
                    "  AND user_item.id = :user_itemId)"
                    " GROUP BY recipe.id, recipe.name, recipe.image"
                    " ORDER BY COUNT(ingredient.id) DESC").params(userId=userId, user_itemId=user_itemId)
        
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append(
                {
                "id": row[0],
                "name": row[1],
                "image": row[2],
                "userIngredient": row[3]
                }
            )
        
        return response

    def recipesToDictionary(response):
        return None
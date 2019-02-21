from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_user import roles_required
from werkzeug.utils import secure_filename

from application import app, db
from application.items.models import Item
from application.recipes.models import Recipe, Ingredient
from application.auth.models import UserRoles, User, Role
from application.recipes.forms import RecipeForm, IngredientForm

from cloudinary.uploader import upload

@app.route("/recipes/<recipeId>/", methods=["GET"])
@login_required
def recipe(recipeId):
    userId = Recipe.query.filter_by(id=recipeId).first().account_id
    userRole = User.get_role(current_user.id)
    authorizedToDelete = userId == current_user.id or userRole == 'admin'

    recipe = Recipe.query.get(recipeId)
    ingredients = Recipe.list_recipes_ingredients(recipeId)

    return render_template("/recipes/recipe.html",
                            recipe=recipe,
                            ingredients=ingredients,
                            authorizedToDelete=authorizedToDelete)

@app.route("/recipes/<recipeId>/", methods=["POST"])
@login_required
def recipe_delete(recipeId):
    userId = Recipe.query.filter_by(id=recipeId).first().account_id
    userRole = User.get_role(current_user.id)
    
    if not (userId == current_user.id or userRole == 'admin'):
        return redirect(url_for("recipes_show"))

    Recipe.query.filter_by(id=recipeId).delete()
    db.session().commit()
    
    return redirect(url_for("recipes_show"))

@app.route("/recipes/", methods=["GET"])
def recipes_show():
    recipes = Recipe.query.all()
    return render_template("/recipes/list.html", recipes=recipes)

@app.route("/recipes/new", methods=["GET", "POST"])
@login_required
def recipes_create():
    if request.method == "GET":
        return render_template("recipes/new.html", form=RecipeForm())

    form = RecipeForm(request.form)
    if not form.validate():
        return render_template("/recipes/new.html", form=form)

    try:
        file = request.files[form.image.name]
        upload_result = upload(file)
        url = upload_result['url']
    except:
        url = None

    r = Recipe(form.name.data, form.instructions.data, url)
    r.account_id = current_user.id

    db.session().add(r)
    db.session().flush()
    recipeId = r.id

    db.session().commit()
    
    return redirect(url_for("recipes_ingredients", recipeId=recipeId))

@app.route("/recipes/ingredients/<recipeId>/" , methods=["GET", "POST"])
@login_required
def recipes_ingredients(recipeId):
    if request.method == "GET":
        return render_template("/recipes/ingredients.html",
                                form=IngredientForm(),
                                ingredients=Recipe.list_recipes_ingredients(recipeId),
                                recipeId=recipeId)

    form = IngredientForm(request.form)
    if not form.validate():
        return redirect(url_for("recipes_ingredients", recipeId=recipeId))
    
    try:
        itemId = Item.query.filter_by(name=form.ingredient.data).first().id
        ingredient = Ingredient(recipeId, itemId)
    except:
        item = Item(form.ingredient.data)
        db.session().add(item)
        db.session().flush()
        ingredient = Ingredient(recipeId, item.id)

    db.session().add(ingredient)
    db.session().commit()

    return redirect(url_for("recipes_ingredients", recipeId=recipeId))

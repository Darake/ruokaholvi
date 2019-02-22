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
    recipe = Recipe.query.get(recipeId)
    ingredients = Recipe.list_recipes_ingredients(recipeId)

    return render_template("/recipes/recipe.html",
                            recipe=recipe,
                            ingredients=ingredients,
                            authorizedToDelete=recipeAuthorization(recipeId))

@app.route("/recipes/<recipeId>/", methods=["POST"])
@login_required
def recipe_delete(recipeId):
    if not recipeAuthorization(recipeId):
        return redirect(url_for("recipes_show"))

    Recipe.query.filter_by(id=recipeId).delete()
    db.session().commit()
    
    return redirect(url_for("recipes_show"))

@app.route("/recipes/<recipeId>/edit", methods=["GET"])
@login_required
def recipes_edit(recipeId):
    if not recipeAuthorization(recipeId):
        return redirect(url_for("recipes_show"))
    
    recipe = Recipe.query.get(recipeId)
    form = RecipeForm()
    form.instructions.data = recipe.instructions
    form.name.data = recipe.name

    return render_template("recipes/edit.html",
                        form=form,
                        recipeId=recipeId)

@app.route("/recipes/<recipeId>/edit", methods=["POST"])
@login_required
def recipes_save_edit(recipeId):
    form = RecipeForm(request.form)
    
    if not form.validate():
        return render_template("/recipes/edit.html",
                                form=form,
                                recipeId=recipeId)

    recipe = Recipe.query.get(recipeId)
    
    recipe.image = uploadImage(form.image.name) or recipe.image
    recipe.name = form.name.data
    recipe.instructions = form.instructions.data
    
    db.session.commit()

    return redirect(url_for("recipes_ingredients", recipeId=recipeId))

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

    url = uploadImage(form.image.name)

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
    if not recipeAuthorization(recipeId):
        return redirect(url_for("recipes_show"))

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

@app.route("/recipes/ingredients/<recipeId>/<ingredientId>/", methods=["POST"])
@login_required
def ingredients_delete(recipeId, ingredientId):
    if not recipeAuthorization(recipeId):
        return redirect(url_for("recipes_show"))

    Ingredient.query.filter_by(id=ingredientId).delete()
    db.session.commit()
    return redirect(url_for('recipes_ingredients',
                            recipeId=recipeId))

def recipeAuthorization(recipeId):
    userId = Recipe.query.filter_by(id=recipeId).first().account_id
    userRole = User.get_role(current_user.id)
    authorizedToDelete = userId == current_user.id or userRole == 'admin'
    return authorizedToDelete

def uploadImage(imageName):
    try:
        file = request.files[imageName]
        upload_result = upload(file)
        return upload_result['url']
    except:
        return None

from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from application import app, db
from application.items.models import Item
from application.recipes.models import Recipe, Ingredient
from application.recipes.forms import RecipeForm, IngredientForm

from cloudinary.uploader import upload

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
                                ingredients=Ingredient.list_recipes_ingredients(recipeId),
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

    app.logger.info(ingredient)

    db.session().add(ingredient)
    db.session().commit()

    return redirect(url_for("recipes_ingredients", recipeId=recipeId))

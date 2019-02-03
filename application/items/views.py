from flask import redirect, render_template, request, url_for

from application import app, db
from application.items.models import Item
from application.items.forms import ItemForm

@app.route("/items", methods=["GET"])
def items_index():
    return render_template("items/list.html", items = Item.query.filter(Item.used == False, Item.expired == False))

@app.route("/items/new/")
def items_form():
    return render_template("items/new.html", form = ItemForm())

@app.route("/items/<item_id>/", methods=["POST"])
def items_set_expired(item_id):
    i = Item.query.get(item_id)
    i.expired = True

    db.session().commit()

    return redirect(url_for("items_index"))

@app.route("/items/<item_id>/", methods=["POST"])
def items_set_used(item_id):
    i = Item.query.get(item_id)
    i.used = True
    
    db.session().commit()

    return redirect(url_for("items_index"))

@app.route("/items/", methods=["POST"])
def items_create():
    form = ItemForm(request.form)

    if not form.validate():
        return render_template("items/new.html", form = form)
    
    i = Item(form.name.data, form.bestBefore.data)

    db.session().add(i)
    db.session().commit()

    return redirect(url_for("items_index"))
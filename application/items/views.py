from application import app, db
from flask import redirect, render_template, request, url_for
from application.items.models import Item

@app.route("/items", methods=["GET"])
def items_index():
    return render_template("items/list.html", items = Item.query.filter(Item.used == False, Item.expired == False))

@app.route("/items/new/")
def items_form():
    return render_template("items/new.html")

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
    i = Item(request.form.get("name"), request.form.get("best_before"))

    db.session().add(i)
    db.session().commit()

    return redirect(url_for("items_index"))

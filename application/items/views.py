import datetime

from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.items.models import Item
from application.items.forms import ItemForm

@app.route("/items", methods=["GET"])
@login_required
def items_index():
    return render_template("items/list.html", items = Item.query.filter(Item.used == False, Item.expired == False))

@app.route("/items/new/")
@login_required
def items_form():
    return render_template("items/new.html", form = ItemForm())

@app.route("/items/expire/<item_id>/", methods=["POST"])
@login_required
def items_set_expired(item_id):
    i = Item.query.get(item_id)
    i.expired = True

    db.session().commit()

    return redirect(url_for("items_index"))

@app.route("/items/use/<item_id>/", methods=["POST"])
@login_required
def items_set_used(item_id):
    i = Item.query.get(item_id)
    i.used = True
    
    db.session().commit()

    return redirect(url_for("items_index"))

@app.route("/items/delete/<item_id>/", methods=["POST"])
@login_required
def items_delete(item_id):
    Item.query.filter_by(id=item_id).delete()
    db.session.commit()

    return redirect(url_for("items_index"))

@app.route("/items/", methods=["POST"])
@login_required
def items_create():
    form = ItemForm(request.form)
    bestBefore = None

    if not form.validate():
        return render_template("items/new.html", form = form)

    if (form.day.data != 0 and form.month.data != 0):
        try:
            bestBefore = datetime.date(
                form.year.data, 
                form.month.data, 
                form.day.data)
        except:
            return render_template("items/new.html", form = form,
                dateError = "Invalid date")
    
    i = Item(form.name.data, bestBefore)
    i.account_id = current_user.id

    db.session().add(i)
    db.session().commit()

    return redirect(url_for("items_index"))

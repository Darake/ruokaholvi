import datetime

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from application import app, db
from application.items.models import Item, UserItem
from application.items.forms import ItemForm

@app.route("/items", methods=["GET"])
@login_required
def items_index():
    return render_template("items/list.html", 
        items = UserItem.list_users_items(),
        form = ItemForm())

@app.route("/items/expire/<item_id>/", methods=["POST"])
@login_required
def items_set_expired(item_id):
    ui = UserItem.query.get(item_id)
    ui.expired = True

    db.session().commit()

    return redirect(url_for("items_index"))

@app.route("/items/use/<item_id>/", methods=["POST"])
@login_required
def items_set_used(item_id):
    ui = UserItem.query.get(item_id)
    ui.used = True
    
    db.session().commit()

    return redirect(url_for("items_index"))

@app.route("/items/delete/<item_id>/", methods=["POST"])
@login_required
def items_delete(item_id):
    UserItem.query.filter_by(id=item_id).delete()
    db.session.commit()

    return redirect(url_for("items_index"))

@app.route("/items", methods=["POST"])
@login_required
def items_create():
    form = ItemForm(request.form)

    if not form.validate():
        return render_template("items/list.html", 
        items = UserItem.list_users_items(),
        form = form)

    ui = UserItem(form.best_before.data)
    ui.account_id = current_user.id
    try:
        ui.item_id = Item.query.filter_by(name=form.name.data).first().id
    except:
        i = Item(form.name.data)
        db.session().add(i)
        db.session().commit()
        ui.item_id = Item.query.filter_by(name=form.name.data).first().id
    
    db.session().add(ui)
    db.session().commit()

    return redirect(url_for("items_index"))

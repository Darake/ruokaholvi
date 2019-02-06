from flask import render_template, redirect, url_for
from flask_login import login_required
from application import app

@app.route("/")
@login_required
def index():
    return redirect(url_for('items_index'))

from app.home import home
from app import db
from flask import render_template


@home.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html", title='Home')
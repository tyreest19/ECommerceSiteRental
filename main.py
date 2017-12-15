import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__, static_folder='templates')

@app.route("/", methods=['GET', 'POST'])
def home():
    return 'we in this bitch'

if __name__ == '__main__':
    app.run()
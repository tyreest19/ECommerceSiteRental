# app/__init__.py

# third-party imports
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

# after the db variable initialization
login_manager = LoginManager()

def create_app(config_name):
    # Explanation of configs: http://flask.pocoo.org/docs/0.12/config/
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login" # Will send user to view if not logged in


    return app

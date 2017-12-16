# app/__init__.py

from flask import Flask
# third-party imports
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


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
    Bootstrap(app)
    migrate = Migrate(app, db)
    from app import database

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from app.posts import posts as posts_blueprint
    app.register_blueprint(posts_blueprint)
    return app

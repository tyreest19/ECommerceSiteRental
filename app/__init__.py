# app/__init__.py
import os
from flask import Flask
# third-party imports
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
mail = Mail()
# after the db variable initialization
login_manager = LoginManager()

stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

def create_app(config_name):
    # Explanation of configs: http://flask.pocoo.org/docs/0.12/config/
    app = Flask(__name__, instance_relative_config=True) # initialize flask app
    app.config.from_object(app_config[config_name])  # Setups basic configuration of the app
    app.config.from_pyfile('config.py', silent=True) # Setsup basic configuration of app using config.py
    db.init_app(app) # Intializes database
    login_manager.init_app(app) #Creates login system
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login" # Will send user to view if not logged in
    Bootstrap(app) # Allows forms to access CSS files
    mail.init_app(app)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.error import error as error_blueprint
    app.register_blueprint(error_blueprint)

    from app.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from app.posts import posts as posts_blueprint
    app.register_blueprint(posts_blueprint)

    from app.payments import payments as payments_blueprint
    app.register_blueprint(payments_blueprint)

    return app

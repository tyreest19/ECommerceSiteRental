"""Sets up routes for home component of app"""
from flask import Blueprint

home = Blueprint('home', __name__)

from . import routes
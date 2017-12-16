"""Sets up routes for authentication component of app"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import routes
"""Sets up routes for posts component of app"""
from flask import Blueprint

posts = Blueprint('posts', __name__)

from . import routes
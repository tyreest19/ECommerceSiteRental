"""Sets up routes for posts component of app"""
from flask import Blueprint

payments = Blueprint('payments', __name__)

from . import routes
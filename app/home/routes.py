from app.home import home
from app import db


@home.route('/', methods=['GET', 'POST'])
def home():
    return "Home"
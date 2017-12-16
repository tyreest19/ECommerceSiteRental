from app.posts import posts
from app import db
from flask_login import login_required


@posts.route('/submitpost', methods=['GET', 'POST'])
@login_required
def submitPost():
    return "make a post"

@posts.route('/listing', methods=['GET', 'POST'])
def viewPost():
    return "listings"
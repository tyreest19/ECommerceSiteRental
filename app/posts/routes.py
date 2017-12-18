from app.posts import posts
from app import db
from app.database import create, Items, Users
from app.posts.forms import ItemForm
from flask import redirect, render_template
from flask_login import current_user,login_required
from functools import lru_cache # explanation: https://stackoverflow.com/a/14731729
from time import gmtime, strftime

@posts.route('/submitpost', methods=['GET', 'POST'])
@login_required
def submitPost():
    """
    Handle requests to the /submitpost route
    Allows users to post items
    """
    form = ItemForm()
    print('User Id', get_current_user())
    if form.validate_on_submit():
        itemID = db.session.query(db.func.max(Items.userID)).scalar() + 1
        cost = form.cost.data * 100 # All money will be dealt with as integers for easy storage
        new_item = Items(name=form.name.data, category=form.category.data,
                         description=form.description.data, cost=cost,
                         itemID=itemID, postedDate=strftime("%Y-%m-%d", gmtime()),
                         userID=get_current_user())
        create(new_item)
        return redirect('/listing')
    # load make_post template
    return render_template('make_post.html', form=form, title='Submit Post') #, get_username=get_username)

@posts.route('/listing', methods=['GET', 'POST'])
def viewPost():
    items = Items.query.all()
    categories = get_all_categories()
    return render_template('listing_page.html', items=items, title='Listing', categories=categories,
                           get_username=get_username)

@posts.route('/listing/category-<category>', methods=['GET', 'POST'])
def viewPostByCategory(category):
    items = Items.query.filter_by(category=category)
    categories = get_all_categories()
    title = 'Listings of all ' + category
    return render_template('listing_page.html', items=items, title=title, categories=categories,
                           get_username=get_username)

@lru_cache()
def get_all_categories():
    categories = []
    items = Items.query.all()
    for item in items:
        print('functions on item', item.category)
        if not item.category in categories:
            print("i worked")
            categories.append(item.category)
            print(categories)
    return categories

@lru_cache()
def get_all_items():
    return Items.query.all()

def get_current_user():
    return current_user.get_id() # return userID in get_id()

def get_username(userID):
    return Items.query.filter_by(userID=userID).first().name
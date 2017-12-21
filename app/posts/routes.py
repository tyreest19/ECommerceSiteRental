from app.posts import posts
from app import db
from app import stripe_keys
from app.database import create, Items
from app.posts.forms import ItemForm
from flask import abort, redirect, render_template
from flask_login import login_required
from app.utils import get_all_categories, get_current_user, get_item, get_item_cost, get_user_fname
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
        itemID = db.session.query(db.func.max(Items.itemID)).scalar() + 1
        cost = form.cost.data * 100 # All money will be dealt with as integers for easy storage. All items price in cents
        new_item = Items(name=form.name.data, category=form.category.data,
                         description=form.description.data, cost=cost,
                         itemID=itemID, postedDate=strftime("%Y-%m-%d", gmtime()),
                         userID=get_current_user(), sold=False)
        create(new_item)
        return redirect('/listing')
    # load make_post template
    return render_template('make_post.html', form=form, title='Submit Post') #, get_username=get_username)

@posts.route('/listing', methods=['GET'])
def viewPost():
    items = Items.query.filter_by(sold=False)
    categories = get_all_categories()
    return render_template('listing_page.html', items=items, title='Listing', categories=categories,
                           get_username=get_user_fname)

@posts.route('/listing/category-<category>', methods=['GET'])
def viewPostByCategory(category):
    items = Items.query.filter_by(category=category, sold=False)
    categories = get_all_categories()
    title = 'Listings of all ' + category
    return render_template('listing_page.html', items=items, title=title, categories=categories,
                           get_username=get_user_fname)

@posts.route('/view-item-<itemID>', methods=['GET'])
def viewItem(itemID):
    item = get_item(itemID)
    return render_template('viewItem.html', key=stripe_keys['publishable_key'], item=item,
                           get_item_cost=get_item_cost, get_username=get_user_fname,
                           page_viewer=get_current_user())

@posts.route('/delete-item-<itemID>-<userID>')
@login_required
def deleteItem(itemID, userID):
    """Deletes a row within a table"""
    if int(get_current_user()) == int(userID):
        row = Items.query.get([itemID, userID])
        db.session.delete(row)
        db.session.commit()
        return redirect('/user-page')
    return render_template('404.html')
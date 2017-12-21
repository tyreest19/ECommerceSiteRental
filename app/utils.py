from app import db
from app.database import Users, Items
from flask_login import current_user
from functools import lru_cache # explanation: https://stackoverflow.com/a/14731729

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

def get_user_email(userID):
    return Users.query.filter_by(userID=userID).first().email

def get_item(itemID):
    return Items.query.filter_by(itemID=itemID).first()

def get_item_cost(itemID):
    return Items.query.filter_by(itemID=itemID).first().cost

def get_item_owner(itemID):
    return Items.query.filter_by(itemID=itemID).first().userID

def get_item_name(itemID):
    return Items.query.filter_by(itemID=itemID).first().name

def get_user_fname(userID):
    return Users.query.filter_by(userID=userID).first().fname

def markItemAsSold(itemID):
    """Updates a table\'s row.
        Arguements:
            id: Id for desired row.
        Returns:
            A dictionary containing containing the rows information.
    """
    row = Items.query.filter_by(itemID=itemID).first()
    buyerID = get_current_user()
    data = {'sold': True, 'itemID': itemID, 'userID': Items.query.filter_by(itemID=itemID).first().userID,
            'buyerID': buyerID}
    for k, v in data.items():
        setattr(row, k, v)
    db.session.commit()

import stripe
from app.database import Items
from app import db
from app.payments import payments
from app.database import update, Items
from app.posts.routes import get_current_user
from flask import render_template, request

@payments.route('/process-payment-<itemID>', methods=['POST'])
def processPayment(itemID):
    item = Items.query.filter_by(itemID=itemID).first()
    amount = item.cost
    customer = stripe.Customer.create(
            email='tyreestevenson@gmail.com',
            source=request.form['stripeToken']
        )
    charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='You purchased a ' + item.name + ' from sneakpeeksp.com'
        )
    markItemAsSold(itemID)
    return render_template('charge.html', amount=amount)

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



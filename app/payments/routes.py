import stripe
from app.payments import payments
from app.database import update, Items
from flask import render_template, request
from app.utils import markItemAsSold
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




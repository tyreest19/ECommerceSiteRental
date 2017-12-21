import stripe
from app import mail
from app.payments import payments
from app.database import update, Items
from app.utils import get_item_name, get_item_owner, get_user_email, get_user_fname, markItemAsSold
from flask import render_template, request
from flask_login import login_required
from flask_mail import Message

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

@payments.route('/rent-<requesterID>-<itemID>-<ownerID>-<itemName>', methods=['GET', 'POST'])
@login_required
def requestRental(requesterID, itemID, ownerID, itemName):
    #Validate recpient email
    requesterFname = get_user_fname(requesterID)
    ownerEmail = get_user_email(ownerID)
    message = Message('Shoe Rental Request', sender='tyreeostevenson@gmail.com',
                      recipients=[ownerEmail],
                      body = requesterFname + " Wants to rent your shoe " + itemName)
    mail.send(message)
    return 'Success'

@payments.route('/rent-<requesterID>-<itemID>-<ownerID>-<itemName>', methods=['GET', 'POST'])
@login_required
def requestRental(requesterID, itemID, ownerID, itemName):
    #Validate recpient email
    requesterFname = get_user_fname(requesterID)
    ownerEmail = get_user_email(ownerID)
    message = Message('Shoe Rental Request', sender='tyreeostevenson@gmail.com',
                      recipients=[ownerEmail],
                      body = requesterFname + " Wants to rent your shoe " + itemName)
    mail.send(message)
    return 'Success'
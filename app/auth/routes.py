import datetime
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from app.auth.forms import LoginForm, RegistrationForm

from app.auth import auth
from app import db
from app.database import create, Users


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an User to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        userID = db.session.query(db.func.max(Users.userID)).scalar() + 1
        new_user = Users(fname=form.first_name.data, lname=form.last_name.data,
                                             username=form.username.data, email=form.email.data,
                                             password=form.password.data, address=form.address.data,
                                             userID=userID,
                                             birthdate=datetime.date(form.year.data, form.month.data,
                                                                        form.day.data))
        create(new_user)
        return redirect('/login')
    # load registration template
    return render_template('registration_page.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an User in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log employee in
            login_user(user)

            # redirect to the dashboard page after login COMING SOON
            return 'success'

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('login_page.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an User out through the logout link
    """
    logout_user()

    # redirect to the login page
    return redirect('/login')
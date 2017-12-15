from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager



def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    return data

# FlaskSql datatypes http://docs.sqlalchemy.org/en/latest/core/type_basics.html

class User(db.Model):
    """This table represents the user"""
    __tablename__ = "User"
    fname = db.Column(db.VARCHAR(100))
    lname = db.Column(db.VARCHAR(100))
    username = db.Column(db.VARCHAR(100))
    password = db.Column(db.VARCHAR(100))
    address = db.Column(db.VARCHAR(100))
    email = db.Column(db.VARCHAR(100))
    birthdate = db.Column(db.DATE())
    userID = db.Column(db.Integer, primary_key=True)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password = password

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return password # Will figure out later check_password_hash(self.password_hash, password)

    def __repr__(self):
        "[" \
        "fname: {fname}," \
        "lname: {lname}," \
        "username: {username}," \
        "email: {email}," \
        "password: {password}," \
        "address: {address}," \
        "birthdate: {birthdate}," \
        "userID: {userID}," \
        "]".format(fname=self.fname, lname=self.lname, username=self.username,
                   email=self.email, password=self.password, address=self.address,
                   userID=self.userID)


class SignUpTable(db.Model):
    """This class represents the Signup table."""
    __tablename__ = "SignUpTable"
    twitterHandle = db.Column(db.VARCHAR(100))
    instagramHandle = db.Column(db.VARCHAR(100))
    signupID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(255))
    pintrestHandle = db.Column(db.VARCHAR(100))
    tumblrHandle = db.Column(db.VARCHAR(100))
    youtubeHandle = db.Column(db.VARCHAR(100))

    def __repr__(self):
        return "[" \
               "twitterHandle: {twitterHandle}," \
               "instagramHandle: {instagramHandle}," \
               "signupID: {signupID}," \
               "email: {email}," \
               "tumblrHandle: {tumblrHandle}," \
               "pintrestHandle: {pintrestHandle}," \
               "youtubeHandle: {youtubeHandle}," \
               "]".format(twitterHandle=self.twitterHandle, instagramHandle=self.instagramHandle,
                          signupID=self.signupID, email=self.email, pintrestHandle=self.pintrestHandle,
                          tumblrHandle=self.tumblrHandle, youtubeHandle=self.youtubeHandle)
    def returnAsDict(self):
        return {
            "twitterHandle": self.twitterHandle,
            "instagramHandle": self.instagramHandle,
            "signupID": self.signupID,
            "email": self.email,
            "pintrestHandle": self.pintrestHandle,
            "tumblrHandle": self.tumblrHandle,
            "youtubeHandle": self.youtubeHandle
        }

def create(table, data):
    """Adds row to a table.
        Arguements:
            table: Pass in the reference to the desired table object above.
            data: Pass in dictionary containing the values for the row.
        Returns:
            A dictionary containing containing the rows information.
    """
    row = table(**data)
    db.session.add(row)
    db.session.commit()
    return from_sql(row)

def create_database(app):
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
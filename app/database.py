from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    return data

# FlaskSql datatypes http://docs.sqlalchemy.org/en/latest/core/type_basics.html

class Users(UserMixin, db.Model):
    """This table represents the user"""
    __tablename__ = "Users"
    fname = db.Column(db.VARCHAR(100))
    lname = db.Column(db.VARCHAR(100))
    username = db.Column(db.VARCHAR(100))
    password = db.Column(db.VARCHAR(100))
    address = db.Column(db.VARCHAR(100))
    email = db.Column(db.VARCHAR(100))
    birthdate = db.Column(db.DATE())
    userID = db.Column(db.Integer, primary_key=True)

    # @property
    # def password(self):
    #     """
    #     Prevent pasword from being accessed
    #     """
    #     raise AttributeError('password is not a readable attribute.')
    #
    # @password.setter
    # def password(self, password):
    #     """
    #     Set password to a hashed password
    #     """
    #     self.password = password
    #
    def get_id(self):
        """Needed to overirde feature of parent class"""
        return self.userID

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return True # Will figure out later check_password_hash(self.password_hash, password)

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

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


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


def read(table, id):
    """Reads a row from desried table within the SaveMeTime database
        Arguements:
            table: Pass in the reference to the desired table object above.
            id: Id for desired row.
        Returns:
            A dictionary containing containing the rows information.
    """
    result = table.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]

def search(table, **kwargs):
    new_dict = {}
    for key in kwargs.keys():
        if kwargs[key] != '':
            new_dict[key] = kwargs[key]
    list_of_results = []
    for result in table.query.filter_by(**new_dict).all():
        list_of_results.append(result.returnAsDict())
    return list_of_results

# [START create]
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
# [END create]


# [START update]
def update(table, id, data):
    """Updates a table\'s row.
        Arguements:
            table: Pass in the reference to the desired table object above.
            id: Id for desired row.
            data: Pass in dictionary containing the values for the row.
        Returns:
            A dictionary containing containing the rows information.
    """
    row = table.query.get(id)
    for k, v in data.items():
        setattr(row, k, v)
    db.session.commit()
    return from_sql(row)

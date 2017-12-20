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

class Items(db.Model):
    """This class represents the Items table."""
    __tablename__ = "Items"
    postedDate = db.Column(db.DATE())
    itemID = db.Column(db.Integer, primary_key=True)
    buyerID = db.Column(db.Integer)
    userID = db.Column(db.Integer, db.ForeignKey('Users.userID'), primary_key=True)
    name = db.Column(db.VARCHAR(100))
    category = db.Column(db.VARCHAR(100))
    cost = db.Column(db.Integer)
    description = db.Column(db.TEXT())
    sold = db.Column(db.BOOLEAN)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

def read(table, id):
    """Reads a row from desried table within the database
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

# [START create]
def create(new_row):
    """Adds row to a table.
        Arguements:
            new_row: New object of the containing the values of the new row that you wish to add to the database.
        Example:
            new_user = Users(enter data)
            create(new_user)
        Returns:
            A dictionary containing containing the rows information.
    """
    db.session.add(new_row)
    db.session.commit()
    return from_sql(new_row)
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

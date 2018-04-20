from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from app import db



class User(db.Model):

    """This class represents the users table."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    businesses = db.relationship('Business', order_by='Business.id', cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        db.create_all()
    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def reset_password(self, new_password):
        self.password = Bcrypt().generate_password_hash(new_password).decode()
        return True

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=55),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                'hard to guess string',
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, 'hard to guess string')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"



class Business(db.Model):

    """This class represents the business table."""

    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    category = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews = db.relationship('Review', backref='businesses', order_by='Review.id', cascade="all, delete-orphan")

    def __init__(self, name, category, location, description, user_id):
        self.name = name
        self.category = category
        self.location = location
        self.description = description
        self.user_id = user_id
        db.create_all()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def get_businesses(page, limit, search_string, filters):
        """ returns all businesses"""       

        result = Business.query

        if search_string is not None:
            result = result.filter(Business.name.like("%"+search_string+"%"))

        if bool(filters):
            result = result.filter_by(**filters)

        paginate = result.paginate(page, limit, False)

        businesses = paginate.items
        output = []
        for business in businesses:
            business_object = {
                'id':business.id,
                'name':business.name,
                'category':business.category,
                'location':business.location,
                'description':business.description
            }
            output.append(business_object)
        next_page = paginate.next_num \
            if paginate.has_next else None
        prev_page = paginate.prev_num \
            if paginate.has_prev else None
        if len(output) > 0:
            return {"success":True, "businesses":output, "next_page":next_page, "prev_page":prev_page}
        return {"success":False, "businesses":output}
    @staticmethod
    def get_all():
        return Business.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    # represents the object instance of the model whenever it is queries.
    def __repr__(self):
        return "<Business: {}>".format(self.name)

class Review(db.Model):

    """This class represents the Review table."""

    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    businessId = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    def __init__(self, description, businessId):
        self.description = description
        self.businessId = businessId
        db.create_all()

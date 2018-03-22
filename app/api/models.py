from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from app import db



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(60))
    businesses = db.relationship('Business', backref='user',
                                 lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        db.create_all()

class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    category = db.Column(db.String(60),  nullable=False)
    location = db.Column(db.String(60),  nullable=False)
    description = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews = db.relationship('Review', backref='business',
                                 lazy='dynamic')
    def __init__(self, name, category, location, description, user_id):
        self.name = name
        self.category = category
        self.location = location
        self.description = description
        self.user_id = user_id
        db.create_all()

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    businessId = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    def __init__(self, description, businessId):
        self.description = description
        self.businessId = businessId
        db.create_all()

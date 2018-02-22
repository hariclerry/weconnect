"""This module defines the application endpoints"""

import uuid
from flask import request, jsonify, url_for, session
from app import user_object, business_object, review_object
from . import main



@main.route('/')
def index():
	"""A route to render the home page"""



@main.route('/api/v1/auth/signup', methods=['GET', 'POST'])
def signup():
	"""A route to handle user registration"""
    
	

@main.route('/api/v1/auth/login', methods=['GET', 'POST'])
def signin():
	"""A route to render the login page and log in a user"""
	

@main.route('/api/v1/logout')
def logout():
	"""A route to logout and remove a user from the session"""
	
@main.route('/api/v1/newbusiness',  methods=[ 'POST'])

def create_business():
	"""A route to render a page for registering businesses"""
	
    

@main.route('/api/v1/businesses', methods=['GET'])

def view_businesses():
	"""A route to return all the registered businesses available"""



@main.route('/api/v1/businesses/<businessid>/edit', methods=['PUT'])

def update_business(businessid):
	"""A route to handle business updates"""

@main.route('/api/v1/businesses/mybusinesses')

def my_businesses():
	"""This route returns businesses belonging to a specific user"""

	
@main.route('/api/v1/businesses/<businessid>/delete', methods=['DELETE'])

def delete_businesses(businessid):
	"""A route to handle deletion of businesses"""
	
	
@main.route('/api/v1/business/<businessid>/review', methods=['POST'])

def addreview(businessid):
	"""A route for user to add review on a particular business"""


@main.route('/api/v1/business/<businessid>/viewreviews', methods=["GET"])

def viewreviews(businessid):
	"""A route to return all the the reviews for a specific business"""


@main.route('/api/v1/auth/resetpass', methods=['PUT'])
def reset_pass():
	"""Route to reset user password"""


@main.route('/api/v1/searchbusinesses', methods=['POST'])
def search_businesses():
	"""A route to search businesses depending on the business category or location"""


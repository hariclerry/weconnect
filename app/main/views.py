"""This module defines the application endpoints"""

import uuid
from flask import request, jsonify, url_for, session, make_response
from functools import wraps
from app import user_object, business_object, review_object
from . import main
import jwt
import datetime


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, 'hard to guess string')
            for user in user_object.user_list:
                if user.get("username"):
                    current_user = user['username']= data['username']
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated





@main.route('/')
def index():
	"""A route to render the index endpoint"""
	return jsonify({'message': 'Welcome to WeConnect'})



@main.route('/api/v1/auth/signup', methods=['GET', 'POST'])
def signup():
	"""A route to handle user registration"""
	if request.method == 'POST':
		data = request.get_json()
		username = data['username']
		email = data['email']
		password = data['password']
		cnfpassword = data['cnfpassword']
		
		for user in user_object.user_list:
				if user['username'] == data['username']  or user['email'] == data['email']:
					jsonify({'message': 'User already exists'})
		#pass the details to the register method
		try:
			res = user_object.register(username, email, password, cnfpassword)
			if res == "Registration successful":
				return jsonify(response=res), 201
			else:
				return jsonify(response=res), 409
		except Exception as e:
			response = {
                'message': str(e)
            }
			return make_response(jsonify(response)), 500
	return jsonify(response="Get request currently not allowed"), 405

    
	
@main.route('/api/v1/auth/login', methods=['GET', 'POST'])
def signin():
	"""A route to render the login page and log in a user"""
	if request.method == 'POST': # POST request with valid input
		data = request.get_json()
		username = data['username']
		password = data['password']
		res = user_object.login(username, password)
		if res == "successful":
			token = jwt.encode({'username' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'hard to guess string')
			return jsonify({'token' : token.decode()})
		return res
	return jsonify(response="Get request currently not allowed"), 405
		
			               
            	

@main.route('/api/v1/logout')
def logout():
	"""A route to logout and remove a user from the session"""
	
@main.route('/api/v1/newbusiness',  methods=[ 'POST'])

def create_business():
	"""A route to handle registering businesses"""
	business_data = request.get_json()
	name = business_data['name']
	category = business_data['category']
	location = business_data['location']
	description = business_data['description']
	# createdby = current_user
	for business in business_object.business_list:
		if business['name'] ==  business_data['name'] and business['location'] ==  business_data['location']:
			jsonify("Business already Exist")
	res = business_object.create(name, category, location, description)
	if res == "business created":
		return jsonify(response=res), 201
	else:
		 return jsonify(response=res), 409
		

@main.route('/api/v1/businesses', methods=['GET'])

def view_businesses():
	"""A route to return all the registered businesses available"""
	businesses = business_object.view_all()
	return jsonify(businesses), 200



@main.route('/api/v1/businesses/<businessid>/edit', methods=['PUT'])

def update_business(businessid):
	"""A route to handle business updates"""
	businessid = uuid.UUID(businessid)
	business_data = request.get_json()
	name = business_data['name']
	category = business_data['category']
	location = business_data['location']
	description = business_data['description']
	# createdby =  business_data['createdby']
	res = business_object.update(businessid, name, category, location, description)
	if res == "update successful":
			return jsonify(response=res), 200
	elif res == "no event with given id":
			return jsonify(response=res), 404
	else:
			return jsonify(response=res), 409


@main.route('/api/v1/businesses/mybusinesses')

def my_businesses():
	"""This route returns businesses belonging to a specific user"""
	# username = session['username']
	# businesses = business_object.createdby_filter(username)

	
@main.route('/api/v1/businesses/<businessid>/delete', methods=['DELETE'])

def delete_businesses(businessid):
	"""A route to handle deletion of businesses"""
	businessid = uuid.UUID(businessid)
	res = business_object.delete(businessid)
	if res == "deleted":
		return jsonify(response="business deleted"),  204
	return jsonify(response=res), 404
	
	
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


"""This module defines the application endpoints"""

import uuid
from flask import request, jsonify, url_for, session, make_response, abort
from functools import wraps
from app import user_object, business_object, review_object
from . import main
import jwt
import datetime
import re


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
		data = request.get_json() #passes in json data to the variable called data
		username = data['username']
		email = data['email']
		password = data['password']
		cnfpassword = data['cnfpassword']
		if username.strip() == "" or not username.isalpha():
			error = {"message": "Invalid name"}
			return jsonify(error)
		if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
			error = {"message": "Invalid Email"}
			return jsonify(error)
		if password.strip() == "" or not password.isalpha():
			error = {"message": "Invalid password"}
			return jsonify(error)
		if password != cnfpassword:
			error = {"message": "password do not match"}
			return jsonify(error)
		
		for user in user_object.user_list:
				if user['username'] == data['username']  or user['email'] == data['email']:
					jsonify({'message': 'User already exists'})
		#pass the details to the register method
		res = user_object.register(username, email, password, cnfpassword)
		if res == "Registration successful":
			return jsonify(response=res), 201
	# return jsonify(response="Get request currently not allowed"), 405

    
	
@main.route('/api/v1/auth/login', methods=['GET', 'POST'])
def signin():
	"""A route to render the login page and log in a user"""
	if request.method == 'POST': # POST request with valid input
		data = request.get_json()
		username = data['username']
		password = data['password']
		res = user_object.login(username, password)
		if res == "successful":
			for user in user_object.user_list:
				if user['username'] == data["username"]:
					session['userid'] = user['id']
					session['username'] = username
					# return jsonify(response="Login Successful"), 200
					token = jwt.encode({'username' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'hard to guess string',algorithm="HS256")
					return jsonify({'token' : token.decode()})
		# return res
	return jsonify(response="wrong username or password"), 404
		
			               
            	

@main.route('/api/v1/auth/logout', methods=[ 'POST'])
@token_required
def logout( current_user):
	"""A route to logout and remove a user from the session"""
	if not  current_user:
		abort(404)
	session.pop('userid')
	session.pop('username')
	return jsonify("successfully logged out"), 200
	
@main.route('/api/v1/businesses',  methods=[ 'POST'])
@token_required
def create_business(current_user):
	"""A route to handle registering businesses"""
	if not  current_user:
		abort(404)
	business_data = request.get_json() # sent data from postman is converted to a python dictionary
	name = business_data['name']
	category = business_data['category']
	location = business_data['location']
	description = business_data['description']
	createdby = current_user

	if name.strip() == "" or not name.isalpha():
		message = {"message": "invalid name"}
		return jsonify(message)
	if category.strip() == "" or not category.isalpha():
		message = {"message": "invalid category"}
		return jsonify(message)
	if location.strip() == "" or not location.isalpha():
		message = {"message": "invalid location"}
		return jsonify(message)
	if description.strip() == "" or not description.isalpha():
		message = {"message": "invalid description"}
		return jsonify(message)
            
	for business in business_object.business_list:
		if business['name'] ==  business_data['name'] and business['location'] ==  business_data['location']:
			jsonify("Business already Exist")
	res = business_object.create(name, category, location, description, createdby)
	if res:
		respond = {
			"success": True,
			"message": "business created successfully",
			"Data" : {
				"business info": business_data
			}
		}
		return jsonify(response=respond), 201
	else:
		respond = {
			"success": False,
			"message": "business not created",
		}

		return jsonify(response=respond), 409 
		

@main.route('/api/v1/businesses', methods=['GET'])
@token_required
def view_businesses(current_user):
	"""A route to return all the registered businesses available"""
	if not  current_user:
		abort(404)
	businesses = business_object.view_all()
	if businesses:
		respond = {
			"success": True,
			"message": "businesses successfully retrieved",
			"Data" : {
				"business info": businesses
			}
		}
		return jsonify(response=respond), 200

@main.route('/api/v1/businesses/<businessid>', methods=['GET'])
@token_required
def single_businesses(current_user, businessid):
	"""This route returns a single business"""
	if not  current_user:
		abort(404)
	business = business_object.find_by_id(businessid)
	if business:
		respond = {
			"success": True,
			"message": "business successful",
			"Data" : {
				"business info": business
			}
		}
		return jsonify(respones=respond), 200
	return jsonify("no business with such id found"), 404

@main.route('/api/v1/businesses/<businessid>', methods=['PUT'])
@token_required
def update_business(current_user, businessid):
	"""A route to handle business updates"""
	if not  current_user:
		abort(404)
	businessid = uuid.UUID(businessid)
	business_data = request.get_json()
	name = business_data['name']
	category = business_data['category']
	location = business_data['location']
	description = business_data['description']
	createdby =  business_data['createdby']

	if name.strip() == "" or not name.isalpha():
		message = {"message": "invalid name"}
		return jsonify(message)
	if category.strip() == "" or not category.isalpha():
		message = {"message": "invalid category"}
		return jsonify(message)
	if location.strip() == "" or not location.isalpha():
		message = {"message": "invalid location"}
		return jsonify(message)
	if description.strip() == "" or not description.isalpha():
		message = {"message": "invalid description"}
		return jsonify(message)

	res = business_object.update(businessid, name, category, location, description, createdby)
	if res == "update successful":
			return jsonify(response=res), 200
	elif res == "no event with given id":
			return jsonify(response=res), 404
	else:
			return jsonify(response=res), 409

	
@main.route('/api/v1/businesses/<businessid>', methods=['DELETE'])
@token_required
def delete_businesses(current_user, businessid):
	"""A route to handle deletion of businesses"""
	if not  current_user:
		abort(404)
	businessid = uuid.UUID(businessid)
	res = business_object.delete(businessid)
	if res == "deleted":
		return jsonify(response="business deleted"), 200
	return jsonify(response=res), 404
	
	
@main.route('/api/v1/business/<businessid>/review', methods=['POST', 'GET'])
@token_required
def addreview(current_user, businessid):
	"""A route for user to add review on a particular business"""
	if not  current_user:
		abort(404)
	businessid = uuid.UUID(businessid)
	if request.method == 'POST': # POST request with valid input
		review_data = request.get_json()
		add_review = review_data['add_review']

		if add_review.strip() == "" or not add_review.isalpha():
			message = {"message": "invalid review"}
			return jsonify(message)

		if not business_object.find_by_id(businessid):
			return jsonify(response="can not add review to a non existing business"), 404
		else:
			res = review_object.create(businessid, add_review)
			if res == "review success":
				return jsonify(response=res), 200
			else:
				return jsonify("You have already added review for this business")

	if request.method == 'GET':
		reviews = review_object.view_reviews(businessid)
		return jsonify(reviews), 200


@main.route('/api/v1/auth/resetpass', methods=['PUT'])
def reset_pass():
	"""Route to reset user password"""



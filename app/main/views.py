"""This module defines the application endpoints"""

import uuid
from flask import request, jsonify, url_for, session, make_response, abort
from functools import wraps
from app import user_object, business_object, review_object
from . import main
import jwt
import datetime
import re
from flasgger import swag_from


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






@main.route('/api/v1/auth/signup', methods=['GET', 'POST'])
@swag_from('../api_docs/signup.yml')
def signup():
	if request.method == 'POST':
		#passes in json data to the variable called data
		data = request.get_json() 
		username = data['username']
		email = data['email']
		password = data['password']
		cnfpassword = data['cnfpassword']
		if username.strip() == "":
			error = {"message": "Invalid name"}
			return jsonify(error)
		if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
			error = {"message": "Invalid Email"}
			return jsonify(error)
		if password.strip() == "":
			error = {"message": "Invalid password"}
			return jsonify(error)
		if len(password) < 4:
			error = {"message": "Password too short"}
			return jsonify(error)
		if password != cnfpassword:
			error = {"message": "password do not match"}
			return jsonify(error)
		
		for user in user_object.user_list:
				if user['username']  == username  or  user['email'] == email :
					return jsonify({'message': 'User already exists'})
		#pass the details to the register method
		res = user_object.register(username, email, password, cnfpassword)
		if res:
			respond = {
			"success": True,
			"message": "Registration successful",
			"Data" : data
		     }
			return jsonify(response=respond), 201
		else:
			respond = {
			"success": False,
			"message": "Registration not successful",
		    }
			return jsonify(response=respond), 409 
			# {"message": "User created", "id": 10}

    
	
@main.route('/api/v1/auth/login', methods=['GET', 'POST'])
def signin():
	"""Endpoint for handling user login """
	if request.method == 'POST': # POST request with valid input
		data = request.get_json()
		username = data['username']
		password = data['password']
		res = user_object.login(username, password)
		if res:
			for user in user_object.user_list:
				if user['username'] == data["username"]:
					session['userid'] = user['id']
					session['username'] = username
					# return jsonify(response="Login Successful"), 200
					token = jwt.encode({'username' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'hard to guess string',algorithm="HS256")
					respond = {
			                    "success": True,
			                    "message": "Registration successful",
			                    "Token" : token.decode()
		                    }
					return jsonify(response=respond), 201
	return jsonify(response="wrong username or password"), 400
		
	
@main.route('/api/v1/businesses',  methods=[ 'POST'])
@token_required
def create_business(current_user):
	"""Endpoint for handling businesses registration """
	if not  current_user:
		abort(404)
	business_data = request.get_json() # sent data from postman is converted to a python dictionary
	name = business_data['name']
	category = business_data['category']
	location = business_data['location']
	description = business_data['description']
	createdby = session['username']

	if name == "":
		message = {"message": "invalid name"}
		return jsonify(message)
	if category == "":
		message = {"message": "invalid category"}
		return jsonify(message)
	if location == "":
		message = {"message": "invalid location"}
		return jsonify(message)
	if description == "":
		message = {"message": "invalid description"}
		return jsonify(message)
            
	for business in business_object.business_list:
		if business['name'] ==  business_data['name'] or business['location'] ==  business_data['location']:
			return jsonify("Business already Exist")
	res = business_object.create(name, category, location, description, createdby)
	if res:
		respond = {
			"success": True,
			"message": "business created successfully",
			 "Business": business_data

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
	"""Endpoint for returning all the registered businesses """
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
	"""Endpoint for returning a single business"""
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
	"""Endpoint for handling business updates"""
	if not  current_user:
		abort(404)
	businessid = uuid.UUID(businessid)
	business_data = request.get_json()
	name = business_data['name']
	category = business_data['category']
	location = business_data['location']
	description = business_data['description']
	createdby =  session['username']

	if name.strip() == "" or not name.isalpha():
		message = {"message": "invalid name"}
		return jsonify(message)
	if category.strip() == "" or not category.isalpha():
		message = {"message": "invalid category"}
		return jsonify(message)
	if location.strip() == "" or not location.isalpha():
		message = {"message": "invalid location"}
		return jsonify(message)
	if description == "":
		message = {"message": "invalid description"}
		return jsonify(message)

	res = business_object.update(businessid, name, category, location, description, createdby)
	if res:
		respond = {
			"success": True,
			"message": "business created successfully",
			"Data" : { "Business": business_data
			}
		    }
		return jsonify(response=respond), 200
			
	elif res == "no business with given id":
			return jsonify(response=respond), 404
	else:
			return jsonify(response=respond), 409

	
@main.route('/api/v1/businesses/<businessid>', methods=['DELETE'])
@token_required
def delete_businesses(current_user, businessid):
	"""Endpoint for handling deletion of businesses"""
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
	"""Endpoint for user to add review on a particular business"""
	if not  current_user:
		abort(404)
	businessid = uuid.UUID(businessid)
	if request.method == 'POST': # POST request with valid input
		review_data = request.get_json()
		add_review = review_data['add_review']

		if add_review == "":
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

@main.route('/api/v1/auth/logout', methods=[ 'POST'])
@token_required
def logout( current_user):
	"""Endpoint for logging out and removing a user from the session"""
	if not  current_user:
		abort(404)
	session.pop('userid')
	session.pop('username')
	return jsonify("successfully logged out"), 200


@main.route('/api/v1/auth/resetpass', methods=['PUT'])
def reset_pass():
	"""Endpoint for user password  reset"""
	user_data = request.get_json()
	email =  user_data['email']
	new_password = user_data['new_password']
	res = user_object.reset_pass(email, new_password)
	if res:
		for user in user_object.user_list:
			if user.email == email:
				user.password = new_password
				return jsonify('password reset, now login'), 200
	return jsonify("password not reset")

  
   


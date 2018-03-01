"""This module defines the application endpoints"""

import uuid
from flask import request, jsonify, url_for, session, make_response, abort
from flasgger import swag_from
from functools import wraps
import jwt
import datetime
import re
from app import user_object, business_object, review_object
from . import main



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        current_user = ""

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is required!'}), 401

        try: 
            data = jwt.decode(token, 'hard to guess string')
            for user in user_object.user_list:
                if user.get("username"):
                    current_user = user['username']= data['username']
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated






@main.route('/api/v1/auth/signup', methods=['POST'])
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
			return jsonify(respond), 201
		else:
			respond = {
			"success": False,
			"message": "Registration not successful",
		    }
			return jsonify(respond), 409 
		   
	
@main.route('/api/v1/auth/login', methods=['POST'])
@swag_from('../api_docs/signin.yml')
def signin():

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
			                    "message": "Login successful",
			                    "Token" : token.decode()
		                    }
					return jsonify(respond), 200
	return jsonify(response="Wrong Username or Password"), 401
		
	
@main.route('/api/v1/businesses',  methods=[ 'POST'])
@token_required
@swag_from('../api_docs/register_business.yml')
def register_business(current_user):
	if not  current_user:
		abort(404)
	business_data = request.get_json() # sent data from postman is converted to a python dictionary
	name = business_data['name'].strip()
	category = business_data['category'].strip()
	location = business_data['location'].strip()
	description = business_data['description'].strip()
	createdby =  business_data['createdby'].strip()

	if name == "":
		message = {"message": "Invalid name"}
		return jsonify(message)
	if category == "":
		message = {"message": "Invalid category"}
		return jsonify(message)
	if location == "":
		message = {"message": "Invalid location"}
		return jsonify(message)
	if description == "":
		message = {"message": "Invalid description"}
		return jsonify(message)
	if createdby == "":
		message = {"message": "Invalid input"}
		return jsonify(message)
            
	for business in business_object.business_list:
		if business['name'] ==  business_data['name'] or business['location'] ==  business_data['location']:
			return jsonify("Business already Exist"), 409
	res = business_object.create(name, category, location, description, createdby)
	if res:
		respond = {
			"Success": True,
			"Message": "Business created successfully",
			 "Data": business_data

		}
		return jsonify(respond), 201
	else:
		respond = {
			"success": False,
			"message": "Business not created",
		}

		return jsonify(respond), 409 
		

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
			"message": "Businesses successfully retrieved",
			"Data": businesses
		    }
		return jsonify(respond), 200
	else:
		respond = {
			"success": False,
			"message": "There is no business registered yet"
		}

		return jsonify(respond),  200

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
			"message": "Business successful",
			"Data" : business
			
		}
		return jsonify(respond), 200

	else:
		respond = {
			"success": False,
			"message": "No business with such id found"
		}
		return jsonify(respond), 404

@main.route('/api/v1/businesses/<businessid>', methods=['PUT'])
@token_required
def update_business(current_user, businessid):
	"""Endpoint for handling business updates"""
	if not  current_user:
		abort(404)
	businessid = uuid.UUID(businessid)
	business_data = request.get_json()
	name = business_data['name'].strip()
	category = business_data['category'].strip()
	location = business_data['location'].strip()
	description = business_data['description'].strip()
	createdby =  business_data['createdby'].strip()

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
	if createdby == "":
		message = {"message": "invalid input"}
		return jsonify(message)

	res = business_object.update(businessid, name, category, location, description, createdby)
	if res:
		respond = {
			"success": True,
			"message": "Business updated successfully",
			"Business": business_data
		    }
		return jsonify(respond), 200
			
	else:
		respond = {
			"success": False,
			"message": "No business with given id"
		    }
		return jsonify(respond), 404
# return jsonify("business not updated"), 409

	
@main.route('/api/v1/businesses/<businessid>', methods=['DELETE'])
@token_required
def delete_businesses(current_user, businessid):
	"""Endpoint for handling deletion of businesses"""
	if not  current_user:
		abort(404)
	businessid = uuid.UUID(businessid)
	res = business_object.delete(businessid)
	if res:
		respond = {
			"success": True,
			"message": "Business deleted"
		    }
		return jsonify(respond), 200
			
	else:
		respond = {
			"success": False,
			"message": "No business with given id"
		    }
		return jsonify(respond), 404
	
	
@main.route('/api/v1/business/<businessid>/review', methods=['POST', 'GET'])
@token_required
def addreview(current_user, businessid):
	"""Endpoint for user to add review on a particular business"""
	if not  current_user:
		abort(404)
	# businessid = uuid.UUID(businessid)
	if request.method == 'POST': # POST request with valid input
		review_data = request.get_json()
		review = review_data['add_review'].strip()

		if review == "":
			message = {"message": "Invalid review"}
			return jsonify(message)

		if not business_object.find_by_id(businessid):
			return jsonify(response="Can not add review to a non existing business"), 404
		else:
			res = review_object.create(businessid, review)
			if res:
				respond = {
			                "success": True,
			                "message": "Review added successfully"
		                  }
				return jsonify(respond), 201
			else:
				respond = {
			                "Success": False,
			                "Message": "You have already added review for this business"
		                      }
				return jsonify(respond), 409
				

	if request.method == 'GET':
		reviews = review_object.view_reviews(businessid)
		if reviews:
			respond = {
			            "Success": True,
			            "Message": "Reviews for this particular business",
						 "Data": review_data
		                  }
			return jsonify(respond), 200
		else:
			respond = {
			                "Message": "No review added yet"
		         }
			return jsonify(respond), 200

@main.route('/api/v1/auth/logout', methods=[ 'POST'])
@token_required
def logout( current_user):
	"""Endpoint for logging out and removing a user from the session"""
	if not  current_user:
		abort(404)
	session.pop('userid')
	session.pop('username')
	return jsonify("Successfully logged out"), 200


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
				return jsonify('Password reset, now login'), 200
	return jsonify("Password not reset")

  
   


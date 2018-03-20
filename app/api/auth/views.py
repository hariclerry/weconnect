"""This module defines the application endpoints"""

import uuid
from flask import request, jsonify, url_for, session, make_response, abort
from flasgger import swag_from
from functools import wraps
import jwt
import datetime
import re
from app import user_object, business_object, review_object
from . import auth



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




@auth.route('/api/auth/register', methods=['POST'])
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
			"message": "User already exists",
		    }
			return jsonify(respond), 409 
		   
	
@auth.route('/api/auth/login', methods=['POST'])
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
		
	
@auth.route('/api/auth/logout', methods=[ 'POST'])
@swag_from('../api_docs/user_logout.yml')
@token_required
def logout(current_user):
        if 'access_token' in request.headers:
            token = request.headers['access_token']
            token = None
            return jsonify({'message':"Successfully logged out"}), 200
        return make_response(("Token required"), 499)


@auth.route('/api/auth/reset-password', methods=['PUT'])
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

  
   


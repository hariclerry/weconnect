"""This module defines the application endpoints"""

from flask import request, jsonify, url_for, session, make_response, abort
import jwt
import random
from flasgger import swag_from
from functools import wraps
import datetime
import re
from . import auth
from app import db, models
from app.api.models import User





def token_required(funct):
    @wraps(funct)
    def decorated_funct(*args, **kwargs):
        token = None
        if 'access_token' in request.headers:
            token = request.headers['access_token']
            if not token:
                return jsonify({"message":"Token is missing"}), 401
            try:
                data = jwt.decode(token, 'hard to guess string')
                user = User.query.filter_by(id=data['sub']).first()
                current_user = user
            except:
                return jsonify({"message":"Token is invalid"}), 401
            return funct(current_user, *args, **kwargs)
        else:
            return jsonify({"error": "Token required"}), 401
    return decorated_funct

@auth.route('/api/auth/register', methods=['POST'])
@swag_from('../api_docs/signup.yml')
def signup():

	"""This Endpoint handles registration of  new users."""

	data = request.get_json()
    # Query to see if the user already exists
	user = User.query.filter_by( email = data['email']).first()

	if user:
		respond = {
                        'message': 'User already exists. Please login'
                    }
		return make_response(jsonify(respond)), 409

	# if there is no user with such email address, register the new user
	user = User(data['username'], data['email'], data['password'])
	user.save()
	respond = {
			"success": True,
			"message": "Registration successful. Please login",
			"Data" : data
		     }
	return jsonify(respond), 201

@auth.route('/api/auth/login', methods=['POST'])
@swag_from('../api_docs/signin.yml')
def signin():
    
	"""This Endpoint handles user login and access token generation."""

	data = request.get_json()
	
	# Get the user object using their email (unique to every user)
	user = User.query.filter_by( email = data['email']).first()
	# Try to authenticate the found user using their password
	if user and user.password_is_valid(data['password']):
		# Generate the access token. This will be used as the authorization header
		access_token = user.generate_token(user.id)
		if access_token:
				respond = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
				return make_response(jsonify(respond)), 200
		
	# User does not exist. Therefore, return an error message
	else:
		respond = {
                    'message': 'Invalid email or password, Please try again'
                }
		return make_response(jsonify(respond)), 401

@auth.route('/api/auth/reset_password', methods = ['POST'])
# @swag_from('../api-docs/v1/reset_password.yml')
@token_required
def reset_password(current_user):

    data = request.get_json()
    if not data['email'] or not data['old_password'] or not data['new_password']:
        return make_response(("Fill all credentials"),401)
    user = models.User.query.filter_by(email = data['email']).first()
    if not user:
        return make_response(("Wrong email"), 401)
    else:
        if user.password_is_valid(user.password):
            user.password = data['new_password']
            return make_response(("Successfully changed password"), 200)
        return make_response(("Input correct old password"), 401)

      


@auth.route('/api/auth/logout', methods = ['POST'])
# @swag_from('../api-docs/v1/logout_user.yml')
@token_required
def logout():
    return make_response(("Successfully logged out"), 200)


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
from app.api.models import User, BlacklistToken


def token_required(funct):
    @wraps(funct)
    def decorated_funct(*args, **kwargs):
        token = None
        if 'access_token' in request.headers:
            token = request.headers['access_token']
            if not token:
                return jsonify({'message': "Token is missing"}), 401
            # check if token is blacklisted
            blacklisted_token = BlacklistToken.query.filter_by(
                token=token).first()
            if blacklisted_token:
                return jsonify({'Message': 'Expired token, Login again'}), 403
            try:
                data = jwt.decode(token, 'hard to guess string')
                user = User.query.filter_by(id=data['sub']).first()
                current_user = user
            except:
                return jsonify({'message': 'Token is invalid'}), 401
            return funct(current_user, *args, **kwargs)
        else:
            return jsonify({'error': 'Token required'}), 401
    return decorated_funct


@auth.route('/api/auth/register', methods=['POST'])
@swag_from('../api_docs/signup.yml')
def signup():
    """This Endpoint handles registration of new users."""

    data = request.get_json()
    username = data['username'].strip()
    email = data['email'].strip()
    password = data['password'].strip()

    if username and email and password:

        if username and isinstance(username, int):
            return make_response(
                jsonify({
                    'message': 'Username cannot be number'
                })), 400

        if username.strip() == "":
            return make_response(
                jsonify({
                    'message': 'Username cannot be empty'
                })), 400
        if re.match(r'.*[\%\$\^\*\@\!\?\(\)\:\;\&\'\"\{\}\[\]].*', username):
            return make_response(
                jsonify({
                    'message': 'Username should not have special characters'
                })), 400
        if email.strip() == "":
            return make_response(
                jsonify({
                    'message': 'Email cannot be empty'
                })), 400
        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return make_response(
                jsonify({
                    'message': 'Invalid Email input'
                })), 400
        if password.strip() == "":
            return make_response(
                jsonify({
                    'message': 'Password cannot be empty'
                })), 400
        if len(password) < 4:
            return make_response(
                jsonify({
                    'message': 'Password is too short'
                })), 400

    # Query to see if the user already exists
    user = User.query.filter_by(email=data['email']).first()

    if user:
        respond = {
            'message': 'User already exists. Please login',
            'status': 'Failed'
        }
        return make_response(jsonify(respond)), 409

    # If there is no user with such email address, register the new user
    user = User(username=username, email=email, password=password)
    user.save()
    respond = {
        'message': 'Registration successful. Please login',
        'status': 'Success'
    }
    return jsonify(respond), 201


@auth.route('/api/auth/login', methods=['POST'])
@swag_from('../api_docs/signin.yml')
def signin():
    """This Endpoint handles user login and access token generation."""

    data = request.get_json()

    # Get the user object using their email (unique to every user)
    user = User.query.filter_by(email=data['email']).first()
    # Try to authenticate the found user using their password
    if user and user.password_is_valid(data['password']):
            # Generate the access token. This will be used as the authorization header
        access_token = user.generate_token(user.id)
        if access_token:
            respond = {
                'message': 'You logged in successfully.',
                'access_token': access_token.decode(),
                'status': 'Success'
            }
            return make_response(jsonify(respond)), 200

    # User does not exist. Therefore, return an error message
    else:
        respond = {
            'message': 'Invalid email or password, Please try again',
            'status': 'Failed'
        }
        return make_response(jsonify(respond)), 401


@auth.route('/api/auth/reset_password', methods=['POST'])
# @swag_from('../api-docs/v1/reset_password.yml')
@token_required
def reset_password(current_user):
    """ This endpoint enables user reset-password """

    data = request.get_json()

    new_password = data.get('new_password')
    user = User.query.filter_by(email=data['email']).first()
    if not user.password_is_valid(new_password):
        user.reset_password(new_password)
        user.save()
        return make_response(
            jsonify({
                    'message': 'Password changed successfully',
                    'status': 'Success'
                    })), 201
    else:
        return make_response(
            jsonify({
                    'message': 'password not changed',
                    'status': 'Failed'
                    })), 400
    return make_response(jsonify({'message': 'Wrong Password',
                                  'status': 'Failed'})), 401


@auth.route('/api/auth/logout', methods=['POST'])
# @swag_from('../api-docs/v1/logout_user.yml')
@token_required
def logout(current_user):
    
    """ This endpoint logs out a logged in user """

    if 'access_token' in request.headers:
        token = request.headers['access_token']

    blacklisted_token = BlacklistToken.query.filter_by(token=token).first()

    if blacklisted_token:
        return jsonify({'Message': 'Logged out already',
                        'Status': 'Failed'}), 403
    else:
        blacklist_token = BlacklistToken(token=token)
        db.session.add(blacklist_token)
        db.session.commit()
        return jsonify({'Message': 'Successfully logged out',
                        'Status': 'Success'}), 200
    return jsonify({'Message': 'Authentication token required',
                    'Status': 'Failed'}), 403

  

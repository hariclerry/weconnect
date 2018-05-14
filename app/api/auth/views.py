"""This module defines the application endpoints"""

from flask import request, jsonify, url_for, session, make_response, abort
import random
import datetime
import re
from functools import wraps
import jwt
from flasgger import swag_from
from app import db, models
from app.api.models import User, BlacklistToken
from . import auth


def token_required(funct):
    @wraps(funct)
    def decorated_funct(*args, **kwargs):
        token = None
        if 'access_token' in request.headers:
            token = request.headers['access_token']
            if token is None:
                return jsonify({'message': 'Token is missing',
                                'status': 'Failed'}), 401
            # check if token is blacklisted
            blacklisted_token = BlacklistToken.query.filter_by(
                token=token).first()
            if blacklisted_token is not None:
                return jsonify({'message': 'Expired token, Login again',
                                'status': 'Failed'}), 403
            try:
                data = jwt.decode(token, 'hard to guess string')
                user = User.query.filter_by(id=data['sub']).first()
                current_user = user
            except:
                return jsonify({'message': 'Token is invalid',
                                'status': 'Failed'}), 401
            return funct(current_user, *args, **kwargs)
        else:
            return jsonify({'error': 'Token required',
                            'status': 'Failed'}), 401
    return decorated_funct


@auth.route('/api/auth/register', methods=['POST'])
@swag_from('../api_docs/signup.yml')
def register_user():
    """This Endpoint handles registration of new users."""

    data = request.get_json()
    username = data['username'].strip()
    email = data['email'].strip()
    password = data['password'].strip()

    if not username or not email or not password:
        return jsonify({'message': 'Please fill in all the credentials',
                        'status': 'Failed'}), 400

    if not username.isalpha():
        return make_response(
            jsonify({'message': 'Username should contain letters only',
                     'status': 'Failed'})), 400
    if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
        return make_response(
            jsonify({'message': 'Invalid Email input',
                     'status': 'Failed'})), 400
    if len(password) < 4:
        return make_response(
            jsonify({'message': 'Password is too short',
                     'status': 'Failed'})), 400

    # Query to see if the user already exists
    user = User.query.filter_by(email=data['email']).first()

    if user is not None:
        response = {
            'message': 'User already exists. Please login',
            'status': 'Failed'
        }
        return make_response(jsonify(response)), 409

    # If there is no user with such email address, register the new user
    user = User(username=username, email=email, password=password)
    user.save()
    response = {
        'message': 'Registration successful. Please login',
        'status': 'Success'
    }
    return make_response(jsonify(response)), 201


@auth.route('/api/auth/login', methods=['POST'])
@swag_from('../api_docs/signin.yml')
def login_user():
    """This Endpoint handles user login and access token generation."""

    data = request.get_json()

    # Get the user object using their email (unique to every user)
    user = User.query.filter_by(email=data['email']).first()
    # Try to authenticate the found user using their password
    if user and user.password_is_valid(data['password']):
        # Generate the access token. This will be used as the authorization header
        access_token = user.generate_token(user.id)
        if access_token:
            response = {
                'message': 'You logged in successfully.',
                'access_token': access_token.decode(),
                'status': 'Success'
            }
            return make_response(jsonify(response)), 200

    # User does not exist. Therefore, return an error message
    else:
        response = {'message': 'Invalid email or password, Please try again',
                    'status': 'Failed'
                    }
        return make_response(jsonify(response)), 401


@auth.route('/api/auth/reset_password', methods=['POST'])
@swag_from('../api-docs/v1/reset_password.yml')
@token_required
def reset_password(current_user):
    """ This endpoint enables user reset-password """

    data = request.get_json()
    email = data['email'].strip()
    new_password = data.get('new_password').strip()
    if not email or not new_password:
        return jsonify({'message': 'Please Fill in all credentials',
                        'status': 'Failed'}), 400
    if len(new_password) < 4:
        return make_response(
            jsonify({'message': 'Password is too short',
                     'status': 'Failed'})), 400

    user = User.query.filter_by(email=data['email']).first()

    if user is None:
        return make_response(jsonify({'message': 'Wrong Email address',
                                      'status': 'Failed'})), 401

    if not user.password_is_valid(new_password):
        user.reset_password(new_password)
        user.save()
        return make_response(
            jsonify({
                    'message': 'Password changed successfully',
                    'status': 'Success'
                    })), 201

    return make_response(
        jsonify({
            'message': 'Password not changed, please enter a new password',
            'status': 'Failed'
        })), 401


@auth.route('/api/auth/logout', methods=['POST'])
@swag_from('../api-docs/v1/logout_user.yml')
@token_required
def logout_user(current_user):
    """ This endpoint logs out a logged in user """

    token = request.headers['access_token']

    blacklisted_token = BlacklistToken.query.filter_by(token=token).first()

    if blacklisted_token is not None:
        return jsonify({'message':  'Authentication token required',
                        'status': 'Failed'}), 403
    else:
        blacklist_token = BlacklistToken(token=token)
        db.session.add(blacklist_token)
        db.session.commit()
        return jsonify({'message': 'Successfully logged out',
                        'status': 'Success'}), 200

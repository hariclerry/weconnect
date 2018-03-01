"""This module defines a user class and methods associated to it"""
#used to validate names
# import re
import uuid
import jwt
from datetime import datetime, timedelta


class UserDetails(object):
    """ A class to handle activities related to a user"""
    def __init__(self):
        # A list to hold all user objects
        self.user_list = []

    def generate_token(self, user_id):
        """Generates the access token to be used as the Authorization header"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=30),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                'hard to guess string',
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, 'hard to guess string')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please log in to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"

    def register(self, username, email, password, cnfpassword):
        """A method to register users with correct and valid details"""

        # empty dict to hold details of the user to be created
        user_details = {}
        # checkif a user with that username exists
        for user in self.user_list:
            if user['username'] == username  or user['email'] == email:
                return "Username or email already exists."     
        else:
                    #register user if all the details are valid
                    user_details['username'] = username
                    user_details['email'] = email
                    user_details['password'] = password
                    user_details['cnfpassword'] = cnfpassword
                    user_details['id'] = uuid.uuid1()
                    self.user_list.append(user_details)
                    return 'Registration successful'

    def login(self, username, password):
        """A method to login a user given valid user details"""
        for user in self.user_list:
            if username == user['username']:
                if password == user['password']:
                    return "successful"
                else:
                    return "wrong password"
        return "user does not exist"

    def find_user_by_id(self, user_id):
        """ Retrieve a user given a user id"""
        for user in self.user_list:
            if user['id'] == user_id:
                return user

    def reset_pass(self, email, new_password):
        """A method to reset a password"""
        for user in self.user_list:
            if user['email'] == email:
                user['password'] = new_password
                return "success"
            return "incorrect username"
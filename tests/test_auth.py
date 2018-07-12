import os
import unittest
import json

from app import create_app, db
from app.api import auth, business, review
from app.api.auth import views as users
from app.api.business import views as businesses
from app.api.review import views as reviews



class AuthTestCase(unittest.TestCase):
    """Test case for the authentication"""

    def setUp(self):
        # create app using the flask import
        self.app = create_app('testing')
                                  
        # create a dict to be used to store user details
        self.user_data = {
            'username': 'barbara',
            'email': 'me@gmail.com',
            'password': 'red55'
        }

        # password reset details
        self.password_info = {
            'email': 'me@gmail.com',
            'new_password': 'lighter',
        }

        # bind the app context
        with self.app.app_context():
            self.client = self.app.test_client
            # create all tables
            db.create_all()

        # register user
        self.log = self.client().post('v1/api/auth/register',
                                      content_type='application/json',
                                      data=json.dumps(self.user_data))

        self.login = self.client().post('v1/api/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(dict(email='me@gmail.com',
                                                             password='red55')))

        self.result = json.loads(self.login.data.decode())

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

     # Test cases

    def test_add_user(self):
        """Test that a new user can be added"""

        self.assertIn(u'Registration successful. Please login',
                      str(self.log.data))
        self.assertEqual(self.log.status_code, 201)

    def test_add_unique_user(self):
        """tests that a unique user is added"""

        response = self.client().post('v1/api/auth/register',
                                      content_type='application/json',
                                      data=json.dumps(dict(username="barbara", email='me@gmail.com',
                                                           password='red55')))

        self.assertIn('User already exists. Please login', str(response.data))
        self.assertEqual(response.status_code, 409)

    def test_login_with_credentials(self):
        """test that a user can sign in with correct credentials"""

        self.assertIn(u'You logged in successfully.', str(self.login.data))
        self.assertEqual(self.login.status_code, 200)

    def test_invalid_login(self):
        """test that a user cannot sign in with incorrect password"""

        response = self.client().post('v1/api/auth/login',
                                      content_type='application/json',
                                      data=json.dumps(dict(email='me@gmail.com',
                                                           password='red5555')))
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            u'Invalid email or password, Please try again', str(response.data))

    def test_token_generate(self):
        """tests user token generated on login"""

        login = self.client().post('v1/api/auth/login',
                                   content_type='application/json',
                                   data=json.dumps(dict(email='me@gmail.com',
                                                        password='red55')))
        result = json.loads(login.data.decode())

        self.assertTrue(result['access_token'])
        self.assertEqual(login.status_code, 200)

    def test_success_password_reset(self):
        """test that a user can reset password with correct credentials"""

        response = self.client().post('v1/api/auth/reset_password',
                                      content_type='application/json',
                                      data=json.dumps(dict(email='me@gmail.com',
                                                           new_password='lighter')),
                                      headers=dict(
                                          access_token=self.result['access_token'])
                                      )

        self.assertIn(u'Password changed successfully', str(response.data))
        self.assertEqual(response.status_code, 201)



    def test_wrong_email_password_reset(self):
        """test that a user cannot reset password with wrong email"""
      
        
        response = self.client().post('v1/api/auth/reset_password',
                                    content_type='application/json',
                                    data=json.dumps(dict(email ='cle@gmail.com',
                                                           new_password='lighter')),
                                    headers=dict(access_token =self.result['access_token'])
                                    )

        self.assertIn(u'Wrong Email address', str(response.data))
        self.assertEqual(response.status_code, 401)

    def test_wrong_password_reset(self):
        """test that a user cannot reset password"""

        self.client().post('v1/api/auth/reset_password',
                                      content_type='application/json',
                                      data=json.dumps(dict(email='me@gmail.com',
                                                           new_password='lighter')),
                                      headers=dict(
                                          access_token=self.result['access_token'])
                                      )

        response = self.client().post('v1/api/auth/reset_password',
                                      content_type='application/json',
                                      data=json.dumps(dict(email='me@gmail.com',
                                                           new_password='lighter')),
                                      headers=dict(
                                          access_token=self.result['access_token'])
                                      )

        self.assertIn(u'Password not changed, please enter a new password', str(response.data))
        self.assertEqual(response.status_code, 401)

    def test_logout_user(self):
        """test that a user can logout"""
      

        response = self.client().post('v1/api/auth/logout',
                                    content_type = 'application/json',
                                    headers = dict(access_token = self.result['access_token']))
        self.assertIn(u'Successfully logged out', str(response.data))
        self.assertEqual(response.status_code, 200)
        



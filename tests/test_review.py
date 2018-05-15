import os
import unittest
import json

from app import create_app, db
from app.api import auth, business, review
from app.api.auth import views as users
from app.api.business import views as businesses
from app.api.review import views as reviews



class ReviewTestCase(unittest.TestCase):
    """Test case for Reviews."""

    def setUp(self):
        # create app using the flask import
        self.app = create_app('testing')

       # create a dict to be used to add a new biz
        self.a_business = {'name': 'Jumia Ltd',
                           'category': 'Property',
                           'location': 'Entebbe',
                           'description': 'Dealers in property management'
                           }

        # create a dict to be used to edit business
        self.edited_business = {'name': 'Jumia Ltd',
                                'category': 'Property and consu',
                                'location': 'Entebbe',
                                'description': 'Dealers in property management'
                                }

        # create a dict to be used to store the review
        self.a_business_review = {'description': 'Great and Awesome service'

                                  }
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

    def add_businesses(self):
        """This is a helper method that adds dummy businesses to the database"""

        response = self.client().post('v1/api/businesses', content_type='application/json',
                                      data=json.dumps(dict(name='Jumia',
                                                           category='Property',
                                                           location='Kiwatule',
                                                           description='Dealers in property management')),
                                      headers=dict(access_token=self.result['access_token']))
        response = self.client().post('v1/api/businesses', content_type='application/json',
                                      data=json.dumps(dict(name='Clerrys Boutique',
                                                           category='Fashion',
                                                           location='Bugolobi',
                                                           description='Dealers in latest fashion craze')),
                                      headers=dict(access_token=self.result['access_token']))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    
    # Test cases

    def test_add_review(self):
        """ensure reviews can be added for business"""

        response = self.client().post('v1/api/businesses', content_type='application/json',
                                      data=json.dumps(self.a_business),
                                      headers=dict(access_token=self.result['access_token']))
        response = self.client().post('v1/api/business/1/reviews',
                                      content_type='application/json',
                                      data=json.dumps(
                                          dict(description='Great and Awesome service')),
                                      headers=dict(access_token=self.result['access_token']))
        self.assertIn(u'Successfully Added Review', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_fail_add_review(self):
        """Ensure review cannot be added with error"""

        response = self.client().post('v1/api/businesses', content_type='application/json',
                                      data=json.dumps(self.a_business),
                                      headers=dict(access_token=self.result['access_token']))
        response = self.client().post('v1/api/business/5/reviews',
                                      content_type='application/json',
                                      data=json.dumps(
                                          dict(description='Great and Awesome service')),
                                      headers=dict(access_token=self.result['access_token']))
        self.assertIn(u'Business does not exist', str(response.data))
        self.assertEqual(response.status_code,  401)

    def test_view_reviews(self):
        """ensure reviews can be viewed for business"""

        response = self.client().post('v1/api/businesses', content_type='application/json',
                                      data=json.dumps(self.a_business),
                                      headers=dict(access_token=self.result['access_token']))

        response = self.client().post('v1/api/business/1/reviews',
                                      content_type='application/json',
                                      data=json.dumps(
                                          dict(description='The best in town')),
                                      headers=dict(access_token=self.result['access_token']))
        response = self.client().get('v1/api/business/1/reviews',
                                     headers=dict(access_token=self.result['access_token']))
        self.assertIn(u'The best in town', str(response.data))
        self.assertEqual(response.status_code,  200)

    def test_fail_view_reviews(self):
        """ensure reviews cannot be viewed for non existent business"""

        response = self.client().post('v1/api/businesses', content_type='application/json',
                                      data=json.dumps(self.a_business),
                                      headers=dict(access_token=self.result['access_token']))
        response = self.client().post('v1/api/business/1/reviews',
                                      content_type='application/json',
                                      data=json.dumps(
                                          dict(description='Great and Awesome service')),
                                      headers=dict(access_token=self.result['access_token']))

        response = self.client().get('v1/api/business/5/reviews',
                                     headers=dict(access_token=self.result['access_token']))
        self.assertIn(u'Business does not exist', str(response.data))
        self.assertEqual(response.status_code,   401)

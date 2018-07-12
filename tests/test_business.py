import os
import unittest
import json

from app import create_app, db
from app.api import auth, business, review
from app.api.auth import views as users
from app.api.business import views as businesses
from app.api.review import views as reviews



class BusinessTestCase(unittest.TestCase):
    """Test case for the Businesses."""

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
    def test_register_business(self):
        """tests that a business can be created"""

        response = self.client().post('v1/api/businesses', content_type='application/json',
                                      data=json.dumps(self.a_business),
                                      headers=dict(access_token=self.result['access_token']))
        self.assertIn(u'Business successfully registered', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_fail_register_business(self):
        """tests that a business cannot be created if it exists"""

        response = self.client().post('v1/api/businesses', content_type='application/json',
                                      data=json.dumps(self.a_business),
                                      headers=dict(access_token=self.result['access_token']))
        response = self.client().post('v1/api/businesses', content_type='application/json',
                                      data=json.dumps(self.a_business),
                                      headers=dict(access_token=self.result['access_token']))
        self.assertIn(u'Business already exists', str(response.data))
        self.assertEqual(response.status_code, 409)

    def test_view_businesses(self):
        """Tests if businesses can be viewed"""
        self.add_businesses()
        response = self.client().get('v1/api/businesses',
                                     content_type='application/json',
                                     headers=dict(access_token=self.result['access_token']))
        self.assertIn(u'Jumia', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_view_business(self):
        """Test retrieve business by id"""
        self.add_businesses()

        response = self.client().get('v1/api/businesses/2',
                                     content_type='application/json',
                                     headers=dict(access_token=self.result['access_token']))
        self.assertIn(u'Clerrys Boutique', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_fail_view_business(self):
        """Test fail to find a business with wrong id"""

        self.add_businesses()

        response = self.client().get('v1/api/businesses/6',
                                     content_type='application/json',
                                     headers=dict(access_token=self.result['access_token']))
        self.assertIn(u'Business does not exist', str(response.data))
        self.assertEqual(response.status_code, 401)

    def test_edit_business(self):
        """Test update business profile"""

        self.add_businesses()
        response = self.client().put('v1/api/businesses/2',
                                     content_type='application/json',
                                     data=json.dumps(dict(name='Clerrys Boutique',
                                                          category='Fashion and design',
                                                          location='Ntinda',
                                                          description='Dealers in latest fashion craze')),
                                     headers=dict(access_token=self.result['access_token']))
        self.assertEqual(response.status_code,  200)
        self.assertIn(u'Successfully updated business', str(response.data))

    def test_edit_business_fail(self):
        """Test if update business profile wrong id fails"""

        self.add_businesses()

        response = self.client().put('v1/api/businesses/5',
                                     content_type='application/json',
                                     data=json.dumps(dict(name='Clerrys Boutique',
                                                          category='Fashion and design',
                                                          location='Ntinda',
                                                          description='Dealers in latest fashion craze')),
                                     headers=dict(access_token=self.result['access_token']))
        self.assertEqual(response.status_code,  401)
        self.assertIn(u'Business does not exist', str(response.data))

    def test_delete_business(self):
        """tests that a business can be deleted"""

        self.add_businesses()

        response = self.client().delete('v1/api/businesses/2',
                                        content_type='application/json',
                                        headers=dict(access_token=self.result['access_token']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Business deleted successfully', str(response.data))

    def test_fail_delete_business(self):
        """tests that a non existent business cannot be deleted"""

        self.add_businesses()

        response = self.client().delete('v1/api/businesses/6',
                                        content_type='application/json',
                                        headers=dict(access_token=self.result['access_token']))
        self.assertEqual(response.status_code, 401)
        self.assertIn(u'Business does not exist', str(response.data))

    
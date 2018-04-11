import os
import unittest
import json
from app.api import auth, main
from app.api.auth import views as users
from app.api.main import views as businesses
from app import create_app, db
# session

class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""
    def setUp(self):
        #create app using the flask import
        self.app = create_app('testing')
                            
       #create a dict to be used to add a new biz
        self.a_business = {'name':'Jumia',
                            'category': 'Property',
                            'location' : 'Dealers in property management'
                            }
        
        #create a dict to be used to add a new biz with values as numbers
        self.a_business_with_some_values_as_numbers = {'name':123,
                            'category': 'IT',
                            'location' : 908
                            }

        #create a dict to be used to edit business
        self.edited_business = {'name':'Jumia Ltd',
                                'category': 'Property',
                                'location' : 'Entebbe',
                                'description': 'Dealers in property management'
                            }

        #create a dict to be used to store the review
        self.a_business_review = {'description': 'Great and Awesome service'
                        
                            }
        #create a dict to be used to store user details
        self.user_data = {
            'username': 'barbara',
            'email': 'me@gmail.com',
            'password': 'red55'
        }

        #password reset details
        self.password_infor = {
            'previous_password': 'red55',
            'new_password': 'hari55',
        }

        

                            

        #bind the app context
        with self.app.app_context():
            self.client = self.app.test_client
            # create all tables
            db.create_all()

        # login details
        self.log = self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(self.user_data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
    
    def test_add_user(self):
        """Test that a new user can be added"""
        response = self.log
        
        self.assertIn(u'Registration successful. Please login', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_add_unique_user(self):
        """tests that a unique user is added"""
        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username= "barbara", email = 'me@gmail.com',
                                                 password = 'red55')))
        
        response = self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username= "barbara", email = 'me@gmail.com',
                                                 password = 'red55')))
        
        self.assertIn(u'User already exists. Please login', str(response.data))
        self.assertEqual(response.status_code, 409)

    def test_login_with_credentials(self):
        """test that a user can sign in with correct credentials"""
        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        response = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))

        self.assertIn(u'You logged in successfully.', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        """test that a user cannot sign in with incorrect password"""
        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        response = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red5555')))
        self.assertEqual(response.status_code, 401)
        self.assertIn(u'Invalid email or password, Please try again', str(response.data))

    def test_token_generate(self):
        """tests user token generated on login"""
        self.client().post('v1/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(username = 'barbara', email='ah@gmail.com',
                                                        password='praise')))
        login = self.client().post('v1/api/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='ah@gmail.com',
                                                      password='praise')))
        result = json.loads(login.data.decode())
        self.assertTrue(result['access_token'])
        self.assertEqual(login.status_code, 200)

    def test_failed_password_reset(self):
        """test that a user cannot reset password with missing credentials"""
        self.client().post('v1/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(username = 'barbara', email='you@gmail.com',
                                                        password='light')))
        login = self.client().post('v1/api/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='you@gmail.com',
                                                      password='light')))
        result = json.loads(login.data.decode())
        
        response = self.client().post('v1/api/auth/reset_password',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'you@gmail.com',
                                                           old_password = '',
                                                           new_password = 'lighter')),
                                    headers =dict(access_token = result['access_token'])
                                    )

        self.assertIn(u'Wrong Password', str(response.data))
        self.assertEqual(response.status_code, 401)

    def test_register_business(self):
        """tests that a business can be created"""
        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        self.assertIn(u'Business successfully registered', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_fail_register_business(self):
        """tests that a business cannot be created if it exists"""

        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        self.assertIn(u'Business already exists', str(response.data))
        self.assertEqual(response.status_code, 409)
    
    def test_view_businesses(self):
        """Tests if businesses can be viewed"""
        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Clerrys Boutique',
                                                          category = 'Fashion',
                                                          location = 'Bugolobi',
                                                          description= 'Dealers in latest fashion craze')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().get('v1/api/businesses',
                                  content_type='application/json',
                                   headers=dict(access_token=result['access_token']))
        self.assertIn(u'Jumia',str(response.data))
        self.assertEqual(response.status_code, 200)
        

    def test_view_business(self):
        """Test retrieve business by id"""

        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Clerrys Boutique',
                                                          category = 'Fashion',
                                                          location = 'Bugolobi',
                                                          description= 'Dealers in latest fashion craze')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().get('v1/api/businesses/2',
                                  content_type='application/json',
                                   headers=dict(access_token=result['access_token']))
        self.assertIn(u'Clerrys Boutique', str(response.data))
        self.assertEqual(response.status_code, 200)
    
    def test_fail_view_business(self):
        """Test fail to find a business with wrong id"""

        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Clerrys Boutique',
                                                          category = 'Fashion',
                                                          location = 'Bugolobi',
                                                          description= 'Dealers in latest fashion craze')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().get('v1/api/businesses/6',
                                  content_type='application/json',
                                   headers=dict(access_token=result['access_token']))
        self.assertIn(u'Business does not exist', str(response.data))
        self.assertEqual(response.status_code, 401)
    
    def test_edit_business(self):
        """Test update business profile"""

        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Clerrys Boutique',
                                                          category = 'Fashion',
                                                          location = 'Bugolobi',
                                                          description= 'Dealers in latest fashion craze')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().put('v1/api/businesses/2',
                                  content_type='application/json',
                            data = json.dumps( dict(name='Clerrys Boutique',
                                                          category = 'Fashion and design',
                                                          location = 'Ntinda',
                                                          description= 'Dealers in latest fashion craze')),
                                   headers=dict(access_token=result['access_token']))
        self.assertEqual(response.status_code,  200)
        self.assertIn (u'Successfully updated business', str(response.data))

    def test_edit_business_fail(self):
        """Test if update business profile wrong id fails"""

        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Clerrys Boutique',
                                                          category = 'Fashion',
                                                          location = 'Bugolobi',
                                                          description= 'Dealers in latest fashion craze')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().put('v1/api/businesses/5',
                                  content_type='application/json',
                            data = json.dumps( dict(name='Clerrys Boutique',
                                                          category = 'Fashion and design',
                                                          location = 'Ntinda',
                                                          description= 'Dealers in latest fashion craze')),
                                   headers=dict(access_token=result['access_token']))
        self.assertEqual(response.status_code,  401)
        self.assertIn (u'Business does not exist', str(response.data))


    def test_delete_business(self):
        """tests that a business can be deleted"""

        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Clerrys Boutique',
                                                          category = 'Fashion',
                                                          location = 'Bugolobi',
                                                          description= 'Dealers in latest fashion craze')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().delete('v1/api/businesses/2',
                                  content_type='application/json',
                                   headers=dict(access_token=result['access_token']))
        self.assertEqual(response.status_code, 200)
        self.assertIn (u'Business deleted successfully', str(response.data))


    def test_fail_delete_business(self):
        """tests that a non existent business cannot be deleted"""

        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Clerrys Boutique',
                                                          category = 'Fashion',
                                                          location = 'Bugolobi',
                                                          description= 'Dealers in latest fashion craze')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().delete('v1/api/businesses/6',
                                  content_type='application/json',
                                   headers=dict(access_token=result['access_token']))
        self.assertEqual(response.status_code, 401)
        self.assertIn (u'Business does not exist', str(response.data))

    def test_add_review(self):
        """ensure reviews can be added for business"""
        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/business/1/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(description = 'Great and Awesome service')),
                                    headers = dict(access_token = result['access_token']))
        self.assertIn(u'Successfully Added Review', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_fail_add_review(self):
        """Ensure review cannot be added with error"""

        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/business/5/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(description = 'Great and Awesome service')),
                                    headers = dict(access_token = result['access_token']))
        self.assertIn(u'Business does not exist', str(response.data))
        self.assertEqual(response.status_code,  401)
   
    def test_view_reviews(self):
        """ensure reviews can be viewed for business"""

        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/business/1/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(description = 'Great and Awesome service')),
                                    headers = dict(access_token = result['access_token']))
        response = self.client().post('v1/api/business/1/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(description = 'The best in town')),
                                    headers = dict(access_token = result['access_token']))
        response = self.client().get('v1/api/business/1/reviews',
                                    headers=dict(access_token=result['access_token']))
        self.assertIn(u'The best in town', str(response.data))
        self.assertEqual(response.status_code,  200)

    def test_fail_view_reviews(self):
        """ensure reviews cannot be viewed for non existent business"""
        self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = 'barbara', email = 'me@gmail.com',
                                                      password = 'red55')))
        login = self.client().post('v1/api/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'red55')))
        
        result = json.loads(login.data.decode())
        response = self.client().post('v1/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Jumia',
                                                          category = 'Property',
                                                          location = 'Kiwatule',
                                                          description= 'Dealers in property management')),
                                    headers =dict(access_token = result['access_token']))
        response = self.client().post('v1/api/business/1/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(description = 'Great and Awesome service')),
                                    headers = dict(access_token = result['access_token']))
        response = self.client().post('v1/api/business/1/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(description = 'The best in town')),
                                    headers = dict(access_token = result['access_token']))
        response = self.client().get('v1/api/business/5/reviews',
                                    headers=dict(access_token=result['access_token']))
        self.assertIn(u'Business does not exist', str(response.data))
        self.assertEqual(response.status_code,   401)
 

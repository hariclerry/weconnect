import unittest
import json
from app.api import auth
from app.api.auth import views as users
from app import create_app, db
# session

class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""
    def setUp(self):
        #create app using the flask import
        self.app = create_app('testing')
                            
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

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
    

    def test_add_user(self):
        """Test that a new user can be added"""
        response = self.client().post('v1/api/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(username = "barbara", email = 'me@gmail.com',
                                                 password = 'red55')))
        
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

    # def test_password_reset(self):
    #     """test that a user can reset password"""
    #     self.client().post('v1/api/auth/register',content_type='application/json',
    #                                data =json.dumps( dict(username = 'barbara', email='you@gmail.com',
    #                                                     password='light')))
    #     login = self.client().post('v1/api/auth/login',
    #                                 content_type='application/json',
    #                                data=json.dumps(dict(email='you@gmail.com',
    #                                                   password='light')))
    #     result = json.loads(login.data.decode())
        
    #     response = self.client().post('v1/api/auth/reset_password',
    #                                 content_type = 'application/json',
    #                                 data = json.dumps(dict(email = 'you@gmail.com',
    #                                                        old_password = 'light',
    #                                                        new_password = 'lighter')),
    #                                 headers =dict(access_token = result['access_token'])
    #                                 )

    #     self.assertIn(u'Successfully changed password', str(response.data))
    #     self.assertEqual(response.status_code, 200)

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

        self.assertIn(u'Fill all credentials', str(response.data))
        self.assertEqual(response.status_code, 401)


    # def test_wrong_email_password_reset(self):
    #     """test that a user cannot reset password with wrong email"""
    #     self.client().post('v1/api/auth/register',content_type='application/json',
    #                                data =json.dumps( dict(username = 'barbara', email='you@gmail.com',
    #                                                     password='light')))
    #     login = self.client().post('v1/api/auth/login',
    #                                 content_type='application/json',
    #                                data=json.dumps(dict(email='you@gmail.com',
    #                                                   password='light')))
    #     result = json.loads(login.data.decode())
        
    #     response = self.client().post('v1/api/v2/auth/reset_password',
    #                                 content_type = 'application/json',
    #                                 data = json.dumps(dict(email = 'me@gmail.com',
    #                                                        old_password = 'light',
    #                                                        new_password = 'lighter')),
    #                                 headers =dict(access_token = result['access_token'])
    #                                 )

    #     self.assertIn(u'Wrong email', str(response.data))
    #     self.assertEqual(response.status_code, 401)

    def test_wrong_password_reset(self):
        """test that a user cannot reset password with wrong email"""
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
                                                           old_password = 'light',
                                                           new_password = 'lighter')),
                                    headers =dict(access_token = result['access_token'])
                                    )

        self.assertIn(u'Input correct old password', str(response.data))
        self.assertEqual(response.status_code, 401)

    # def test_logout_user(self):
    #     self.tester.post('v1/api/v2/auth/register',content_type='application/json',
    #                                data =json.dumps( dict(username = 'barbara', email='jh@gmail.com',
    #                                                     password='amazons')))
    #     login = self.tester.post('v1/api/v2/auth/login',
    #                                 content_type='application/json',
    #                                data=json.dumps(dict(email='jh@gmail.com',
    #                                                   password='amazons')))
    #     result = json.loads(login.data.decode())

    #     response = self.tester.post('v1/api/v2/auth/logout',
    #                                 content_type = 'application/json',
    #                                 headers = dict(access_token = result['token']))
    #     self.assertIn(u'Successfully logged out', response.data)
    #     self.assertEqual(response.status_code, 200)
   

if __name__ == '__main__':
    unittest.main()
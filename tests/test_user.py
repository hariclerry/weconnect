"""This module defines tests for the user class and its methods"""
import unittest
from app.models.user import UserDetails

class UserTests(unittest.TestCase):
    """Define and setup testing class"""
    

    def setUp(self):
        """ Set up user object before each test"""
        self.user = UserDetails()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.user

    def test_successful_registration(self):
        """Test if a user with correct credentials can register sucessfully"""
        res = self.user.register("clerry", "clerry@mail.com", "password", "password")
        self.assertEqual(res, 'Registration successful')
        
    def test_existing_user_username(self):
        """Test with an already existing username, try registering a user twice"""
        self.user.register("clerry", "clerry@mail.com", "password", "password")
        res = self.user.register("clerry", "clerry@mail.com", "password", "password")
        self.assertEqual(res, "Username or email already exists.")

    def test_existing_user_email(self):
        """Test registering a user with an existing email"""
        self.user.register("clerry", "clerry@mail.com", "password", "password")
        res = self.user.register("clerry", "clerry@mail.com", "password", "password")
        self.assertEqual(res, "Username or email already exists.")

    def test_user_login(self):
        """Test if a user with valid details can login"""
        self.user.register("clerry", "clerry@mail.com", "password", "password")
        res = self.user.login("clerry", "password")
        self.assertEqual(res, "successful")
    def test_wrong_username(self):
        """Test for a login attempt with a wrong username"""
        self.user.register("clerry", "clerry@mail.com", "password", "password")
        res = self.user.login("clerries", "password")
        self.assertEqual(res, "user does not exist")

    def test_wrong_password(self):
        """Test for a login attempt with a wrong password"""
        self.user.register("clerry", "clerry@mail.com", "password", "password")
        res = self.user.login("clerry", "passwwordds")
        self.assertEqual(res, "wrong password")

    def test_non_existing_user_login(self):
        """Test if a non-existing user can login"""
        self.user.register("clerry", "clerry@mail.com", "password", "password")
        res = self.user.login("harriet", "654123")
        self.assertEqual(res, "user does not exist")

    def test_find_user_by_id(self):
        """ Test if the method will find a user given a user id"""
        #first register a user and get their id
        self.user.register("clerry", "clerry@mail.com", "password", "password")
        user_id = self.user.user_list[0]['id']
        res = self.user.find_user_by_id(user_id)
        #test if it returns a dictionery with user details 
        self.assertIsInstance(res, dict)
        #test if the username of the returned user is the one registered
        username = res['username']
        self.assertIs(username, "clerry")

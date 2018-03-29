# test_business.py
import unittest
import os
import json
from app.api.main import views 
from app import create_app, db

class BusinessTestCase(unittest.TestCase):
    """This class represents the business test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.business = {'name': 'Clerry Construction Ltd', 'category': 'Property', 'location': 'Gulu', 'description': 'awesome'}
        

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_business_registration(self):
        """Test API can create a business (POST request)"""
        res = self.client().post('v1/api/businesses', data=self.business)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Clerry Construction Ltd', str(res.data))

    def test_api_can_get_all_businesses(self):
        """Test API can get a business (GET request)."""
        res = self.client().post('v1/api/businesses', data=self.business)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('v1/api/businesses')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Clerry Construction Ltd', str(res.data))

    def test_api_can_get_business_by_id(self):
        """Test API can get a single business by using it's id."""
        rv = self.client().post('/businesses/', data=self.business)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/bucketlists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Clerry Construction Ltd', str(result.data))

    def test_business_can_be_edited(self):
        """Test API can edit an existing business. (PUT request)"""
        rv = self.client().post(
            '/businesses/',
            data={'name': 'Andela Uganda'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/bucketlists/1',
            data={
                "name": "Andela Uganda Ltd :-)"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/businesses/1')
        self.assertIn('Ltd', str(results.data))

    def test_business_deletion(self):
        """Test API can delete an existing business. (DELETE request)."""
        rv = self.client().post(
            '/businesses/',
            data={'name': 'Andela Uganda'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/businesses/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/businesses/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
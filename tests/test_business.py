"""Module contains tests for the events class"""
import unittest
from app.models.business import Business

class BusinessTests(unittest.TestCase):
    """Class definition and setup"""

    def setUp(self):
        """ Set up user object before each test"""
        self.business = Business()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.business 

    def test_create_business_works(self):
    	"""Test that with correct business  details the method works"""
		

    	res = self.business.create("infoclan", "technology",  "kampala", "world changers", \
              "clerry")
    	self.assertEqual(res, "Business created")

    def test_create_existing_business (self):
    	""" Test if a business  can be created twice"""
    	self.business.create("infoclan", "technology",  "kampala", "world changers", "clerry")
    	self.business.business_list = [{"name" :'infoclan',  "category":'technology',  "location":'kampala', "description" :'world changers',\
          "createdby":'clerry'}]
    	res = self.business.existing_business("infoclan", "kampala", "clerry")
    	self.assertEqual(res, "Business exists")

    def test_same_business_diff_location(self):
    	""" Test if a user can create the same business  but in different locations"""
    	self.business.business_list = [{"name" :'infoclan',  "category":'technology',  "location":'kampala', "description" :'world changers',\
          "createdby":'clerry'}]
    	res = self.business.create("infoclan", "technology",  "kampala", "world changers", \
              "clerry")
    	self.assertEqual(res, "Business created")

    def test_category_filter(self):
    	"""Test if filter category works"""
    	self.business.create("infoclan", "technology",  "kampala", "world changers", "clerry")
    	self.business.create("jumia property", "real estate", "gulu", "the best in town",  "clerry")
    	res = self.business.category_filter("real estate")
    	business_name= res[0]['name']
    	self.assertIs(business_name, "jumia property")
    	self.assertIsNot(business_name, "infoclan")
    	self.assertEqual(len(res), 1)
    	self.assertIsInstance(res, list)

    def test_location_filter(self):
    	"""Test if filter location works"""
    	self.business.create("infoclan", "technology",  "kampala", "world changers", "clerry")
    	self.business.create("jumia property", "real estate", "gulu", "the best in town",  "clerry")
    	res = self.business.location_filter("gulu")
    	business_name = res[0]['name']
    	self.assertIs(business_name, "jumia property")
    def test_delete(self):
    	"""Test if given an id the method will delete a business """
    	self.business.create("infoclan", "technology",  "kampala", "world changers", "clerry")
    	business_id = self.business.business_list[0]['id']
    	res = self.business.delete(business_id)
    	self.assertEqual(res, "deleted")
    	self.assertEqual(len(self.business.business_list), 0)

    def test_update(self):
    	"""Test if method can update a business  successfully"""
    	self.business.create("infoclan", "technology",  "kampala", "world changers", "clerry")
    	business_id = self.business.business_list[0]['id']
    	#update business
    	res = self.business.update("infoclan", "technology", "gulu", "world changers", "clerry", business_id)
    	self.assertEqual(res, "update successful")
    
    # def test_find_by_id_works(self):
    #     """Test if the method finds the exactly specified id"""
    #     self.business.create("infoclan", "technology",  "kampala", "world changers", "clerry")
    #     business_id = self.business.business_list[0]['id']
    #     business_name = self.business.business_list[0]['name']
    #     foundbusiness  = self.business.find_by_id(business_id)
    #     self.assertEqual(foundbusiness ['name'], business_name)

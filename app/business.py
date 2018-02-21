
import uuid

class Business(object):
	""" A class to handle actions related to businesses"""

	def __init__(self):
		"""define an empty list to hold all the business objects"""
		self.business_list = []

	def existing_business(self, name, location, createdby):
		"""A method to check if a user already has that business in same location"""
		for business in self.business_list:
			#test to see if the user has the same business, in the same location in their list 
			if business['name'] == name and business['createdby'] == createdby:
				if business['location'] == location:
					return True
		else:
			return False

	# def valid_name(self, name):
	# 	"""check name length and special characters"""
	# 	if len(name) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", name):
	# 		return False
	# 	else:
	# 		return True

	# def valid_date(self, event_date):
	# 	"""Check if the given date is less than the current date"""
	# 	date = datetime.strptime(event_date, '%Y-%m-%d').date()
	# 	if date < date.today():
	# 		return False
	# 	return True

	def create(self, name, category, location, description, createdby):
		"""A method for creating a new business"""
		self.business_details = {}
		self.business_details['name'] = name
		self.business_details['category'] = category
		self.business_details['location'] = location
		self.business_details['description'] = description
		self.business_details['createdby'] = createdby
		self.business_details['id'] = uuid.uuid1()
		self.business_list.append(self.business_details)
		return "Business created"	
		
		# if self.existing_business(name, createdby, location):
		# 	return "Business exists"

		
			

	def view_all(self):
		""" A method to return a list of all Businesses"""
		return self.business_list
	
	def location_filter(self, location):
		"""A method to return a list of Businesses in a certain location"""
		new_business_list = [business for business in self.business_list if business['location'] == location]
		return new_business_list

	def category_filter(self, category):
		"""A method to find businesses of a given category """
		new_business_list = [business for business in self.business_list if business['category'] == category]
		return new_business_list

	def createdby_filter(self, username):
		"""Filter and return the businesses created by a particular user"""
		new_business_list = [business for business in self.business_list if business['createdby'] == username]
		return new_business_list

	def find_by_id(self, businessid):
		"""A method to find a business given an id"""
		for business in self.business_list:
			if business['id'] == businessid:
				return business
		return False
	def update(self, businessid, name, category, location,  description, createdby):
		""" Find a business with the given id and update its details"""
		for business in self. business_list:
			if business['id'] == businessid:
				self.business_list.remove(business)
				if self.existing_business(name, createdby, location):
					return "Business cannot be updated, a similar event exists"
				# else:
				# 	if not self.valid_name(name):
				# 		return "name too short or invalid"
				# 	elif not self.valid_date(event_date):
				# 		return "event can only have a future date"
		else:
					business['name'] = name
					business['category'] = category
					business['location'] = location
					business['description'] = description
					business['createdby'] = createdby
					business['id'] = businessid
					self.business_list.append(self.business_details)
					return "update successful"
		# else:
		# 	return "no Business with given id"

	def delete(self, businessid):
		""" A method to delete a business from business list"""
		for business in self.business_list:
			if business['id'] == businessid:
				self.business_list.remove(business)
				return "deleted"
		else:
			return "error, Business not found"






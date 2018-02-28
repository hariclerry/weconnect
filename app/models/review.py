class Review(object):
	"""a class to handle Reviews"""

	def __init__(self):
		self.review_list = []

	def create(self, business_id, add_review):
		""" give review on  a particular business"""
		self.review_details = {}
		for review in self.review_list:
			if review['business_id'] == business_id:
				return "user already added review on this business"
		else:
			self.review_details['business_id'] = business_id
			self.review_details['add_review'] = add_review
			self.review_list.append(self.review_details)
			return "review success"

	def view_reviews(self, business_id):
		""" 
		Get the user id's of users who have reviewed a business
		These will be passed to the user object to retrieve the user details
		"""
		for review in self.review_list:
			if  review['business_id'] == business_id:
				return review
		return self.review_list


		
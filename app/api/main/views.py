# """This module defines the application endpoints"""

# import uuid
from flask import request, jsonify, url_for, session, make_response, abort
from flasgger import swag_from
from functools import wraps
import jwt
import datetime
import re
from app import db, models
from app.api.models import Business, Review
# from app import user_object, business_object, review_object
from . import main



# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         current_user = ""

#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']

#         if not token:
#             return jsonify({'message' : 'Token is required!'}), 401

#         try: 
#             data = jwt.decode(token, 'hard to guess string')
#             for user in user_object.user_list:
#                 if user.get("username"):
#                     current_user = user['username']= data['username']
#         except:
#             return jsonify({'message' : 'Token is invalid!'}), 401

#         return f(current_user, *args, **kwargs)

#     return decorated



@main.route('/', methods=['GET'])

def index():
	return jsonify({"message":"Welcome to WeConnect"})


# @main.route('/api/businesses',  methods=[ 'POST'])
# @token_required
# @swag_from('../api_docs/register_business.yml')
# def register_business(current_user):
# 	if not  current_user:
# 		abort(404)
# 	business_data = request.get_json() # sent data from postman is converted to a python dictionary
# 	name = business_data['name'].strip()
# 	category = business_data['category'].strip()
# 	location = business_data['location'].strip()
# 	description = business_data['description'].strip()
# 	createdby =  business_data['createdby'].strip()

# 	if name == "":
# 		message = {"message": "Invalid name"}
# 		return jsonify(message)
# 	if category == "":
# 		message = {"message": "Invalid category"}
# 		return jsonify(message)
# 	if location == "":
# 		message = {"message": "Invalid location"}
# 		return jsonify(message)
# 	if description == "":
# 		message = {"message": "Invalid description"}
# 		return jsonify(message)
# 	if createdby == "":
# 		message = {"message": "Invalid input"}
# 		return jsonify(message)
            
# 	for business in business_object.business_list:
# 		if business['name'] ==  business_data['name'] or business['location'] ==  business_data['location']:
# 			return jsonify("Business already Exist"), 409
# 	res = business_object.create(name, category, location, description, createdby)
# 	if res:
# 		respond = {
# 			"Success": True,
# 			"Message": "Business created successfully",
# 			 "Data": business_data

# 		}
# 		return jsonify(respond), 201
# 	else:
# 		respond = {
# 			"success": False,
# 			"message": "Business not created",
# 		}

# 		return jsonify(respond), 409 
		

# @main.route('/api/businesses', methods=['GET'])
# @token_required
# @swag_from('../api_docs/view_businesses.yml')
# def view_businesses(current_user):
# 	"""Endpoint for returning all the registered businesses """
# 	if not  current_user:
# 		abort(404)
# 	businesses = business_object.view_all()
# 	if businesses:
# 		respond = {
# 			"success": True,
# 			"message": "Businesses successfully retrieved",
# 			"Data": businesses
# 		    }
# 		return jsonify(respond), 200
# 	else:
# 		respond = {
# 			"success": False,
# 			"message": "There is no business registered yet"
# 		}

# 		return jsonify(respond),  200

# @main.route('/api/businesses/<businessid>', methods=['GET'])
# @token_required
# @swag_from('../api_docs/view_business.yml')
# def single_businesses(current_user, businessid):
# 	"""Endpoint for returning a single business"""
# 	if not  current_user:
# 		abort(404)
# 	business = business_object.find_by_id(businessid)
# 	if business:
# 		respond = {
# 			"success": True,
# 			"message": "Business successful",
# 			"Data" : business
			
# 		}
# 		return jsonify(respond), 200

# 	else:
# 		respond = {
# 			"success": False,
# 			"message": "No business with such id found"
# 		}
# 		return jsonify(respond), 404

# @main.route('/api/businesses/<businessid>', methods=['PUT'])
# @token_required
# @swag_from('../api_docs/update_business.yml')
# def update_business(current_user, businessid):
# 	"""Endpoint for handling business updates"""
# 	if not  current_user:
# 		abort(404)
# 	# businessid = uuid.UUID(businessid)
# 	business_data = request.get_json()
# 	name = business_data['name'].strip()
# 	category = business_data['category'].strip()
# 	location = business_data['location'].strip()
# 	description = business_data['description'].strip()
# 	createdby =  business_data['createdby'].strip()

# 	if name == "":
# 		message = {"message": "invalid name"}
# 		return jsonify(message)
# 	if category == "":
# 		message = {"message": "invalid category"}
# 		return jsonify(message)
# 	if location == "":
# 		message = {"message": "invalid location"}
# 		return jsonify(message)
# 	if description == "":
# 		message = {"message": "invalid description"}
# 		return jsonify(message)
# 	if createdby == "":
# 		message = {"message": "invalid input"}
# 		return jsonify(message)
	
# 	# for business in business_object.business_list:
# 	# 	if business['name'] ==  business_data['name'] or business['location'] ==  business_data['location']:
# 	# 		return jsonify("Business already Exist"), 409

# 	res = business_object.update(businessid, name, category, location, description, createdby)
# 	if res:
# 		respond = {
# 			"success": True,
# 			"message": "Business updated successfully",
# 			"Business": business_data
# 		    }
# 		return jsonify(respond), 200
			
# 	else:
# 		respond = {
# 			"success": False,
# 			"message": "No business with given id"
# 		    }
# 		return jsonify(respond), 404
# # return jsonify("business not updated"), 409

	
# @main.route('/api/businesses/<businessid>', methods=['DELETE'])
# @token_required
# @swag_from('../api_docs/delete_business.yml')
# def delete_businesses(current_user, businessid):
# 	"""Endpoint for handling deletion of businesses"""
# 	if not  current_user:
# 		abort(404)
# 	businessid = uuid.UUID(businessid)
# 	res = business_object.delete(businessid)
# 	if res:
# 		respond = {
# 			"success": True,
# 			"message": "Business deleted"
# 		    }
# 		return jsonify(respond), 200
			
# 	else:
# 		respond = {
# 			"success": False,
# 			"message": "No business with given id"
# 		    }
# 		return jsonify(respond), 404
	
	
# @main.route('/api/business/<businessid>/reviews', methods=['POST'])
# @token_required
# @swag_from('../api_docs/add_review.yml')
# def addreview(current_user, businessid):
# 	"""Endpoint for user to add review on a particular business"""
# 	if not  current_user:
# 		abort(404)
# 	# businessid = uuid.UUID(businessid)
# 	if request.method == 'POST': # POST request with valid input
# 		review_data = request.get_json()
# 		review = review_data['review'].strip()

# 		if review == "":
# 			message = {"message": "Invalid review"}
# 			return jsonify(message)

# 		if not business_object.find_by_id(businessid):
# 			return jsonify(response="Can not add review to a non existing business"), 404
# 		else:
# 			res = review_object.create(businessid, review)
# 			if res:
# 				respond = {
# 			                "success": True,
# 			                "message": "Review added successfully"
# 		                  }
# 				return jsonify(respond), 201
# 			else:
# 				respond = {
# 			                "Success": False,
# 			                "Message": "You have already added review for this business"
# 		                      }
# 				return jsonify(respond), 409
				
# @main.route('/api/business/<businessid>/reviews', methods=['GET'])
# @token_required
# @swag_from('../api_docs/view_reviews.yml')
# def viewreview(current_user, businessid):
# 	if request.method == 'GET':
# 		reviews = review_object.view_reviews(businessid)
# 		if reviews:
# 			respond = {
# 			            "Success": True,
# 			            "Message": "Reviews for this particular business",
# 						 "Data": reviews
# 		                  }
# 			return jsonify(respond), 200
# 		else:
# 			respond = {
# 			                "Message": "No review added yet"
# 		         }
# 			return jsonify(respond), 200


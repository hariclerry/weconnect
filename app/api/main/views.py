# """This module defines the application endpoints"""

# import uuid
from flask import request, jsonify, url_for, session, make_response, abort
from flasgger import swag_from
from functools import wraps
import jwt
import datetime
import re
from app import db, models
from app.api.auth.views import token_required
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


@main.route('/api/businesses',  methods=[ 'POST'])
# @token_required
# @swag_from('../api_docs/register_business.yml')
def register_business():

    data = request.get_json()

    name = data['name']
    category = data['category']
    location = data['location']
    description = data['description']
    # created_by = data['created_by']

    if data:
        business = Business(name=name,
	                           category=category,
							   location=location,
                               description=description)
        business.save()
        response = jsonify({
                    'id': business.id,
                    'name': business.name,
                    'category': business.category,
                    'location': business.location,
                    'description': business.description
                    # 'created_by': business.created_by
                })
        response.status_code = 201
        return response

    return make_response(
                jsonify({
                    'message': "Business already exists"
                })), 409
    

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
		

@main.route('/api/businesses', methods=['GET'])
# @token_required
# @swag_from('../api_docs/view_businesses.yml')
def view_businesses():
    
    """Endpoint for returning all the registered businesses """
    
    businesses = Business.get_all()
    results = []
    for business in businesses:
                data = {
                    'id': business.id,
                    'name': business.name,
                    'category': business.category,
                    'location': business.location,
                    'description': business.description
                    }
                results.append(data)
    response = jsonify(results)
    response.status_code = 200
    return response
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

@main.route('/api/businesses/<id>', methods=['GET'])
# @token_required
# @swag_from('../api_docs/view_business.yml')
def single_businesses(id):
    
    """Endpoint for returning a single business"""
    business = Business.query.filter_by(id=id).first()
    if business:
        output = {}
        output['name'] = business.name
        output['category'] = business.category
        output['location'] = business.location
        output['description'] = business.description
        return jsonify({"business":output}),  200
    return make_response(("Business does not exist"), 401)



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

@main.route('/api/businesses/<businessid>', methods=['PUT'])
# @token_required
# @swag_from('../api_docs/update_business.yml')
def update_business(current_user, businessid):
    
    """Endpoint for handling business updates"""
    data = request.get_json()
    business = Business.query.filter_by(id=id).first()
    if business:
        business.name = data['new_name'].strip()
        business.description=data['new_description']
        business.location = data['new_location']
        business.category = data['new_category']

        business.save()

        return jsonify({"mesage":"Successfully updated business"})
    return make_response(("Business does not exist"), 401)
    
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

	
@main.route('/api/businesses/<id>', methods=['DELETE'])
# @token_required
# @swag_from('../api_docs/delete_business.yml')
def delete_businesses(id):
    
    """Endpoint for handling deletion of businesses"""
    business = Business.query.filter_by(id=id).first()
    if business:
        business.delete()
        return jsonify({
            "message": "Business {} deleted successfully".format(business.id)}), 200
    return make_response(("Business does not exist"),401)

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
	
	
@main.route('/api/business/<id>/reviews', methods=['POST'])
# @token_required
# @swag_from('../api_docs/add_review.yml')
def addreview(id):
    
    """Endpoint for user to add review on a particular business"""
    data=request.get_json()
    business = Business.query.filter_by(id=id).first()
    if business:
        try:
            review = Review(description=data['description'],businessId=id)
            db.session.add(review)
            db.session.commit()
            message = "Successfully Added Review"
        except:
            return make_response(("Exited with error"), 401)
    else:
        return make_response(("Business does not exist"), 401)
    return jsonify({"messgae":message})

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
				
@main.route('/api/business/<id>/reviews', methods=['GET'])
# @token_required
# @swag_from('../api_docs/view_reviews.yml')
def viewreview(id):
    
    # data=request.get_json()
    business = Business.query.filter_by(id=id).first()
    if business:
        all_reviews = Review.query.all()
        reviews = []
        for review in all_reviews:
            output = {
                'description':review.description,
                'businessId':review.businessId}
            reviews.append(output)
        value = []
        for review in reviews:
            if review['businessId']:
                value.append(review)
        return jsonify({"Reviews":value})
    else:
        return make_response(("Business does not exist"), 401)
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


# """This module defines the application endpoints"""

from flask import request, jsonify, url_for, session, make_response, abort
from flasgger import swag_from
from functools import wraps
import jwt
import datetime
import re
from app import db, models
from app.api.auth.views import token_required
from app.api.models import Business, Review
from . import main




@main.route('/', methods=['GET'])

def index():
	return jsonify({"message":"Welcome to WeConnect"})


@main.route('/api/businesses',  methods=[ 'POST'])
# @token_required
# @swag_from('../api_docs/register_business.yml')
def register_business():

    """Endpoint for handling business registration """
    
    # sent data from postman is converted to a python dictionary
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
        return jsonify(response), 200

    return make_response(
                jsonify({
                    'message': "Business already exists"
                })), 409
    
		

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
    return jsonify(results), 200
    


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




@main.route('/api/businesses/<id>', methods=['PUT'])
# @token_required
# @swag_from('../api_docs/update_business.yml')
def update_business(id):
    
    """Endpoint for handling business updates"""
    
    data = request.get_json()
    business = Business.query.filter_by(id=id).first()
    if business:
        business.name = data['name'].strip()
        business.category = data['category']
        business.location = data['location']
        business.description=data['description']

        business.save()

        return jsonify({"mesage":"Successfully updated business",
                        "Business": data
                        })
    return make_response(("Business does not exist"), 401)

	
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

				
@main.route('/api/business/<id>/reviews', methods=['GET'])
# @token_required
# @swag_from('../api_docs/view_reviews.yml')
def viewreview(id):

    """Endpoint for viewing added reviews for a particular business"""
    
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



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
from app.api.service.business_service import BusinessService

BS = BusinessService()

BUSINESSES_PER_PAGE = 3


@main.route('/', methods=['GET'])
def index():
    return jsonify({"Message": "Welcome to WeConnect"})


@main.route('/api/businesses',  methods=['POST'])
@token_required
@swag_from('../api_docs/register_business.yml')
def register_business(current_user):
    """Endpoint for handling business registration """

    # sent data from postman is converted to a python dictionary
    data = request.get_json()

    name = data['name'].strip()
    category = data['category'].strip()
    location = data['location'].strip()
    description = data['description'].strip()

    # validate json inputs
    if name.strip() == "":
        return make_response(
            jsonify({
                'Message': "Name cannot be empty"
            })), 400
    if name.isdigit():
        return make_response(
            jsonify({
                'Message': "Name cannot be integer"
            })), 400
    if re.match(r'.*[\%\$\^\*\@\!\?\(\)\:\;\&\'\"\{\}\[\]].*',
                str(name)):
        return make_response(
            jsonify({
                'Message': "Name should not have special characters"
            })), 400
    if category and isinstance(category, int):
        return make_response(
            jsonify({
                'Message': "Category cannot be number"
            })), 400
    if category and category.isdigit():
        return make_response(
            jsonify({
                'Message': 'Category cannot be Integer'
            })), 400
    if category.strip() == "":
        return make_response(
            jsonify({
                'Message': "Category cannot be empty"
            })), 400
    if re.match(r'.*[\%\$\^\*\@\!\?\(\)\:\;\&\'\"\{\}\[\]].*',
                str(category)):
        return make_response(
            jsonify({
                'Message': "Category should not have special characters"
            })), 400
    if location and isinstance(location, int):
        return make_response(
            jsonify({
                'Message': "Location cannot be number"
            })), 400
    if re.match(r'.*[\%\$\^\*\@\!\?\(\)\:\;\&\'\"\{\}\[\]].*',
                str(location)):
        return make_response(
            jsonify({
                'Message':
                "Location should not have special characters"
            })), 400
    if location.strip() == "":
        return make_response(
            jsonify({
                'Message': "Location cannot be empty"
            })), 400
    if location and location.isdigit():
        return make_response(
            jsonify({
                'Message': 'Location cannot be Integer'
            })), 400
    if description and isinstance(description, int):
        return make_response(
            jsonify({
                'Message': "Description cannot be number"
            })), 400
    if re.match(r'.*[\%\$\^\*\@\!\?\(\)\:\;\&\'\"\{\}\[\]].*',
                str(description)):
        return make_response(
            jsonify({
                'Message':
                "Description should not have special characters"
            })), 400
    if description.strip() == "":
        return make_response(
            jsonify({
                'Message': "Description cannot be empty"
            })), 400
    if description and description.isdigit():
        return make_response(
            jsonify({
                'Message': 'Description cannot be Integer'
            })), 400

    # Check to see if business with that name exists before adding a new business
    business = Business.query.filter_by(name=name).first()

    if business:
        response = {
            'Message': 'Business already exists'
        }
        return make_response(jsonify(response)), 409
    # adding a new business
    business = Business(name=name,
                        category=category,
                        location=location,
                        description=description,
                        user_id=current_user.id)
    business.save()
    response = {
        'Id': business.id,
        'Name': business.name,
        'Category': business.category,
        'Location': business.location,
        'Description': business.description,
        'User_id': current_user.id,
        'Message': "Business successfully registered"
    }
    return jsonify(response), 201


@main.route('/api/businesses', methods=['GET'])
@token_required
@swag_from('../api_docs/view_businesses.yml')
def view_businesses(current_user):
    """
    get businesses, search by name, filter by location, categoory
    paginate result
    """
    search_string = request.args.get('q', None)
    location = request.args.get('location', None)
    category = request.args.get('category', None)

    # get page nuumber
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', BUSINESSES_PER_PAGE, type=int)

    return BS.get_businesses(page, limit, search_string, location, category)


@main.route('/api/businesses/<id>', methods=['GET'])
@token_required
@swag_from('../api_docs/view_business.yml')
def single_businesses(current_user, id):
    """Endpoint for returning a single business"""
    business = Business.query.filter_by(id=id).first()
    if business:
        output = {}
        output['name'] = business.name
        output['category'] = business.category
        output['location'] = business.location
        output['description'] = business.description
        return jsonify({"Business Data": output}),  200
    return make_response(("Business does not exist"), 401)


@main.route('/api/businesses/<id>', methods=['PUT'])
@token_required
@swag_from('../api_docs/update_business.yml')
def update_business(current_user, id):
    """Endpoint for handling business updates"""

    data = request.get_json()
    business = Business.query.filter_by(id=id).first()
    if business:
        business.name = data['name'].strip()
        business.category = data['category']
        business.location = data['location']
        business.description = data['description']

        business.save()

        return jsonify({"Mesage": "Successfully updated business",
                        "Business Data": data
                        })
    return make_response(("Business does not exist"), 401)


@main.route('/api/businesses/<id>', methods=['DELETE'])
@token_required
@swag_from('../api_docs/delete_business.yml')
def delete_businesses(current_user, id):
    """Endpoint for handling deletion of businesses"""

    business = Business.query.filter_by(id=id).first()
    if business:
        business.delete()
        return jsonify({
            "Message": "Business deleted successfully"
        }), 200
    return make_response(("Business does not exist"), 401)


@main.route('/api/business/<id>/reviews', methods=['POST'])
@token_required
@swag_from('../api_docs/add_review.yml')
def addreview(current_user, id):
    """Endpoint for user to add review on a particular business"""

    data = request.get_json()

    description = data['description'].strip()
    # validate json inputs
    if description and isinstance(description, int):
        return make_response(
            jsonify({
                'Message': "Description cannot be number"
            })), 400
    if re.match(r'.*[\%\$\^\*\@\!\?\(\)\:\;\&\'\"\{\}\[\]].*',
                str(description)):
        return make_response(
            jsonify({
                'Message': "Description should not have special characters"
            })), 400
    if description.strip() == "":
        return make_response(
            jsonify({
                'Message': "Description cannot be empty"
            })), 400
    if description and description.isdigit():
        return make_response(
            jsonify({
                'Message': 'Description cannot be Integer'
            })), 400

    business = Business.query.filter_by(id=id).first()
    if business:
        try:
            review = Review(description=data['description'], businessId=id)
            db.session.add(review)
            db.session.commit()
            response = {"Messgae": "Successfully Added Review",
                        "Review Data": data
                        }
        except:
            return make_response(("Exited with error"), 401)
    else:
        return make_response(("Business does not exist"), 401)
    return jsonify(response), 201


@main.route('/api/business/<id>/reviews', methods=['GET'])
@token_required
@swag_from('../api_docs/view_reviews.yml')
def viewreview(current_user, id):
    """Endpoint for viewing added reviews for a particular business"""

    business = Business.query.filter_by(id=id).first()
    if business:
        all_reviews = Review.query.all()
        reviews = []
        for review in all_reviews:
            output = {
                'description': review.description,
                'businessId': review.businessId}
            reviews.append(output)
        value = []
        for review in reviews:
            if review['businessId']:
                value.append(review)
        return jsonify({"Reviews": value})
    else:
        return make_response(("Business does not exist"), 401)

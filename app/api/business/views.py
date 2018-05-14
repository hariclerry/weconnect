# """This module defines the application endpoints"""

from flask import request, jsonify, url_for, session, make_response, abort
import datetime
import re
from functools import wraps
from flasgger import swag_from
import jwt
from app import db, models
from app.api.models import Business
from . import business
from app.api.auth.views import token_required
from .business_helper import BusinessService

PAG_PAGE = BusinessService()

BUSINESSES_PER_PAGE = 3


@business.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to WeConnect',
                    'status': 'Success'}), 200


@business.route('/api/businesses',  methods=['POST'])
@token_required
@swag_from('../api_docs/register_business.yml')
def register_business(current_user):
    """Endpoint for handling business registration """

    # Sent data from postman is converted to a python dictionary
    data = request.get_json()

    name = data['name'].strip()
    category = data['category'].strip()
    location = data['location'].strip()
    description = data['description'].strip()

    # Validate json inputs
    if not name or not category or not location or not description:
        return jsonify({'message': 'Please fill in all the credentials',
                        'status': 'Failed'}), 400

    # Check to see if business with that name exists before adding a new business
    business = Business.query.filter_by(name=name).first()

    if business is not None:
        response = {
            'message': 'Business already exists',
            'status': 'Failed'
        }
        return make_response(jsonify(response)), 409
    # Add a new business
    business = Business(name=name,
                        category=category,
                        location=location,
                        description=description,
                        user_id=current_user.id)
    business.save()
    response = {
        'Business_data': {'Id': business.id,
                          'Name': business.name,
                          'Category': business.category,
                          'Location': business.location,
                          'Description': business.description,
                          'User_id': current_user.id},
        'message': 'Business successfully registered',
        'status': 'Success'
    }
    return jsonify(response), 201


@business.route('/api/businesses', methods=['GET'])
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

    # Get page number
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', BUSINESSES_PER_PAGE, type=int)

    return PAG_PAGE.get_businesses(page, limit, search_string, location, category)


@business.route('/api/businesses/<id>', methods=['GET'])
@token_required
@swag_from('../api_docs/view_business.yml')
def view_business(current_user, id):
    """Endpoint for returning a single business"""
    business = Business.query.filter_by(id=id).first()

    if business is None:
        return make_response(jsonify({'message': 'Business does not exist',
                                      'status': 'Failed'})), 401

    else:
        output = {}
        output['name'] = business.name
        output['category'] = business.category
        output['location'] = business.location
        output['description'] = business.description
        return jsonify({'Business Data': output}),  200


@business.route('/api/businesses/<id>', methods=['PUT'])
@token_required
@swag_from('../api_docs/update_business.yml')
def update_business(current_user, id):
    """Endpoint for handling business updates"""

    data = request.get_json()

    name = data['name'].strip()
    category = data['category'].strip()
    location = data['location'].strip()
    description = data['description'].strip()

    # validate json inputs
    if not name or not category or not location or not description:
        return jsonify({'message': 'Please fill in all the credentials',
                        'status': 'Failed'}), 400

    business = Business.query.filter_by(id=id).first()

    if business is None:
        return make_response(jsonify({'message': 'Business does not exist',
                                      'status': 'Failed'})), 401
    else:
        business.name = data['name']
        business.category = data['category']
        business.location = data['location']
        business.description = data['description']

        business.save()

        return jsonify({'message': 'Successfully updated business',
                        'business_data': data,
                        'status': 'Succes'}), 200


@business.route('/api/businesses/<id>', methods=['DELETE'])
@token_required
@swag_from('../api_docs/delete_business.yml')
def delete_business(current_user, id):
    """Endpoint for handling deletion of businesses"""

    business = Business.query.filter_by(id=id).first()

    if business is None:
        return make_response(jsonify({'message': 'Business does not exist',
                                      'status': 'Failed'})), 401

    else:
        business.delete()
        return jsonify({
            'message': 'Business deleted successfully',
            'status': 'Success'}), 200

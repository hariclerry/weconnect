# """This module defines the application endpoints"""

from flask import request, jsonify, url_for, session, make_response, abort
from flasgger import swag_from
from functools import wraps
import jwt
import datetime
import re
from app import db, models
from app.api.auth.views import token_required
from ..models import Review
from app.api.models import Business
from . import review



   
@review.route('/api/business/<id>/reviews', methods=['POST'])
@token_required
@swag_from('../api_docs/add_review.yml')
def add_review(current_user, id):
    """Endpoint for user to add review on a particular business"""

    data = request.get_json()

    description = data['description'].strip()
    # Validate json inputs
    if not description:
            return jsonify({'message': 'Please enter description',
                        'status': 'Failed'}), 400
   
    business = Business.query.filter_by(id=id).first()

    if business is None:
         return make_response(jsonify({'message': 'Business does not exist',
                                       'status': 'Failed'})), 401
    else:
            review = Review(description=data['description'], businessId=id)
            db.session.add(review)
            db.session.commit()
            response = {'review_data': data,
                        'message': 'Successfully Added Review',
                        'status': 'Success' }
            return jsonify(response), 201
  

@review.route('/api/business/<id>/reviews', methods=['GET'])
@token_required
@swag_from('../api_docs/view_reviews.yml')
def view_reviews(current_user, id):
    """Endpoint for viewing added reviews for a particular business"""

    business = Business.query.filter_by(id=id).first()

    if business is None:
        return make_response(jsonify({'message': 'Business does not exist',
                                      'status': 'Failed'})), 401
    else:
        all_reviews = Review.query.all()
        reviews = []
        for review in all_reviews:
            output = {
                'description': review.description,
                'businessId': review.businessId}
            reviews.append(output)
        value = []
        for review in reviews:
            if review['businessId'] is not None:
                value.append(review)
        return jsonify({'review_data': value,
                        'status': 'Success'})
    
        

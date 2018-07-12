# """This module defines the application endpoints for Business Reviews"""

import re
import datetime
from functools import wraps

import jwt
from flasgger import swag_from
from flask import request, jsonify, url_for, session, make_response, abort

from app import db, models
from app.api.models import Business
from app.api.auth.views import token_required
from . import review
from ..models import Review



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
        review = Review(description=description, businessId=id, 
                        created_by=current_user.username, user_id=current_user.id)
        db.session.add(review)
        db.session.commit()
        response = {'review_data': { 'reviewId': review.id,
                                      'description': review.description},
                    'message': 'Successfully Added Review',
                    'status': 'Success'}
        return jsonify(response), 201


@review.route('/api/business/<id>/reviews', methods=['GET'])
@token_required
@swag_from('../api_docs/view_reviews.yml')
def view_reviews(current_user, id):
    """Endpoint for viewing added reviews for a particular business"""

    
    reviews = Review.query.filter_by(businessId=id).all()

    if reviews:
        business = Business.query.filter_by(id=id).first()

        review_data=[]
        for review in reviews:
            output={}
            output['description']=review.description
            output['username']=review.created_by

            review_data.append(output)

        return jsonify({'status':'Success',
                            'review_data': review_data}), 200
    else:
        return jsonify({'Status':'Failed',
                            'Message':'No reviews found'}), 404


  
# third-party imports
import os
from flask import Flask
from app import user, business, review, middleware
from config import app_config

# local imports
#import the user, business and review classes
user_object = user.UserDetails()
business_object = business.Business()
review_object = review.Review()

def create_app(config_name):
	# Initialize flask app
	app = Flask(__name__)
	#load from config.py in root folder
	app.config.from_object(app_config[config_name])
	app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
	

	#specify application route url
	# app.wsgi_app = middleware.PrefixMiddleware(app.wsgi_app, prefix='/api/v1')

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	
	return app
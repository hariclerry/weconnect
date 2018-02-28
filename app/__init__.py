# third-party imports
import os
from flask import Flask
from app.models import user, business, review
from config import app_config
from flasgger import Swagger

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
	app.config['SECRET_KEY'] = 'hard to guess string'
	swagger = Swagger(app)
	

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	
	return app
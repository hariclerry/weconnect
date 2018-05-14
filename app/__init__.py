# third-party imports
import os
from flask import Flask
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config


app = Flask(__name__)
# db variable initialization
db = SQLAlchemy()

from app.api import models

def create_app(config_name):
	# Initialize flask app
	app = Flask(__name__)
	#load from config.py in root folder
	app.config.from_object(app_config[config_name])
	app.config['SECRET_KEY'] = 'hard to guess string'
	swagger = Swagger(app)
	db.init_app(app)
	migrate = Migrate(app, db)


	
    
	from app.api.auth import auth as auth5_blueprint
	app.register_blueprint(auth5_blueprint, url_prefix='/v1')

	from app.api.business import business as business_blueprint
	app.register_blueprint(business_blueprint, url_prefix='/v1')

	from app.api.review import review as review_blueprint
	app.register_blueprint(review_blueprint, url_prefix='/v1')

	

	
	return app

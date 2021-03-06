""" Import the create_app method, create the app and start the server"""
import os
from flask import redirect
from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()

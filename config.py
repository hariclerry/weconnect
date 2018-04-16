import os

class Config(object):
    """
    Common configurations
    """
    SECRET_KEY = 'hard to guess string'

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # Put any configurations here that are common across all environments
class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:clerry@localhost/weconnect'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = True

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:clerry@localhost/weconnect'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    

class ProductionConfig(Config):
    """
    Production configurations
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:clerry@localhost/weconnect'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

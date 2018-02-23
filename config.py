class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

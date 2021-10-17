import os 

class Config(object):
    DEBUG = False
    DEVELOPEMENT = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ['POSTGRES_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEBUG = True
    DEVELOPEMENT = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPEMENT = True
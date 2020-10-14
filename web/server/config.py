import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'blackid'
    DATABASE_TYPE = 'postgresql'
    DATABASE_USER = 'traceback'
    DATABASE_PASS = '12345678'
    DATABASE_HOST = '127.0.0.1'
    DATABASE_PORT = '5432'
    DATABASE_NAME = 'traceback'
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(DATABASE_TYPE, DATABASE_USER, DATABASE_PASS, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
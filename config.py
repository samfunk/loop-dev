import os
import pandas as pd
basedir = os.path.abspath(os.path.dirname(__file__))
pd.options.mode.chained_assignment = None


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'change me in production'  # changeme
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class ProductionConfig(Config):
    SECRET_KEY = os.getenv('LOOP_SECRET')
    DEBUG = False


class StagingConfig(Config):
    SECRET_KEY = os.getenv('LOOP_SECRET')
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

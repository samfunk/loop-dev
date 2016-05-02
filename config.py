import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '28f80735910ed7457b2ab4ebbdc76edd6c67712088029d020c4f42fb2ff78ae87b8fad0a918b5f5470130ec22dc0a38281c2e69cef20fb49a0a0d400ebb389ce' #changeme
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    SECRET_KEY = os.environ['LOOP_SECRET']
    DEBUG = False


class StagingConfig(Config):
    SECRET_KEY = os.environ['LOOP_SECRET']
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

import os


class Config(object):
    """App Config"""


class DevConfig(Config):
    """Dev App Config"""
    ENV = 'dev'
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:password@localhost:5432/anduin-dev'


class TestConfig(Config):
    """Test App Config"""
    ENV = 'test'
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:password@localhost:5432/anduin-test'


class ProdConfig(Config):
    """Prod App Config"""
    ENV = 'prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

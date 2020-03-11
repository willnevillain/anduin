import os

LOCAL_DB_PASSWORD = 'shirebaggins'


class Config(object):
    """App Config"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """Dev App Config"""
    ENV = 'dev'
    SQLALCHEMY_DATABASE_URI = f'postgres+psycopg2://postgres:{LOCAL_DB_PASSWORD}@localhost:5432/anduin_dev'


class TestConfig(Config):
    """Test App Config"""
    ENV = 'test'
    SQLALCHEMY_DATABASE_URI = f'postgres+psycopg2://postgres:{LOCAL_DB_PASSWORD}@localhost:5432/anduin_test'


class ProdConfig(Config):
    """Prod App Config"""
    ENV = 'prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

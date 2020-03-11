import os

from anduin.constants import ENV_DEV, ENV_PROD, ENV_TEST

LOCAL_DB_PASSWORD = 'shirebaggins'


class Config(object):
    """App Config"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """Dev Ap Config"""
    ENV = ENV_DEV
    SQLALCHEMY_DATABASE_URI = f'postgres+psycopg2://postgres:{LOCAL_DB_PASSWORD}@localhost:5432/anduin_dev'


class TestConfig(Config):
    """Test App Config"""
    ENV = ENV_TEST
    SQLALCHEMY_DATABASE_URI = f'postgres+psycopg2://postgres:{LOCAL_DB_PASSWORD}@localhost:5432/anduin_test'


class ProdConfig(Config):
    """Prod App Config"""
    ENV = ENV_PROD
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

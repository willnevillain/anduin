import pytest
from webtest import TestApp

from anduin.app import create_app
from anduin.database import db as _db

TEST_CONFIG = 'anduin.config.TestConfig'


@pytest.yield_fixture
def app():
    """Test Application Context"""
    _app = create_app(TEST_CONFIG)
    with _app.app_context():
        _db.create_all()
    ctx = _app.test_request_context()
    ctx.push()

    yield _app


@pytest.fixture
def testapp(app):
    return TestApp(app)


@pytest.yield_fixture
def db(app):
    """Test Database"""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()

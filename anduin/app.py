from flask import Flask

from anduin.db import db


def create_app():
    """Build Flask application"""
    app = Flask(__name__)
    init_db(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def init_db(app):
    """Initialize SQLAlchemy, dynamically create schema"""
    db.init_app(app)
    db.create_all()


def register_blueprints(app):
    """Register blueprints (API endpoint definitions)"""
    pass


def register_errorhandlers(app):
    """Register error handlers"""
    def handle_error(error):
        response = error.to_json()
        response.status_code = error.http_status_code
        return response
    # app.errorhandler(DBError)(handle_error)

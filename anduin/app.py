from flask import Flask

from anduin.extensions import db, migrate


def create_app(config):
    """Build Flask application"""
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)
    register_errorhandlers(app)
    register_extensions(app)
    return app


def register_extensions(app):
    """Register Flask extensions"""
    db.init_app(app)
    migrate.init_app(app, db)


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

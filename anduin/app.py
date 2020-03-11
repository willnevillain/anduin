from flask import Flask

from anduin import cli
from anduin.extensions import db, migrate


def create_app(config):
    """Build Flask application"""
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)
    register_cli(app)
    register_errorhandlers(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    """Register blueprints (API endpoint definitions)"""
    pass


def register_cli(app):
    """Register custom cli commands"""
    app.cli.add_command(cli.backfill)
    app.cli.add_command(cli.empty)


def register_errorhandlers(app):
    """Register error handlers"""
    def handle_error(error):
        response = error.to_json()
        response.status_code = error.http_status_code
        return response
    # app.errorhandler(DBError)(handle_error)


def register_extensions(app):
    """Register Flask extensions"""
    from anduin import models  # Necessary to get Alembic to detect models
    db.init_app(app)
    migrate.init_app(app, db)

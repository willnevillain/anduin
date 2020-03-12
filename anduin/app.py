from flask import Flask

from anduin import cli
from anduin.exceptions import InvalidDataIntegrity, RowNotFound
from anduin.extensions import db, migrate


def create_app(config):
    """Build Flask application"""
    app = Flask(__name__)
    app.config.from_object(config)
    register_cli(app)
    register_errorhandlers(app)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    """Register API routes"""
    from anduin.views.offers import offers_blueprint
    from anduin.views.users import users_blueprint
    app.register_blueprint(offers_blueprint)
    app.register_blueprint(users_blueprint)


def register_cli(app):
    """Register custom cli commands"""
    app.cli.add_command(cli.backfill)
    app.cli.add_command(cli.empty)


def register_errorhandlers(app):
    """Register error handlers"""
    def build_error_body(e):
        return {'error': f'{e.__class__.__name__}: {str(e)}'}

    @app.errorhandler(InvalidDataIntegrity)
    def handle_invalid_data_integrity(e):
        return build_error_body(e), 400

    @app.errorhandler(RowNotFound)
    def handle_row_not_found(e):
        return build_error_body(e), 404


def register_extensions(app):
    """Register Flask extensions"""
    from anduin import models  # Necessary to get Alembic to detect models
    db.init_app(app)
    migrate.init_app(app, db)

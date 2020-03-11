from flask import Flask

from anduin.db import db


def create_app():
    """Build Flask application"""
    app = Flask(__name__)
    db.init_app(app)
    return app

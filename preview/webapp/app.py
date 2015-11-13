#!/usr/bin/env python
"""Web application."""
from flask import Flask

from preview.webapp.api.webhook import webhook


def create_app():
    """Instantiate the Flask app."""
    app = Flask(__name__)
    app.debug = True  # TODO: determine this some other way

    app.register_blueprint(webhook)

    @app.route('/status')
    def status():
        return '200 OK', 200

    return app

#!/usr/bin/env python
"""Web application."""
from flask import Flask

app = Flask(__name__)
app.debug = True  # TODO: determine this some other way

with app.app_context():
    import preview.api.webhook  # noqa

if __name__ == '__main__':
    app.run(host='127.0.0.1')

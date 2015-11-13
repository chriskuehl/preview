#!/usr/bin/env python
import os

from flask import Flask

app = Flask(__name__)
app.debug = True
app.github_webhook_secret = os.environ['PREVIEW_GITHUB_WEBHOOK_SECRET']
app.github_user = os.environ['PREVIEW_GITHUB_USER']
app.github_password = os.environ['PREVIEW_GITHUB_PASSWORD']

with app.app_context():
    import preview.api.views  # noqa
    import preview.webui.views  # noqa

if __name__ == '__main__':
    app.run(host='127.0.0.1')

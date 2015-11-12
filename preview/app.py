#!/usr/bin/env python
from flask import Flask

app = Flask(__name__)
app.debug = True

with app.app_context():
    import preview.api.views  # noqa
    import preview.webui.views  # noqa

if __name__ == '__main__':
    app.run(host='0.0.0.0')

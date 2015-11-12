"""api views"""
from flask import current_app


@current_app.route('/')
def root():
    return 'derp'

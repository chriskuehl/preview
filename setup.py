from setuptools import find_packages
from setuptools import setup

setup(
    name='preview',
    author='Chris Kuehl',
    author_email='ckuehl@ocf.berkeley.edu',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'celery[redis]',
        'flask',
        'github3.py',
        'gunicorn',
    ],
)

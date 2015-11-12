from setuptools import find_packages
from setuptools import setup

setup(
    name='preview',
    author='Chris Kuehl',
    author_email='ckuehl@ocf.berkeley.edu',
    packages=find_packages(),
    install_requires=[
        'flask',
        'gunicorn',
    ],
)

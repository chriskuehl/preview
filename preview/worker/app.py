#!/usr/bin/env python
"""Celery worker."""
from preview.config import get_celery


if __name__ == '__main__':
    celery = get_celery()

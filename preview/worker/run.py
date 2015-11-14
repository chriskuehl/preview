#!/usr/bin/env python3
"""Celery worker wrapper."""
import argparse

from celery.bin.celery import main as celery_main

from preview.config import get_celery


celery = get_celery()

# TODO: this is really dumb, is there a better way...?
import preview.github  # noqa


def main(argv=None):
    """Entrypoint into wrapper."""
    parser = argparse.ArgumentParser(
        description='run preview celery worker',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-l',
        '--log-level',
        default='info',
        help='Logging level',
    )
    parser.add_argument(
        '-d',
        '--debug',
        default=False,
        action='store_true',
        help='Whether to run in debug mode (allows interactive debuggers).',
    )
    args = parser.parse_args(argv)
    extra_args = []

    if args.debug:
        extra_args += ['-P', 'solo']

    exit(celery_main(
        [
            'celery', 'worker',
            '-A', 'preview.worker.run',
            '--without-gossip',
            '--without-mingle',
            '-l', args.log_level,
        ] + extra_args,
    ))


if __name__ == '__main__':
    exit(main())

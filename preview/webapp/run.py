#!/usr/bin/env python3
import argparse

from preview.webapp.app import create_app


app = create_app()


def main(argv=None):
    """Entrypoint into web application."""
    parser = argparse.ArgumentParser(
        description='run preview webapp',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-d',
        '--debug',
        default=False,
        action='store_true',
        help='Whether to run in debug mode (allows interactive debuggers).',
    )
    parser.add_argument(
        '-b',
        '--bind',
        default='127.0.0.1',
        help='Address to bind to.',
    )
    parser.add_argument(
        '-p',
        '--port',
        default=5000,
        help='Port number to bind to.',
    )
    args = parser.parse_args(argv)

    if args.debug:
        app.run(host=args.bind, port=args.port, debug=True)
    else:
        # TODO: gunicorn
        raise NotImplementedError()


if __name__ == '__main__':
    exit(main())

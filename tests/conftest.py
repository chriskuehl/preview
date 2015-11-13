import os
import random
import socket
import subprocess
import sys
import time

import mock
import pytest
import requests


@pytest.yield_fixture(scope='session', autouse=True)
def mock_sane_config():
    sane_config = {
        'PREVIEW_GITHUB_USER': 'test-user',
        'PREVIEW_GITHUB_PASSWORD': 'test-password',
        'PREVIEW_GITHUB_WEBHOOK_SECRET': 'test-webhook-secret',
        'PREVIEW_REDIS_URI': 'redis://localhost',
    }
    with mock.patch.dict(os.environ, sane_config, clear=True):
        yield


@pytest.fixture(scope='session')
def unused_port():
    """Return a random unused port."""
    def used(port):
        s = socket.socket()
        try:
            s.bind(('127.0.0.1', port))
        except Exception:
            return True
        else:
            s.close()
            return False

    port = None
    while port is None or used(port):
        port = random.randint(10000, 65535)

    return port


@pytest.yield_fixture(scope='session')
def running_webapp(unused_port, mock_sane_config):
    """Start a running preview webapp instance.

    Yields a prefix like "http://localhost:1234".

    Example usage:
    assert requests.get(running_webapp + '/status').status_code == 200
    """
    # we'd like to use unix sockets here, but they are poorly supported by
    # requests (and the third-party requests-unixsocket module is buggy)
    proc = subprocess.Popen((
        sys.executable,
        '-m', 'gunicorn.app.wsgiapp',
        '-b', '127.0.0.1:' + str(unused_port),
        'preview.webapp.app:app',
    ))
    prefix = 'http://127.0.0.1:' + str(unused_port)

    start = time.time()
    while time.time() - start < 5:
        try:
            if requests.get(prefix + '/status').status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass

        time.sleep(0.1)
    else:
        raise TimeoutError('Unable to start preview within 5 seconds.')

    yield prefix

    proc.terminate()
    proc.wait()
    assert proc.returncode == 0

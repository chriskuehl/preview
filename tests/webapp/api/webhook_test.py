import pytest

from preview.webapp.api.webhook import _hmac_matches


@pytest.mark.parametrize(('msg', 'signature', 'expected'), [
    (b'hello world', 'derp', False),
    (b'hello world', 'sha1=derp', False),
    (b'hello world', 'sha1=9edc3e5b6db7c7334e7ed362cf4d58c773beb444', True),
    (b'hello world 2', 'sha1=9edc3e5b6db7c7334e7ed362cf4d58c773beb444', False),
    (b'hello world', 'sha2=9edc3e5b6db7c7334e7ed362cf4d58c773beb444', False),
])
def test_hmac_matches(msg, signature, expected):
    assert _hmac_matches(msg, signature) is expected

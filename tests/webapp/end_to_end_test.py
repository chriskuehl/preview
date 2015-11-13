import requests


def test_webapp_status(running_webapp):
    """The web app should start and respond to status."""
    resp = requests.get(running_webapp + '/status')
    assert resp.status_code == 200

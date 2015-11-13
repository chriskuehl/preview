"""GitHub webhook handler."""
import hashlib
import hmac

from flask import current_app
from flask import request

from preview.config import get_config
from preview.github import create_status


def _hmac_matches(msg, signature):
    if not signature or not signature.startswith('sha1='):
        return False

    return signature[5:] == hmac.new(
        get_config().github.webhook_secret.encode('ascii'),
        msg=msg,
        digestmod=hashlib.sha1,
    ).hexdigest()


@current_app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handle an incoming GitHub webhook.

    Example webhooks:

      * New pull request:
        https://gist.github.com/anonymous/abb6dfe180ebed7025a2

      * Updated existing pull request:
        https://gist.github.com/anonymous/22f90074414c89d191ca
    """
    if not _hmac_matches(request.data, request.headers.get('X-Hub-Signature')):
        return '403 Forbidden', 403

    if request.headers['X-Github-Event'] != 'pull_request':
        return '200 OK', 200

    head_repo_name = request.json['pull_request']['head']['repo']['name']
    head_owner = request.json['pull_request']['head']['repo']['owner']['login']
    head_sha = request.json['pull_request']['head']['sha']

    create_status(
        head_owner,
        head_repo_name,
        head_sha,
        'pending',
        'http://www.yelp.com/',
        'what is a description anyway',
    )

    return '200 OK', 200

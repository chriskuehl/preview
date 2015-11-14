"""GitHub webhook handler."""
import hashlib
import hmac
import logging

from flask import Blueprint
from flask import request

from preview.config import get_config
from preview.github import create_status


_logger = logging.getLogger(__name__)
webhook = Blueprint('webhook', __name__)


def _hmac_matches(msg, signature):
    if not signature or not signature.startswith('sha1='):
        return False

    return signature[5:] == hmac.new(
        get_config().github.webhook_secret.encode('ascii'),
        msg=msg,
        digestmod=hashlib.sha1,
    ).hexdigest()


@webhook.route('/api/webhook', methods=['POST'])
def webhook_view():
    """Handle an incoming GitHub webhook.

    Example webhooks:

      * New pull request:
        https://gist.github.com/anonymous/abb6dfe180ebed7025a2

      * Updated existing pull request:
        https://gist.github.com/anonymous/22f90074414c89d191ca
    """
    event_type = request.headers.get('X-Github-Event')
    signature = request.headers.get('X-Hub-Signature')

    _logger.debug('Received webhook with event_type={}'.format(event_type))

    if not _hmac_matches(request.data, signature):
        _logger.warning('Received bad webhook, HMAC validation failed for signature: {}'.format(signature))
        return '403 Forbidden', 403

    if event_type != 'pull_request':
        return '200 OK', 200

    head_repo_name = request.json['pull_request']['head']['repo']['name']
    head_owner = request.json['pull_request']['head']['repo']['owner']['login']
    head_sha = request.json['pull_request']['head']['sha']

    _logger.info('Handling pull request event; head_repo_name={}; head_owner={}; head_sha={}'.format(
        head_repo_name,
        head_owner,
        head_sha,
    ))

    create_status.delay(
        head_owner,
        head_repo_name,
        head_sha,
        'pending',
        'http://www.yelp.com/',
        'what is a description anyway',
    )

    return '200 OK', 200

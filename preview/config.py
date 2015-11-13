"""Read and provide config options."""
import os
from collections import namedtuple
from functools import lru_cache

from celery import Celery

Config = namedtuple('Config', ['github', 'celery'])
GitHubConfig = namedtuple('GitHubConfig', ['webhook_secret', 'user', 'password'])


class CeleryConfig(namedtuple('CeleryConfig', ['backend', 'broker'])):

    @classmethod
    def from_redis_uri(cls, uri):
        return cls(backend=uri, broker=uri)


@lru_cache()
def get_config():
    return Config(
        github=GitHubConfig(
            user=os.environ['PREVIEW_GITHUB_USER'],
            password=os.environ['PREVIEW_GITHUB_PASSWORD'],
            webhook_secret=os.environ['PREVIEW_GITHUB_WEBHOOK_SECRET'],
        ),
        celery=CeleryConfig.from_redis_uri(
            os.environ.get('PREVIEW_REDIS_URI', 'redis://localhost'),
        ),
    )


@lru_cache()
def get_celery():
    config = get_config()
    return Celery(
        broker=config.celery.broker,
        backend=config.celery.backend,
    )

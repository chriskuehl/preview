"""Celery tasks."""
from collections import namedtuple

PreviewTasks = namedtuple('PreviewTasks', ['launch'])


def get_tasks(celery):
    """Return a PreviewTasks object of tasks.

    The purpose of embedding these in a function is that it allows us to pass
    an instantiated Celery app which they use decorators from.
    """
    @celery.task
    def launch():
        return 'oh, hi'

    return PreviewTasks(
        launch=launch,
    )

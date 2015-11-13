import github3
from flask import current_app


def login():
    """Log in to the GitHub api.

    :return: github3.GitHub object
    """
    return github3.login(
        username=current_app.github_user,
        password=current_app.github_password,
    )


def create_status(owner, repo, sha, status, target_url, description):
    """Create a status for a commit.

    :param owner:
    :param repo:
    :param sha:
    :param status: one of 'pending', 'success', 'error', 'failure'
    :param target_url:
    :param description:
    """
    repo = login().repository(owner, repo)
    repo.create_status(
        sha,
        status,
        target_url=target_url,
        description=description,
        context='continuous-intergration/preview',
    )

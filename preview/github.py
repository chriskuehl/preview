import github3

from preview.config import get_config


def login():
    """Log in to the GitHub api.

    :return: github3.GitHub object
    """
    config = get_config()
    return github3.login(
        username=config.github.user,
        password=config.github.password,
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

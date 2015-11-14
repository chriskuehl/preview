"""Building, deploying, and running of revisions.

Docker images for a revision get built into tarballs and stored in the defined
path. During runtime, they can be quickly spun up while the user waits.
"""
import os.path
import re
from hashlib import sha256


IMAGE_PATH = '/var/preview/images/'


def _image_name(repo, revision):
    """Generate a unique name for a (repo, revision) tuple.

    We try to make a somewhat-readable string while still being unique. Sadly,
    we don't do a very good job.

    The only component we rely on for uniqueness is the last 16 characters.

    >>> _image_name('https://github.com/chriskuehl/dotfiles.git', '62ad482324be1883621c4938b7268440e4d8dabd')
    'github.com.chriskuehl.dotfiles-62ad4823-e0917b320a4fa34f'
    """
    # replace consecutive runs of non-alphanum chars with a single dot
    repo = re.sub('[^a-z0-9]+', '.', repo)

    if repo.startswith('https.') or repo.startswith('git.'):
        repo = '.'.join(repo.split('.')[1:])
    if repo.endswith('.git'):
        repo = '.'.join(repo.split('.')[:-1])

    return (
        repo + '-' + revision[:8] + '-' +
        sha256(repo.encode('ascii') + b'\0' + revision.encode('ascii')).hexdigest()[:16]
    )


def image_path(repo, revision):
    return os.path.join(IMAGE_PATH, _image_name(repo, revision))


def build_revision(repo, revision):
    pass

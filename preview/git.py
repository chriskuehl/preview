from subprocess import check_call
from tempfile import mkdtemp


def clone(repo, ref):
    """Clone a git repository, and check out a specific reference.

    :return: path to the checked-out repository
    """
    tempdir = mkdtemp()
    check_call(('git', 'clone', '-n', '--', repo, tempdir))
    check_call(('git', '-C', tempdir, 'checkout', ref))
    check_call(('git', '-C', tempdir, 'submodule', 'update', '--init'))
    return tempdir

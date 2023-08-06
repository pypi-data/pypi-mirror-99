# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Tests with Gitaly are the tests where we directly compare the Hgitaly
response with Gitaly response. Here, the main motive is to make sure that
Hgitaly responses are what Gitlab expects.

In these tests we use Heptapod's GitLab mirror to write the Git repo.

Lots of duplication from py-heptapod tests and setup reuse from
other HGitaly tests feels weird because asymetrical, but it makes the
point.

We don't need to pre-create the Git repo, because GitLab mirror will
do it automatically.
"""
import os
from pathlib import Path

import hgitaly
import logging
import subprocess

logger = logging.getLogger(__name__)


def gitaly_install_dir():  # pragma no cover
    """Return an absolute Path object for the Gitaly source checkout to use.

    The Gitaly sources must have been built.
    This first version assumes we are in HDK context or that
    the ``GITALY_INSTALL_DIR`` environment variable is set (typically in CI).
    """
    from_env = os.environ.get("GITALY_INSTALL_DIR")
    if from_env is not None:
        return Path(from_env).resolve()

    hgitaly_clone = Path(hgitaly.__file__).resolve().parent.parent
    hdk = hgitaly_clone.parent
    install_dir = hdk / 'gitaly'
    if install_dir.is_dir():
        gitaly = (install_dir / 'gitaly')
        if gitaly.is_file():
            # startup costs about 0.15s. That's a lot, but it will
            # make sure our skip is correct and it is useful to log the
            # version number
            version = subprocess.check_output((str(gitaly),
                                               '-version')).decode()
            assert 'Gitaly' in version
            logger.info("Found %s at %s. Will lauch comparison tests "
                        "of HGitaly with Gitaly", version, gitaly)
            return install_dir


GITALY_INSTALL_DIR = gitaly_install_dir()


def gitaly_not_installed():
    return GITALY_INSTALL_DIR is None


def skip_comparison_tests():
    return (gitaly_not_installed()
            or os.environ.get('SKIP_GITALY_COMPARISON_TESTS'))

# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import logging
import re

from mercurial import (
    error,
    scmutil,
)
from hgext3rd.heptapod.branch import get_default_gitlab_branch
from heptapod.gitlab.branch import (
    gitlab_branch_from_ref,
)
from .branch import (
    gitlab_branch_head
)
from .gitlab_ref import (
    gitlab_special_ref_target
)

logger = logging.getLogger(__name__)

# 40 hex digits for SHA-1, 64 hex digits for SHA-2
_HASH_RX = r'^([0-9A-Fa-f]{40})|([0-9A-Fa-f]{64})$'
CHANGESET_HASH_BYTES_REGEXP = re.compile(_HASH_RX.encode('ascii'))
CHANGESET_HASH_STR_REGEXP = re.compile(_HASH_RX)


def gitlab_revision_changeset(repo, revision):
    """Find the changeset for a given GitLab revision.

    In theory, a GitLab revision could be any Git valid revspec, that
    we'd had to translate into its Mercurial counterpart.

    At this point, we support changeset IDs in hex, GitLab branches, tags and
    ``HEAD`` (default GitLab branch).

    Obsolescence
    ------------
    Changeset IDs can return obsolete changesets (this is actually used in
    force push detection, or in Merge Request updates), while symbolic ones
    (branch, tags etc) *should* always return non obsolete changesets.

    :return: the changeset as a :class:`changectx` instance, or ``None``
             if not found.
    """
    if revision == b'HEAD':
        revision = get_default_gitlab_branch(repo)

    # non ambigous ref forms: they should obviously take precedence
    # TODO direct reference to tag here as well
    gl_branch = gitlab_branch_from_ref(revision)
    if gl_branch is not None:
        # can return None
        return gitlab_branch_head(repo, gl_branch)

    # special ref
    ctx = gitlab_special_ref_target(repo, revision)
    if ctx is not None:
        return ctx

    # direct GitLab branch name
    ctx = gitlab_branch_head(repo, revision)
    if ctx is not None:
        return ctx

    try:
        # TODO we should probably give precedence to tags, as Mercurial
        # does, although we should check what Git(aly) really does in
        # case of naming conflicts
        return scmutil.revsingle(repo.unfiltered(), revision)
    except error.RepoLookupError:
        return None  # voluntarily explicit

# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Helper functions for interacting with package licenses
"""

from functools import lru_cache
from typing import List, Union

from portmod.config import get_config
from portmod.config.use import get_use
from portmod.parsers.usestr import use_reduce
from portmod.pybuild import Pybuild
from portmod.repo import get_repo, get_repo_root
from portmod.repo.metadata import get_license_groups


def is_license_accepted(mod: Pybuild) -> bool:
    """
    Returns true if the mod's license(s) are accepted by the user's configuration

    For a license to be accepted, it must be both listed, either explicitly,
    part of a group, or with the * wildcard  and it must not be blacklisted
    by a license or license group prefixed by a '-'
    """
    if mod.INSTALLED:
        license_groups = get_license_groups(get_repo(mod.REPO).location)
    else:
        license_groups = get_license_groups(get_repo_root(mod.FILE))

    ACCEPT_LICENSE = get_config()["ACCEPT_LICENSE"]

    def accepted(group: Union[str, List]) -> bool:
        if not group:
            return True

        if isinstance(group, str):
            allowed = False
            # Check if license is allowed by anything in ACCEPT_LICENSE
            for license in ACCEPT_LICENSE:
                if license.startswith("-") and (
                    license == group
                    or (license[1] == "@" and group in license_groups[license[2:]])
                ):
                    # not allowed if matched by this
                    return False
                if license == "*":
                    allowed = True
                if license.startswith("@") and group in license_groups[license[1:]]:
                    allowed = True
            return allowed
        if group[0] == "||":
            return any(accepted(license) for license in group)

        return all(accepted(license) for license in group)

    enabled, disabled = get_use(mod)
    return accepted(use_reduce(mod.LICENSE, enabled, disabled, opconvert=True))

    # TODO: implement package-specific license acceptance via package.license config file


@lru_cache()
def has_eula(package: Pybuild) -> bool:
    groups = get_license_groups(get_repo_root(package.FILE))
    # FIXME: This should be reworked.
    # For one thing, this doesn't currently handle || operators
    return any(
        license_name in groups.get("EULA", set())
        for license_name in use_reduce(
            package.LICENSE, get_use(package)[0], get_use(package)[1], flat=True
        )
    )

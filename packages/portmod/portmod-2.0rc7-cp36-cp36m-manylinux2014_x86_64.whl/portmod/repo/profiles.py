# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Module for interacting with the user's profile
and iterating over the various associated directories
"""

import os
from pathlib import Path
from typing import List, Set

from portmod.atom import Atom
from portmod.functools import prefix_aware_cache
from portmod.globals import env
from portmod.parsers.list import read_list


def profile_exists() -> bool:
    return bool(
        env.PREFIX_NAME
        and os.path.exists(os.path.join(env.prefix().PORTMOD_CONFIG_DIR, "profile"))
    )


def get_profile_path() -> str:
    """Returns the path to the profile directory"""
    profilepath = os.path.join(env.prefix().PORTMOD_CONFIG_DIR, "profile")
    if not os.path.exists(profilepath) or not os.path.islink(profilepath):
        raise Exception(
            f"{profilepath} does not exist.\n"
            "Please choose a profile before attempting to install packages"
        )
    # Note: Path must be resolved with pathlib to ensure that
    # the path doesn't include \\?\ on Windows
    return str(Path(os.readlink(profilepath)).resolve())


@prefix_aware_cache
def profile_parents() -> List[str]:
    """
    Produces the paths of all the parent directories for the selected profile, in order
    """
    if not env.PREFIX_NAME:
        return []

    first = get_profile_path()

    def get_parents(directory: str) -> List[str]:
        parentfile = os.path.join(directory, "parent")
        parents = []
        if os.path.exists(parentfile):
            for parent in read_list(parentfile):
                parentpath = os.path.normpath(os.path.join(directory, parent))
                parents.extend(get_parents(parentpath))
                parents.append(parentpath)

        return parents

    parents = [first]
    parents.extend(get_parents(first))

    userpath = os.path.join(env.prefix().PORTMOD_CONFIG_DIR, "profile.user")
    if os.path.exists(userpath):
        parents.append(userpath)
        parents.extend(get_parents(userpath))

    return parents


def get_system() -> Set[Atom]:
    """Calculates the system set using the user's currently selected profile"""
    system: Set[Atom] = set()
    for parent in profile_parents():
        packages = os.path.join(parent, "packages")
        if os.path.exists(packages):
            system |= {
                Atom(mod.lstrip("*"))
                for mod in read_list(packages)
                if mod.startswith("*")
            }

    return system

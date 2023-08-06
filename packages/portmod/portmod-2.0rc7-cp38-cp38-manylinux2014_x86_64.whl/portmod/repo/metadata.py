# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Helper functions for interacting with repository metadata files.
"""

import glob
import os
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple

from portmod.config import read_config
from portmod.globals import env
from portmod.parsers.list import read_list
from portmod.portmod import (
    PackageMetadata,
    parse_category_metadata,
    parse_package_metadata,
    parse_yaml_dict,
    parse_yaml_dict_dict,
)
from portmod.pybuild import Pybuild

from . import Repo, get_repo

# Note: All repository files should be encoded as utf-8.


@lru_cache()
def __get_layout(repo_path) -> Dict:
    path = os.path.join(repo_path, "metadata", "layout.conf")
    if os.path.exists(path):
        return read_config(path, {})
    return {}


@lru_cache()
def get_master_names(repo_path: str) -> Set[str]:
    """Returns the direct masters for the repository at the given path"""
    masters = set()
    for master in __get_layout(repo_path).get("masters", "").split():
        masters.add(master)
    return masters


@lru_cache()
def get_masters(repo_path: str) -> List[Repo]:
    """Returns the direct masters for the repository at the given path"""
    return [get_repo(master) for master in get_master_names(repo_path)]


@lru_cache()
def get_categories(repo: str) -> Set[str]:
    """Retrieves the list of categories given a path to a repo"""
    categories: Set[str] = {"common"}
    path = os.path.join(repo, "profiles", "categories")
    if os.path.exists(path):
        categories |= set(read_list(path, encoding="utf-8"))
    for master in get_masters(repo):
        categories |= get_categories(master.location)

    return categories


@lru_cache()
def get_archs(repo: str) -> Set[str]:
    """Returns the available architectures in a given repo"""
    archs: Set[str] = set()
    path = os.path.join(repo, "profiles", "arch.list")
    if os.path.exists(path):
        archs |= set(read_list(path, encoding="utf-8"))

    for master in get_masters(repo):
        archs |= get_archs(master.location)

    return archs


@lru_cache()
def get_global_use(repo) -> Dict[str, str]:
    """
    Returns the global use flag declarations for a given repository

    Each mapping in the result dictionary represents a use flag
    and its description
    """
    use: Dict[str, str] = {}
    path = os.path.join(repo, "profiles", "use.yaml")
    if os.path.exists(path):
        use.update(parse_yaml_dict(path))

    for master in get_masters(repo):
        use.update(get_global_use(master.location))

    return use


@lru_cache()
def get_profiles() -> List[Tuple[str, str, str]]:
    """
    Returns the list of profiles available from all known repositories

    Result is a tuple containing the profile's path, name and stability keyword
    """
    profiles: List[Tuple[str, str, str]] = []
    for repo in env.prefix().REPOS:
        path = os.path.join(repo.location, "profiles", "profiles.yaml")
        if os.path.exists(path):
            repo_profiles = parse_yaml_dict_dict(path)
            for keyword in sorted(repo_profiles):
                for profile in sorted(repo_profiles[keyword]):
                    path = os.path.join(repo.location, "profiles", profile)
                    profiles.append((path, profile, repo_profiles[keyword][profile]))
    return profiles


@lru_cache()
def license_exists(repo: str, name: str) -> bool:
    """
    Returns true if the given license name corresponds to a
    licence in the repository
    """
    path = os.path.join(repo, "licenses", name)
    if os.path.exists(path):
        return True

    for master in get_masters(repo):
        if license_exists(master.location, name):
            return True

    return False


@lru_cache()
def get_license(repo: str, name: str) -> str:
    """Returns the full content of the named license"""
    path = os.path.join(repo, "licenses", name)
    if os.path.exists(path):
        with open(path, mode="r", encoding="utf-8") as license_file:
            return license_file.read()
    else:
        for master in get_masters(repo):
            license_contents = get_license(master.location, name)
            if license is not None:
                return license_contents

        raise Exception("Nonexistant license: {}".format(name))


@lru_cache()
def get_license_groups(repo: str) -> Dict[str, Set[str]]:
    """
    Returns license groups defined by this repository and its masters

    @param repo: path to repository
    @returns set of license groups
    """
    result = {}
    path = os.path.join(repo, "profiles", "license_groups.yaml")
    if os.path.exists(path):
        groups = parse_yaml_dict(path)

        for name, values in groups.items():
            if values is not None:
                result[name] = set(values.split())
            else:
                result[name] = set()

    def substitute(group: str):
        groups = []
        for license in result[group]:
            if license.startswith("@"):
                groups.append(license)
        for subgroup in groups:
            result[group].remove(subgroup)
            substitute(subgroup.lstrip("@"))
            result[group] |= result[subgroup.lstrip("@")]

    for group in result:
        substitute(group)

    for master in get_masters(repo):
        result.update(get_license_groups(master.location))

    return result


@lru_cache()
def get_package_metadata(mod: Pybuild) -> Optional[PackageMetadata]:
    """Loads the metadata file for the given mod"""
    path = os.path.join(os.path.dirname(mod.FILE), "metadata.yaml")
    if not os.path.exists(path):
        return None

    return parse_package_metadata(path)


@lru_cache()
def get_category_metadata(repo: str, category: str):
    """Loads the metadata file for the given category"""
    path = os.path.join(repo, category, "metadata.yaml")

    if os.path.exists(path):
        return parse_category_metadata(path)

    for master in get_masters(repo):
        metadata = get_category_metadata(master.location, category)
        if metadata is not None:
            return metadata

    return None


@lru_cache()
def get_use_expand(repo: str) -> Set[str]:
    """Returns all possible use expand values for the given repository"""
    groups = set()
    for file in glob.glob(os.path.join(repo, "profiles", "desc", "*.yaml")):
        use_expand, _ = os.path.splitext(os.path.basename(file))
        groups.add(use_expand.upper())
    for master in get_masters(repo):
        groups |= get_use_expand(master.location)

    return groups


@lru_cache()
def get_use_expand_values(repo: str, use_expand: str) -> Dict[str, str]:
    """Returns all possible use expand values for the given repository"""
    values = {}
    for master in get_masters(repo):
        values.update(get_use_expand_values(master.location, use_expand))

    lowered = use_expand.lower()
    path = os.path.join(repo, "profiles", "desc", lowered + ".yaml")
    if os.path.exists(path):
        kvps = parse_yaml_dict(path)
        values.update(kvps)

    return values


@lru_cache()
def check_use_expand_flag(repo: str, variable: str, flag: str) -> bool:
    """
    Returns true if the given use flag is declared
    in a USE_EXPAND desc file for the given variable
    """
    path = os.path.join(repo, "profiles", "desc", variable.lower() + ".yaml")
    if os.path.exists(path):
        if flag in parse_yaml_dict(path):
            return True

    for master in get_masters(repo):
        if check_use_expand_flag(master.location, variable, flag):
            return True

    return False

# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Functions for interacting with the OpenMW VFS
"""

import os
import shutil
from logging import error, info, warning
from tempfile import gettempdir
from typing import Dict, List, Set, Tuple

from .atom import Atom, atom_sat
from .fs.archives import extract_archive_file, list_archive
from .fs.util import ci_exists
from .functools import clear_vfs_cache, vfs_cache
from .globals import env
from .l10n import l10n
from .loader import load_all_installed_map, load_installed_pkg
from .parsers.list import read_list, write_list
from .parsers.userconf import read_userconfig
from .parsers.usestr import use_reduce
from .pybuild import InstalledPybuild
from .tsort import CycleException, tsort


def _usedep_matches_installed(atom: Atom) -> bool:
    mod = load_installed_pkg(atom.strip_use())
    if not mod:
        return False  # If override isn't installed, it won't be in the graph

    for flag in atom.USE:
        if flag.startswith("-") and flag.lstrip("-") in mod.INSTALLED_USE:
            return False  # Required flag is not set
        elif not flag.startswith("-") and flag not in mod.INSTALLED_USE:
            return False  # Required flag is not set

    return True


def sort_vfs_if_needed(user_function):
    """
    Decorator that sorts the vfs before executing the given function
    if it is necessary
    """

    def decorating_function(*args, **kwargs):
        if vfs_needs_sorting():
            try:
                sort_vfs()
                clear_vfs_sort()
            except CycleException as err:
                error(f"{err}")
        return user_function(*args, **kwargs)

    return decorating_function


@vfs_cache
def find_file(name: str) -> str:
    """
    Locates the path of a file within the OpenMW virtual file system

    args:
        name: The relative path within the VFS to search for

    returns:
        The absolute path of the file
    """
    # FIXME: This should respect the CASE_INSENSITIVE_FILES setting
    for directory in reversed(get_vfs_dirs()):
        path = ci_exists(os.path.join(directory, name))
        if path:
            return path

    for archive in reversed(get_vfs_archives()):
        contents = list_archive(archive)
        for file in contents:
            if os.path.normpath(file).lower() == os.path.normpath(name).lower():
                return extract_archive_file_to_tmp(archive, file)

    raise FileNotFoundError(name)


@vfs_cache
def list_dir(name: str) -> List[str]:
    """
    Locates all path of files matching the given pattern within the OpenMW
    virtual file system

    args:
        name: The relative path of the directory within the VFS
    returns:
        A list of files contained within the directory
    """
    files: Dict[str, str] = {}
    normalized = os.path.normpath(name).lower()

    # FIXME: This should respect the CASE_INSENSITIVE_FILES setting

    for directory in reversed(get_vfs_dirs()):
        path = ci_exists(os.path.join(directory, normalized))
        if path:
            for file in os.listdir(path):
                if file.lower() not in files:
                    files[file.lower()] = file

    for archive in reversed(get_vfs_archives()):
        contents = list_archive(archive)
        for file in contents:
            if (
                os.path.commonpath([normalized, os.path.normpath(file).lower()])
                == normalized
            ):
                suffix = os.path.relpath(os.path.normpath(file).lower(), normalized)
                component, _, _ = suffix.partition(os.sep)
                files[component] = component

    return sorted(files.values())


def _cleanup_tmp_archive_dir():
    path = os.path.join(gettempdir(), ".archive_files")
    if os.path.exists(path):
        shutil.rmtree(path)


def extract_archive_file_to_tmp(archive: str, file: str) -> str:
    """Extracts the given file from the archive and places it in a temprorary directory"""
    temp = gettempdir()
    output_dir = os.path.join(
        temp, ".archive_files", os.path.basename(archive), os.path.dirname(file)
    )
    os.makedirs(output_dir, exist_ok=True)
    result_file = os.path.join(output_dir, os.path.basename(file))
    extract_archive_file(archive, file, output_dir)
    if not os.path.exists(result_file):
        raise Exception(l10n("archive-extraction-failed", file=file, dest=result_file))
    return result_file


@vfs_cache
def get_vfs_dirs() -> List[str]:
    """Returns an ordered list of the VFS directories, in reverse order of priority"""
    return read_list(os.path.join(env.prefix().PACKAGE_DIR, "vfs"))


def __set_vfs_dirs__(dirs: List[str]):
    """Updates the vfs directories"""
    write_list(os.path.join(env.prefix().PACKAGE_DIR, "vfs"), dirs)


@vfs_cache
def get_vfs_archives() -> List[str]:
    """Returns an ordered list of the VFS directories, in reverse order of priority"""
    return read_list(os.path.join(env.prefix().PACKAGE_DIR, "vfs-archives"))


def __set_vfs_archives(archives: List[str]):
    """Updates the vfs directories"""
    write_list(os.path.join(env.prefix().PACKAGE_DIR, "vfs-archives"), archives)


def require_vfs_sort():
    """
    Creates a file that indicates the vfs still needs to be sorted
    """
    open(
        os.path.join(env.prefix().PORTMOD_LOCAL_DIR, ".vfs_sorting_incomplete"), "a"
    ).close()


def clear_vfs_sort():
    """Clears the file indicating the config needs sorting"""
    path = os.path.join(env.prefix().PORTMOD_LOCAL_DIR, ".vfs_sorting_incomplete")
    if os.path.exists(path):
        os.remove(path)


def vfs_needs_sorting():
    """Returns true if changes have been made since the config was sorted"""
    return os.path.exists(
        os.path.join(env.prefix().PORTMOD_LOCAL_DIR, ".vfs_sorting_incomplete")
    )


def sort_vfs():
    """Regenerates the vfs list"""
    info(l10n("sorting-vfs"))
    _sort_vfs_dirs()
    _sort_vfs_archives()
    clear_vfs_cache()


def load_userconfig(typ: str, installed_dict: Dict[str, List[InstalledPybuild]]):
    """Checks entries in userconfig and warns on errors"""
    # Keys refer to master atoms (overridden).
    # values are a set of overriding mod atomso
    user_config_path = os.path.join(
        env.prefix().PORTMOD_CONFIG_DIR, "config", f"{typ}.csv"
    )
    userconfig: Dict[str, Set[str]] = read_userconfig(user_config_path)

    for entry in userconfig.keys() | {
        item for group in userconfig.values() for item in group
    }:
        possible_mods = installed_dict.get(Atom(entry).PN, [])
        if not possible_mods:
            warning(
                l10n("user-config-not-installed", entry=entry, path=user_config_path)
            )
        elif len(possible_mods) > 1:
            warning(
                l10n(
                    "user-config-ambiguous",
                    entry=entry,
                    path=user_config_path,
                    packages=" ".join([mod.ATOM.CPF for mod in possible_mods]),
                )
            )
    return userconfig


def _sort_vfs_archives():
    installed_dict = load_all_installed_map()
    installed = [mod for group in installed_dict.values() for mod in group]

    graph: Dict[str, Set[str]] = {}
    priorities = {}

    for mod in installed:
        for install, file in mod.get_files("ARCHIVES"):
            path = mod.get_file_path(install, file)
            graph[path] = set()
            priorities[path] = mod.TIER

    userconfig = load_userconfig("archives", installed_dict)

    # Add edges in the graph for each data override
    for mod in installed:
        for install, file in mod.get_files("ARCHIVES"):
            path = mod.get_file_path(install, file)

            masters = set()
            if isinstance(file.OVERRIDES, str):
                masters |= set(use_reduce(file.OVERRIDES, mod.INSTALLED_USE))
            else:
                masters |= set(file.OVERRIDES)

            if file.NAME in userconfig:
                masters |= set(userconfig[path])

            for master in masters:
                if master in graph:
                    graph[master].add(path)
    try:
        sorted_archives = tsort(graph, priorities)
    except CycleException as error:
        raise CycleException(l10n("vfs-cycle-error"), error.cycle) from error

    __set_vfs_archives(sorted_archives)


def _sort_vfs_dirs():
    installed_dict = load_all_installed_map()
    installed = [mod for group in installed_dict.values() for mod in group]

    graph: Dict[Tuple[str, str, bool], Set[Tuple[str, str, bool]]] = {}
    priorities = {}

    userconfig = load_userconfig("install", installed_dict)

    # Determine all Directories that are enabled
    for mod in installed:
        for install in mod.get_directories():
            default = os.path.normpath(install.PATCHDIR) == "."
            path = mod.get_dir_path(install)
            graph[(mod.ATOM.CP, path, default)] = set()
            priorities[(mod.CP, path, default)] = mod.TIER

    # Add edges in the graph for each data override
    for mod in installed:
        for install in mod.get_directories():
            idefault = os.path.normpath(install.PATCHDIR) == "."
            ipath = mod.get_dir_path(install)
            parents = set(
                use_reduce(
                    mod.DATA_OVERRIDES + " " + install.DATA_OVERRIDES,
                    mod.INSTALLED_USE,
                    flat=True,
                    token_class=Atom,
                )
            ) | {
                Atom(override)
                for name in userconfig
                for override in userconfig[name]
                if atom_sat(mod.ATOM, Atom(name))
            }

            for parent in parents:
                if not _usedep_matches_installed(parent):
                    continue

                for (atom, path, default) in graph:
                    if atom_sat(Atom(atom), parent) and default:
                        if Atom(atom).BLOCK:
                            # Blockers have reversed edges
                            graph[(mod.ATOM.CP, ipath, idefault)].add(
                                (atom, path, default)
                            )
                        else:
                            graph[(atom, path, default)].add((mod.CP, ipath, idefault))
    try:
        sorted_mods = tsort(graph, priorities)
    except CycleException as error:
        raise CycleException(l10n("vfs-cycle-error"), error.cycle) from error

    new_dirs = [path for _, path, _ in sorted_mods]
    __set_vfs_dirs__(new_dirs)

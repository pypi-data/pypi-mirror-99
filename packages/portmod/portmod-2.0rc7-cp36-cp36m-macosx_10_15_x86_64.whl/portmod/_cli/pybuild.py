# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
CLI for interacting with individual pybuild files
"""

import os
import py_compile
import sys
from glob import glob
from logging import error, info

from portmod.download import download_source
from portmod.globals import env
from portmod.l10n import l10n
from portmod.loader import load_file
from portmod.parsers.manifest import FileType, Manifest, ManifestEntry
from portmod.pybuild import Pybuild, manifest_path
from portmod.repo import get_repo_root
from portmod.repos import Repo
from portmod.source import HashAlg


def create_manifest(mod: Pybuild):
    """
    Automatically downloads mod DIST files (if not already in cache)
    and creates a manifest file
    """
    pybuild_file = mod.FILE
    manifest = Manifest(manifest_path(pybuild_file))
    manifest.entries = {}

    directory = os.path.dirname(pybuild_file)

    for file in glob(os.path.join(directory, "*.pybuild")):
        thismod = load_file(file)
        sources = thismod._get_sources(matchall=True)

        # Add sources to manifest
        for source in sources:
            filename = download_source(mod, source)
            if filename is None:
                error("Unable to get shasum for unavailable file " + source.name)
                continue

            manifest.add_entry(
                ManifestEntry.from_path(
                    FileType.DIST, filename, source.name, [HashAlg.BLAKE3, HashAlg.MD5]
                )
            )

    # Write changes to manifest
    manifest.write()


def pybuild_validate(file_name):
    # Verify that pybuild is valid python
    py_compile.compile(file_name, doraise=True)

    # Verify fields of pybuild
    pkg = load_file(file_name)
    pkg.validate()


def pybuild_manifest(file_name):
    if not os.path.exists(file_name):
        raise FileNotFoundError(l10n("file-does-not-exist", file=file_name))

    repo_root = get_repo_root(file_name)

    if repo_root is None:
        raise FileNotFoundError(l10n("repository-does-not-exist"))

    # Register repo in case it's not already in repos.cfg
    REAL_ROOT = os.path.realpath(repo_root)
    if not any([REAL_ROOT == os.path.realpath(repo.location) for repo in env.REPOS]):
        sys.path.append(os.path.join(repo_root))
        env.REPOS.append(Repo(os.path.basename(repo_root), repo_root))

    if env.ALLOW_LOAD_ERROR:
        raise Exception("Cannot allow load errors when generating manifest!")

    mod = load_file(file_name)

    create_manifest(mod)
    info(l10n("created-manifest", atom=mod.ATOM))

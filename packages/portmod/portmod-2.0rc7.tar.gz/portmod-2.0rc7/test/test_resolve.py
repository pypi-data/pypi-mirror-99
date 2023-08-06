# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import sys

import pytest

from portmod._deps import resolve
from portmod.atom import Atom, version_gt
from portmod.config.sets import get_set
from portmod.config.use import add_use
from portmod.loader import load_installed_pkg
from portmod.merge import configure
from portmod.transactions import Downgrade, New, Reinstall, Update

from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def test_simple(setup):
    """Tests that simple dependency resolution works"""
    selected = {Atom("test/test")}
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert transactions.pkgs[0].pkg.CPN == "test/test"
    assert isinstance(transactions.pkgs[0], New)

    configure(["test/test"], no_confirm=True)
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert transactions.pkgs[0].pkg.CPN == "test/test"
    assert isinstance(transactions.pkgs[0], Reinstall)


def test_rebuild(setup):
    """
    Tests that packages are selected to be rebuilt, even if we don't
    use the Category-PackageName format
    """
    selected = {Atom("~test/test-1.0")}
    configure(selected, no_confirm=True)
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert transactions.pkgs[0].pkg.CPN == "test/test"
    assert transactions.pkgs[0].pkg.REPO == "test"
    assert isinstance(transactions.pkgs[0], Reinstall)


def test_upgrade(setup):
    """Tests that upgrades resolve correctly"""
    selected = {Atom("test/test")}
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert version_gt(transactions.pkgs[0].pkg.PVR, "1.0")
    assert isinstance(transactions.pkgs[0], Update)


def test_oneshot(setup):
    """Tests that oneshot resolves correctly"""
    selected = {Atom("test/test")}
    configure(selected, no_confirm=True)
    transactions = resolve(selected, set(), selected, set(), set())
    assert len(transactions.pkgs) == 1
    assert not version_gt(transactions.pkgs[0].pkg.PVR, "2.0")
    assert not version_gt("2.0", transactions.pkgs[0].pkg.PVR)
    assert isinstance(transactions.pkgs[0], Reinstall)
    assert not transactions.new_selected


@pytest.mark.xfail(
    sys.platform == "win32" and "APPVEYOR" in os.environ,
    reason="For some reason a file is being accessed by another process",
    raises=PermissionError,
)
def test_downgrade(setup):
    """Tests that downgrades resolve correctly"""
    configure(["=test/test-2.0"], no_confirm=True)
    selected = {Atom("=test/test-1.0")}
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert version_gt("2.0", transactions.pkgs[0].pkg.PVR)
    assert isinstance(transactions.pkgs[0], Downgrade)


def test_auto_depclean(setup):
    """
    Tests that auto depclean doesn't change configuration to remove packages

    There are two possibly changes that it shouldn't make for this test.
    test7-1.0 could be downgraded to test7-0.1 to remove the dependencies
    And test7-1.0's flags could be disabled to remove the dependencies.
    """
    configure(["=test/test7-1.0[baz]"], no_confirm=True)
    pkg = load_installed_pkg(Atom("test/test5"))
    assert pkg
    transactions = resolve(
        {Atom("test/test7")},
        set(),
        set(),
        set(),
        {"world"},
        update=True,
        newuse=True,
        deep=True,
        noreplace=True,
        depclean=True,
    )
    assert len(transactions.pkgs) == 0


def test_upgrade_configuration(setup):
    """
    Tests that upgrades will pull in new packages and change configuration if necessary
    """
    configure(["@installed"], no_confirm=True, delete=True)
    configure(
        ["=test/test7-0.1"],
        no_confirm=True,
        update=True,
        newuse=True,
        deep=True,
        noreplace=True,
    )
    add_use("baz")
    pkg = load_installed_pkg(Atom("test/test5"))
    assert not pkg
    transactions = resolve(
        get_set("world"),
        set(),
        set(),
        set(),
        {"world"},
        update=True,
        newuse=True,
        deep=True,
        noreplace=True,
    )
    for change in transactions.config:
        raise Exception(f"Unexpected configuration change {change}")
    assert len(transactions.pkgs) == 3
    for change in transactions.pkgs:
        if isinstance(change, Update):
            assert change.pkg.P == "test7-1.0"
        elif isinstance(change, New):
            assert change.pkg.PN in {"test5", "test4"}
        else:
            raise Exception(f"Unexpected transaction ({change.REPR}) {change.pkg}")

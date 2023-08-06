# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import re
import sys
from typing import AbstractSet, Any, Callable, Dict, Iterable, List, Optional, Set, cast

from .atom import Atom, FQAtom, QualifiedAtom, atom_sat, version_gt
from .colour import blue, bright, green, lgreen, red, yellow
from .config import get_config
from .config.sets import is_selected
from .config.use import get_use, get_use_expand
from .download import get_download_size
from .l10n import l10n
from .loader import (
    SandboxedError,
    _sandbox_execute_pybuild,
    load_installed_pkg,
    load_pkg_fq,
)
from .parsers.flags import collapse_flags
from .parsers.usestr import use_reduce
from .perms import Permissions
from .pybuild import InstalledPybuild, Pybuild
from .query import get_flag_string
from .tsort import CycleException, tsort
from .util import select_package


class PackageDoesNotExist(Exception):
    """Indicates that no mod matching this atom could be loaded"""

    def __init__(self, atom: Optional[Atom] = None, *, msg=None):
        super().__init__(msg or l10n("package-does-not-exist", atom=green(atom)))


class Trans:
    """Transaction class"""

    REPR: str
    COLOUR: Callable[[str], str]
    pkg: Pybuild

    def __init__(self, pkg: Pybuild):
        self.pkg = pkg

    def __str__(self):
        return f"{self.__class__.__name__}({self.pkg})"

    def __repr__(self):
        return str(self)


class Delete(Trans):
    """Delete Transaction"""

    REPR = "d"
    COLOUR = red
    pkg: InstalledPybuild

    def __init__(self, pkg: InstalledPybuild):
        super().__init__(pkg)


class New(Trans):
    """New Package Transaction"""

    REPR = "N"
    COLOUR = lgreen


class Change(Trans):
    """Update Package Transaction"""

    COLOUR = blue

    def __init__(self, pkg: Pybuild, old: InstalledPybuild):
        super().__init__(pkg)
        self.old = old


class Update(Change):
    """Downgrade Package Transaction"""

    REPR = "U"


class Downgrade(Change):
    """Downgrade Package Transaction"""

    REPR = "D"


class Reinstall(Trans):
    """Reinstall Package Transaction"""

    REPR = "R"
    COLOUR = yellow


class Transactions:
    pkgs: List[Trans]
    config: Set[Any]
    new_selected: Set[Pybuild]

    def __init__(self):
        self.pkgs = []
        self.config = set()
        self.new_selected = set()

    def copy(self) -> "Transactions":
        new = Transactions()
        new.pkgs = self.pkgs.copy()
        new.config = self.config.copy()
        new.new_selected = self.new_selected.copy()
        return new

    def append(self, trans: Trans):
        self.pkgs.append(trans)

    def add_new_selected(self, pkg: Pybuild):
        self.new_selected.add(pkg)

    def extend(self, trans: "Transactions"):
        self.pkgs.extend(trans.pkgs)
        self.config |= trans.config
        self.new_selected |= trans.new_selected

    def find(self, pkg: Pybuild) -> Optional[Trans]:
        for trans in self.pkgs:
            if pkg == trans.pkg:
                return trans
        return None


class UseDep:
    def __init__(self, atom: FQAtom, flag: str, oldvalue: Optional[str]):
        self.atom = atom
        self.flag = flag
        self.oldvalue = oldvalue

    def __repr__(self):
        if self.oldvalue:
            return f"UseDep({self.atom}, {self.oldvalue} -> {self.flag})"
        else:
            return f"UseDep({self.atom}, {self.flag})"


def get_usestrings(
    mod: Pybuild,
    installed_use: Optional[Set[str]],
    verbose: bool,
    transactions: Optional[Transactions] = None,
) -> List[str]:
    enabled_use, disabled_use = get_use(mod)
    if transactions:
        for use in filter(lambda x: isinstance(x, UseDep), transactions.config):
            if atom_sat(mod.ATOM, use.atom):
                if use.flag.startswith("-"):
                    enabled_use.remove(use.flag.lstrip("-"))
                else:
                    enabled_use.add(use.flag)

    # Note: flags containing underscores are USE_EXPAND flags
    # and are displayed separately
    IUSE_STRIP = {flag.lstrip("+") for flag in mod.IUSE if "_" not in flag}

    texture_options = use_reduce(
        mod.TEXTURE_SIZES, enabled_use, disabled_use, flat=True, token_class=int
    )

    use_expand_strings = []
    for use in get_config().get("USE_EXPAND", []):
        if use in get_config().get("USE_EXPAND_HIDDEN", []):
            continue

        enabled_expand, disabled_expand = get_use_expand(mod, use)
        if enabled_expand or disabled_expand:
            installed_expand: Optional[Set[str]]
            if installed_use is not None:
                installed_expand = {
                    re.sub(f"^{use.lower()}_", "", flag)
                    for flag in installed_use
                    if flag.startswith(use.lower() + "_")
                }
            else:
                installed_expand = None
            string = get_flag_string(
                use, enabled_expand, disabled_expand, installed_expand, verbose=verbose
            )
            use_expand_strings.append(string)

    if mod.TEXTURE_SIZES is not None and len(texture_options) >= 2:
        texture_size = next(
            (
                use.lstrip("texture_size_")
                for use in enabled_use
                if use.startswith("texture_size")
            ),
            None,
        )
        if texture_size is not None:
            texture_string = get_flag_string(
                "TEXTURE_SIZE",
                [texture_size],
                map(str, sorted(set(texture_options) - {int(texture_size)})),
            )
        else:
            texture_string = ""
    else:
        texture_string = ""

    usestring = get_flag_string(
        "USE",
        enabled_use & IUSE_STRIP,
        IUSE_STRIP - enabled_use,
        installed_use,
        verbose=verbose,
    )

    return [usestring] + use_expand_strings + [texture_string]


def print_transactions(
    transactions: Transactions,
    verbose: bool = False,
    out=sys.stdout,
    summarize: bool = True,
):
    pkgs = transactions.pkgs
    download_size = get_download_size(
        [trans.pkg for trans in pkgs if not isinstance(trans, Delete)]
    )

    for trans in pkgs:
        pkg = trans.pkg
        installed_mod = load_installed_pkg(Atom(trans.pkg.CPN))
        if installed_mod is None:
            installed_use = None
        else:
            installed_use = installed_mod.INSTALLED_USE

        v = verbose or isinstance(trans, New)

        if isinstance(trans, Delete):
            usestring = ""
        else:
            usestrings = get_usestrings(pkg, installed_use, v, transactions)
            usestring = " ".join(list(filter(None, usestrings)))

        trans_colour = trans.__class__.COLOUR
        oldver = ""
        if isinstance(trans, Change):
            oldver = blue(" [" + trans.old.PVR + "]")

        modstring: str
        if verbose:
            modstring = pkg.ATOM
        else:
            modstring = pkg.ATOM.CPF

        if is_selected(pkg.ATOM) or pkg in transactions.new_selected:
            modstring = bright(green(modstring))
        else:
            modstring = green(modstring)

        print(
            "[{}] {}{}{}".format(
                bright(trans_colour(trans.REPR)), modstring, oldver, " " + usestring
            ),
            file=out,
        )

    if summarize:
        print(
            l10n(
                "transaction-summary",
                packages=len(pkgs),
                updates=len([trans for trans in pkgs if isinstance(trans, Change)]),
                new=len([trans for trans in pkgs if isinstance(trans, New)]),
                reinstalls=len(
                    [trans for trans in pkgs if isinstance(trans, Reinstall)]
                ),
                removals=len([trans for trans in pkgs if isinstance(trans, Delete)]),
                download=download_size,
            ),
            file=out,
        )


def get_all_deps(depstring: str) -> List[Atom]:
    dependencies = use_reduce(depstring, token_class=Atom, matchall=True, flat=True)

    # Note that any || operators will still be included. strip those out
    return list(
        [dep for dep in dependencies if dep != "||" and not dep.startswith("!")]
    )


def use_changed(installed: InstalledPybuild, flagupdates: Iterable[str] = []) -> bool:
    """
    Checks whether or not the use flag configuration for the given mod
    has changed since it was installed.
    """
    (enabled, _) = get_use(installed)
    enabled = set(filter(lambda x: x[0] != "-", collapse_flags(enabled, flagupdates)))
    return enabled != installed.INSTALLED_USE


def sort_transactions(transactions: Transactions):
    """
    Create graph and do a topological sort to ensure that mods are installed/removed
    in the correct order given their dependencies
    """

    def get_dep_graph(rdepend=True):
        graph: Dict[Atom, Set[Atom]] = {}
        priorities = {}

        for trans in transactions.pkgs:
            graph[trans.pkg.ATOM] = set()
            priorities[trans.pkg.ATOM] = trans.pkg.TIER

        def add_depends(mod, key: str, delete: bool):
            depends = {}
            depstring = getattr(mod, key)
            for dep in get_all_deps(depstring):
                for trans in transactions.pkgs:
                    if atom_sat(trans.pkg.ATOM, dep):
                        depends[trans.pkg.ATOM] = trans.pkg

            if delete:
                # When removing packages, remove them before their dependencies
                graph[mod.ATOM] |= set(depends.keys())
            else:
                # When adding or updating packages, packages, add or update their dependencies
                # before them
                for dep in depends:
                    graph[dep].add(mod.ATOM)
                    if key == "DEPEND":
                        # Also ensure runtime dependencies are available for build dependencies
                        # Whether or not we enforce runtime dependencies for all packages
                        add_depends(depends[dep], "RDEPEND", False)

        for trans in transactions.pkgs:
            add_depends(trans.pkg, "DEPEND", isinstance(trans, Delete))
            if rdepend:
                add_depends(trans.pkg, "RDEPEND", isinstance(trans, Delete))
        return graph, priorities

    # Attempt to sort using both runtime and build dependencies. If this fails,
    # fall back to just build dependencies
    graph, priorities = get_dep_graph()
    try:
        mergeorder = tsort(graph, priorities)
    except CycleException:
        try:
            graph, priorities = get_dep_graph(rdepend=False)
            mergeorder = tsort(graph, priorities)
        except CycleException as exception:
            raise CycleException(
                l10n("cycle-encountered-when-sorting-transactions"), exception.cycle
            )

    new_trans = transactions.copy()
    new_trans.pkgs = []
    for atom in mergeorder:
        for trans in transactions.pkgs:
            if trans.pkg.ATOM == atom:
                new_trans.pkgs.append(trans)
                break

    return new_trans


def generate_transactions(
    enabled: Iterable[FQAtom],
    disabled: Iterable[FQAtom],
    newselected: AbstractSet[QualifiedAtom],
    usedeps: Iterable[UseDep],
    *,
    noreplace: bool = False,
    emptytree: bool = False,
    update: bool = False,
) -> Transactions:
    """
    Generates a list of transactions to update the system such that
    all packages in enabled are installed and all packages in disabled are not

    Packages will not be rebuilt unless a change has occurred, or they are included
    in the new_selected parameter set and noreplace is not specified.

    args:
        enabled: Packages that should be enabled, if not already
        disabled: Packages that should be disabled, if not already
        new_selected: Packages that were selected by the user for this operation
                      These should be re-installed, even if no change has been
                      made, unless noreplace is also passed
        usedeps: Use changes that should accompany the transactions
        noreplace: If true, don't re-install selected packages that haven't changed
        update: If true, will update live packages

    returns:
        Onject representing the transactions
    """
    transactions = Transactions()
    flagupdates: Dict[str, List[str]] = {}
    for dep in usedeps:
        if dep.atom in flagupdates:
            flagupdates[dep.atom].append(dep.flag)
        else:
            flagupdates[dep.atom] = [dep.flag]

    for atom in enabled:
        pkg = load_pkg_fq(atom)

        if "local" in pkg.PROPERTIES:
            continue

        (to_install, dep) = select_package([pkg])

        if dep is not None:
            transactions.config.add(dep)

        installed = load_installed_pkg(Atom(atom.CPN))

        if not (to_install or installed):
            raise PackageDoesNotExist(atom)

        if (
            to_install is not None
            and to_install.ATOM.CPN in newselected
            or (installed and installed.ATOM.CPN in newselected)
        ):
            transactions.add_new_selected(cast(Pybuild, to_install or installed))

        if emptytree:
            transactions.append(Reinstall(cast(Pybuild, to_install or installed)))
            continue

        # TODO: There might be advantages to preferring installed over to_install
        # such as avoiding re-downloading files just because the sources changed in a trivial
        # manner

        def can_update_live(pkg: InstalledPybuild):
            try:
                return _sandbox_execute_pybuild(
                    pkg.FILE,
                    "can-update-live",
                    Permissions(network=True),
                    installed=True,
                )
            except SandboxedError:
                return False

        if installed is not None:
            if version_gt((to_install or installed).ATOM.PVR, installed.ATOM.PVR) or (
                update
                and "live"
                in use_reduce(installed.PROPERTIES, installed.INSTALLED_USE, flat=True)
                and can_update_live(installed)
            ):
                transactions.append(Update(to_install or installed, installed))
            elif version_gt(installed.ATOM.PVR, (to_install or installed).ATOM.PVR):
                # to_install cannot be None if it has a smaller version
                transactions.append(Downgrade(to_install, installed))
            elif use_changed(
                installed, flagupdates.get((to_install or installed).ATOM, [])
            ):
                transactions.append(Reinstall(to_install or installed))
            elif not noreplace and installed.ATOM.CPN in newselected:
                transactions.append(Reinstall(to_install or installed))
            elif to_install and not atom.R.endswith("::installed"):
                # If the repo's version is enabled, this means the dep generator
                # wants the package re-installed using the repo's version for some reason
                transactions.append(Reinstall(to_install))
        elif to_install is not None:
            new_mod = to_install
            transactions.append(New(new_mod))

    for atom in disabled:
        to_remove = load_installed_pkg(Atom(atom))
        if to_remove is not None:
            transactions.append(Delete(to_remove))

    # Only add usedeps that differ from their current setting
    # for the mod to be installed
    for dep in usedeps:
        for trans in transactions.pkgs:
            if atom_sat(trans.pkg.ATOM, dep.atom):
                enabled_use, _ = get_use(trans.pkg)
                if (
                    dep.flag[0] == "-"
                    and dep.flag.lstrip("-") in enabled_use
                    or dep.flag[0] != "-"
                    and dep.flag not in enabled_use
                ):
                    transactions.config.add(dep)

    return transactions

## Help Message Strings
description = CLI Package manager designed for packaging game mods

merge-help = Install or remove packages

sync-help = Fetch and update remote package repositories

# Placeholder shown in parameter lists
atom-placeholder = ATOM
# Placeholder shown in parameter lists
archive-placeholder = ARCHIVE
# Placeholder shown in parameter lists
set-placeholder = SET
# Placeholder shown in parameter lists
directory-placeholder = DIRECTORY
# Placeholder shown in parameter lists
query-placeholder = QUERY
# Placeholder shown in parameter lists
number-placeholder = NUMBER

package-help = Packages to install. Can be either a package atom ("category/name") set
    ("@set_name") or source archive path ("path/to/archive.ext")

depclean-help = Removes packages and their dependencies. Packages dependent
    on the given packages will also be removed. If no arguments are given, this will
    remove packages that aren't needed by other packages and aren't in the world file
    or system set.

auto-depclean-help = Automatically remove unneeded dependencies before finishing.
    Equivalent to running `portmod <prefix> merge --depclean` after other operations.

unmerge-help = Removes the given packages without checking dependencies.

no-confirm-help = Don't prompt for confirmation and always select the default option instead.

oneshot-help = Do not make any changes to the world set when installing or removing packages

nodeps-help = Ignore dependencies when installing specified packages. Note: This may
    cause packages to fail to install if their build dependencies aren't satisfied,
    and fail to work if their runtime dependencies aren't satisfied.

noreplace-help = Skips packages specified on the command line that have already been
    installed. Implicitly enabled by the newuse and update options.

update-help = Updates packages to the best version available and excludes packages
    if they are already up to date.

newuse-help = Includes packages whose use flags have changed since they were last
    installed.

emptytree-help = Reinstalls target packages and their entire deep dependency tree, as
    if no packages are currently installed.

deep-help = Consider the entire dependency tree when doing updates
    instead of just the packages specified on the command line.

search-help = Searches the repository for packages with a name or atom matching the given search terms

search-query-help = Search query phrases to match against

searchdesc-help = Also consider descriptions when searching

merge-select-help = Adds specified packages to the world set (unused. This is the default
    if deselect is not provided).

merge-deselect-help = Removes specified packages from the world set. This is implied by
    uninstall actions such as --depclean and --unmerge. Use --deselect=n to prevent
    uninstalls from removing packages from the world set.

validate-help = Check if the packages in the package directory are installed, and that the
    directories in the config all exist.

sort-vfs-help = Sorts the vfs list. This is for debugging purposes, as the vfs is
    normally sorted as necessary.

merge-debug-help = Enables exception traces for debugging and skips the cleanup stage so that
    the contents of temporary directories can be inspected. Note that you will need to
    clean up leftover files manually.

ignore-default-opts-help = Causes the OMWMERGE_DEFAULT_OPTS environment variable to be ignored

version-help = Displays the version number of Portmod.

info-help = Displays the values of several global variables for debugging purposes.
# $commit (String) - the hash for the head commit of the repository
info-repository-commit = Head commit: { $commit }
info-repository-date= Timestamp: { $date }
info-repositories = Repositories:

############## Misc ##################
# $atom (String) - The atom passed on the command line
not-installed = No package matching { $atom } is installed!
not-found = No package matching { $atom } could be found!
skipping-system-package = Skipping removal of system package { $atom }
fetch-instructions = Fetch instructions for { $atom }:
add-to-world = Adding { $atom } to world favourites file
remove-from-world = Removing { $atom } from world favourites file
no-matching-world-atom = No matching atoms found in world favourites file...
pkg-messages = Messages for package { $atom }:
ambiguous-atom = Atom { $atom } is ambiguous and could refer to any of the following:
ambiguous-atom-fq = Fully Qualified Atom { $atom } is ambiguous and could refer to any of the following:
in-database-not-installed = Package { $atom } is in the database but is not installed!
installed-not-in-database = Package { $atom } is installed but is not in the database!
in-database-could-not-load = Installed package { $atom } could not be loaded
package-does-not-exist = Cannot find package to satisfy atom { $atom }.
package-does-not-exist-in-world = Cannot find package to satisfy the world file atom { $atom }.
created-manifest = Created manifest for { $atom }

# $num (Integer) number of packages which were merged
merge-success = Successfully merged { $num ->
       [1]  1 package
       *[other] { $num } packages
    }.
merge-success-and-error = Successfully merged { $num ->
       [1]  1 package
       *[other] { $num } packages
    }.
    Error occurred when attempting to merge { $atom }
rebuild-message = The following packages need to be rebuilt:
rebuild-prompt = You can use { $command } to rebuild these packages.
checking-rebuild = Checking for packages which need to be rebuilt...

initial-commit = Initial Commit
initialized-repository = Initialized Repository { $repo }
# $repo (String) - The repository name
syncing-repo = Syncing repo { $repo }...
done-syncing-repo = Done syncing repo { $repo }.
update-message = A new version of Portmod is available. It is highly
    recommended that you update as soon as possible, as we do not provide support
    for outdated versions and new packages in the tree may not work as expected.
# $version (String) - A version string
# Note: these two should be formatted such that the versions line up in the same column
current-version = Current Version:  { $version }
new-version =     New Version:      { $version }

# $type (String) the invalid sync type
# $repo (String) the repo name for which the error was encountered
# $supported (String) - a comma separated list of sync types
invalid-sync-type = Sync type "{ $type }" for repo "{ $repo }" is not supported.
    Supported types are: { $supported }.

cache-cleanup = Cleaning up cache for repository "{ $repo }" which no longer exists

nothing-to-do = Nothing to do.
nothing-else-to-do = Nothing else to do.
to-install = These are the packages to be installed, in order:
to-remove = These are the packages to be removed, in order:
necessary-keyword-changes = The following keyword changes are necessary to proceed.

    This will enable the installation of a package that is unstable
    (if the keyword is prefixed by a "~"), or untested (if the keyword is "**")

necessary-license-changes = The following license changes are necessary to proceed.
    Please review these licenses and make the changes manually.
necessary-flag-changes = The following use flag changes are necessary to proceed.
enabled-comment = Note: currently enabled
disabled-comment = Note: currently disabled

nodeps-and-depclean = --nodeps and --depclean cannot be used together.
    If you want to remove mods without checking dependencies, please use
    --unmerge

file-does-not-exist = File { $file } does not exist!
repository-does-not-exist = Cannot find repository for the given file.

# $packages (Integer) Numer of packages in transaction list
# $updates (Integer) Numer of packages in transaction list which are updates
# $new (Integer) Numer of packages in transaction list which are new installs
# $reinstalls (Integer) Numer of packages in transaction list which are reinstalls
# $removals (Integer) Numer of packages in transaction list which are removals
# $download (Float) download size in MiB
transaction-summary = Total: { $packages ->
        [1] 1 package
        *[other] { $packages } packages
    } ({ $updates ->
        [1] 1 update
        *[other] { $updates } updates
    }, { $new ->
        [1] 1 new
        *[other] { $new } new
    }, { $reinstalls ->
        [1] 1 reinstall
        *[other] { $reinstalls } reinstalls
    }, { $removals ->
        [1] 1 removal
        *[other] { $removals} removals
    }),
    Size of downloads: { $download } MiB

cycle-encountered-when-sorting-transactions = Could not sort transactions! There is a
    cycle in the dependency graph!


tmp-space-too-small = The temporary directory { $dir } only has { $free } MiB of free space, but as much as { $size } MiB may be needed!

pkg-pretend = Executing pkg_pretend for package { $atom }

## Query messages
use-expand = (use_expand)
flag-desc-not-found = Missing description for flag { $flag }
omit-already-displayed-tree = (omitting tree which has already been displayed...)
package-name = Name:
package-available-versions = Available Versions:
package-installed-version = Installed Version:
package-size-of-files = Size of files:
package-homepage = Homepage:
package-description = Description:
package-license = License:
package-upstream-author = Upstream Author/Maintainer:
packages-found = Packages found: { $num }

query-help = Query information about packages
query-subcommands-title = subcommands
query-all-help = Also query packages which are not installed
query-depends-help = List all packages directly depending on ATOM
query-depends-atom-help = Package atom to query
query-has-help = List all packages matching variable.

    This can only be used to scan variables in the base Pybuild spec, not custom
    fields declared by specific Pybuilds or their superclasses.
query-has-var-help = Pybuild field to search
# Placeholder for a pybuild field. Used in the `query has` command
field-placeholder = FIELD
# Placeholder for matching against the value of a pybuild field. Used in the `query has` command
value-placeholder = VALUE
query-has-expr-help = Value to match in field
query-has-searching-msg = Searching for { $var }
# Placeholder for commands taking a use flag as an argument
flag-placeholder = FLAG
query-hasuse-help = List all packages that declare the given use flag.

        Note that this only includes those with the flag in their IUSE
        field and inherited flags through IUSE_EFFECTIVE will not be counted
query-hasuse-use-help = Use flag to match against
query-hasuse-searching-msg = Searching for use flag { $use }
query-uses-help = Display use flags and their descriptions
query-uses-atom-help = Atom specifying the package whose flags are to be displayed
query-uses-found = Found these use flags for { $atom }
# Should be just one line
query-uses-final = final flag setting for installation
# Should be just one line
query-uses-installed = package is installed with flag
query-uses-legend = Legend
query-list-atom-help = Atoms specifying the packages to list
query-list-tree-help = If specified, also list packages in the remote repositories
query-list-help = List all packages matching ATOM.

    By default only lists installed packages.

    Produces output in the form of:

    {"["}IR{"]"} category/package-version


    The Presence of the I flag indicates that the package is installed
    The Presence of the R flag indicates that the package is available in a repository

query-local-flags = Local USE flags:
query-global-flags = Global USE flags:
# $type (String) - The use expand category
query-use-expand-flags = USE_EXPAND flags ({ $type }):

texture-size-desc = Enables textures of size { $size }
package-maintainer = Maintainer:
package-location = Location:
package-keywords = Keywords:
package-upstream = Upstream:

query-meta-help = Display metadata for a package
query-meta-atom-help = Atom specifying the package whose metadata is to be displayed

query-depgraph-help = Display dependency graph for package
query-depgraph-atom-help = Atom specifying package whose dependency graph is to be displayed
query-depgraph-depth-help = Maximum depth of the tree to be displayed. Default is 10
query-depgraph-depgraph = dependency graph for { $atom }
query-depgraph-max-depth = max depth

## Package phase messages
pkg-removing = Removing { $atom }
pkg-finished-removing = Finished removing { $atom }
pkg-installing = Starting installation of { $atom }
pkg-unable-to-download = Unable to download { $atom }. Aborting.
pkg-unpacking = Unpacking package...
pkg-unpacking-source = Unpacking { $archive }...
pkg-preparing = Preparing source in { $dir } ...
pkg-prepared = Source Prepared
pkg-installing-into = Installing { $atom } into { $dir }
pkg-existing-install-dir = Installed directory already existed. Overwriting.
pkg-installed = Installed { $atom }
pkg-installed-into = Installed { $atom } into { $dir }
cleaned-up = Cleaned up { $dir }

# size: Size of directory in MiB
pkg-final-size-build = Final size of build directory: { $size } MiB
# size: Size of directory in MiB
pkg-final-size-installed = Final size of installed tree: { $size } MiB

## Module messages
symlink-to = symlink to { $path }
binary-data = Binary Data
skipped-blacklisted-file = Skipped change to blacklisted file "{ $file }"
skipped-update-noninteractive = Skipped update to file { $file } as mode is not interactive
apply-change = Apply Change
module-do-not-apply-change = Do not apply the change to this file
module-apply-always = Apply change now, and whitelist this file so that you
    aren't prompted again in future. Note that you will be
    informed of changes to the file.
module-apply-never = Never apply changes to this file. Note that you will
    be informed when changes are attempted.

## Dependency messages
calculating-dependencies = Calculating Dependencies...
done = Done!
unable-to-satisfy-dependencies = Unable to satisfy dependencies:
contradicts = Contradicts:
# TODO: There are a number of context strings that may eventually be passed to DepError
# which should be internationalized

## Download messages
fetching = Fetching { $url }
file-moving = Moving "{ $src }" -> "{ $dest }"
remote-hash-mismatch = Local hash is { $hash1 }, but remote hash is { $hash2 }!"
local-hash-mismatch = { $filename } should have { $hash } of "{ $hash1 }",
    but instead it is "{ $hash2 }"
possible-local-hash-mismatch = Filename "{ $filename }" matches source name "{ $name }"
    but the hash doesn't match
retrying-download = Retrying Download of { $url }...
source-unfetchable = Source { $source } could not be found in the cache and cannot be fetched
fetch-abort = Unable to fetch package archives. Aborting.

## Config messages

exec-error = { $error } in { $file }
reserved-variable = Variable { $key } is reserved for use in profiles
    and cannot be overridden or modified

config-placeholder-header = This is a placeholder config file for Portmod { $version }
    This file is created if no config file is found, and not updated when Portmod updates.
    To regenerate this config file for the latest version of Portmod, delete it and run
    { $info_command }.

    This file contains optional config values that override those set by your profile.
    See { $wiki_page } for a full description of the options used by Portmod itself.
    Note that some variables may be used for specific packages and may not be listed
    on the wiki

config-placeholder-global-use = Valid global use flags can be found in the profiles/use.yaml
    file of the repository Default USE flag configurations vary with the profile

config-placeholder-texture-size = Valid TEXTURE_SIZE options are

    max

    min

    max <= SIZE (e.g. 2048)

    min >= SIZE

    The default is "min"

config-placeholder-accept-keywords = Keywords to accept. Valid choices at the global level are
    arch (stable packages only) and ~arch (stable and testing packages). Defaults to arch

config-placeholder-accept-license = Licenses to accept. Packages with licenses not accepted here
    will not be able to be installed unless overridden by a package-specific rule in
    package.accept_license

    Defaults to "* -EULA"

config-placeholder-openmw-config = Auto-detected by default, however if it fails to detect the
    location, specify it here

    OPENMW_CONFIG_DIR="/path/to/config"

config-placeholder-morrowind-path = Auto-detected by default, however if it fails to detect the
    location, specify it here Note that this should be the root where the executable is found,
    not the data files directory Note that this only applies to the `base/morrowind` package
    in the `openmw` repo.

    MORROWIND_PATH="/path/to/Morrowind"


## News messages
important = IMPORTANT:
news-unread = { $unread ->
        [1] 1 news item needs
        *[other] { $unread } news items need
    } reading for repository '{ $repo }'
news-read = Use { $command } to view news items.

title = Title:
posted = Posted:
author = Author:
translator = Translator:
revision = Revision:

news-help = Manage news
news-list-help = List all news articles
news-read-help = Displays news article and marks as read
news-read-target-help = new (default) all or item number
news-read-target-new = new
news-read-target-all = all
news-target-placeholder = item
news-unread-help = Marks news article as unread
news-unread-target-help = all or item number
news-items = News Items:

## Flags messages

flag-add = Adding flag { $flag } to { $atom } in { $file }
flag-remove = Removing flag { $flag } from { $atom } in { $file }

## Use flag messages

multiple-texture-flags = Invalid use configuration.
    Multiple texture size options { $flag1 } and { $flag2 } enabled for package { $atom }"

invalid-flag-atom = { $flag } is not a valid use flag for package { $atom }
invalid-flag = { $flag } is not a valid global use flag
use-flag-desc = { $flag }: { $desc }
adding-use-flag = Adding flag { $flag } to USE in portmod.conf
removing-use-flag = Removing flag { $flag } from USE in portmod.conf
flag-not-set-globally = Use flag "{ $flag }" is not set globally
global-use-flag-already-enabled = Use flag "{ $flag }" is already enabled globally
global-use-flag-already-disabled = Use flag "{ $flag }" is already disabled globally
invalid-use-flag-warning = { $flag } is not a valid use flag for package { $atom1 }, the default selected version of package { $atom2 }

## Conflicts UI Messages

conflicts-ui-help = Display conflicts between files in the VFS

## Select messages

select-help = Select between configuration options

## Profile messages
profile-help = Manage the profile symlink
profile-list-help = List available profiles
profile-set-help = Set a new profile symlink target
profile-number-help = Profile number
profile-show-help = Show the current profile symlink target
profile-available = Available profile symlink targets:
profile-current-symlink = Current { $path } symlink:

## Use flag configuration messages
use-help = Enable and disable use flags
use-enable = Enable use flag
use-disable = Explicitly disable use flag
use-remove = Remove references to the given use flag (enabled or disabled)
use-package = Package atom for setting local use flag. If not set, enables/disables global use flags.

## VFS messages
user-config-not-installed = Package { $entry } in { $path } is not installed!
user-config-ambiguous = Package { $entry } in { $path } is ambiguous! It could refer to any of { $packages }
archive-extraction-failed = Attempted to extract file "{ $file }" but destination file "{ $dest }" does not exist!
vfs-cycle-error = Encountered cycle when sorting vfs!
sorting-vfs = Sorting VFS order...

user-config-warning = Line "{ $line }" in user config "{ $path }" contains just one entry and will not do anything.

## Loader messages

repo-does-not-exist-warning = Repository { $name } does not exist at configured location { $path }
    You might need to run { $command } if this is a remote repository
multiple-versions-installed = Multiple versions of package "{ $atom }" installed!
# Used to indicate that a wrapper command failed. Not usually displayed to the user
command-failed = { $path } { $command } failed!
could-not-load-pybuild = Could not load pybuild "{ $file }"

## Use string messages

# Note: Should be a single hyphenated word, if possible
exactly-one-of = exactly-one-of
# Note: Should be a single hyphenated word, if possible
any-of = any-of
# Note: Should be a single hyphenated word, if possible
at-most-one-of = at-most-one-of

## Questions
apply-changes-qn = Would you like to automatically apply these changes?
continue-qn = Would you like to continue?
remove-from-world-qn = Would you like to remove these packages from your world favourites?
apply-above-change-qn = Would you like to apply the above change?

# Prompt options
yes = Yes
no = No
yes-short = y
no-short = n
always-short = a
never-short = N
true-short = t
true = True
false-short = f
false = False
yes-or-no = { yes }/{ no }

# $yes (String) - The localization of yes, including any colourization
# $no (String) - The localization of no, including any colourization
prompt-invalid-response = Please respond with '{ $yes }' or '{ $no }':
prompt-invalid-response-multiple = Please respond with one of [{ $options }]:
prompt-invalid-range-multi = Please enter numbers between 0 and { $max } using a-b to indicate a range and a,b to indicate individual numbers:
prompt-invalid-range = Please enter a number between 0 and { $max }
prompt-range-too-large = Please ensure that the numbers are between 0 and { $max }

## Argparse generic
debug-help = Enables exception traces for debugging
quiet-help = Don't display anything but the most important information.
verbose-help = Increase verbosity of output.

## Pybuild Messages
applying-patch = Applying { $patch }...
installing-directory-into = Installing directory "{ $dir }" into "{ $dest }"
skipping-directory = Skipping directory "{ $dir }" due to unsatisfied use requirements { $req }

## Mirror Messages

copying-file = Copying { $src } -> { $dest }
mirror-help = Update a local mirror
mirror-dir-help = Directory to mirror into

## Repo Messages

repo-missing-location = Repo "{ $name }" is missing a location. Skipping...

repo-help = Configure the repositories associated with this prefix
repo-list-help = List available package repositories
repo-add-help = Add a package repository to this prefix
repo-remove-help = Remove a package repository from this prefix
repo-does-not-exist = Repository { $name } does not exist
repo-adding = Adding repository { $name } to { $conf }
repo-removing = Removing repository { $name } from { $conf }
repos-available = Available Repositories
repo-placeholder = REPO
repo-identifier-help = Identifier for the repository. Either the repository name, or its index in the list.

## Init Messages

init-help = Create a new prefix
# Placeholder for use in commands that accept a prefix name as an argument
prefix-placeholder = PREFIX
init-prefix-help = Prefix name which will be used in commands that interact with the prefix
init-arch-help = Game engine Architecture of the prefix
unknown-arch = Architecture { $arch } could not be found. It may not be a supported Architecture.

## Prefix messages
# $prefix (String) - The prefix name
initialized-prefix = Initialized prefix { $prefix }
# $prefix (String) - The prefix name
prefix-help = Interact with the { $prefix } prefix
# $prefix (String) - The prefix name
prefix-exists = The prefix { $prefix } already exists
# $prefix (String) - The prefix name
invalid-prefix = The prefix { $prefix } does not exist

## Locking Messages

acquiring-write-vdb = Waiting for write access to the package database
acquiring-read-vdb = Waiting for read access to the package database
acquiring-exclusive = Waiting for exclusive access to the portmod system

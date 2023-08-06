from collections import Counter
from dataclasses import dataclass
from distutils.version import LooseVersion
import logging
from pathlib import Path
import sys
import tempfile
from typing import Tuple, Optional, Iterable, Set

import click

from .local import (
    LocalPackageDatabase,
)
from .remote import (
    ContentDB,
    RemotePackageSpec,
    RemotePackage,
    PackageType,
)


@dataclass
class MinetestUserData:
    userpath: Path


class ApplicationError(click.ClickException):
    def show(self, file=None):
        logging.error(self.message)


def validate_packages(packages: Iterable[str]) -> Set[RemotePackageSpec]:
    invalid_packages = []
    valid_packages = []
    for package in packages:
        package_split = package.split("/")
        if len(package_split) == 2:
            valid_packages.append(
                RemotePackageSpec(author=package_split[0], name=package_split[1])
            )
        else:
            invalid_packages.append(package)
    if invalid_packages:
        raise ApplicationError(
            f"Invalid package specifications: {', '.join(invalid_packages)}"
        )

    return set(valid_packages)


def enforce_version(mtver: Optional[str]) -> None:
    if mtver is not None and (LooseVersion(mtver) < LooseVersion("5.0")):
        raise ApplicationError("mtpkg only supports Minetest version 5+")


def append_req_file(
    requirements_path: Optional[Path], packages: Tuple[str, ...]
) -> Tuple[str, ...]:
    if requirements_path is not None:
        with open(requirements_path) as requirements_file:
            addl_packages = tuple((line.rstrip() for line in requirements_file))
        return packages + addl_packages
    return packages


def dedup_packages(package_strs: Tuple[str, ...]) -> Set[str]:
    """ Check for duplicate package specs """
    package_str_set = set(package_strs)
    if len(package_strs) != len(package_str_set):
        logging.warning("Duplicate packages specified for installation, ignoring")
    return package_str_set


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    count=True,
    help="Display debugging messages.",
)
@click.option("-q", "--quiet", is_flag=True, help="Suppress infomational messages.")
@click.option(
    "-u",
    "--userpath",
    type=Path,
    default=Path.cwd(),
    help="Path to the Minetest user data directory, usually named '.minetest'. Defaults to the current directory.",
)
@click.pass_context
def main(ctx: click.Context, verbosity: int, quiet: bool, userpath: Optional[Path]):
    """A command-line package manager for Minetest."""
    logging.basicConfig(
        format="[{levelname}] {message}",
        style="{",
        level=max(logging.DEBUG, logging.INFO - (verbosity * 10) + (int(quiet) * 10)),
        stream=sys.stdout,
    )

    userpath = userpath if userpath is not None else Path.cwd()
    if not userpath.exists():
        raise ApplicationError(f"Provided user path '{userpath}' doesn't exist")

    ctx.obj = MinetestUserData(userpath=userpath)


@main.command()
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite any package conflicts with package from ContentDB.",
)
@click.option(
    "-f",
    "--file",
    "requirements_path",
    type=Path,
    help="Path to a package requirements file, which has a single 'author/name' package per line.",
)
@click.option(
    "--mtver",
    help="The version of Minetest installed. Queries the ContentDB for the latest non-dev version if not specified.",
    metavar="X[.Y[.Z]]",
)
@click.option(
    "--game",
    help="Enable recursive dependency resolution using a ContentDB 'author/name' identifier as the base game.",
    metavar="author/name",
)
@click.option(
    "--enable",
    help="Enable mods for the given world ID after installation.",
    metavar="world_id",
)
@click.option(
    "--install-optional",
    is_flag=True,
    help="Also install optional dependencies during recursive dependency resolution.",
)
@click.option(
    "-y",
    "--assume-yes",
    is_flag=True,
    help="Assume yes to any user prompts and accept package suggestions with highest score.",
)
@click.argument("packages", nargs=-1)
@click.pass_obj
def install(
    mtuserdata: MinetestUserData,
    packages: Tuple[str, ...],
    force: bool,
    requirements_path: Optional[Path],
    mtver: Optional[str],
    game: Optional[str],
    enable: Optional[str],
    install_optional: bool,
    assume_yes: bool,
):
    """Install packages from the ContentDB.

    PACKAGES is a list of space-separated 'author/name' package identifiers to be installed from the ContentDB.
    """

    enforce_version(mtver)

    packages = append_req_file(requirements_path, packages)

    if game is not None:
        packages += tuple([game])

    if not packages:
        raise click.UsageError("No packages specified to install")

    package_str_set = dedup_packages(packages)

    local_db = LocalPackageDatabase(mtuserdata.userpath)
    if (enable is not None) and (not local_db.world_exists(enable)):
        raise ApplicationError(f"Can't find world with id '{enable}'")

    # Validate package names
    valid_package_specs = validate_packages(package_str_set)

    remote_db = ContentDB()
    # Fetch latest minetest version if not provided
    if not mtver:
        mtver = remote_db.get_latest_minetest_version()
    logging.info(f"Using Minetest version: '{mtver}'")

    # Fetch packages from ContentDB
    remote_packages = remote_db.get_packages(valid_package_specs)

    if game is not None:
        remote_packages |= remote_db.get_recursive_dependencies(
            remote_packages, optional=install_optional, assume_yes=assume_yes
        )

    # Check for already-installed packages, remove those from remote_packages with a logging.info
    installable_packages = set()
    for package in remote_packages:
        if local_db.is_installed(package):
            logging.info(f"Package '{package.author}/{package.name}' already installed")
        else:
            installable_packages.add(package)

    # Check for package conflicts
    ## check between requested and installed packages
    local_db.check_conflicts(installable_packages, force)

    ## check within requested packages
    pkg_typename_cnt = Counter(
        ((package.type, package.name) for package in installable_packages)
    )
    conflicting_typenames = {
        key for key, value in pkg_typename_cnt.items() if value > 1
    }
    if conflicting_typenames:
        for package in installable_packages:
            if (package.type, package.name) in conflicting_typenames:
                logging.error(
                    f"Conflict found for package '{package.author}/{package.name}'"
                )
        raise ApplicationError("There were conflicts between requested packages")

    # Get latest compatible release id for all requested packages
    latest_compat_release_ids = remote_db.get_latest_compatible_release_ids(
        installable_packages, mtver, game is not None
    )

    # Download the chosen release ID
    for package in installable_packages:
        latest_release_id = latest_compat_release_ids[package]
        with tempfile.TemporaryFile() as tmp:
            remote_db.download_release(package, latest_release_id, tmp)
            local_db.install_release(package, latest_release_id, tmp)

    if enable is not None:
        # enable all mods installed
        local_db.enable_mods(
            enable,
            {
                mod
                for package in remote_packages
                if package.type != PackageType.GAME
                for mod in package.provides
            },
        )
        if (game is not None) and (
            not local_db.is_world_game(enable, game.split("/")[1])
        ):
            # log warning if game id set in world isn't equal to given base game
            logging.warning(
                f"'{game}' is not the game specified for world '{enable}' but it was defined as the base game for dependency resolution and mods were enabled for the world"
            )


@main.command()
@click.option(
    "-f",
    "--file",
    "requirements_path",
    type=Path,
    help="Path to a package requirements file, which has a single 'author/name' package per line.",
)
@click.option(
    "--mtver",
    help="The version of Minetest installed. Queries the ContentDB for the latest non-dev version if not specified.",
    metavar="X[.Y[.Z]]",
)
@click.argument("packages", nargs=-1)
@click.pass_obj
def update(
    mtuserdata: MinetestUserData,
    packages: Tuple[str, ...],
    requirements_path: Optional[Path],
    mtver: Optional[str],
):
    """Update packages using the ContentDB.

    PACKAGES is a list of space-separated 'author/name' package identifiers to be updated from the ContentDB.

    If no packages are provided, all packages previously downloaded from the ContentDB will be updated.
    """

    enforce_version(mtver)

    packages = append_req_file(requirements_path, packages)

    package_str_set = dedup_packages(packages)

    local_db = LocalPackageDatabase(mtuserdata.userpath)
    if not package_str_set:
        valid_package_specs = local_db.get_installed_ContentDB_packages()
    else:
        valid_package_specs = validate_packages(package_str_set)

    remote_db = ContentDB()
    # Fetch latest minetest version if not provided
    if not mtver:
        mtver = remote_db.get_latest_minetest_version()
    logging.info(f"Using Minetest version: '{mtver}'")

    # Fetch packages from ContentDB
    remote_packages = remote_db.get_packages(valid_package_specs)

    # Check for installed packages, remove not installed ones from remote_packages with a logging.info
    installed_packages = set()
    for package in remote_packages:
        if not local_db.is_installed(package):
            logging.warning(
                f"Package '{package.author}/{package.name}' not installed, ignoring"
            )
        else:
            installed_packages.add(package)

    # Get latest compatible release id for all requested packages
    latest_compat_release_ids = remote_db.get_latest_compatible_release_ids(
        installed_packages, mtver
    )

    # Mark which packages are not at the latest compatible release so they can be updated
    updatable_packages = []
    errors = []
    for package in installed_packages:
        installed_release = local_db.get_installed_release(package)
        if installed_release is None:
            logging.warning(
                f"Couldn't get the installed release for {package.author}/{package.name}, this shouldn't have happened"
            )
            continue
        latest_compat_release = latest_compat_release_ids[package]
        if installed_release == latest_compat_release:
            logging.info(
                f"{package.author}/{package.name} is already at the latest release"
            )
        elif installed_release < latest_compat_release:
            updatable_packages.append(package)
            logging.info(
                f"{package.author}/{package.name} will be upgraded from release {installed_release} to {latest_compat_release}"
            )
        elif installed_release > latest_compat_release:
            errors.append(
                ApplicationError(
                    f"{package.author}/{package.name} has a newer release ({installed_release}) installed than the latest compatible one (latest_compat_release)"
                )
            )
    if errors:
        for error in errors:
            error.show()
        raise ApplicationError(
            "There were problems checking if the installed packages were at the latest version"
        )

    # Download the chosen release ID
    for package in updatable_packages:
        latest_release_id = latest_compat_release_ids[package]
        with tempfile.TemporaryFile() as tmp:
            remote_db.download_release(package, latest_release_id, tmp)
            local_db.install_release(package, latest_release_id, tmp)

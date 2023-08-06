"""
local.py

Module related to operations on packages installed to the Minetest user path
"""


from dataclasses import dataclass
import logging
from pathlib import Path
import shutil
import tempfile
from typing import Optional, Tuple, Dict, Set, IO
import zipfile

import click

from .remote import PackageType, RemotePackage, RemotePackageSpec


class LocalError(click.ClickException):
    def show(self, file=None):
        logging.error(self.message)


def pkgtype_to_dirname(pkgtype: PackageType) -> str:
    if pkgtype == PackageType.MOD:
        return "mods"
    if pkgtype == PackageType.GAME:
        return "games"
    if pkgtype == PackageType.TEXTURE_PACK:
        return "textures"
    raise ValueError("Unknown package type '{}'".format(pkgtype))


@dataclass(frozen=True)
class LocalPackage:
    name: str
    type: PackageType
    path: Path
    author: Optional[str] = None
    release: Optional[int] = None


class LocalPackageDatabase:

    _pkgs: Dict[Tuple[PackageType, str], LocalPackage]
    _mod2pack: Dict[str, LocalPackage]

    def __init__(self, userpath: Path):
        self.userpath = userpath
        self._pkgs = {}
        self._mod2pack = {}

        mods_path = userpath / "mods"
        if not mods_path.exists():
            raise LocalError(f"Could not find a mods directory in '{userpath}'")

        # search mods
        for mods_child in mods_path.iterdir():
            if mods_child.is_dir():
                # check if modpack
                if (mods_child / "modpack.conf").exists():
                    pkg_conf = parse_conf_file(mods_child / "modpack.conf")
                    local_pkg = LocalPackage(
                        name=pkg_conf.get("name", mods_child.name),
                        type=PackageType.MOD,
                        path=mods_child,
                        author=pkg_conf.get("author", None),
                        release=int(pkg_conf["release"])
                        if "release" in pkg_conf
                        else None,
                    )
                    if (mods_child / "mod.conf").exists():
                        raise LocalError(
                            f"'{mods_child}' has both a modpack.conf and a mod.conf"
                        )
                    # recursively add mods to mod2pack
                    for submod in filter(lambda p: p.is_dir(), mods_child.iterdir()):
                        if (submod / "mod.conf").exists():
                            submod_conf = parse_conf_file(submod / "mod.conf")
                            submod_name = submod_conf.get("name", submod.name)
                        else:
                            submod_name = submod.name
                        if submod_name in self._mod2pack:
                            raise LocalError(
                                f"Modpacks '{local_pkg.name}' and '{self._mod2pack[submod_name].name}' provide the same mod: '{submod_name}'"
                            )
                        self._mod2pack[submod_name] = local_pkg
                elif (mods_child / "mod.conf").exists():
                    pkg_conf = parse_conf_file(mods_child / "mod.conf")
                    local_pkg = LocalPackage(
                        name=pkg_conf.get("name", mods_child.name),
                        type=PackageType.MOD,
                        path=mods_child,
                        author=pkg_conf.get("author", None),
                        release=int(pkg_conf["release"])
                        if "release" in pkg_conf
                        else None,
                    )
                else:
                    logging.warning(
                        f"Found folder in mod directory without a proper configuration file at '{mods_child}'"
                    )
                    continue
                key = (PackageType.MOD, local_pkg.name)
                if key in self._pkgs:
                    raise LocalError(
                        f"Multiple packages with name '{local_pkg.name}' at '{local_pkg.path}' and '{self._pkgs[key].path}'"
                    )
                self._pkgs[key] = local_pkg
            else:
                logging.warning(
                    "Found non-package file '{}' in mod folder".format(mods_child)
                )

        # search games
        games_path = userpath / "games"
        if not games_path.exists():
            raise LocalError(f"Could not find a games directory in '{userpath}'")

        for games_child in games_path.iterdir():
            if games_child.is_dir():
                if (games_child / "game.conf").exists():
                    pkg_conf = parse_conf_file(games_child / "game.conf")
                else:
                    raise LocalError(
                        f"'{games_child}' does not have a configuration file"
                    )
                gameid = games_child.name
                if gameid.endswith("_game"):
                    gameid = gameid[:-5]
                local_pkg = LocalPackage(
                    name=gameid,
                    type=PackageType.GAME,
                    path=games_child,
                    author=pkg_conf.get("author", None),
                    release=int(pkg_conf["release"]) if "release" in pkg_conf else None,
                )
                self._pkgs[(PackageType.GAME, local_pkg.name)] = local_pkg
            else:
                logging.warning(
                    "Found non-package file '{}' in game folder".format(games_child)
                )

        # search texture packs
        textures_path = userpath / "textures"
        if not textures_path.exists():
            raise LocalError(f"Could not find a textures directory in '{userpath}'")

        for textures_child in textures_path.iterdir():
            if textures_child.is_dir():
                if (textures_child / "texture_pack.conf").exists():
                    pkg_conf = parse_conf_file(textures_child / "texture_pack.conf")
                else:
                    raise LocalError(
                        f"'{textures_child}' does not have a configuration file"
                    )
                local_pkg = LocalPackage(
                    name=textures_child.name,
                    type=PackageType.GAME,
                    path=textures_child,
                    author=pkg_conf.get("author", None),
                    release=int(pkg_conf["release"]) if "release" in pkg_conf else None,
                )
                self._pkgs[(PackageType.TEXTURE_PACK, local_pkg.name)] = local_pkg
            else:
                logging.warning(
                    "Found non-package file '{}' in texture pack folder".format(
                        textures_child
                    )
                )

    def has_conflict(self, pkg: RemotePackage, force: bool) -> bool:
        # check for path conflicts
        installation_path = self.userpath / pkgtype_to_dirname(pkg.type) / pkg.name
        if (not force) and installation_path.exists():
            raise LocalError(
                f"'{pkg.author}/{pkg.name}' would be installed to '{installation_path}' but it already exists"
            )

        # check for name conflicts with mods/modpacks
        if pkg.type == PackageType.MOD:
            if (pkg.type, pkg.name) in self._pkgs:
                # mods and modpacks
                conflicting_pkg = self._pkgs[(pkg.type, pkg.name)]
                raise LocalError(
                    f"ContentDB package '{pkg.author}/{pkg.name}' has a name conflict with mod/modpack installed at '{conflicting_pkg.path}'"
                )
            if pkg.name in self._mod2pack:
                modpack = self._mod2pack[pkg.name]
                raise LocalError(
                    f"ContentDB package '{pkg.author}/{pkg.name}' has a name conflict with a mod in the modpack '{modpack.name}'"
                )
            if len(pkg.provides) >= 1:
                conflicts = set(pkg.provides) & set(
                    [k[1] for k in self._pkgs] + list(self._mod2pack.keys())
                )
                if conflicts:
                    raise LocalError(
                        f"ContentDB modpack '{pkg.author}/{pkg.name}' has a name conflict with installed mod/modpacks: {', '.join(conflicts)}"
                    )

        elif pkg.type == PackageType.GAME:
            if pkg.name.endswith("_game"):
                gameid = pkg.name[:-5]
            else:
                gameid = pkg.name

            if (pkg.type, gameid) in self._pkgs:
                conflicting_pkg = self._pkgs[(pkg.type, pkg.name)]
                raise LocalError(
                    f"ContentDB package '{pkg.author}/{pkg.name}' has a name conflict with game installed at '{conflicting_pkg.path}'"
                )

        return False

    def check_conflicts(self, packages: Set[RemotePackage], force: bool) -> None:
        errors = []
        for package in packages:
            try:
                self.has_conflict(package, force)
            except LocalError as e:
                errors.append(e)
        if errors:
            for error in errors:
                error.show()
            raise LocalError("There were conflicts with one or more packages")

    def is_installed(self, package: RemotePackage) -> bool:
        if package.type == PackageType.GAME and package.name.endswith("_game"):
            package_name = package.name[:-5]
        else:
            package_name = package.name
        if (package.type, package_name) in self._pkgs:
            local_pkg = self._pkgs[(package.type, package_name)]
            if local_pkg.author == package.author:
                return True
        return False

    def get_installed_release(self, package: RemotePackage) -> Optional[int]:
        if package.type == PackageType.GAME and package.name.endswith("_game"):
            package_name = package.name[:-5]
        else:
            package_name = package.name
        if (package.type, package_name) in self._pkgs:
            local_pkg = self._pkgs[(package.type, package_name)]
            if (local_pkg.author == package.author) and (local_pkg.release is not None):
                return local_pkg.release
        return None

    def get_install_path(self, package: RemotePackage) -> Path:
        return self.userpath / pkgtype_to_dirname(package.type) / package.name

    def world_exists(self, world_id: str) -> bool:
        return (self.userpath / "worlds" / world_id).exists()

    def enable_mods(self, world_id: str, mods: Set[str]):
        world_mt_path = self.userpath / "worlds" / world_id / "world.mt"
        to_append = mods.copy()
        # check which mods are 1) enabled, 2) disabled, and 3) missing from world.mt
        with tempfile.TemporaryFile("r+") as tmp:
            with open(world_mt_path) as world_mt_file:
                for line in world_mt_file:
                    if line.startswith("load_mod_"):
                        key, value = line.split("=")
                        mod_name = key.strip()[9:]
                        if value.strip() == "true":
                            # already enabled, ignore
                            to_append.discard(mod_name)
                            tmp.write(line)
                        elif value.strip() == "false":
                            if mod_name in to_append:
                                tmp.write(f"load_mod_{mod_name} = true\n")
                                to_append.remove(mod_name)
                            else:
                                tmp.write(line)
                        else:
                            raise LocalError(
                                f"World '{world_id}' has an invalid value in this line: '{line.rstrip()}'"
                            )
                    else:
                        tmp.write(line)
            for mod_name in to_append:
                tmp.write(f"load_mod_{mod_name} = true\n")
            tmp.seek(0)
            world_mt_path.unlink()
            with open(world_mt_path, "w") as world_mt_file:
                shutil.copyfileobj(tmp, world_mt_file)

    def get_world_game(self, world_id: str) -> str:
        world_mt_path = self.userpath / "worlds" / world_id / "world.mt"
        world_conf = parse_conf_file(world_mt_path)
        if "gameid" not in world_conf:
            raise LocalError(
                f"Configuration file for world '{world_id}' doesn't have a gameid defined"
            )
        return world_conf["gameid"]

    def is_world_game(self, world_id: str, game_id: str) -> bool:
        if game_id.endswith("_game"):
            game_id = game_id[:-5]
        return game_id == self.get_world_game(world_id)

    def get_installed_ContentDB_packages(self) -> Set[RemotePackageSpec]:
        specs = set()
        for package in self._pkgs.values():
            if (package.author is not None) and (package.release is not None):
                specs.add(RemotePackageSpec(author=package.author, name=package.name))
        return specs

    def install_release(self, package: RemotePackage, release_id: int, src: IO[bytes]):
        install_path = self.get_install_path(package)
        src.seek(0)
        with zipfile.ZipFile(src) as compressed_release:
            # search for [mod|modpack|game|texture_pack].conf at depth 1 or 2, error if not found at either depth
            ziproot = zipfile.Path(compressed_release)
            depth1_contents = list(ziproot.iterdir())
            conf_depth = None  # type: Optional[int]
            conf_filenames = get_possible_conf_names(package.type)
            if len(depth1_contents) == 1 and depth1_contents[0].is_dir():
                # check if conf exists under dir, at depth 2
                for child in depth1_contents[0].iterdir():
                    if child.name in conf_filenames and conf_depth is None:
                        conf_name = child.name
                        conf_depth = 2
                    elif child.name in conf_filenames and conf_depth is not None:
                        raise LocalError(
                            f"Multiple configuration files detected in package '{package.author}/{package.name}'. Aborting."
                        )
            elif len(depth1_contents) > 1:
                # check if conf exists at depth 1
                for child in depth1_contents:
                    if child.name in conf_filenames and conf_depth is None:
                        conf_name = child.name
                        conf_depth = 1
                    elif child.name in conf_filenames and conf_depth is not None:
                        raise LocalError(
                            f"Multiple configuration files detected in package '{package.author}/{package.name}'. Aborting."
                        )
            else:
                raise LocalError(
                    f"Downloaded release {release_id} of '{package.author}/{package.name}' but it had no files in it!"
                )

            if conf_depth is None:
                raise LocalError(
                    f"Could not find an appropriate configuration file in release {release_id} of '{package.author}/{package.name}'!"
                )

            # create folder to install to, removing existing one if necessary
            if install_path.exists():
                try:
                    shutil.rmtree(install_path)
                except Exception as e:
                    raise LocalError(
                        f"There was a problem removing the old package at '{install_path}'"
                    ) from e

            if conf_depth == 1:
                install_path.mkdir()
                compressed_release.extractall(install_path)
            elif conf_depth == 2:
                # extract contents of depth 1 dir
                depth1_dir = list(zipfile.Path(compressed_release).iterdir())[0].name
                # extract to tempdir and move to correctly-named dir
                with tempfile.TemporaryDirectory() as tmpdir:
                    compressed_release.extractall(tmpdir)
                    moddir = Path(tmpdir) / depth1_dir
                    moddir.rename(install_path)
            else:
                raise LocalError(
                    f"Something went wrong while searching for a configuration file in release '{release_id}' for package '{package.author}/{package.name}'. This shouldn't happen."
                )

        # update the conf file with author and release ID
        with open(install_path / conf_name, "a") as conf_file:
            conf_file.write(f"author = {package.author}\n")
            conf_file.write(f"release = {release_id}\n")

        # add to package db
        local_pkg = LocalPackage(
            name=package.name,
            type=package.type,
            path=install_path,
            author=package.author,
            release=release_id,
        )
        self._pkgs[(package.type, package.name)] = local_pkg

        # recursively add mods to mod2pack
        for submod in filter(lambda p: p.is_dir(), install_path.iterdir()):
            if (submod / "mod.conf").exists():
                submod_conf = parse_conf_file(submod / "mod.conf")
                submod_name = submod_conf.get("name", submod.name)
            else:
                submod_name = submod.name
            self._mod2pack[submod_name] = local_pkg


def get_possible_conf_names(pkgtype: PackageType) -> Set[str]:
    if pkgtype == PackageType.MOD:
        return {"mod.conf", "modpack.conf"}
    if pkgtype == PackageType.GAME:
        return {"game.conf"}
    if pkgtype == PackageType.TEXTURE_PACK:
        return {"texture_pack.conf"}
    raise ValueError(f"Unknown package type '{pkgtype}'")


def parse_conf_file(path: Path) -> Dict[str, str]:
    conf = {}
    with open(path) as conf_file:
        for line in conf_file:
            key, value = (e.strip() for e in line.split("=", maxsplit=1))
            conf[key] = value

    return conf

"""
remote.py

Module for interacting with the Minetest ContentDB
"""


from dataclasses import dataclass
from distutils.version import LooseVersion
from enum import Enum, unique
from functools import partial
import logging
import operator
from pathlib import Path
import pickle
import time
from typing import Dict, Any, Set, FrozenSet, IO, Union, List, Optional

import click
import requests
from tqdm import tqdm  # type: ignore


ParsedJSON = Union[List[Any], Dict[str, Any]]


@unique
class PackageType(Enum):
    MOD = 1
    GAME = 2
    TEXTURE_PACK = 3

    @classmethod
    def from_cdb_type(cls, cdb_type: str) -> "PackageType":
        cdb_type = cdb_type.lower()
        if cdb_type == "mod":
            return cls.MOD
        if cdb_type == "game":
            return cls.GAME
        if cdb_type == "txp":
            return cls.TEXTURE_PACK
        raise ValueError(f"Invalid ContentDB package type '{cdb_type}'")


@dataclass(frozen=True)
class RemotePackageSpec:
    author: str
    name: str


class RemoteError(click.ClickException):
    def show(self, file=None):
        logging.error(self.message)


class PackageNotFoundError(RemoteError):
    pass


@dataclass(frozen=True)
class RemotePackage:
    name: str
    author: str
    type: PackageType
    provides: FrozenSet[str]
    score: float


class ContentDB:

    _global_sleep: float = 0.4
    _metadata_cache_name: str = "metadata.pkl"
    _cache: Dict[str, Dict[str, Any]]

    def __init__(
        self, server: str = "https://content.minetest.net", cache: Optional[Path] = None
    ):
        self.server = server
        self.base_url = f"{server}/api"
        self._cache = {"get": {}, "head": {}}
        if cache is not None:
            metadata_cache_path = cache / self._metadata_cache_name
            # ignore cache if created more than 24 hours ago
            if metadata_cache_path.exists():
                if (time.time() - metadata_cache_path.stat().st_ctime) <= 86400:
                    logging.debug("Loading persistent cache for ContentDB")
                    with open(metadata_cache_path, "rb") as metadata_cache_file:
                        self._cache = pickle.load(metadata_cache_file)
                else:
                    logging.debug("Cache too old, ignoring")
        self.cache = cache

    def write_cache(self):
        if self.cache is not None:
            metadata_cache_path = self.cache / self._metadata_cache_name
            if metadata_cache_path.exists():
                metadata_cache_path.unlink()
            with open(metadata_cache_path, "wb") as metadata_cache_file:
                pickle.dump(self._cache, metadata_cache_file)
            logging.debug("Cache dumped successfully")

    def _get_request_json(self, url: str) -> ParsedJSON:
        if url in self._cache["get"]:
            response_json = self._cache["get"][url]
            if response_json == 404:
                fake_response = requests.Response()
                fake_response.status_code = 404
                raise requests.HTTPError(response=fake_response)
        else:
            response = requests.get(url)
            if response.status_code == 404:
                # cache 404 errors too
                self._cache["get"][url] = 404
            response.raise_for_status()
            response_json = response.json()
            self._cache["get"][url] = response_json
            time.sleep(self._global_sleep)
        return response_json

    def _head_request(
        self, url: str, allow_redirects: bool = False
    ) -> requests.structures.CaseInsensitiveDict:
        if url in self._cache["head"]:
            headers = self._cache["head"][url]
        else:
            response = requests.head(url, allow_redirects=allow_redirects)
            response.raise_for_status()
            headers = response.headers
            self._cache["head"][url] = headers
            time.sleep(self._global_sleep)
        return headers

    def get_latest_minetest_version(self) -> str:
        """Fetches the latest stable Minetest version from the ContentDB.

        Returns the version name as a string and the integer client protocol version.
        """
        try:
            versions = self._get_request_json(f"{self.base_url}/minetest_versions/")
        except requests.HTTPError as e:
            raise RemoteError(
                "Failed to get latest Minetest version from ContentDB"
            ) from e
        non_dev_versions = filter(lambda v: not v["is_dev"], versions)
        latest_version = sorted(
            non_dev_versions, key=lambda v: LooseVersion(v["name"]), reverse=True
        )[0]

        return latest_version["name"]

    def get_package(self, author: str, name: str) -> RemotePackage:
        try:
            package_details = self._get_request_json(
                f"{self.base_url}/packages/{author}/{name}/"
            )
        except requests.HTTPError as e:
            if (e.response is not None) and e.response.status_code == 404:
                raise PackageNotFoundError(
                    f"Package '{author}/{name}' not found in the ContentDB"
                ) from e
            raise RemoteError(
                f"Error retrieving package details for '{author}/{name}' from ContentDB"
            ) from e
        if isinstance(package_details, list):
            raise RemoteError(
                f"Invalid JSON received while retrieving details for package '{author}/{name}'"
            )
        return RemotePackage(
            name=package_details["name"],
            author=package_details["author"],
            type=PackageType.from_cdb_type(package_details["type"]),
            provides=frozenset((str(p) for p in package_details["provides"])),
            score=package_details["score"],
        )

    def get_packages(self, specs: Set[RemotePackageSpec]) -> Set[RemotePackage]:
        errors = []
        packages = set()
        for spec in specs:
            try:
                packages.add(self.get_package(spec.author, spec.name))
            except RemoteError as e:
                errors.append(e)

        if errors:
            for error in errors:
                error.show()
            raise RemoteError("There were errors retrieving one or more packages")

        return packages

    def get_latest_compatible_release_id(
        self, package: RemotePackage, mtver: str, game_provided: bool
    ) -> int:
        try:
            releases = self._get_request_json(
                f"{self.base_url}/packages/{package.author}/{package.name}/releases/"
            )
        except requests.HTTPError as e:
            raise RemoteError(
                f"Error retrieving releases for '{package.author}/{package.name}' from ContentDB"
            ) from e
        if isinstance(releases, dict):
            raise RemoteError(
                f"Invalid JSON received while retrieving releases for package '{package.author}/{package.name}'"
            )
        latest_release = releases[0]["id"]

        # filter releases to compatible and sort by descending release ID
        is_compatible = partial(self.is_compatible, mtver=mtver)
        compatible_releases = filter(is_compatible, releases)
        sorted_releases = sorted(
            compatible_releases, key=operator.itemgetter("id"), reverse=True
        )
        if len(sorted_releases) < 1:
            raise RemoteError(
                f"No compatible releases found for package '{package.author}/{package.name}'"
            )
        latest_compatible_release = sorted_releases[0]["id"]
        if game_provided and (latest_release != latest_compatible_release):
            logging.warning(
                f"The latest release of '{package.author}/{package.name}' isn't compatible with the requested Minetest version '{mtver}' but recursive dependency resolution was requested. The ContentDB currently only provides dependencies for the latest release through the API, so dependency resolution may not be accurate for this package."
            )

        return latest_compatible_release

    def get_latest_compatible_release_ids(
        self, packages: Set[RemotePackage], mtver: str, game_provided: bool = False
    ) -> Dict[RemotePackage, int]:
        latest_compat_release_ids = {}
        errors = []
        for package in packages:
            try:
                latest_compat_release_ids[
                    package
                ] = self.get_latest_compatible_release_id(package, mtver, game_provided)
            except RemoteError as e:
                errors.append(e)

        if errors:
            for error in errors:
                error.show()
            raise RemoteError(
                "There were problems getting the latest release information for one or more packages"
            )

        return latest_compat_release_ids

    @staticmethod
    def is_compatible(release: Dict[str, Any], mtver: str) -> bool:
        maxver = release["max_minetest_version"]
        minver = release["min_minetest_version"]
        if maxver and (LooseVersion(mtver) > LooseVersion(maxver["name"])):
            return False
        if minver and (LooseVersion(mtver) < LooseVersion(minver["name"])):
            return False
        return True

    def get_release_download_url(self, package: RemotePackage, release_id: int) -> str:
        return f"{self.server}/packages/{package.author}/{package.name}/releases/{release_id}/download/"

    def download_release(
        self, package: RemotePackage, release_id: int, dest: IO[bytes]
    ) -> None:
        download_url = self.get_release_download_url(package, release_id)
        try:
            headers = self._head_request(download_url, allow_redirects=True)
        except requests.HTTPError as e:
            raise RemoteError(
                f"There was a problem requesting the file size of release '{release_id}' for package '{package.author}/{package.name}'"
            ) from e
        filesize = int(headers["Content-Length"])
        with requests.get(download_url, stream=True) as response, tqdm(
            desc=f"{package.author}/{package.name}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            total=filesize,
        ) as progress:
            if response.status_code != 200:
                raise RemoteError(
                    f"There was a problem downloading release {release_id} for '{package.author}/{package.name}'. Server returned status code {response.status_code}."
                )
            for chunk in response.iter_content(chunk_size=32768):
                datasize = dest.write(chunk)
                progress.update(datasize)

    def get_recursive_dependencies(
        self,
        packages: Set[RemotePackage],
        optional: bool = False,
        assume_yes: bool = False,
    ) -> Set[RemotePackage]:
        query_url = self.base_url + "/packages/{author}/{name}/dependencies/"
        if not optional:
            query_url += "?only_hard=1"
        provided = {mod for package in packages for mod in package.provides}
        queries = packages.copy()
        required = set()  # type: Set[RemotePackage]
        # for each package, check if dependencies are in provided, otherwise add to required and queries
        while queries:
            query = next(iter(queries))
            try:
                response_json = self._get_request_json(
                    query_url.format(author=query.author, name=query.name)
                )
            except requests.HTTPError as e:
                raise RemoteError(
                    f"Error retrieving dependencies for package '{query.author}/{query.name}'"
                ) from e
            if isinstance(response_json, list):
                raise RemoteError(
                    f"Invalid JSON received while retrieving dependencies for package '{query.author}/{query.name}'"
                )
            dependencies = response_json[f"{query.author}/{query.name}"]
            for dependency in dependencies:
                if dependency["name"] not in (provided | required):
                    choices = []
                    for package in dependency["packages"]:
                        try:
                            choices.append(self.get_package(*package.split("/")))
                        except PackageNotFoundError:
                            continue
                    # filter out games
                    filtered_choices = filter(
                        lambda c: c.type != PackageType.GAME, choices
                    )
                    # filter out modpacks that provide things that are already provided
                    filtered_choices = filter(
                        lambda c: c.provides.isdisjoint(provided), choices
                    )
                    # sort by score (secondary), then exact name matches (primary)
                    choices = sorted(
                        filtered_choices, key=operator.attrgetter("score"), reverse=True
                    )
                    name_matches = partial(operator.eq, dependency["name"])
                    choices = sorted(
                        choices,
                        key=name_matches,
                        reverse=True,
                    )

                    if not choices:
                        raise RemoteError(
                            f"There are no packages on the ContentDB that can satisfy the requirement '{dependency['name']}'"
                        )

                    choice = -1
                    if assume_yes or (len(choices) == 1):
                        choice = 0
                    else:
                        while (choice < 0) or (choice >= len(choices)):
                            prompt = "\n".join(
                                (
                                    f"[{i}]: {c.author}/{c.name}"
                                    for i, c in enumerate(choices)
                                )
                            )
                            choice = click.prompt(
                                f"{prompt}\nPlease select the number of the dependency to install",
                                type=int,
                            )
                    queries.add(choices[choice])
                    required.add(choices[choice])
            queries.remove(query)
        return required

import asyncio
from collections import defaultdict
from dataclasses import dataclass
import hashlib
import logging
import math
import pathlib
import re
import requests
import json
import os
import shutil
import typing
import zipfile
from enum import Enum, IntEnum
from Utils import cache_path, version_tuple

import Utils
from worlds import world_sources
from worlds.Files import InvalidDataError
from ._vendor.packaging.version import Version, VERSION_PATTERN, InvalidVersion

class GithubRateLimitExceeded(Exception):
    pass

@dataclass
class ApWorldVersion:
    blessed: bool

@dataclass
class ApWorldMetadataAllVersions:
    name: str
    developers: list[str]
    installed_version: typing.Optional[str]
    versions: dict[str, ApWorldVersion]



class RemoteWorldSource(Enum):
    SOURCE_CODE = 0
    LOCAL = 1
    REMOTE_BLESSED = 2
    REMOTE = 3

@dataclass
class ApWorldMetadata:
    source: RemoteWorldSource
    data: dict[str, typing.Any]
    is_in_cache = False
    # source: WorldSource
    # TODO: .validate()

    @property
    def id(self) -> str:
        return self.data['metadata']['id']

    @property
    def name(self) -> str:
        return self.data['metadata']['game']

    @property
    def world_version(self) -> str:
        return self.data['metadata']['world_version']

    @property
    def version_tuple(self) -> tuple[int, int, int]:
        v = parse_version(self.world_version)
        return Utils.Version(v.major, v.minor, v.micro)

    @property
    def source_url(self) -> str:
        return self.data['source_url']

    @property
    def download_url(self) -> str:
        return self.data['world']

    @property
    def created_at(self) -> str:
        return self.data['metadata'].get('created_at')

    @property
    def minimum_ap_version(self) -> tuple[int, int, int]:
        v = self.data['metadata'].get('minimum_ap_version', (0, 0, 0))
        if isinstance(v, str):
            v = Utils.tuplize_version(v)
        return v

    @property
    def maximum_ap_version(self) -> tuple[int, int, int]:
        v = self.data['metadata'].get('maximum_ap_version', (math.inf,))
        if isinstance(v, str):
            v = Utils.tuplize_version(v)
        return v

    @property
    def after_dark(self) -> bool:
        return self.data['metadata'].get('after_dark', False) or self.data['metadata'].get('flags', {}).get('after_dark', False)

    @property
    def unready(self) -> bool:
        return self.data['metadata'].get('flags', {}).get('unready', False)

class Repository:
    def __init__(self, world_source: RemoteWorldSource, path: str, apworld_cache_path) -> None:
        self.path = path
        self.index_json = None
        self.world_source = world_source
        self.apworld_cache_path = apworld_cache_path
        self.worlds: typing.List[ApWorldMetadata] = []

    def refresh(self):
        try:
            self.get_repository_json()
        except requests.exceptions.ConnectionError as e:
            logging.exception(e)

    def get_repository_json(self):
        if self.world_source == RemoteWorldSource.REMOTE or self.world_source == RemoteWorldSource.REMOTE_BLESSED:
            response = requests.get(self.path)
            self.index_json = response.json()

            self.worlds = [
                ApWorldMetadata(self.world_source, world) for world in self.index_json['worlds']
            ]
            for world in self.worlds.copy():
                world.data['source_url'] = self.path
                if world.minimum_ap_version > version_tuple or world.maximum_ap_version < version_tuple:
                    self.worlds.remove(world)
                    continue

        elif self.world_source == RemoteWorldSource.LOCAL:
            self.worlds = []
            for file in os.listdir(self.path):
                path = os.path.join(self.path, file)

                try:
                    with open(path, 'rb') as f:
                        hash_sha256 = hashlib.sha256(f.read()).hexdigest()
                    metadata_str = zipfile.ZipFile(path).read('archipelago.json')
                    metadata = json.loads(metadata_str)
                    metadata = {
                        'metadata': metadata,
                        'hash_sha256': hash_sha256,
                        'size': os.path.getsize(path),
                        'source_url': self.path,
                    }
                    world = ApWorldMetadata(self.world_source, metadata)
                    self.worlds.append(world)
                except Exception as e:
                    continue

                cache_dir = os.path.join(self.apworld_cache_path, hash_sha256)
                if not os.path.exists(cache_dir):
                    os.mkdir(cache_dir)
                world_cache_path = os.path.join(cache_dir, file)
                json_cache_path = os.path.join(cache_dir, 'archipelago.json')
                if not os.path.exists(world_cache_path) or not os.path.exists(json_cache_path):
                    json.dump(metadata, open(json_cache_path, 'w'))
                    shutil.copyfile(path, world_cache_path)
                    print(f"Copied {file} to cache")
                    # TODO: Log this
                world.is_in_cache = True

        else:
            assert False

        self.worlds.sort(key = lambda x: x.name)

class GithubRepository(Repository):
    def __init__(self, world_source: RemoteWorldSource, url: str, apworld_cache_path) -> None:
        super().__init__(world_source, url, apworld_cache_path)
        if url.startswith("https://github.com"):
            url = url.replace("https://github.com", "https://api.github.com/repos")
        if url.endswith("/"):
            url = url[:-1]
        self.url = url
        os.makedirs(os.path.join(apworld_cache_path, "github"), exist_ok=True)

    def get_license(self) -> typing.Optional[str]:
        """Get the license for this repository."""
        data = self.fetch(self.url)
        if data.get('license'):
            license = data['license']['spdx_id']
            if license == 'NOASSERTION':
                return None
            return license
        return None

    def get_repository_json(self):
        self.worlds = []
        # response = requests.get(f"{self.url}/contents/README.md")
        # readme = response.json()
        # description = readme['content']
        # if readme['encoding'] == 'base64':
        #     description = base64.b64decode(description).decode('utf-8')


        releases_endpoint_url = f"{self.url}/releases"
        endpoint_sha = hashlib.sha256(releases_endpoint_url.encode()).hexdigest()
        cached_request = pathlib.Path(self.apworld_cache_path, "github", f'{endpoint_sha}.json')

        releases = self.fetch(releases_endpoint_url)

        if isinstance(releases, dict) and 'message' in releases:
            print(f"Error getting releases from {self.url}: {releases['message']}")
            if cached_request.exists():
                releases = json.load(cached_request.open())
            elif releases['message'].startswith("API rate limit exceeded for"):
                raise GithubRateLimitExceeded(releases['message'])
            else:
                return
        else:
            with cached_request.open('w') as f:
                json.dump(releases, f)
        self.release_json = releases
        if not releases:
            print(f"No releases found for {self.url}")
            return
        for release in releases:
            tag = release['tag_name']
            for asset in release['assets']:
                if asset['name'].endswith('.apworld'):
                    world_id = asset['name'].replace('.apworld', '').replace(tag, '').rstrip('-_')

                    world = {}
                    world['metadata'] = {
                        'id': world_id,
                        'game': '',
                        'world_version': tag,
                        'description': '',
                        'created_at': release.get('created_at') or release.get('published_at'),
                        'title': release.get('name'),
                    }
                    world['source_url'] = self.url
                    world['world'] = asset['browser_download_url']
                    world['size'] = asset['size']
                    self.worlds.append(ApWorldMetadata(self.world_source, world))
        response = requests.get(f"{self.url}/releases/tags/{tag}")
        self.index_json = response.json()

    def fetch(self, url):
        from . import RepoWorld
        gh_token = RepoWorld.settings.github_token
        if not gh_token:
            headers = {}
        else:
            headers = {"Authorization": f"Bearer {gh_token}"}
        response = requests.get(url, headers=headers)
        releases = response.json()
        return releases


class RepositoryManager:
    def __init__(self) -> None:
        self.all_known_package_ids: typing.Set[str] = set()
        self.repositories: typing.List[Repository] = []
        self.local_packages_by_id: typing.Dict[str, ApWorldMetadata] = {}
        self.packages_by_id_version: typing.DefaultDict[str, typing.Dict[str, ApWorldMetadata]] = defaultdict(dict)
        self.apworld_cache_path = cache_path("apworlds")
        os.makedirs(self.apworld_cache_path, exist_ok=True)

    def load_repos_from_settings(self):
        from . import RepoWorld
        for repo, enabled in RepoWorld.settings.repositories.items():
            if not enabled:
                continue

            if repo.startswith("https://github.com/"):
                self.add_github_repository(repo)
            elif repo.startswith("https://"):
                self.add_remote_repository(repo)
            else:
                self.add_local_dir(repo)

    def add_local_dir(self, path: str) -> Repository:
        repo = Repository(RemoteWorldSource.LOCAL, path, self.apworld_cache_path)
        self.repositories.append(repo)
        return repo

    def add_remote_repository(self, url: str, blessed: bool = False) -> Repository:
        repo = Repository(RemoteWorldSource.REMOTE_BLESSED if blessed else RemoteWorldSource.REMOTE, url, self.apworld_cache_path)
        self.repositories.append(repo)
        return repo

    def add_github_repository(self, url: str, blessed: bool = False) -> GithubRepository:
        """This is not recommended for general use, as it will bump against the github api rate limit.  But it's useful for testing."""
        repo = GithubRepository(RemoteWorldSource.REMOTE_BLESSED if blessed else RemoteWorldSource.REMOTE, url, self.apworld_cache_path)
        self.repositories.append(repo)
        return repo

    def refresh(self):
        self.packages_by_id_version.clear()
        for repo in self.repositories:
            repo.refresh()
            if repo.world_source == RemoteWorldSource.LOCAL:
                for world in repo.worlds:
                    self.all_known_package_ids.add(world.id)
                    self.local_packages_by_id[world.id] = world
            else:
                for world in repo.worlds:
                    self.all_known_package_ids.add(world.id)
                    self.packages_by_id_version[world.id][world.world_version] = world

    def download_remote_world(self, world: ApWorldMetadata, add_missing_metadata: bool = True) -> str:
        world_version_pathsafe = world.world_version.replace('/', '_')
        path = os.path.join(self.apworld_cache_path, f"{world.id}-{world_version_pathsafe}.apworld")
        if not os.path.exists(path):
            response = requests.get(world.download_url)
            with open(path, 'wb') as f:
                f.write(response.content)
        if add_missing_metadata:
            try:
                metadata_str = zipfile.ZipFile(path).read('archipelago.json')
                metadata = json.loads(metadata_str)
            except KeyError:
                print("No archipelago.json in ", path)
                metadata = {
                        "version": 6,
                        "compatible_version": 5,
                        'game': world.name,
                        'id': world.id,
                        'world_version_full': world.world_version,
                        'world_version': world.version_tuple.as_simple_string(),
                        'description': '',
                }
                if world.data['metadata'].get('minimum_ap_version'):
                    metadata['minimum_ap_version'] = world.data['metadata']['minimum_ap_version']
                if world.data['metadata'].get('maximum_ap_version'):
                    metadata['maximum_ap_version'] = world.data['metadata']['maximum_ap_version']

                with zipfile.ZipFile(path, 'a') as zf:
                    zf.writestr("archipelago.json", json.dumps(metadata, indent=4))
        return path

    def find_release_by_hash(self, hash_sha256: str) -> typing.Optional[ApWorldMetadata]:
        for repo in self.repositories:
            for world in repo.worlds:
                if world.data.get('hash_sha256') == hash_sha256:
                    return world
        return None

def parse_version(version: str) -> Version:
    if isinstance(version, tuple):
        version = '.'.join(str(x) for x in version)
    if version.startswith("v"):
        version = version[1:]
    try:
        return Version(version)
    except InvalidVersion as e:
        matches = list(re.finditer(VERSION_PATTERN, version, re.VERBOSE | re.IGNORECASE))
        matches.sort(key=lambda x: len(x.group(0)), reverse=True)
        if matches:
            return Version(matches[0].group(0))
        return Version(f"0.0.0+{version}")

class SortStages(IntEnum):
    UPDATE_AVAILABLE = 3
    BUNDLED_BUT_UPDATABLE = 2
    INSTALLED = 1
    DEFAULT = 0
    AFTER_DARK = -4
    MANUAL = -5
    NO_REMOTE = -9
    BUNDLED = -10

repositories = RepositoryManager()

def refresh_apworld_table() -> list[dict[str, typing.Any]]:
        """Refresh the list of available APWorlds from the repositories."""
        from worlds import AutoWorld
        from .container import RepoWorldContainer

        register = AutoWorld.AutoWorldRegister
        apworlds = []
        installed = set()
        for name, world in register.world_types.items():
            file: pathlib.Path = world.zip_path
            if not file:
                # data = {"title": name, "description": "Unpacked World", "metadata": {"game": None}}
                # apworlds.append(data)
                installed.add(world.__module__.split(".")[1])
                continue

            container = RepoWorldContainer(file)
            installed.add(file.stem)
            try:
                container.read()
            except InvalidDataError as e:
                print(f"Error reading manifest for {file}: {e}")
                # continue
            except FileNotFoundError as e:
                print(f"Error reading manifest for {file}: {e}")
                continue
            manifest_data = container.get_manifest()
            remote = repositories.packages_by_id_version.get(file.stem)
            local_version = manifest_data.get("world_version_full", "")
            if not local_version:
                local_version = manifest_data.setdefault("world_version", "0.0.0")
            if local_version == "0.0.0":
                with open(file, 'rb') as f:
                    hash = hashlib.sha256(f.read()).hexdigest()
                if local := repositories.find_release_by_hash(hash):
                    local_version = local.world_version
            if local_version == "0.0.0":
                if local := getattr(world, "world_version", None):
                    local_version = local
            description = "Placeholder text"
            data = {
                "title": name,
                "installed": True,
                "manifest": manifest_data,
                "remotes": remote,
                'update_available': False,
                'install_text': '-',
                "after_dark": manifest_data.get("after_dark", False),
                "file": file,
            }
            source = [s for s in world_sources if s.path == str(file) or s.path == str(file.name)]
            if source and source[0].relative:
                # We can't update a frozen world right now
                # This will change when https://github.com/ArchipelagoMW/Archipelago/pull/4516 is merged
                description = "Bundled with AP"
                data['sort'] = SortStages.BUNDLED
                if local_version != "0.0.0" and remote:
                    highest_remote_version = max(remote.values(), key=lambda w: parse_version(w.world_version))
                    data["latest_version"] = highest_remote_version
                    v_local = parse_version(local_version)
                    v_remote = parse_version(highest_remote_version.world_version)
                    data['update_available'] = v_remote > v_local
                    if data['update_available']:
                        description = f"Update available: {v_local} -> {v_remote}"
                        data['sort'] = SortStages.BUNDLED_BUT_UPDATABLE
                        data['install_text'] = "Unbundle and Update"
            elif not remote:
                description = "No remote data available"
                data['sort'] = SortStages.NO_REMOTE
            else:
                highest_remote_version = max(remote.values(), key=lambda w: parse_version(w.world_version))
                data["latest_version"] = highest_remote_version
                v_local = parse_version(local_version)
                v_remote = parse_version(highest_remote_version.world_version)
                data['update_available'] = v_remote > v_local
                if data['update_available']:
                    description = f"Update available: {v_local} -> {v_remote}"
                    data['sort'] = SortStages.UPDATE_AVAILABLE
                    data['install_text'] = "Update"
                else:
                    description = "Up to date"
                    data['sort'] = SortStages.INSTALLED
                    data['install_text'] = "-"
            data["description"] = description
            apworlds.append(data)

        from . import RepoWorld
        show_after_dark = RepoWorld.settings.show_after_dark
        show_manuals = RepoWorld.settings.show_manuals

        for world in sorted(repositories.all_known_package_ids):
            if world in installed:
                continue
            remote = repositories.packages_by_id_version.get(world)
            if not remote:
                continue
            highest_remote_version = sorted(remote.values(), key=lambda x: x.version_tuple)[-1]
            data = {
                "title": highest_remote_version.name or f'{world}.apworld',
                "description": "Available to install",
                "latest_version": highest_remote_version,
                "update_available": True,
                "manifest": {},
                "installed": False,
                "sort": SortStages.DEFAULT,
                "install_text": "Install",
                "after_dark": highest_remote_version.data['metadata'].get("after_dark", False),
                "file": None,
                }
            if highest_remote_version.data['metadata'].get("after_dark", False):
                data['sort'] = SortStages.AFTER_DARK
                if not show_after_dark:
                    continue
            if world.lower().startswith('manual_'):
                data['sort'] = SortStages.MANUAL
                if not show_manuals:
                    continue
            apworlds.append(data)
        apworlds.sort(key=lambda x: x['sort'], reverse=True)
        return apworlds

if __name__ == '__main__':
    local_dir = './worlds_test_dir'

    repositories.load_repos_from_settings()

    if os.path.exists(local_dir):
        repositories.add_local_dir(local_dir)
    repositories.add_remote_repository('https://raw.githubusercontent.com/zig-for/Archipelago/zig/apworld_manager/PackageLib/index.json')
    repositories.add_github_repository('https://github.com/DeamonHunter/ArchipelagoMuseDash/')
    repositories.add_github_repository('https://github.com/Rurusachi/Archipelago')
    # Comment this out to test refresh from nothing
    repositories.refresh()
    from .md_app import WorldManagerApp
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = WorldManagerApp(repositories)

    loop.run_until_complete(app.async_run())
    loop.close()

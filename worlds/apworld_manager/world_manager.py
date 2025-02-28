import asyncio
from collections import defaultdict
from dataclasses import dataclass
import hashlib
import pathlib
import re
import requests
import json
import os
import shutil
import typing
import zipfile
from enum import Enum
from Utils import cache_path

import Utils
from ._vendor.packaging.version import Version, VERSION_PATTERN, InvalidVersion


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

class Repository:
    def __init__(self, world_source: RemoteWorldSource, path: str, apworld_cache_path) -> None:
        self.path = path
        self.index_json = None
        self.world_source = world_source
        self.apworld_cache_path = apworld_cache_path
        self.worlds: typing.List[ApWorldMetadata] = []

    def refresh(self):
        self.get_repository_json()

    def get_repository_json(self):
        if self.world_source == RemoteWorldSource.REMOTE or self.world_source == RemoteWorldSource.REMOTE_BLESSED:
            response = requests.get(self.path)
            self.index_json = response.json()

            self.worlds = [
                ApWorldMetadata(self.world_source, world) for world in self.index_json['worlds']
            ]
            for world in self.worlds:
                world.data['source_url'] = self.path

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

        from . import RepoWorld
        gh_token = RepoWorld.settings.github_token or os.environ.get('GITHUB_TOKEN')
        if not gh_token:
            headers = {}
        else:
            headers = {"Authorization": f"Bearer {gh_token}"}
        response = requests.get(releases_endpoint_url, headers=headers)
        releases = response.json()

        if isinstance(releases, dict) and 'message' in releases:
            print(f"Error getting releases from {self.url}: {releases['message']}")
            if cached_request.exists():
                releases = json.load(cached_request.open())
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
                        'world_version': tag.replace('v', ''),
                        'description': '',
                        'created_at': release.get('created_at') or release.get('published_at'),
                    }
                    world['source_url'] = self.url
                    world['world'] = asset['browser_download_url']
                    world['size'] = asset['size']
                    self.worlds.append(ApWorldMetadata(self.world_source, world))
        response = requests.get(f"{self.url}/releases/tags/{tag}")
        self.index_json = response.json()


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

    def download_remote_world(self, world: ApWorldMetadata, add_missing_metadata: True) -> str:
        path = os.path.join(self.apworld_cache_path, f"{world.id}-{world.world_version}.apworld")
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
    try:
        return Version(version)
    except InvalidVersion as e:
        simple = re.search(VERSION_PATTERN, version, re.VERBOSE | re.IGNORECASE)
        if simple:
            return Version(simple.group(0))
        return Version(f"0.0.0+{version}")


if __name__ == '__main__':
    local_dir = './worlds_test_dir'

    repositories = RepositoryManager()
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

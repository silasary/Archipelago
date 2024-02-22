import base64
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
# from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.uix.dropdown import DropDown
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from collections import defaultdict
from dataclasses import dataclass
import hashlib
import packaging.version
import requests
import json
import os
import shutil
import typing
import zipfile
from Utils import title_sorted
from worlds import AutoWorldRegister
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# Config.set('graphics', 'width', '1600')
Config.write()

ap_worlds = {w.zip_path.name.replace('.apworld', ''):w for n, w in AutoWorldRegister.world_types.items() if w.zip_path is not None}

class CustomDropDown(DropDown):
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

from enum import Enum


class WorldSource(Enum):
    SOURCE_CODE = 0
    LOCAL = 1
    REMOTE_BLESSED = 2
    REMOTE = 3

@dataclass
class ApWorldMetadata:
    source: WorldSource
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
    def source_url(self) -> str:
        return self.data['source_url']

class Repository:
    def __init__(self, world_source: WorldSource, path: str, apworld_cache_path) -> None:
        self.path = path
        self.index_json = None
        self.world_source = world_source
        self.apworld_cache_path = apworld_cache_path
        self.worlds: typing.List[ApWorldMetadata] = []

    def refresh(self):
        self.get_repository_json()

    def get_repository_json(self):
        if self.world_source == WorldSource.REMOTE or self.world_source == WorldSource.REMOTE_BLESSED:
            response = requests.get(self.path)
            self.index_json = response.json()

            self.worlds = [
                ApWorldMetadata(self.world_source, world) for world in self.index_json['worlds']
            ]
            for world in self.worlds:
                world.data['source_url'] = self.path

        elif self.world_source == WorldSource.LOCAL:
            self.worlds = []
            for file in os.listdir(self.path):
                path = os.path.join(self.path, file)

                try:
                    with open(path, 'rb') as f:
                        hash_sha256 = hashlib.sha256(f.read()).hexdigest()
                    metadata_str = zipfile.ZipFile(path).read('metadata.json')
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
                json_cache_path = os.path.join(cache_dir, 'metadata.json')
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
    def __init__(self, world_source: WorldSource, url: str, apworld_cache_path) -> None:
        super().__init__(world_source, url, apworld_cache_path)
        if url.startswith("https://github.com"):
            url = url.replace("https://github.com", "https://api.github.com/repos")
        if url.endswith("/"):
            url = url[:-1]
        self.url = url


    def get_repository_json(self):
        self.worlds = []
        # response = requests.get(f"{self.url}/contents/README.md")
        # readme = response.json()
        # description = readme['content']
        # if readme['encoding'] == 'base64':
        #     description = base64.b64decode(description).decode('utf-8')

        response = requests.get(f"{self.url}/releases")
        releases = response.json()
        if isinstance(releases, dict) and 'message' in releases:
            print(f"Error getting releases from {self.url}: {releases['message']}")
            return
        for release in releases:
            tag = release['tag_name']
            for asset in release['assets']:
                if asset['name'].endswith('.apworld'):
                    world_id = asset['name'].replace('.apworld', '')
                    world = {}
                    world['metadata'] = {
                        'id': world_id,
                        'game': '',
                        'world_version': tag.replace('v', ''),
                        'description': '',
                    }
                    world['source_url'] = asset['browser_download_url']
                    self.worlds.append(ApWorldMetadata(self.world_source, world))
        response = requests.get(f"{self.url}/releases/tags/{tag}")
        self.index_json = response.json()

        # for world in self.worlds:
        #     world.data['source_url'] = self.url

from Utils import cache_path

class RepositoryManager:
    def __init__(self) -> None:
        self.all_known_package_ids: typing.Set[str] = set()
        self.repositories: typing.List[Repository] = []
        self.local_packages_by_id: typing.Dict[str, ApWorldMetadata] = {}
        self.packages_by_id_version: typing.DefaultDict[str, typing.Dict[str, ApWorldMetadata]] = defaultdict(dict)
        self.apworld_cache_path = cache_path("apworlds")
        os.makedirs(self.apworld_cache_path, exist_ok=True)

    def add_local_dir(self, path: str):
        self.repositories.append(Repository(WorldSource.LOCAL, path, self.apworld_cache_path))

    def add_remote_repository(self, url: str, blessed: bool = False) -> None:
        self.repositories.append(Repository(WorldSource.REMOTE_BLESSED if blessed else WorldSource.REMOTE, url, self.apworld_cache_path))

    def add_github_repository(self, url: str, blessed: bool = False) -> None:
        self.repositories.append(GithubRepository(WorldSource.REMOTE_BLESSED if blessed else WorldSource.REMOTE, url, self.apworld_cache_path))

    def refresh(self):
        self.packages_by_id_version.clear()
        for repo in self.repositories:
            repo.refresh()
            if repo.world_source == WorldSource.LOCAL:
                for world in repo.worlds:
                    self.all_known_package_ids.add(world.id)
                    self.local_packages_by_id[world.id] = world
            else:
                for world in repo.worlds:
                    self.all_known_package_ids.add(world.id)
                    self.packages_by_id_version[world.id][world.world_version] = world




class MainLayout(GridLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.cols = 1

from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp

from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.list import OneLineAvatarListItem

from kivymd.uix.list import OneLineListItem

KV = '''
<Item>
    MDRaisedButton:
        text: root.text
    ImageLeftWidget:
        source: root.source

'''
class Item(OneLineListItem):
    divider = None
    source = StringProperty()

class WorldManagerApp(MDApp):
    def __init__(self, repositories: RepositoryManager) -> None:
        self.repositories = repositories
        super().__init__()

    def get_world_info(self):
        world_info = []
        self.world_name_to_id = {}
        self.available_versions = {}
        self.descriptions = {}
        self.installed_version = {}
        for world_id in repositories.all_known_package_ids:
            available_versions = {}
            self.available_versions[world_id] = available_versions
            world_name = world_id

            for world in self.repositories.packages_by_id_version[world_id].values():
                # Note, probably we need to use actual "properties" here to get good refresh
                world_name = world.name
                #world_info['available.text'] = str(world.world_version)
                available_versions[world.world_version] = world
                self.descriptions[world_id] = world.data['metadata']['description']

            if world_id in self.repositories.local_packages_by_id:
                world = self.repositories.local_packages_by_id[world_id]
                world_name = world.name
                #world_info['installed.text'] = str(world.world_version)
                available_versions[world.world_version] = world
                self.descriptions[world_id] = world.data['metadata']['description']
                self.installed_version[world_id] = world.world_version

            if not world_name:
                # Missing data
                if w := ap_worlds.get(world_id):
                    world_name = w.game
                else:
                    world_name = world_id + ".apworld"
                world.data['metadata']['game'] = world_name

            if installed := AutoWorldRegister.world_types.get(world_name):
                if world_id not in self.installed_version:
                    self.installed_version[world_id] = installed.world_version
                else:
                    local = packaging.version.parse(self.installed_version[world_id])
                    installed = packaging.version.parse(installed.world_version)
                    if installed > local:
                        self.installed_version[world_id] = installed

            installed_version = self.installed_version.get(world_id, 'N/A')

            # Unfortunate
            self.world_name_to_id[world_name] = world_id

            max_version = max(available_versions, key=packaging.version.parse)
            world_info.append([
                world_name,
                installed_version,
                max_version,
                'Info/Set Version...',
            ])

        world_info = title_sorted(world_info, key=lambda x: x[0])
        return world_info

    def refresh(self):
        self.repositories.refresh()
        self.data_tables.update_row_data(self.data_tables, self.get_world_info())

    def do_install(self):
        print(repr(self.data_tables.get_row_checks()))
        for row in self.data_tables.get_row_checks():
            world_name = row[0]
            world_id = self.world_name_to_id[world_name]
            available_versions = self.available_versions[world_id]
            max_version = max(available_versions, key=packaging.version.parse)
            world = available_versions[max_version]
            print(f"Installing {world_name} {max_version}")
            path = os.path.join(self.repositories.apworld_cache_path, f'{world_id}_{max_version}.apworld')
            with open(path, 'wb') as f:
                response = requests.get(world.source_url)
                f.write(response.content)
            try:
                metadata_str = zipfile.ZipFile(path).read('metadata.json')
                metadata = json.loads(metadata_str)
            except KeyError:
                print("No metadata.json in ", path)
                metadata = {
                        'id': world_id,
                        'game': world_name,
                        'world_version': max_version,
                        'description': '',
                }
                with zipfile.ZipFile(path, 'a') as zf:
                    zf.writestr("metadata.json", json.dumps(metadata, indent=4))
            print("done")



    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.rows = self.get_world_info()
        self.data_tables = MDDataTable(
            use_pagination=False,
            check=True,
            column_data=[
                ("Game", dp(80)),
                ("Installed Version", dp(30)),
                ("Newest Available", dp(30)),
                ("Set Version...", dp(40)),
            ],
            row_data=self.rows,
            sorted_on="Game",
            sorted_order="ASC",
            # elevation=200,
            rows_num=10000,
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        # self.data_tables.bind(on_check_press=self.on_check_press)
        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical')
        header = MDBoxLayout(orientation='horizontal', adaptive_height=True)
        header.add_widget(MDRaisedButton(text="Refresh", on_release=lambda x: self.refresh()))

        footer = MDBoxLayout(orientation='horizontal', adaptive_height=True)

        footer.add_widget(MDRaisedButton(text="Update"))
        footer.add_widget(MDRaisedButton(text="Install", on_release=lambda x: self.do_install()))
        footer.add_widget(MDRaisedButton(text="Uninstall"))
        layout.add_widget(header)
        layout.add_widget(self.data_tables)
        layout.add_widget(footer)
        screen.add_widget(layout)

        return screen

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        col_num = index%cols_num

        cell_row = instance_table.table_data.view_adapter.get_visible_view(row_num*cols_num)

        # instance_table.background_color = self.theme_cls.primary_light
        # for id, widget in instance_row.ids.items():
        #     if id == "label":
        #         widget.color = self.theme_cls.primary_color

        # instance_row.add_widget(MDFlatButton(text="test"))
        #print(instance_table, instance_row, cell_row)
        #print(instance_row.text)
        if cols_num - 1 == col_num:
            # menu_items = [
            #     {
            #         "text": f"1.{i}.0",
            #         "viewclass": "OneLineListItem",

            #         "on_release": lambda x=f"Item {i}": print(x),
            #     } for i in range(3)
            # ]
            # MDDropdownMenu(
            #     caller=instance_row,
            #     items=menu_items,
            #     width_mult=2,
            #     opening_time=0,

            # ).open()
            from kivymd.uix.dialog import MDDialog
            from inspect import cleandoc
            world_name = cell_row.text
            world_id = self.world_name_to_id[world_name]
            available_versions = self.available_versions[world_id]

            install_text = [
                f'Install {version}' if version != self.installed_version.get(world_id, 'N/A') else f'Install {version} (Installed)' for version in available_versions
            ]
            disabled = [
                version == self.installed_version.get(world_id, 'N/A') for version in available_versions
            ]
            desc = cleandoc(self.descriptions[world_id]).replace('\n',' ')
            dialog = MDDialog(
                    type="simple",
                    # TODO: type="custom", would let us make our own buttons

                    text=f"[b]{cell_row.text}[/b]\n\n{desc}",
                    items = [
                       OneLineAvatarIconListItem(text=t, disabled=disabled[i]) for i, t in enumerate(install_text)
                    ],
                    buttons=[
                        MDRaisedButton(
                            text="Close",
                            on_release=lambda x: dialog.dismiss(force=True),
                        ),
                    ],
                    on_release=lambda x: print(x)
                )
            # dialog.add_widget(
            #         MDRaisedButton(
            #             text="v1.1.0",
            #             on_release=lambda x: dialog.dismiss(force=True))
            #     )
            dialog.open()
        # if cell_row.ids.check.state == 'normal':
        #     instance_table.table_data.select_all('normal')
        #     cell_row.ids.check.state = 'down'
        # else:
        #     cell_row.ids.check.state = 'normal'
        # instance_table.table_data.on_mouse_select(instance_row)

import asyncio


if __name__ == '__main__':
    local_dir = './worlds_test_dir'

    repositories = RepositoryManager()
    if os.path.exists(local_dir):
        repositories.add_local_dir(local_dir)
    repositories.add_remote_repository('https://raw.githubusercontent.com/zig-for/Archipelago/zig/apworld_manager/PackageLib/index.json')
    repositories.add_github_repository('https://github.com/DeamonHunter/ArchipelagoMuseDash/')
    repositories.add_github_repository('https://github.com/doshyw/CelesteArchipelago')
    # Comment this out to test refresh from nothing
    repositories.refresh()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = WorldManagerApp(repositories)

    loop.run_until_complete(app.async_run())
    loop.close()

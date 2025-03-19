import hashlib
from worlds.Files import InvalidDataError
from .world_manager import RepositoryManager, parse_version
from worlds.LauncherComponents import install_apworld
from worlds import world_sources

def launch():
    from kvui import (
        App,
        BoxLayout,
        Builder,
        Label,
        RecycleDataViewBehavior,
        RecycleView,
        TabbedPanel,
        TabbedPanelItem,
        )
    from kivy.properties import DictProperty

    try:
        from worlds.Files import APWorldContainer
    except ImportError:
        from ._vendor.world_container import APWorldContainer

    # from kivy.app import App
    # from kivy.lang import Builder
    # from kivy.properties import DictProperty
    # from kivy.uix.boxlayout import BoxLayout
    # from kivy.uix.label import Label
    # from kivy.uix.recycleview import RecycleView
    # from kivy.uix.recycleview.views import RecycleDataViewBehavior
    # from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
    kv = """
<ApworldDirectoryWindow>:
    tab_width: root.width / 2
    default_tab_text: "APWorlds"

<ApworldDirectoryItem>
    Label:
        text: root.details["title"]
        size_hint: .5, 1
    Label:
        text: root.details["description"]
        size_hint: .3, 1
    Button:
        text: root.details["install_text"]
        size_hint: .2, 1
        on_press: root.download_latest()
    Button:
        text: "Details"
        size_hint: .2, 1
        on_press: root.switch_to_detail()

<RV>:
    viewclass: 'ApworldDirectoryItem'
    RecycleBoxLayout:
        default_size: root.width, dp(30)
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<ApworldDetails>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: root.details["title"]
            size_hint: 1, 0.1
        # Label:
        #     text: root.details["description"]
        #     size_hint: 1, 0.1
        Button:
            text: root.latest_text
            size_hint: 1, 0.1
            on_press: root.download_latest()

"""
    Builder.load_string(kv)

    class DirectoryApp(App):
        tab_count = 1  # kvui for some reason monkeypatches tab_length to require this,,

        def __init__(self, *args, apworlds={}, **kwargs):
            super().__init__(*args, **kwargs)
            self.apworlds = apworlds
            from . import RepoWorld
            self.title = f'APWorld Manager {RepoWorld.world_version}'

        def build(self):
            window = ApworldDirectoryWindow()
            window.default_tab_content = RV(self.apworlds)
            return window

    class ApworldDirectoryWindow(TabbedPanel):
        def switch_to(self, header, do_scroll=False):
            if header == self.default_tab:
                self.clear_tabs()
            super().switch_to(header, do_scroll=do_scroll)

    class ApworldDetails(TabbedPanelItem):
        def __init__(self, details, *args, **kwargs):
            self.details = details
            super().__init__(*args, **kwargs)

        def download_latest(self):
            print("Downloading latest version")
            path = repositories.download_remote_world(self.details["latest_version"])
            install_apworld(path)
            app.apworlds = refresh_apworld_table()

        @property
        def latest_text(self):
            if self.details["installed"] and self.details["update_available"]:
                return f"Update available: {self.details['latest_version'].world_version}"
            elif self.details["installed"]:
                return "Up to date"
            else:
                return f"Install {self.details['latest_version'].world_version}"

    class ApworldDirectoryItem(RecycleDataViewBehavior, BoxLayout):
        details = DictProperty({"title": "game name", "description": "short description", "install_text": "N/A"})

        def refresh_view_attrs(self, rv, index, details):
            self.details = details
            super().refresh_view_attrs(rv, index, details)

        def switch_to_detail(self):
            details_tab = ApworldDetails(self.details, text=self.details["title"])
            directory_window = App.get_running_app().root
            directory_window.add_widget(details_tab)
            directory_window.switch_to(details_tab)

        def download_latest(self):
            print("Downloading latest version")
            path = repositories.download_remote_world(self.details["latest_version"])
            install_apworld(path)
            app.apworlds = refresh_apworld_table()


    class RV(RecycleView):
        def __init__(self, data, **kwargs):
            super().__init__(**kwargs)
            self.data = data

    class VersionView(RecycleView):
        def __init__(self, data, **kwargs):
            super().__init__(**kwargs)
            self.data = data

    repositories = RepositoryManager()
    repositories.load_repos_from_settings()
    repositories.refresh()

    def refresh_apworld_table():
        from worlds import AutoWorld
        register = AutoWorld.AutoWorldRegister
        apworlds = []
        installed = set()
        for name, world in register.world_types.items():
            file = world.zip_path
            if not file:
                # data = {"title": name, "description": "Unpacked World", "metadata": {"game": None}}
                # apworlds.append(data)
                continue

            container = APWorldContainer(file)
            installed.add(file.stem)
            try:
                container.read()
            except InvalidDataError as e:
                print(f"Error reading {file}: {e}")
                # continue
            manifest_data = container.get_manifest()
            remote = repositories.packages_by_id_version.get(file.stem)
            local_version = manifest_data.setdefault("world_version", "0.0.0")
            if local_version == "0.0.0":
                with open(file, 'rb') as f:
                    hash = hashlib.sha256(f.read()).hexdigest()
                if local := repositories.find_release_by_hash(hash):
                    local_version = local.world_version
            description = "Placeholder text"
            data = {"title": name, "installed": True, "manifest": manifest_data, "remotes": remote, 'update_available': False, 'install_text': '-'}
            if not remote:
                source = [s for s in world_sources if s.path == str(file)]
                if source and source[0].relative:
                    description = "Bundled with AP"
                    data['sort'] = -10
                else:
                    description = "No remote data available"
                    data['sort'] = -9
            else:
                highest_remote_version = max(remote.values(), key=lambda w: parse_version(w.world_version))
                data["latest_version"] = highest_remote_version
                v_local = parse_version(local_version)
                v_remote = parse_version(highest_remote_version.world_version)
                data['update_available'] = v_remote > v_local
                if data['update_available']:
                    description = f"Update available: {v_local} -> {v_remote}"
                    data['sort'] = 2
                    data['install_text'] = "Update"
                else:
                    description = "Up to date"
                    data['sort'] = 1
                    data['install_text'] = "-"
            data["description"] = description
            apworlds.append(data)

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
                "sort": 0,
                "install_text": "Install",
                }
            if world.lower().startswith('manual_'):
                data['sort'] = -5
            apworlds.append(data)
        apworlds.sort(key=lambda x: x['sort'], reverse=True)
        return apworlds

    apworlds = refresh_apworld_table()

    app = DirectoryApp(apworlds=apworlds)
    app.run()




if __name__ == '__main__':
    launch()

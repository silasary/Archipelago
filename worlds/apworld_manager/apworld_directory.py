import re
from Utils import Version, tuplize_version
from worlds.Files import InvalidDataError
from .world_manager import RepositoryManager


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
    default_tab_text: "Directory"

<ApworldDirectoryItem>
    Button:
        on_press: root.switch_to_detail()
        text: root.details["title"]
        size_hint: .3, 1
    Label:
        text: root.details["description"]
        size_hint: .7, 1

<RV>:
    viewclass: 'ApworldDirectoryItem'
    RecycleBoxLayout:
        default_size: root.width, dp(30)
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

# <ApworldDetails>:
#     Label:
#         id: text
"""
    Builder.load_string(kv)

    class DirectoryApp(App):
        tab_count = 1  # kvui for some reason monkeypatches tab_length to require this,,

        def __init__(self, *args, apworlds={}, **kwargs):
            super().__init__(*args, **kwargs)
            self.apworlds = apworlds

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
            super().__init__(*args, **kwargs)
            self.add_widget(Label(text=str(details)))

    class ApworldDirectoryItem(RecycleDataViewBehavior, BoxLayout):
        details = DictProperty({"title": "game name", "description": "short description"})

        def refresh_view_attrs(self, rv, index, details):
            self.details = details
            super().refresh_view_attrs(rv, index, details)

        def switch_to_detail(self):
            details_tab = ApworldDetails(self.details, text=self.details["title"])
            directory_window = App.get_running_app().root
            directory_window.add_widget(details_tab)
            directory_window.switch_to(details_tab)

    class RV(RecycleView):
        def __init__(self, data, **kwargs):
            super().__init__(**kwargs)
            self.data = data

    repositories = RepositoryManager()
    repositories.load_repos_from_settings()
    repositories.refresh()

    from worlds import AutoWorld, world_sources
    register = AutoWorld.AutoWorldRegister
    apworlds = []
    installed = set()
    for name, world in register.world_types.items():
        file = world.zip_path
        if not file:
            # data = {"title": name, "description": world.__doc__ if False else "Placeholder text", "metadata": {"game": None}}
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
        local_version = manifest_data.get("world_version", Version(0, 0, 0))
        description = "Placeholder text"
        if not remote:
            description = "No remote data available"
        else:
            highest_remote_version = sorted(remote.values(), key=lambda x: x.version_tuple)[-1]
            manifest_data["latest_version"] = highest_remote_version
            manifest_data['update_available'] = highest_remote_version.version_tuple > local_version
            if manifest_data['update_available']:
                description = "Update available"
            else:
                description = "Up to date"

        data = {"title": name, "description": description, "manifest": manifest_data, "installed": True}
        apworlds.append(data)

    for world in repositories.all_known_package_ids:
        if world in installed:
            continue
        remote = repositories.packages_by_id_version.get(world)
        if not remote:
            continue
        highest_remote_version = sorted(remote.values(), key=lambda x: x.version_tuple)[-1]
        data = {"title": world, "description": "Available to install", "manifest": {"latest_version": highest_remote_version, "update_available": True}, "installed": False}
        apworlds.append(data)

    app = DirectoryApp(apworlds=apworlds)
    app.run()


if __name__ == '__main__':
    launch()

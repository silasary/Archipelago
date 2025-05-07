from .world_manager import refresh_apworld_table, repositories
from worlds.LauncherComponents import install_apworld


def launch():
    import kvui  # noqa
    from kivy.properties import DictProperty

    from kivy.app import App
    from kivy.lang import Builder
    # from kivy.properties import DictProperty
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.recycleview import RecycleView
    from kivy.uix.recycleview.views import RecycleDataViewBehavior
    from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
    from kivy.uix.popup import Popup
    from kivy.core.window import Window

    # I do not like this, but kivyMD messageboxes don't work with non-MD Apps, so we'll backport the original messagebox so install_apworld can use it
    class MessageBox(Popup):
        class MessageBoxLabel(Label):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self._label.refresh()
                self.size = self._label.texture.size
                if self.width + 50 > Window.width:
                    self.text_size[0] = Window.width - 50
                    self._label.refresh()
                    self.size = self._label.texture.size

        def __init__(self, title, text, error=False, **kwargs):
            label = MessageBox.MessageBoxLabel(text=text)
            separator_color = [217 / 255, 129 / 255, 122 / 255, 1.] if error else [47 / 255., 167 / 255., 212 / 255, 1.]
            super().__init__(title=title, content=label, size_hint=(None, None), width=max(100, int(label.width) + 40),
                            separator_color=separator_color, **kwargs)
            self.height += max(0, label.height - 18)

    kvui.MessageBox = MessageBox

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
        disabled: root.details["install_text"] == "-"
    # Button:
    #     text: "Details"
    #     size_hint: .2, 1
    #     on_press: root.switch_to_detail()

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

    repositories.load_repos_from_settings()
    repositories.refresh()



    apworlds = refresh_apworld_table()

    app = DirectoryApp(apworlds=apworlds)
    app.run()


if __name__ == '__main__':
    launch()

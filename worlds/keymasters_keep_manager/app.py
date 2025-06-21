import hashlib
import pathlib

import requests

from typing import Any, Dict, List, Optional

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget

from Utils import user_path


class GameImplementationLayout(BoxLayout):
    game_implementation_key: str
    data: Dict[str, Any]

    state_button: Button
    download_button: Button

    def __init__(self, game_implementation_key: str, data: Dict[str, Any]) -> None:
        super().__init__(orientation="horizontal", size_hint_y=None, height="40dp", spacing="8dp")

        self.game_implementation_key = game_implementation_key
        self.data = data

        self.state_button = Button(
            text=self.data["states"][self.game_implementation_key],
            width="150dp",
            size_hint_x=None,
            halign="left",
            disabled=True,
        )

        self.add_widget(self.state_button)

        self.download_button = Button(
            text="Download",
            width="88dp",
            size_hint_x=None,
            halign="left",
            disabled=False,
        )

        self.download_button.bind(on_press=self.on_download_button_press)

        self.add_widget(self.download_button)

        name: str = self.data["remote"][self.game_implementation_key]["name"]
        repository: str = self.data["remote"][self.game_implementation_key]["repository"]

        name_label: Label = Label(
            text=f"[b]{name}[/b]\n[color=bbbbbb]{repository}[/color]",
            markup=True,
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        name_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(Widget(width="8dp", size_hint_x=None))
        self.add_widget(name_label)

    def on_download_button_press(self, _) -> None:
        self.download_button.disabled = True

        try:
            download_url: str = self.data["download_urls"][self.game_implementation_key]
            response: requests.Response = requests.get(download_url)

            if response.status_code == 200:
                keymasters_keep_downloads_path: str = user_path("keymasters_keep", "downloads")

                file_path: pathlib.Path = pathlib.Path(
                    keymasters_keep_downloads_path, self.data["remote"][self.game_implementation_key]["name"]
                )

                with open(file_path, "wb") as f:
                    f.write(response.content)

                self.state_button.text = "Downloaded"
            else:
                self.state_button.text = "Error"
        except Exception:
            self.state_button.text = "Error"

        self.download_button.disabled = False


class GameImplementationsLayout(ScrollView):
    data: Dict[str, Any]
    layout: BoxLayout

    game_implementation_layouts: Dict[str, GameImplementationLayout]

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(size_hint=(0.7, 1.0))

        self.data = data

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing="4dp")
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.layout.add_widget(Widget(height="16dp"))

        self.game_implementation_layouts = dict()

        key: str
        for key in self.data.get("sorted_keys", list()):
            game_implementation_layout: GameImplementationLayout = GameImplementationLayout(key, self.data)

            self.game_implementation_layouts[key] = game_implementation_layout
            self.layout.add_widget(game_implementation_layout)

        self.layout.add_widget(Widget(height="16dp"))

        self.add_widget(self.layout)


class KeymastersKeepManager(App):
    base_title: str = "Keymaster's Keep Manager"
    data: Optional[Dict[str, Any]] = None

    tab_panel: TabbedPanel

    layout: BoxLayout
    layout_game_implementations: GameImplementationsLayout

    def __init__(self) -> None:
        self.title = self.base_title
        super().__init__()

    def build(self) -> BoxLayout:
        self.update_data()

        self.tab_panel = TabbedPanel(
            default_tab_text="Game Implementations",
            tab_width="200dp",
        )

        self.layout = BoxLayout(orientation="horizontal", spacing="16dp", padding=["8dp", "0dp"])
        self.layout_game_implementations = GameImplementationsLayout(self.data)
        self.layout.add_widget(self.layout_game_implementations)

        self.tab_panel.default_tab.content = self.layout

        return self.tab_panel

    def update_data(self) -> None:
        # Local game implementations
        keymasters_keep_path: str = user_path("keymasters_keep")

        local_game_implementation_files: Dict[str, str] = dict()

        file_path: pathlib.Path
        for file_path in pathlib.Path(keymasters_keep_path).glob("*.py"):
            if file_path.name == "__init__.py":
                continue

            file_size: int = file_path.stat().st_size
            hasher: hashlib.sha1 = hashlib.sha1()

            header = f"blob {file_size}\0".encode("utf-8")
            hasher.update(header)

            content: bytes = file_path.read_bytes()
            hasher.update(content)

            local_game_implementation_files[file_path.name] = hasher.hexdigest()

        # Remote game implementations
        repositories_file_path: str = user_path("keymasters_keep", "repositories.txt")

        repositories: List[str]

        with open(repositories_file_path, "r") as f:
            repositories = [line.strip() for line in f.readlines()]

        remote_game_implementation_files: Dict[str, Dict[str, Any]] = dict()
        download_urls: Dict[str, str] = dict()
        states: Dict[str, str] = dict()

        repository: str
        for repository in repositories:
            url = f"https://api.github.com/repos/{repository}/git/trees/main?recursive=1"

            try:
                response: requests.Response = requests.get(url)

                if response.status_code == 200:
                    data: Dict[str, Any] = response.json()

                    file_entry: Dict[str, Any]
                    for file_entry in data.get("tree", list()):
                        file_name: str = file_entry["path"].split("/")[-1]

                        if file_name.endswith(".py") and file_name != "__init__.py":
                            file_key: str = f"{file_name} - {repository}"

                            remote_game_implementation_files[file_key] = {
                                "name": file_name,
                                "repository": repository,
                                "path": file_entry["path"],
                                "hash": file_entry["sha"],
                            }

                            download_urls[file_key] = f"https://raw.githubusercontent.com/{repository}/main/{file_entry['path']}"

                            state: str = "Not Installed"

                            if file_name in local_game_implementation_files:
                                if local_game_implementation_files[file_name] == file_entry["sha"]:
                                    state = "Installed - Matches"
                                else:
                                    state = "Installed - Differs"

                            states[file_key] = state
            except Exception:
                continue

        self.data = {
            "local": local_game_implementation_files,
            "remote": remote_game_implementation_files,
            "download_urls": download_urls,
            "states": states,
            "sorted_keys": sorted(remote_game_implementation_files.keys()),
        }


def main() -> None:
    KeymastersKeepManager().run()

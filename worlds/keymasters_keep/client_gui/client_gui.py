from typing import List, Tuple

from kvui import GameManager

from kivy.uix.layout import Layout

from ..client import KeymastersKeepContext

from .client_gui_layouts import KeymastersKeepTabLayout, TrialsTabLayout, TrialsCompletedTabLayout


class KeymastersKeepManager(GameManager):
    ctx: KeymastersKeepContext

    logging_pairs: List[Tuple[str, str]] = [("Client", "Archipelago")]
    base_title: str = "Archipelago Keymaster's Keep Client"

    keymasters_keep_tab_layout: KeymastersKeepTabLayout
    trials_tab_layout: TrialsTabLayout
    trials_completed_tab_layout: TrialsCompletedTabLayout

    def build(self) -> Layout:
        container: Layout = super().build()

        self.keymasters_keep_tab_layout = KeymastersKeepTabLayout(self.ctx)
        self.add_client_tab("Keymaster's Keep", self.keymasters_keep_tab_layout)

        self.trials_tab_layout = TrialsTabLayout(self.ctx)
        self.available_trials_tab = self.add_client_tab("Available Trials", self.trials_tab_layout)

        self.trials_completed_tab_layout = TrialsCompletedTabLayout(self.ctx)
        self.add_client_tab("Completed Trials", self.trials_completed_tab_layout)

        return container

    def update_tabs(self) -> None:
        self.keymasters_keep_tab_layout.update()
        self.trials_tab_layout.update()
        self.trials_completed_tab_layout.update()

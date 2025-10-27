from __future__ import annotations

from dataclasses import dataclass

from Options import OptionError, OptionSet

from ..enums import KeymastersKeepGamePlatforms
from ..game import Game
from ..game_objective_template import GameObjectiveTemplate


@dataclass
class CustomArchipelagoOptions:
    custom_objective_list: CustomObjectiveList


class CustomGame(Game):
    name = "Custom"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = CustomArchipelagoOptions

    def optional_game_constraint_templates(self) -> list[GameObjectiveTemplate]:
        return []

    def game_objective_templates(self) -> list[GameObjectiveTemplate]:
        if not self.objectives():
            raise OptionError("Custom (META) was selected, but custom_objective_list was empty.")

        return [
            GameObjectiveTemplate(
                label="OBJECTIVE",
                data={"OBJECTIVE": (self.objectives, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    def objectives(self) -> list[str]:
        return sorted(self.archipelago_options.custom_objective_list.value)


# Archipelago Options
class CustomObjectiveList(OptionSet):
    """
    A freeform list of custom objectives for Keymaster's Keep. The trials will sample directly from this list.
    """

    display_name = "Custom Challenge List"
    default = [
        "Custom Challenge 1",
        "Custom Challenge 2",
        "...",
    ]


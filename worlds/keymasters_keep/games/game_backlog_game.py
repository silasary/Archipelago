from __future__ import annotations

from dataclasses import dataclass

from Options import OptionError, OptionSet

from ..enums import KeymastersKeepGamePlatforms
from ..game import Game
from ..game_objective_template import GameObjectiveTemplate


@dataclass
class GameBacklogArchipelagoOptions:
    game_backlog_game_selection: GameBacklogGameSelection
    game_backlog_actions: GameBacklogActions


class GameBacklogGame(Game):
    name = "Game Backlog"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = GameBacklogArchipelagoOptions

    def optional_game_constraint_templates(self) -> list[GameObjectiveTemplate]:
        return []

    def game_objective_templates(self) -> list[GameObjectiveTemplate]:
        if not self.games():
            raise OptionError("Game Backlog (META) was selected, but game_backlog_game_selection was empty.")
        if not self.actions():
            raise OptionError("Game Backlog (META) was selected, but game_backlog_actions was empty.")

        return [
            GameObjectiveTemplate(
                label="ACTION GAME",
                data={"ACTION": (self.actions, 1), "GAME": (self.games, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    def actions(self) -> list[str]:
        return sorted(self.archipelago_options.game_backlog_actions.value)

    def games(self) -> list[str]:
        return sorted(self.archipelago_options.game_backlog_game_selection.value)


# Archipelago Options
class GameBacklogGameSelection(OptionSet):
    """
    Defines which games are in the player's backlog.

    Replace the placeholders with values of your own choosing.
    """

    display_name = "Game Backlog Game Selection"

    default = ["Game 1", "Game 2", "..."]


class GameBacklogActions(OptionSet):
    """
    Defines the possible actions that could be required on a game in the backlog.

    You can customize this list to your liking.
    """

    display_name = "Game Backlog Actions"

    default = [
        "TRY",
        "FINISH",
        "COMPLETE",
    ]

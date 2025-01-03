from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class FourteenMinesweeperVariantsArchipelagoOptions:
    pass


class FourteenMinesweeperVariantsGame(Game):
    name = "14 Minesweeper Variants"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = FourteenMinesweeperVariantsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete SIZE VARIANT board",
                data={
                    "SIZE": (self.sizes, 1),
                    "VARIANT": (self.variants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def sizes() -> List[str]:
        return [
            "a 5x5",
            "a 6x6",
            "a 7x7",
            "an 8x8",
        ]

    @staticmethod
    def variants() -> List[str]:
        return [
            "[V] Vanilla",
            "[Q] Quad",
            "[C] Connected",
            "[T] Triplet",
            "[O] Outside",
            "[D] Dual",
            "[S] Snake",
            "[B] Balance",
            "[M] Multiple",
            "[L] Liar",
            "[W] Wall",
            "[N] Negation",
            "[X] Cross",
            "[P] Partition",
            "[E] Eyesight",
            "[#] Double Rules",
        ]


# Archipelago Options
# ...

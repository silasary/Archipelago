from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass  # no options, is this needed???
class InsaniquariumOptions:
    pass


class InsaniquariumGame(Game):
    # Initial implementation by RoobyRoo. Adapted from Guitar Hero by JCBoorgo

    name = "Insaniquarium Deluxe"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.AND,
    ]

    is_adult_only_or_unrated = False

    options_cls = InsaniquariumOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()
    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete Tank LEVEL with the following pets: PETS",
                data={
                    "LEVEL": (self.level, 1),
                    "PETS": (self.pets, 3)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1
            )
        ]

    @functools.cached_property
    def level(self) -> List[str]:
        return [
            "1-1",
            "1-2",
            "1-3",
            "1-4",
            "1-5",
            "2-1",
            "2-2",
            "2-3",
            "2-4",
            "2-5",
            "3-1",
            "3-2",
            "3-3",
            "3-4",
            "3-5",
            "4-1",
            "4-2",
            "4-3",
            "4-4",
            "4-5"
        ]
    
    @functools.cached_property
    def pets(self) -> List[str]:
        return [
            "Stinky",
            "Niko",
            "Itchy",
            "Prego",
            "Zorf",
            "Clyde",
            "Vert",
            "Rufus",
            "Meryl",
            "Wadsworth",
            "Seymour",
            "Shrapnel",
            "Gumbo",
            "Blip",
            "Rhubarb",
            "Nimbus",
            "Amp",
            "Gash",
            "Angie",
            "Presto",
            "Brinkley",
            "Nostradamus",
            "Stanley",
            "Walter"
        ]


# Archipelago Options - none needed

from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RhythmHeavenFeverArchipelagoOptions:
    pass


class RhythmHeavenFeverGame(Game):
    name = "Rhythm Heaven Fever"
    platform = KeymastersKeepGamePlatforms.WII

    platforms_other = [
        KeymastersKeepGamePlatforms.WIIU,
    ]

    is_adult_only_or_unrated = False

    options_cls = RhythmHeavenFeverArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Get RESULT in LEVEL",
                data={
                    "RESULT": (self.results, 1),
                    "LEVEL": (self.levels + "Night Walk", 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]
        if self.allow_perfect:
            templates.extend([
                GameObjectiveTemplate(
                    label="Get RESULT in LEVEL",
                    data={
                        "RESULT": (self.results + "Perfect", 1),
                        "LEVEL": (self.levels, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])
        return templates

    @staticmethod
    def results() -> List[str]:
        return [
            "OK or better",
            "Superb or better",
        ]

    @staticmethod
    def levels() -> List[str]:
        return [
            "Hole In One",
            "Screwbot Factory",
            "See-Saw",
            "Double Date",
            "Remix 1",
            "Fork Lifter",
            "Tambourine",
            "Board Meeting",
            "Monkey Watch",
            "Remix 2",
            "Working Dough",
            "Built to Scale",
            "Air Rally",
            "Figure Fighter",
            "Remix 3",
            "Ringside",
            "Packing Pests",
            "Micro-Row",
            "Samurai Slice",
            "Remix 4",
            "Catch of the Day",
            "Flipper-Flop",
            "Exhibition Match",
            "Flock Step",
            "Remix 5",
            "Launch Party",
            "Donk-Donk",
            "Bossa Nova",
            "Love Rap",
            "Remix 6",
            "Tap Troupe",
            "Shrimp Shuffle",
            "Cheer Readers",
            "Karate Man",
            "Remix 7",
            "Samurai Slice 2",
            "Working Dough 2",
            "Built to Scale 2",
            "Double Date 2",
            "Remix 8",
            "Love Rap 2",
            "Cheer Readers 2",
            "Hole in One 2",
            "Screwbot Factory 2",
            "Remix 9",
            "Figure Fighter 2",
            "Micro-Row 2",
            "Packing Pests 2",
            "Karate Man 2",
            "Remix 10",
        ]
        
    @property
    def allow_perfect(self) -> bool:
        return "True" in self.archipelago_options.allow_perfects.value

# Archipelago Options
class RhythmHeavenFeverPerfectsEnabled(OptionSet):
    """
    Allows the player to choose whether they want to have to get Perfect grades, done by waiting for the game to offer the opportunity to do so.
    """

    display_name = "Allow Perfects"
    valid_keys = [
        "True",
        "False",
    ]

    default = "False"

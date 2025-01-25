from __future__ import annotations
from typing import List
from dataclasses import dataclass

from Options import OptionSet
from ..game import Game
from ..game_objective_template import GameObjectiveTemplate
from ..enums import KeymastersKeepGamePlatforms

@dataclass
class DeadByDaylightArchipelagoOptions:
    dead_by_daylight_killers: DeadByDaylightKillers
    dead_by_daylight_survivors: DeadByDaylightSurvivors


class DeadByDaylightGame(Game):
    name = "Dead By Daylight"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = True

    options_cls = DeadByDaylightArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Escape as the last Survivor or earn Merciless Killer without using any Perks",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Earn 4 Iridescent Emblems",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As KILLERSOWNED earn Merciless Killer",
                data={
                    "KILLERSOWNED": (self.killers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As KILLERSOWNED sacrifice 2 Survivors without any addons",
                data={
                    "KILLERSOWNED": (self.killers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As KILLERSOWNED down every Survivor at least once before using your power",
                data={
                    "KILLERSOWNED": (self.killers, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Grab 2 Survivors either from off a generator or out of a locker",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete MEDIUM Generators by yourself",
                data={
                    "MEDIUM": (self.medium_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Heal MEDIUM other Survivors",
                data={
                    "MEDIUM": (self.medium_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Escape 2 games in a row",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Using only SURVIVORSOWNED's perks, escape",
                data={
                    "SURVIVORSOWNED": (self.survivors_all, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    def killers(self) -> List[str]:
        return sorted(self.archipelago_options.dead_by_daylight_killers.value)

    def survivors(self) -> List[str]:
        return sorted(self.archipelago_options.dead_by_daylight_survivors.value)

    @staticmethod
    def survivors_all() -> List[str]:
        return [
            "Laurie", "Ace", "Bill", "Feng Min", "David", "Quentin", "Tapp", "Kate", "Adam", "Jeff",
            "Jane", "Ash", "Nancy", "Steve", "Yui", "Zarina", "Cheryl", "Felix", "Elodie", "Yun-Jin",
            "Jill", "Leon", "Mikaela", "Jonah", "Yoichi", "Haddie", "Ada", "Rebecca", "Vittorio", "Thalita",
            "Renato", "Gabriel", "Nicolas", "Ellen", "Alan", "Sable", "Aestri", "Lara", "Trevor"
        ]

    @staticmethod
    def killers_all() -> List[str]:
        return [
            "Trapper", "Wraith", "Hillbilly", "Nurse", "Huntress", "Michael Myers", "Hag", "Doctor",
            "Leatherface", "Freddy Krueger", "Amanda Young", "Clown", "Spirit", "Legion", "Plague", "Ghost Face",
            "Demogorgan", "Oni", "Deathslinger", "Pyramid Head", "Blight", "Twins", "Trickster", "Nemesis",
            "Pinhead", "Artist", "Sadako", "Dredge", "Albert Wesker", "Knight", "Skull Merchant", "Singularity",
            "Xenomorph", "Chucky", "Unknown", "Vecna", "Dracula", "Houndmaster",
        ]

    @staticmethod
    def medium_range() -> range:
        return range(2, 3)


# Archipelago Options using OptionSet
class DeadByDaylightKillers(OptionSet):
    """
    Indicates which Killers the player has access to.
    """
    display_name = "Dead By Daylight Killers Unlocked"
    valid_keys = DeadByDaylightGame().killers_all()
    default = valid_keys


class DeadByDaylightSurvivors(OptionSet):
    """
    Indicates which Survivors the player has access to, thus what perks they also have access to.
    """
    display_name = "Dead By Daylight Survivors Unlocked"
    valid_keys = DeadByDaylightGame().survivors_all()
    default = valid_keys

from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SaltAndSacrificeArchipelagoOptions:
    pass


class SaltAndSacrificeGame(Game):
    name = "Salt and Sacrifice"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = SaltAndSacrificeArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Cannot use these Weapon Types: WEAPONTYPE",
                data={
                    "WEAPONTYPE": (self.weapontype, 5),
                },
                ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat a Mage in WORLDS",
                data={"WORLDS": (self.worlds, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat ALTARSTONEBOSSES in the Heart of Altarstone",
                data={"ALTARSTONEBOSSES": (self.altarstonebosses, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat DREADSTONEBOSSES in Dreadstone Peak",
                data={"DREADSTONEBOSSES": (self.dreadstonebosses, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat ELDERCOPSEBOSSES in Elder's Copse",
                data={"ELDERCOPSEBOSSES": (self.eldercopsebosses, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat ASHBOURNEBOSSES in Corvius Mire",
                data={"ASHBOURNEBOSSES": (self.ashbournebosses, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat ANYBOSS using WEAPONTYPE",
                data={"WEAPONTYPE": (self.weapontype(), 1), "ANYBOSS": (self.anyboss(), 1)}
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat ANYBOSS using a weapon you aren't proficient with",
                data={"ANYBOSS": (self.anyboss(), 1)}
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Locate the TOOLS and pick it up",
                data={"TOOLS": (self.tools(), 1)}
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
        ]

    @staticmethod
    def worlds() -> List[str]:
        return [
            "Ashbourne Village",
            "Bol Gerahn",
            "Corvius Mire",
            "Dreadstone Peak",
            "The Elder Copse",
            "Hallowed HIll",
            "Heart of Altarstone",
        ]

    @staticmethod
    def altarstonebosses() -> List[str]:
        return [
            "The Keeper and the Kin",
            "Shirenna, True Herbalist",
            "The Four Divines",
            "Barix, First of the Marked",
        ]

    @staticmethod
    def eldercopsebosses() -> List[str]:
        return [
            "Kinetomancer Parxa Krass",
            "Bibliomancer Logostus Rime",
            "Icon of Pandemonium",
            "The Worm That Does Not Die",
            "Inquisitor Amben",
            "The Undone Sacrifice",
        ]

    @staticmethod
    def bolbosses() -> List[str]:
        return [
            "Neuromancer Zyzak Zuun",
            "Chronomancer Zaruman Tam",
            "Dracomancer Draeaxenerion",
            "Diablomancer Nephael Mos",
            "Umbramancer Vodin Tenebre",
            "The Two That Remain",
            "Inquisitor Selet",
            "Kraeaxenar, Wyrm of the Sky",
        ]

    @staticmethod
    def ashbournebosses() -> List[str]:
        return [
            "Pyromancer Arzhan Tin",
            "Cryomancer Celus Zend",
            "Hydromancer Kundry Kahn",
            "Venomancer Varren Ovrin",
            "Electromancer Ekriks Greycloud",
            "Uryks Necklace-of-Ears",
            "The Green Huntsman",
        ]

    @staticmethod
    def anyboss() -> List[str]:
        return [
            "Pyromancer Arzhan Tin",
            "Cryomancer Celus Zend",
            "Hydromancer Kundry Kahn",
            "Venomancer Varren Ovrin",
            "Electromancer Ekriks Greycloud",
            "Uryks Necklace-of-Ears",
            "The Green Huntsman",
            "Neuromancer Zyzak Zuun",
            "Chronomancer Zaruman Tam",
            "Dracomancer Draeaxenerion",
            "Diablomancer Nephael Mos",
            "Umbramancer Vodin Tenebre",
            "The Two That Remain",
            "Inquisitor Selet",
            "Kraeaxenar, Wyrm of the Sky",
            "Kinetomancer Parxa Krass",
            "Bibliomancer Logostus Rime",
            "Icon of Pandemonium",
            "The Worm That Does Not Die",
            "Inquisitor Amben",
            "The Undone Sacrifice",
            "The Keeper and the Kin",
            "Shirenna, True Herbalist",
            "The Four Divines",
            "Barix, First of the Marked",
        ]

    @staticmethod
    def weapontype() -> List[str]:
        return [
            "Bludgeons",
            "Glaives",
            "Greatblades",
            "Greathammers",
            "Halfspears",
            "Highblades",
            "Rapiers",
            "Sickles",
            "Staves",
            "Twindaggers",
            "Twohanders",
            "Vanguards",
            "Whips",
            "Channeling Rods",
            "Crossbows",
            "Shortbows",
            "Divine Glyphs (Prayer)", # The distinction between the two magics are important, as they required skills to use.
            "Forbidden Glyphs (Arcane)",
            "Thrown Weapons", # Includes Axes, Daggers, and other objects under the Thrown class.
        ]

    @staticmethod
    def tools() -> List[str]:
        return [
            "Grappling Hook", # Ashbourne Village
            "Magnesin Supply", # Bol Gerahn
            "Luminstone", # Corvius' Mire
            "Ethercloth Bolt", # Dreadstone Peak
        ]

# Archipelago Options
# ...

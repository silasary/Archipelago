from __future__ import annotations

from typing import List, Set

from dataclasses import dataclass

# from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms



@dataclass
class StarWarsBattlefrontIIClassicArchipelagoOptions:
    # star_wars_battlefront_ii_classic_custom_maps: StarWarsBattlefrontIIClassicCustomMaps
    pass


class StarWarsBattlefrontIIClassicGame(Game):
    # Initial Proposal by @theroadkill on Discord

    name = "Star Wars: Battlefront II (Classic)"
    options_cls = StarWarsBattlefrontIIClassicArchipelagoOptions
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS2,
        KeymastersKeepGamePlatforms.PSP,
        KeymastersKeepGamePlatforms.XBOX,
    ]

    is_adult_only_or_unrated = False

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Heroes disabled",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Soldier class prohibited",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Switch classes after every death",
                data=dict(),
            )
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a MODE_GROUND match on MAP_GROUND_GCW as FACTIONS_GCW with AI_DIFFICULTY",
                data={
                    "MODE_GROUND": (self.modes_ground, 1),
                    "MAP_GROUND_GCW": (self.maps_ground_gcw, 1),
                    "FACTIONS_GCW": (self.factions_gcw, 1),
                    "AI_DIFFICULTY": (self.ai_difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a MODE_SPACE match on MAP_SPACE_GCW as FACTIONS_GCW with AI_DIFFICULTY",
                data={
                    "MODE_SPACE": (self.modes_space, 1),
                    "MAP_SPACE_GCW": (self.maps_space_gcw, 1),
                    "FACTIONS_GCW": (self.factions_gcw, 1),
                    "AI_DIFFICULTY": (self.ai_difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a MODE_GROUND match on MAP_GROUND_CW as FACTIONS_CW with AI_DIFFICULTY",
                data={
                    "MODE_GROUND": (self.modes_ground, 1),
                    "MAP_GROUND_CW": (self.maps_ground_cw, 1),
                    "FACTIONS_CW": (self.factions_cw, 1),
                    "AI_DIFFICULTY": (self.ai_difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a MODE_SPACE match on MAP_SPACE_CW as FACTIONS_CW with AI_DIFFICULTY",
                data={
                    "MODE_SPACE": (self.modes_ground, 1),
                    "MAP_SPACE_CW": (self.maps_ground_cw, 1),
                    "FACTIONS_CW": (self.factions_cw, 1),
                    "AI_DIFFICULTY": (self.ai_difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win consecutive MODE_GROUND matches on MAP_GROUND_GCW as FACTIONS_GCW with AI_DIFFICULTY",
                data={
                    "MODE_GROUND": (self.modes_ground, 1),
                    "MAP_GROUND_GCW": (self.maps_ground_gcw, 3),
                    "FACTIONS_GCW": (self.factions_gcw, 1),
                    "AI_DIFFICULTY": (self.ai_difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win consecutive MODE_GROUND matches on MAP_GROUND_CW as FACTIONS_CW with AI_DIFFICULTY",
                data={
                    "MODE_GROUND": (self.modes_ground, 1),
                    "MAP_GROUND_CW": (self.maps_ground_cw, 3),
                    "FACTIONS_CW": (self.factions_cw, 1),
                    "AI_DIFFICULTY": (self.ai_difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Hero Assault game on MAP_HERO_ASSAULT_WITH_FACTION with AI_DIFFICULTY",
                data={
                    "MAP_HERO_ASSAULT_WITH_FACTION": (self.maps_hero_assault_with_faction, 1),
                    "AI_DIFFICULTY": (self.ai_difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Hunt game on MAP_HUNT_WITH_FACTION with AI_DIFFICULTY (Timer: OFF, Score Limit: 75)",
                data={
                    "MAP_HUNT_WITH_FACTION": (self.maps_hunt_with_faction, 1),
                    "AI_DIFFICULTY": (self.ai_difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win Galactic Conquest - GAME_GALACTIC_CONQUEST",
                data={
                    "GAME_GALACTIC_CONQUEST": (self.games_galactic_conquest, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def modes_ground() -> List[str]:
        return [
            "Conquest",
            "CTF",
        ]

    @staticmethod
    def modes_space() -> List[str]:
        return [
            "Assault",
            "CTF",
        ]

    @staticmethod
    def maps_ground_gcw() -> List[str]:
        # TODO: Add custom maps from options?

        return [
            "Coruscant: Jedi Temple",
            "Dagobah: Swamp",
            "Death Star: Interior",
            "Endor: Bunker",
            "Felucia: Marshland",
            "Hoth: Echo Base",
            "Kamino: Cloning Facility",
            "Kashyyyk: Beachhead",
            "Mustafar: Refinery",
            "Mygeeto: War-Torn City",
            "Naboo: Theed",
            "Polis Massa: Medical Facility",
            "Tantive IV: Interior",
            "Tatooine: Jabba's Palace",
            "Tatooine: Mos Eisley",
            "Utapau: Sinkhole",
            "Yavin 4: Temple",
        ]

    @staticmethod
    def maps_ground_cw() -> List[str]:
        # TODO: Add custom maps from options?

        return [
            "Coruscant: Jedi Temple",
            "Dagobah: Swamp",
            "Death Star: Interior",
            "Felucia: Marshland",
            "Geonosis: Dust Plains",
            "Kamino: Cloning Facility",
            "Kashyyyk: Beachhead",
            "Mustafar: Refinery",
            "Mygeeto: War-Torn City",
            "Naboo: Theed",
            "Polis Massa: Medical Facility",
            "Tantive IV: Interior",
            "Tatooine: Jabba's Palace",
            "Tatooine: Mos Eisley",
            "Utapau: Sinkhole",
            "Yavin 4: Temple",
        ]

    @staticmethod
    def maps_hero_assault_with_faction() -> List[str]:
        return [
            "Tatooine: Mos Eisley as Heroes",
            "Tatooine: Mos Eisley as Villains",
        ]

    @staticmethod
    def maps_hunt_with_faction() -> List[str]:
        # TODO: Add custom maps from options?

        return [
            "Endor: Bunker as Ewoks",
            "Endor: Bunker as Scout Troopers",
            "Geonosis: Dust Plains as Geonosians",
            "Geonosis: Dust Plains as Clone Sharpshooters",
            "Hoth: Echo Base as Wampa",
            "Hoth: Echo Base as Rebels",
            "Kashyyyk: Beachhead as Wookiees",
            "Kashyyyk: Beachhead as MagnaGuards",
            "Naboo: Theed as Gungans",
            "Naboo: Theed as Super Battle Droids",
            "Tatooine: Mos Eisley as Jawas",
            "Tatooine: Mos Eisley as Tusken Raiders",
        ]

    @staticmethod
    def maps_space_gcw() -> List[str]:
        # TODO: Add custom maps from options?

        return [
            "Space Hoth",
            "Space Tatooine",
            "Space Yavin",
        ],

    @staticmethod
    def maps_space_cw() -> List[str]:
        # TODO: Add custom maps from options?

        return [
            "Space Felucia",
            "Space Kashyyyk",
            "Space Mygeeto",
        ]

    @staticmethod
    def factions_gcw() -> List[str]:
        return [
            "Empire",
            "Rebels",
        ]

    @staticmethod
    def factions_cw() -> List[str]:
        return [
            "CIS",
            "Republic",
        ]

    @staticmethod
    def ai_difficulties() -> List[str]:
        return [
            "Normal AI",
            "Elite AI",
        ]

    @staticmethod
    def games_galactic_conquest() -> List[str]:
        return [
            "Birth of the Rebellion",
            "Dark Reign of the Empire",
            "Republic Sovereignty",
            "The Confederate Uprising",
        ]

    # @property
    # def custom_maps(self) -> Set[str]:
    #     return self.archipelago_options.star_wars_battlefront_ii_classic_custom_maps.value


# Archipelago Options
# class StarWarsBattlefrontIIClassicCustomMaps(OptionSet):
#     """
#     Defines the custom maps available for Star Wars Battlefront II (Classic).
#     """
#
#     display_name = "Star Wars Battlefront II (Classic) Custom Maps"
#     default = list()

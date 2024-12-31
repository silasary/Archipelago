from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MarioParty2KeymastersKeepOptions:
    pass

class MarioParty2Game(Game):
    name = "Mario Party 2"
    platform = KeymastersKeepGamePlatforms.N64

    # Virtual Console and Nintendo Online re-releases
    platforms_other = [
        KeymastersKeepGamePlatforms.WII,
        KeymastersKeepGamePlatforms.WIIU,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = MarioParty2KeymastersKeepOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Never use a ITEM", # All items start with a consonant
                data={"ITEM": (self.items, 1)},
                is_time_consuming=True, # All board objectives are time-consuming, and this only affects those
                weight=10
            ),
            GameObjectiveTemplate(
                label="Set the Computer Character skill levels individually in the following order: SKILLS",
                data={"SKILLS": (self.skill_levels_duplicated, 3)},
                weight=10
            ),
            GameObjectiveTemplate(
                label="Set the Computer Character skill levels all the same to SKILL",
                data={"SKILL": (self.skill_levels, 1)},
                is_difficult=True, # Only because this could land on all Hard
                weight=5
            ),
            GameObjectiveTemplate(
                label="Do not use any items",
                data={},
                is_difficult=True,
                is_time_consuming=True, # All board objectives are time-consuming, and this only affects those
                weight=1
            ),
            GameObjectiveTemplate(
                label="Say no the first time you are offered a Star in a board",
                data={},
                is_difficult=True,
                is_time_consuming=True, # All board objectives are time-consuming, and this only affects those
                weight=1
            ),
            GameObjectiveTemplate(
                label="For all Mini-Game objectives, include at least one Computer Player not on your team set"
                      " to Super Hard",
                data={},
                is_difficult=True,
                weight=1
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return ([
            GameObjectiveTemplate(
                label="Win a TURNS turn game on BOARD with Bonus Stars TOGGLE",
                data={"TURNS": (self.board_turn_counts, 1), "BOARD": (self.boards, 1), "TOGGLE": (self.off_on, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Win a TURNS turn Trial in Mini-Game Stadium",
                data={"TURNS": (self.minigame_trial_turn_counts, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a WINCOUNT-Win GAMEMODE Battle in Mini-Game Stadium",
                data={"WINCOUNT": (self.minigame_battle_counts, 1), "GAMEMODE": (self.base_minigame_categories, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Win a DIFFICULTY Course Mini-Game Coaster",
                data={"DIFFICULTY": (self.skill_levels, 1)}, # Course names are the same as COM Skill Levels
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win at MINIGAME",
                data={"MINIGAME": (self.minigame_list_winnable, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=30,
            ),
            GameObjectiveTemplate(
                label="Collect the most coins in MINIGAME",
                data={"MINIGAME": (self.minigame_list_coin, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a ITEM in an Item Mini-Game", # All items start with a consonant
                data={"ITEM": (self.items, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Have at least COINCOUNT coins at once",
                data={"COINCOUNT": (self.board_coin_counts, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ])

    @staticmethod
    def off_on() -> List[str]:
        return [
            "Off",
            "On",
        ]

    @staticmethod
    def boards() -> List[str]:
        return [
            "Pirate Land",
            "Western Land",
            "Space Land",
            "Mystery Land",
            "Horror Land",
            "Bowser Land",
        ]

    @staticmethod
    def items() -> List[str]:
        return [
            "Mushroom",
            "Skeleton Key",
            "Plunder Chest",
            "Dueling Glove",
            "Warp Block",
            "Golden Mushroom",
            "Magic Lamp",
            "Boo Bell",
            "Bowser Suit",
            "Bowser Bomb"
        ]

    @staticmethod
    def board_turn_counts() -> List[int]:
        return [
            20,
            35,
            50,
        ]

    @staticmethod
    def skill_levels() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
        ]

    @staticmethod
    def skill_levels_duplicated() -> List[str]:
        return [ # Two of each difficulty to allow one duplicate for the Set Individually challenges
            "Easy",
            "Easy",
            "Normal",
            "Normal",
            "Hard",
            "Hard",
        ]

    @staticmethod
    def base_minigame_categories() -> List[str]:
        return [ # As a hack, all categories are listed here twice to compensate for the two 1 VS 3 options
            "4-Player Game",
            "4-Player Game",
            "1 VS 3 Game (as the 1)",
            "1 VS 3 Game (as the 3)",
            "2 VS 2 Game",
            "2 VS 2 Game",
        ]

    @staticmethod
    def minigame_battle_counts() -> List[int]:
        return [
            3,
            5,
            7
        ]

    @staticmethod
    def minigame_trial_turn_counts() -> List[int]:
        return [
            10,
            20,
            30
        ]

    @staticmethod
    def minigame_list_4p() -> List[str]:
        return [
            "Lava Tile Isle",
            "Hot Rope Jump",
            "Shell Shocked",
            "Toad in the Box",
            "Mecha-Marathon",
            "Roll Call",
            "Abandon Ship",
            "Platform Peril",
            "Totem Pole Pound",
            "Bumper Balls",
            "Bombs Away",
            "Tipsy Tourney",
            "Honeycomb Havoc",
            "Hexagon Heat",
            "Skateboard Scamper",
            "Slot Car Derby",
            "Shy Guy Says",
            "Sneak 'n' Snore",
            "Dizzy Dancing",
            "Tile Driver",
            # "Deep Sea Salvage", # Coin Minigame, different objective
        ]

    @staticmethod
    def minigame_list_1v3as1() -> List[str]:
        return [
            "Bowl Over (as the 1)",
            "Crane Game (as the 1)",
            "Move to the Music (as the 1)",
            "Bob-omb Barrage (as the 1)",
            "Look Away (as the 1)",
            "Shock, Drop or Roll (as the 1)",
            "Lights Out (as the 1)",
            "Filet Relay (as the 1)",
            "Archer-ival (as the 1)",
            #"Quicksand Cache (as the 1)", # Coin Minigame, different objective
            "Rainbow Run (as the 1)",
        ]

    @staticmethod
    def minigame_list_1v3as3() -> List[str]:
        return [
            "Bowl Over (as the 3)",
            "Crane Game (as the 3)",
            "Move to the Music (as the 3)",
            "Bob-omb Barrage (as the 3)",
            "Look Away (as the 3)",
            "Shock, Drop or Roll (as the 3)",
            "Lights Out (as the 3)",
            "Filet Relay (as the 3)",
            "Archer-ival (as the 3)",
            #"Quicksand Cache (as the 3)", # Coin Minigame, different objective
            "Rainbow Run (as the 3)",
        ]

    @staticmethod
    def minigame_list_2v2() -> List[str]:
        return [
            "Toad Bandstand",
            "Bobsled Run",
            "Handcar Havoc",
            "Balloon Burst",
            "Sky Pilots",
            "Speed Hockey",
            "Cake Factory",
            # "Magnet Carta", # Coin Minigame, different objective
            "Looney Lumberjacks",
            "Torpedo Targets",
            "Destruction Duet",
            "Dungeon Dash",
        ]

    @staticmethod
    def minigame_list_battle() -> List[str]:
        return [
            "Grab Bag",
            "Bumper Balloon Cars",
            "Rakin' 'em In",
            "Day at the Races",
            "Face Lift",
            "Crazy Cutters",
            "Hot Bob-omb",
            "Bowser's Big Blast",
        ]

    @staticmethod
    def minigame_list_duel() -> List[str]:
        return [
            "Saber Swipes",
            "Quick Draw Corks",
            "Time Bomb",
            "Psychic Safari",
            "Mushroom Brew",
            "Rock, Paper, Mario",
        ]

    def minigame_list_winnable(self) -> List[str]:
        # Add all Mini-Games twice as weight against for the different 1v3 variants
        minigames: List[str] = self.minigame_list_4p()[:]
        minigames.extend(self.minigame_list_4p()[:])
        minigames.extend(self.minigame_list_1v3as1()[:])
        minigames.extend(self.minigame_list_1v3as3()[:])
        minigames.extend(self.minigame_list_2v2()[:])
        minigames.extend(self.minigame_list_2v2()[:])
        minigames.extend(self.minigame_list_battle()[:])
        minigames.extend(self.minigame_list_battle()[:])
        minigames.extend(self.minigame_list_duel()[:])
        minigames.extend(self.minigame_list_duel()[:])
        return minigames

    @staticmethod
    def minigame_list_coin() -> List[str]:
        return [
            "Deep Sea Salvage",
            "Quicksand Cache (as the 1)",
            "Quicksand Cache (as the 3)",
            "Magnet Carta"
        ]

    @staticmethod
    def board_coin_counts() -> range:
        return range(50, 100)

# Archipelago Options
# ...

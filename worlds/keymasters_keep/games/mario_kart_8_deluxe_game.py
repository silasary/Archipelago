from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MarioKart8DeluxeArchipelagoOptions:
    mario_kart_8_deluxe_dlc_owned: MarioKart8DeluxeDLCOwned
    mario_kart_8_deluxe_include_battle_mode: MarioKart8DeluxeIncludeBattleMode


class MarioKart8DeluxeGame(Game):
    name = "Mario Kart 8 Deluxe"
    platform = KeymastersKeepGamePlatforms.SW

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = MarioKart8DeluxeArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play with CPU on DIFFICULTY difficulty",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Play with the following parts:  Body: BODY  Tires: TIRES  Glider: GLIDER",
                data={
                    "BODY": (self.bodies, 1),
                    "TIRES": (self.tires, 1),
                    "GLIDER": (self.gliders, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Finish 1st on COURSE as CHARACTER in a CC race",
                data={
                    "COURSE": (self.courses, 1),
                    "CHARACTER": (self.characters, 1),
                    "CC": (self.cc_normal, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish POSITION on COURSES as CHARACTER in CC races",
                data={
                    "POSITION": (self.positions, 1),
                    "COURSES": (self.courses, 4),
                    "CHARACTER": (self.characters, 1),
                    "CC": (self.cc_normal, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish POSITION in CUP as CHARACTER in CC races",
                data={
                    "POSITION": (self.positions, 1),
                    "CUP": (self.cups, 1),
                    "CHARACTER": (self.characters, 1),
                    "CC": (self.cc_normal, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            # Same with hard CC and 1 weight
            GameObjectiveTemplate(
                label="Finish 1st on COURSE as CHARACTER in a CC race",
                data={
                    "COURSE": (self.courses, 1),
                    "CHARACTER": (self.characters, 1),
                    "CC": (self.cc_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish POSITION on COURSES as CHARACTER in CC races",
                data={
                    "POSITION": (self.positions, 1),
                    "COURSES": (self.courses, 4),
                    "CHARACTER": (self.characters, 1),
                    "CC": (self.cc_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish POSITION in CUP as CHARACTER in CC races",
                data={
                    "POSITION": (self.positions, 1),
                    "CUP": (self.cups, 1),
                    "CHARACTER": (self.characters, 1),
                    "CC": (self.cc_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Hit CHARACTER with an item",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish 1st in a race while holding the follwing item: ITEM",
                data={
                    "ITEM": (self.items, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

        if self.includes_battle_mode:
            objectives.append(
                GameObjectiveTemplate(
                    label="Win a round of BATTLE_MODE on BATTLE_STAGE as CHARACTER",
                    data={
                        "BATTLE_MODE": (self.battle_modes, 1),
                        "BATTLE_STAGE": (self.battle_stages, 1),
                        "CHARACTER": (self.characters, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )

        return objectives

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.mario_kart_8_deluxe_dlc_owned.value)

    @property
    def has_booster_course_pass(self) -> bool:
        return "Booster Course Pass" in self.dlc_owned

    @property
    def includes_battle_mode(self) -> bool:
        return bool(self.archipelago_options.mario_kart_8_deluxe_include_battle_mode.value)

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Baby Daisy",
            "Baby Luigi",
            "Baby Mario",
            "Baby Peach",
            "Baby Rosalina",
            "Bowser Jr.",
            "Bowser",
            "Cat Peach",
            "Daisy",
            "Donkey Kong",
            "Dry Bones",
            "Dry Bowser",
            "Iggy",
            "Inkling",
            "Isabelle",
            "King Boo",
            "Koopa Troopa",
            "Lakitu",
            "Larry",
            "Lemmy",
            "Link",
            "Ludwig",
            "Luigi",
            "Mario",
            "Metal Mario",
            "Mii",
            "Morton",
            "Peach",
            "Pink Gold Peach",
            "Rosalina",
            "Roy",
            "Shy Guy",
            "Tanooki Mario",
            "Toad",
            "Toadette",
            "Villager",
            "Waluigi",
            "Wario",
            "Wendy",
            "Yoshi",
        ]

    @functools.cached_property
    def characters_booster_course_pass(self) -> List[str]:
        return [
            "Birdo",
            "Diddy Kong",
            "Funky Kong",
            "Kamek",
            "Pauline",
            "Peachette",
            "Petey Piranha",
            "Wiggler",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        if self.has_booster_course_pass:
            characters.extend(self.characters_booster_course_pass[:])

        return characters

    @staticmethod
    def bodies() -> List[str]:
        return [
            "300 SL Roadster",
            "Badwagon",
            "Biddybuggy",
            "Blue Falcon",
            "Bone Rattler",
            "Cat Cruiser",
            "Circuit Special",
            "City Tripper",
            "Comet",
            "Flame Rider",
            "GLA",
            "Gold Standard",
            "Inkstriker",
            "Jet Bike",
            "Koopa Clown",
            "Landship",
            "Mach 8",
            "Master Cycle Zero",
            "Master Cycle",
            "Mr. Scooty",
            "P-Wing",
            "Prancer",
            "Sneeker",
            "Splat Buggy",
            "Sport Bike",
            "Sports Coupe",
            "Standard ATV",
            "Standard Bike",
            "Standard KartPipe Frame",
            "Steel Driver",
            "Streetle",
            "Tanooki KartB Dasher",
            "Teddy Buggy",
            "The Duke",
            "Tri-Speeder",
            "Varmint",
            "W 25 Silver Arrow",
            "Wild Wiggler",
            "Yoshi Bike",
        ]

    @staticmethod
    def tires() -> List[str]:
        return [
            "Ancient Tires",
            "Azure Roller Tires",
            "Blue Standard Tires",
            "Button Tires",
            "Crimson Slim Tires",
            "Cushion Tires",
            "Cyber Slick Tires",
            "GLA Tires",
            "Gold Tires",
            "Hot Monster Tires",
            "Leaf Tires",
            "Metal Tires",
            "Monster Tires",
            "Off-Road Tires",
            "Retro Off-Road Tires",
            "Roller Tires",
            "Slick Tires",
            "Slim Tires",
            "Sponge Tires",
            "Standard Tires",
            "Triforce Tires",
            "Wood Tires",
        ]

    @staticmethod
    def gliders() -> List[str]:
        return [
            "Bowser Kite",
            "Cloud Glider",
            "Flower Glider",
            "Gold Glider",
            "Hylian Kite",
            "MKTV Parafoil",
            "Paper Glider",
            "Parachute",
            "Parafoil",
            "Paraglider",
            "Peach Parasol",
            "Plane Glider",
            "Super Glider",
            "Waddle Wing",
            "Wario Wing",
        ]

    @functools.cached_property
    def courses_base(self) -> List[str]:
        return [
            "Mario Kart Stadium (Mushroom)",
            "Water Park (Mushroom)",
            "Sweet Sweet Canyon (Mushroom)",
            "Thwomp Ruins (Mushroom)",
            "Mario Circuit (Flower)",
            "Toad Harbor (Flower)",
            "Twisted Mansion (Flower)",
            "Shy Guy Falls (Flower)",
            "Sunshine Airport (Star)",
            "Dolphin Shoals (Star)",
            "Electrodrome (Star)",
            "Mount Wario (Star)",
            "Cloudtop Cruise (Special)",
            "Bone-Dry Dunes (Special)",
            "Bowser's Castle (Special)",
            "Rainbow Road (Special)",
            "GCN Yoshi Circuit (Egg)",
            "Excitebike Arena (Egg)",
            "Dragon Driftway (Egg)",
            "Mute City (Egg)",
            "GCN Baby Park (Crossing)",
            "GBA Cheese Land (Crossing)",
            "Wild Woods (Crossing)",
            "Animal Crossing (Crossing)",
            "Wii Moo Moo Meadows (Shell)",
            "GBA Mario Circuit (Shell)",
            "DS Cheep Cheep Beach (Shell)",
            "N64 Toad's Turnpike (Shell)",
            "GCN Dry Dry Desert (Banana)",
            "SNES Donut Plains 3 (Banana)",
            "N64 Royal Raceway (Banana)",
            "3DS DK Jungle (Banana)",
            "DS Wario Stadium (Leaf)",
            "GCN Sherbet Land (Leaf)",
            "3DS Music Park (Leaf)",
            "N64 Yoshi Valley (Leaf)",
            "DS Tick-Tock Clock (Lightning)",
            "3DS Piranha Plant Slide (Lightning)",
            "Wii Grumble Volcano (Lightning)",
            "N64 Rainbow Road (Lightning)",
            "Wii Wario's Gold Mine (Triforce)",
            "SNES Rainbow Road (Triforce)",
            "Ice Ice Outpost (Triforce)",
            "Hyrule Circuit (Triforce)",
            "3DS Neo Bowser City (Bell)",
            "GBA Ribbon Road (Bell)",
            "Super Bell Subway (Bell)",
            "Big Blue (Bell)",
        ]

    @functools.cached_property
    def courses_booster_course_pass(self) -> List[str]:
        return [
            "Tour Paris Promenade (Golden Dash)",
            "3DS Toad Circuit (Golden Dash)",
            "N64 Choco Mountain (Golden Dash)",
            "Wii Coconut Mall (Golden Dash)",
            "Tour Tokyo Blur (Lucky Cat)",
            "DS Shroom Rdige (Lucky Cat)",
            "GBA Sky Garden (Lucky Cat)",
            "Ninja Hideaway (Lucky Cat)",
            "Tour New York Minute (Turnip)",
            "SNES Mario Circuit 3 (Turnip)",
            "N64 Kalamari Desert (Turnip)",
            "DS Waluigi Pinball (Turnip)",
            "Tour Sydney Sprint (Propeller)",
            "GBA Snow Land (Propeller)",
            "Wii Mushroom Gorge (Propeller)",
            "Sky-High Sundae (Propeller)",
            "Tour London Loop (Rock)",
            "GBA Boo Lake (Rock)",
            "3DS Rock Rock Mountain (Rock)",
            "Wii Maple Treeway (Rock)",
            "Tour Berlin Byways (Moon)",
            "DS Peach Gardens (Moon)",
            "Merry Mountain (Moon)",
            "3DS Rainbow Road (Moon)",
            "Tour Amsterdam Drift (Fruit)",
            "GBA Riverside Park (Fruit)",
            "Wii DK Summit (Fruit)",
            "Yoshi's Island (Fruit)",
            "Tour Bangkok Rush (Boomerang)",
            "DS Mario Circuit (Boomerang)",
            "GCN Waluigi Stadium (Boomerang)",
            "Tour Singapore Speedway (Boomerang)",
            "Tour Athens Dash (Feather)",
            "GCN Daisy Cruiser (Feather)",
            "Wii Moonview Highway (Feather)",
            "Squeaky Clean Sprint (Feather)",
            "Tour Los Angeles Laps (Cherry)",
            "GBA Sunset Wilds (Cherry)",
            "Wii Koopa Cape (Cherry)",
            "Tour Vancouver Velocity (Cherry)",
            "Tour Rome Avanti (Acorn)",
            "GCN DK Mountain (Acorn)",
            "Wii Daisy Circuit (Acorn)",
            "Piranha Plant Cove (Acorn)",
            "Tour Madrid Drive (Spiny)",
            "3DS Rosalina's Ice World (Spiny)",
            "SNES Bowser Castle 3 (Spiny)",
            "Wii Rainbow Road (Spiny)",
        ]

    def courses(self) -> List[str]:
        courses: List[str] = self.courses_base[:]

        if self.has_booster_course_pass:
            courses.extend(self.courses_booster_course_pass[:])

        return courses

    @functools.cached_property
    def cups_base(self) -> List[str]:
        return [
            "Banana Cup",
            "Bell Cup",
            "Crossing Cup",
            "Egg Cup",
            "Flower Cup",
            "Leaf Cup",
            "Lightning Cup",
            "Mushroom Cup",
            "Shell Cup",
            "Special Cup",
            "Star Cup",
            "Triforce Cup",
        ]

    @functools.cached_property
    def cups_booster_course_pass(self) -> List[str]:
        return [
            "Acorn Cup",
            "Boomerang Cup",
            "Cherry Cup",
            "Feather Cup",
            "Fruit Cup",
            "Golden Dash Cup",
            "Lucky Cat Cup",
            "Moon Cup",
            "Propeller Cup",
            "Rock Cup",
            "Spiny Cup",
            "Turnip Cup",
        ]

    def cups(self) -> List[str]:
        cups: List[str] = self.cups_base[:]

        if self.has_booster_course_pass:
            cups.extend(self.cups_booster_course_pass[:])

        return cups

    @staticmethod
    def cc_normal() -> List[str]:
        return [
            "50cc",
            "100cc",
            "150cc",
        ]

    @staticmethod
    def cc_hard() -> List[str]:
        return [
            "Mirror",
            "200cc",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
        ]

    @staticmethod
    def battle_modes() -> List[str]:
        return [
            "Balloon Battle",
            "Bob-omb Blast",
            "Coin Runners",
            "Renegade Roundup",
            "Shine Thief",
        ]

    @staticmethod
    def battle_stages() -> List[str]:
        return [
            "3DS Wuhu Town",
            "Battle Stadium",
            "Dragon Palace",
            "GCN Luigi Mansion",
            "Lunar Colony",
            "SNES Battle Course 1",
            "Sweet Sweet Kingdom",
            "Urchin Underpass",
        ]

    @staticmethod
    def items() -> List[str]:
        return [
            "Banana",
            "Blooper",
            "Boo",
            "Boomerang Flower",
            "Bullet Bill",
            "Coin",
            "Fire Flower",
            "Golden Mushroom",
            "Green Shell",
            "Lightning",
            "Mushroom",
            "Piranha Plant",
            "Red Shell",
            "Spiny Shell",
            "Super Horn",
            "Triple Banana",
            "Triple Green Shells",
            "Triple Mushrooms",
            "Triple Red Shells",
        ]

    @staticmethod
    def positions() -> List[str]:
        return [
            "1st",
            "2nd or better",
            "3rd or better",
        ]


# Archipelago Options
class MarioKart8DeluxeDLCOwned(OptionSet):
    """
    Indicates which Mario Kart 8 Deluxe DLC the player owns, if any.
    """

    display_name = "Mario Kart 8 Deluxe DLC Owned"
    valid_keys = [
        "Booster Course Pass",
    ]

    default = valid_keys


class MarioKart8DeluxeIncludeBattleMode(Toggle):
    """
    Indicates whether the player wants to include Mario Kart 8 Deluxe Battle Mode objectives
    """

    display_name = "Mario Kart 8 Deluxe Include Battle Mode"

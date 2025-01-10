from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ArcaeaArchipelagoOptions:
    arcaea_dlc_owned: ArcaeaDLCOwned


class ArcaeaGame(Game):
    name = "Arcaea"
    platform = KeymastersKeepGamePlatforms.SW

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = ArcaeaArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play SONG on DIFFICULTY difficulty",
                data={
                    "SONG": (self.songs, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Play SONGS on DIFFICULTY difficulty",
                data={
                    "SONGS": (self.songs, 2),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play SONGS on DIFFICULTY difficulty",
                data={
                    "SONGS": (self.songs, 3),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete 5 Steps on a World Mode Map",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.arcaea_dlc_owned.value)

    @property
    def has_dlc_x_lanota(self) -> bool:
        return "Arcaea X Lanota" in self.dlc_owned

    @property
    def has_dlc_x_groove_coaster(self) -> bool:
        return "Arcaea X Groove Coaster" in self.dlc_owned

    @property
    def has_dlc_ephemeral_page(self) -> bool:
        return "Ephemeral Page" in self.dlc_owned

    @property
    def has_dlc_esoteric_order(self) -> bool:
        return "Esoteric Order" in self.dlc_owned

    @property
    def has_dlc_light_of_salvation(self) -> bool:
        return "Light of Salvation" in self.dlc_owned

    @property
    def has_dlc_x_wacca(self) -> bool:
        return "Arcaea x WACCA" in self.dlc_owned

    @property
    def has_dlc_muse_dash(self) -> bool:
        return "Arcaea x Muse Dash" in self.dlc_owned

    @property
    def has_dlc_binary_enfold(self) -> bool:
        return "Binary Enfold" in self.dlc_owned

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Hikari",
            "Tairitsu",
            "Kou",
            "Lethe",
            "Axium Tairitsu",
            "Ilith",
            "Shirabe",
            "Zero Hikari",
            "Fracture Hikari",
            "Ayu",
            "Saya",
            "Kanae",
            "Sia",
            "Mir",
            "Shirahime",
            "Reunion Hikari & Tairitsu",
            # Hard
            "Grievous Lady Tairitsu",
            "Tempest Tairitsu",
            "Fatalis Hikari",
        ]

    @functools.cached_property
    def characters_x_lanota(self) -> List[str]:
        return [
            "Hikari & Fisica",
        ]

    @functools.cached_property
    def characters_x_groove_coaster(self) -> List[str]:
        return [
            "Yume",
            "Hikari & Seine",
            "Linka",
        ]

    @functools.cached_property
    def characters_ephemeral_page(self) -> List[str]:
        return [
            "Alice & Tenniel",
        ]

    @functools.cached_property
    def characters_esoteric_order(self) -> List[str]:
        return [
            "Lagrange",
        ]

    @functools.cached_property
    def characters_light_of_salvation(self) -> List[str]:
        return [
            "Nami",
        ]

    @functools.cached_property
    def characters_x_wacca(self) -> List[str]:
        return [
            "Saya & Elizabeth",
            "Lily",
        ]

    @functools.cached_property
    def characters_muse_dash(self) -> List[str]:
        return [
            "Marija",
        ]

    @functools.cached_property
    def characters_binary_enfold(self) -> List[str]:
        return [
            "Vita",
            "Eto",
            "Luna",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        if self.has_dlc_x_lanota:
            characters.extend(self.characters_x_lanota)

        if self.has_dlc_x_groove_coaster:
            characters.extend(self.characters_x_groove_coaster)

        if self.has_dlc_ephemeral_page:
            characters.extend(self.characters_ephemeral_page)

        if self.has_dlc_esoteric_order:
            characters.extend(self.characters_esoteric_order)

        if self.has_dlc_light_of_salvation:
            characters.extend(self.characters_light_of_salvation)

        if self.has_dlc_x_wacca:
            characters.extend(self.characters_x_wacca)

        if self.has_dlc_muse_dash:
            characters.extend(self.characters_muse_dash)

        if self.has_dlc_binary_enfold:
            characters.extend(self.characters_binary_enfold)

        return sorted(characters)

    @functools.cached_property
    def songs_base(self) -> List[str]:
        return [
            "Fairytale",
            "Harutopia ~Utopia of Spring~",
            "Infinity Heaven",
            "Kanagawa Cyber Culvert",
            "Sayonara Hatsukoi",
            "1F√",
            "Altair (feat. *spiLa*)",
            "Brand new world",
            "Clotho and the stargazer",
            "Dandelion",
            "DDD",
            "Diode",
            "enchanted love",
            "Grimheart",
            "Illegal Paradise",
            "inkar-usi",
            "Lapis",
            "One Last Drive",
            "Purgatorium",
            "Rabbit in The Black Room",
            "Reinvent",
            "Rise",
            "Snow White",
            "Suomi",
            "Turbocharger",
            "Vexaria",
            "Vivid Theory",
            "Babarogue",
            "Bamboo",
            "BlackLotus",
            "blue comet",
            "Chronostasis",
            "Dancin'on a Cat's Paw",
            "Dement ~after legend~",
            "ENERGY SYNERGY MATRIX",
            "Faint Light (Arcaea Edit)",
            "False Embellishment",
            "GIMME DA BLOOD",
            "Give Me a Nightmare",
            "Ignotus",
            "Life is PIANO",
            "Lucifer",
            "LunarOrbit -believe in the Espebranch road-",
            "Nhelv",
            "NULCTRL",
            "oBLIVIA",
            "ReviXy",
            "Rugie",
            "Sakura Fubuki",
            "san skia",
            "Senkyou",
            "Shade of Light in a Transcendent Realm",
            "SUPERNOVA",
            "Syro",
            "Vandalism",
            "VECTOЯ",
            "world.execute(me);",
            "Ävril-Flicka i krans-",
            "Blaster",
            "Bookmaker (2D Version)",
            "CROSS†OVER",
            "Cybernecia Catharsis",
            "Dreamin' Attraction!!",
            "FREEF4LL",
            "Gekka (Short Version)",
            "Glow",
            "GOODTEK (Arcaea Edit)",
            "HIVEMIND",
            "init()",
            "Lost Civilization",
            "Monochrome Princess",
            "Purple Verse",
            "qualia -ideaesthesia-",
            "Red and Blue",
            "Redraw the Colorless World",
            "Trap Crow",
            # Divided Heart
            "First Snow",
            "Blue Rose",
            "Blocked Library",
            "nέo κósmo",
            "Lightning Screw",
            # Memory Archive Base
            "Call My Name feat. Yukacco",
            "Dot to Dot feat. shully",
            "dropdead",
            "amygdata",
            "Astral tale",
            "Auxesia",
            "Avant Raze",
            "Be There",
            "carmine:scythe",
            "CROSS†SOUL",
            "DataErr0r",
            "Empire of Winter",
            "Fallensquare",
            "Feels So Right feat. Renko",
            "Impure Bird",
            "La'qryma of the Wasteland",
            "Libertas",
            "MAHOROBA",
            "Phantasia",
            "Altale",
            "BADTEK",
            "BATTLE NO.1",
            "Dreadnought",
            "Einherjar Joker",
            "Filament",
            "Galaxy Friends",
            "Heavenly caress",
            "Scarlet Cage",
            "Alexandrite",
            "IZANA",
            "Malicious Mischance",
            "Metallic Punisher",
            "Mirzam",
            "Modelista",
            "SAIKYO STRONGER",
            # Eternal Core
            "cry of viyella",
            "I've heard it said",
            "memoryfactory.lzh",
            "Relentless",
            "Lumia",
            "Essence of Twilight",
            "PRAGMATISM",
            "Sheriruth",
            "Solitary Dream",
            # Vicious Labyrinth
            "Iconoclast",
            "SOUNDWiTCH",
            "trappola bewitching",
            "conflict",
            "Axium Crisis",
            "Grievous Lady",
            # Luminous Sky
            "Maze No.9",
            "The Message",
            "Sulfur",
            "Halcyon",
            "Ether Strike",
            "Fracture Ray",
            # Adverse Prelude
            "Vindication",
            "Heavensdoor",
            "Ringed Genesis",
            "BLRINK",
            # Black Fate
            "Equilibrium",
            "Antagonism",
            "Lost Desire",
            "Dantalion",
            "#1f1e33",
            "Tempestissimo",
            "Arcahv",
            # Final Verdict
            "Defection",
            "Infinite Strife,",
            "World Ender",
            "Pentiment",
            "Arcana Eden",
            "Testify",
            # Silent Answer
            "Loveless Dress",
            "Last",
            "Callima Karma",
            # Crimson Solace
            "Paradise",
            "Flashback",
            "Flyburg and Endroll",
            "Party Vinyl",
            "Nirv lucE",
            "GLORY：ROAD",
            # Ambivalent Vision
            "Blossoms",
            "Romance Wars",
            "Moonheart",
            "Genesis",
            "Lethaeus",
            "corps-sans-organes",
            # Binary Enfold
            "next to you",
            "Silent Rush",
            "Strongholds",
            "Memory Forest",
            "Singularity",
            # Absolute Reason
            "Antithese",
            "Corruption",
            "Black Territory",
            "Vicious Heroism",
            "Cyaegha",
            # Sunset Radiance
            "Chelsea",
            "Tie me down gently",
            "AI[UE]OON",
            "A Wandering Melody of Love",
            "Valhalla:0",
        ]

    @functools.cached_property
    def songs_x_lanota(self) -> List[str]:
        return [
            "Dream goes on",
            "Journey",
            "Prism",
            "Quon",
            "Specta",
            "Protoflicker",
            "cyanine",
            "Stasis",
        ]

    @functools.cached_property
    def songs_x_groove_coaster(self) -> List[str]:
        return [
            "MERLIN",
            "DX Choseinou Full Metal Shojo",
            "OMAKENO Stroke",
            "Scarlet Lance",
            "Got hive of Ra",
            "ouroboros -twin stroke of the end-",
            "BUCHiGiRE Berserker",
            "Aurgelmir",
        ]

    @functools.cached_property
    def songs_ephemeral_page(self) -> List[str]:
        return [
            "Beside You",
            "Eccentric Tale",
            "Alice à la mode",
            "Alice's Suitcase",
            "Jump",
            "Heart Jackin'",
            "Felis",
            "To: Alice Liddell",
        ]

    @functools.cached_property
    def songs_esoteric_order(self) -> List[str]:
        return [
            "Coastal Highway",
            "Paper Witch",
            "Crystal Gravity",
            "ΟΔΥΣΣΕΙΑ",
            "Far Away Light",
            "Löschen",
            "Overwhelm",
            "Aegleseeker",
        ]

    @functools.cached_property
    def songs_light_of_salvation(self) -> List[str]:
        return [
            # Memory Archive DLC 1
            "Xanatos",
            "AttraqtiA",
            "THE ULTIMACY",
            "REKKA RESONANCE",
            # Memory Archive DLC 2
            "Gengaozo",
            "Can I Friend You on Bassbook? Lol",
            "Xeraphinite",
            "Summer Fireworks of Love",
            # Esoteric Order Light of Salvation
            "Seclusion",
            "Small Cloud Sugar Candy",
            "AlterAle",
            "Divine Light of Myriad",
        ]

    @functools.cached_property
    def songs_x_wacca(self) -> List[str]:
        return [
            "Quon",
            "Let you DIVE! (nitro rmx)",
            "with U",
            "Mazy Metroplex",
            "GENOCIDER",
            "Sheriruth (Laur Remix)",
            "eden",
            "XTREME",
            "Meta-Mysteria",
        ]

    @functools.cached_property
    def songs_x_muse_dash(self) -> List[str]:
        return [
            "Lights of Muse",
            "Final Step!",
            "Haze of Autumn",
            "Medusa",
        ]

    @functools.cached_property
    def songs_binary_enfold(self) -> List[str]:
        return [
            # Memory Archive DLC 3
            "Redolent Shape",
            "γuarδina",
            "Macrocosmic Modulation",
            "Kissing Lucifer",
            "NEO WINGS",
            "µ",
            "PUPA",
            "Head BONK ache",
            "INTERNET OVERDOSE",
            "PICO-Pico-Translation!",
            "Evening in Scarlet",
            "lastendconductor",
            "goldenslaughterer",
            # Shared Time
            "Cosmica",
            "Ascent",
            "Live Fast Die Young",
        ]

    def songs(self) -> List[str]:
        songs: List[str] = self.songs_base[:]

        if self.has_dlc_x_lanota:
            songs.extend(self.songs_x_lanota)

        if self.has_dlc_x_groove_coaster:
            songs.extend(self.songs_x_groove_coaster)

        if self.has_dlc_ephemeral_page:
            songs.extend(self.songs_ephemeral_page)

        if self.has_dlc_esoteric_order:
            songs.extend(self.songs_esoteric_order)

        if self.has_dlc_light_of_salvation:
            songs.extend(self.songs_light_of_salvation)

        if self.has_dlc_x_wacca:
            songs.extend(self.songs_x_wacca)

        if self.has_dlc_muse_dash:
            songs.extend(self.songs_x_muse_dash)

        if self.has_dlc_binary_enfold:
            songs.extend(self.songs_binary_enfold)

        return songs

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "past",
            "present",
            "future",
        ]


# Archipelago Options
class ArcaeaDLCOwned(OptionSet):
    """
    Indicates which Arcaea DLC the player owns, if any.
    """

    display_name = "Arcaea DLC Owned"
    valid_keys = [
        "Arcaea X Lanota",
        "Arcaea X Groove Coaster",
        "Ephemeral Page",
        "Esoteric Order",
        "Light of Salvation",
        "Arcaea x WACCA",
        "Arcaea x Muse Dash",
        "Binary Enfold",
    ]

    default = valid_keys

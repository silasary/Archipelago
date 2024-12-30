from __future__ import annotations

import functools
from msilib.schema import Property
from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PokemonRSEKeymastersKeepOptions:
    pokemon_rse_owned_games: RSEOwnedGames
    pokemon_rse_objectives: RSEObjectives


class PokemonRSEGame(Game):
    name = "Pokémon Ruby, Sapphire, and Emerald Versions"
    platform = KeymastersKeepGamePlatforms.GBA

    is_adult_only_or_unrated = False

    options_cls = PokemonRSEKeymastersKeepOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use POKEMON as your lead whenever possible",
                data={"POKEMON": (self.wild_pokemon, 1)},
                weight=3
            ),
            GameObjectiveTemplate(
                label="Use RAREPOKEMON as your lead whenever possible",
                data={"RAREPOKEMON": (self.difficult_pokemon, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = []
        if self.objective_catching:
            objectives += self.catching_objectives()
        if self.objective_contests:
            objectives += self.contest_objectives()
        if self.objective_battles:
            objectives += self.battle_objectives()
        if self.objective_battle_frontier:
            objectives += self.battle_frontier_objectives()
        if len(objectives) == 0: # Fallback default objectives. Better versions of these exist in other categories
            objectives += [
                GameObjectiveTemplate(
                    label="Without using Fly, travel between the following cities: CITY",
                    data={"CITY": (self.cities, 2)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=20
                ),
                GameObjectiveTemplate(
                    label="Encounter a wild POKEMON",
                    data={"POKEMON": (self.wild_pokemon, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Encounter a wild Feebas",
                    data={},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1
                ),
            ]

        return objectives

    def catching_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Catch a wild POKEMON",
                data={"POKEMON": (self.wild_pokemon, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Catch a wild POKEMON in a BALL",
                data={"POKEMON": (self.wild_pokemon, 1), "BALL": (self.poke_ball_types, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=70,
            ),
            GameObjectiveTemplate(
                label="Catch a wild Feebas",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Catch a wild Feebas in a BALL",
                data={"BALL": (self.poke_ball_types, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Catch a wild POKEMON in the Safari Zone",
                data={"POKEMON": (self.safari_pokemon, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=25,
            ),
        ]


    def contest_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Make a COLOR Pokéblock",
                data={"COLOR": (self.common_pokeblock_types, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=50,
            ),
            GameObjectiveTemplate(
                label="Make a COLOR Pokéblock",
                data={"COLOR": (self.rare_pokeblock_types, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win a RANKING Rank Contest",
                data={"RANKING": (self.base_contest_ranks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=30,
            ),
            GameObjectiveTemplate(
                label="Win a Hyper Rank Contest",
                data={},
                is_time_consuming=True,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Win a Master Rank Contest",
                data={},
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win a RANKING Rank TYPE Contest",
                data={"RANKING": (self.base_contest_ranks, 1), "TYPE": (self.contest_types, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Win a Hyper Rank TYPE Contest",
                data={"TYPE": (self.contest_types, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win a Master Rank TYPE Contest",
                data={"TYPE": (self.contest_types, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=8,
            ),
        ]

    def battle_objectives(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Defeat the Pokémon League and enter the Hall of Fame",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=25,
            ),
            GameObjectiveTemplate(
                label="Defeat a wild POKEMON",
                data={"POKEMON": (self.wild_pokemon, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Defeat the Pokémon League and enter the Hall of Fame with only one Pokémon",
                data={},
                is_time_consuming=False,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Without using Fly, items, or a Pokémon Center, travel between the following cities "
                      "and defeat every wild encounter you see: CITY",
                data={"CITY": (self.cities, 2)},
                is_time_consuming=True,
                is_difficult=False,
                weight=35,
            ),
        ]

        if self.has_emerald:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Win any Match Call rematch",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=35,
                ),
                GameObjectiveTemplate(
                    label="Win a Match Call rematch against a Gym Leader",
                    data={},
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
            ])

        return objectives

    def battle_frontier_objectives(self) -> List[GameObjectiveTemplate]:
        if self.has_emerald:
            return [
                GameObjectiveTemplate(
                    label="Win 3 battles in a row in the FACILITY",
                    data={"FACILITY": (self.battle_tents, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=30,
                ),
                GameObjectiveTemplate(
                    label="Win 7 battles in a row in the FACILITY",
                    data={"FACILITY": (self.battle_frontier_facilities, 1)},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=60,
                ),
                GameObjectiveTemplate(
                    label="Complete 7 floors in a row in the Battle Pyramid",
                    data={},
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Win a battle against BRAIN",
                    data={"BRAIN": (self.battle_frontier_brains, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
            ]
        else:
            return [
                GameObjectiveTemplate(
                    label="Win 7 battles in a row in the Battle Tower",
                    data={},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=20,
                ),
            ]

    @property
    def games_owned(self) -> Set[str]:
        return self.archipelago_options.pokemon_rse_owned_games.value

    @property
    def has_ruby(self) -> bool:
        return "Ruby" in self.games_owned

    @property
    def has_sapphire(self) -> bool:
        return "Sapphire" in self.games_owned

    @property
    def has_emerald(self) -> bool:
        return "Emerald" in self.games_owned

    @property
    def objectives(self) -> Set[str]:
        return self.archipelago_options.pokemon_rse_objectives.value

    @property
    def objective_catching(self) -> bool:
        return "Catching" in self.objectives

    @property
    def objective_contests(self) -> bool:
        return "Contests" in self.objectives

    @property
    def objective_battles(self) -> bool:
        return "Battles" in self.objectives

    @property
    def objective_battle_frontier(self) -> bool:
        return "Battle Frontier" in self.objectives

    def wild_pokemon(self) -> List[str]:
        # List fully in common with all three games
        pokemon: List[str] = self.wild_rse()[:]

        # Full version exclusives
        if self.has_ruby:
            pokemon.extend(self.wild_r()[:])
        if self.has_sapphire:
            pokemon.extend(self.wild_s()[:])
        if self.has_emerald:
            pokemon.extend(self.wild_e()[:])

        # Exclusive to two games
        if self.has_ruby or self.has_sapphire:
            pokemon.extend(self.wild_rs()[:])
        if self.has_ruby or self.has_emerald:
            pokemon.extend(self.wild_re()[:])
        if self.has_sapphire or self.has_emerald:
            pokemon.extend(self.wild_se()[:])

        return pokemon

    def difficult_pokemon(self) -> List[str]:
        # Evolutions, Breeding, and other rare repeatable Pokémon
        pokemon: List[str] = [
            # Evolution exclusive
            "Beautifly",
            "Dustox",
            "Kirlia",
            "Gardevoir",
            "Breloom",
            "Vigoroth",
            "Slaking",
            "Kadabra",
            "Ninjask",
            "Shedinja",
            "Exploud",
            "Azumarill",
            "Crobat",
            "Aggron",
            "Machoke",
            "Swalot",
            "Camerupt",
            "Magcargo",
            "Muk",
            "Weezing",
            "Grumpig",
            "Sandslash",
            "Vibrava",
            "Flygon",
            "Cacturne",
            "Crawdaunt",
            "Glalie",
            "Sealeo",
            "Walrein",
            "Lanturn",
            "Seadra",
            "Shelgon",
            "Salamence",
            
            # Breeding exclusive
            "Azurill",
            "Igglybuff",
            "Pichu",
            "Wynaut",

            # Safari Zone exclusives (and their evolutions)
            "Seaking",
            "Doduo",
            "Dodrio",
            "Pikachu",
            "Raichu",
            "Psyduck",
            "Golduck",
            "Wobbuffet",
            "Natu",
            "Xatu",
            "Girafarig",
            "Phanpy",
            "Donphan",
            "Pinsir",
            "Heracross",
            "Rhyhorn",
            "Rhydon",

            # Feebas
            "Feebas",
            "Milotic",
        ]

        if not self.has_ruby:
            pokemon.append("Dusclops") # Evolution-only in all other games
        if not self.has_sapphire and not self.has_emerald:
            pokemon.append("Banette") # Evolution-only in Ruby
        if not self.has_emerald:
            pokemon.append("Mightyena") # Evolution-only outside of Emerald

        if self.has_ruby or self.has_sapphire:
            pokemon.append("Masquerain")

        if self.has_emerald:
            pokemon.extend([
                "Hoothoot",
                "Noctowl",
                "Ledyba",
                "Ledian",
                "Spinarak",
                "Ariados",
                "Mareep",
                "Flaaffy",
                "Ampharos",
                "Aipom",
                "Sunkern",
                "Sunflora",
                "Wooper",
                "Quagsire",
                "Pineco",
                "Forretress",
                "Gligar",
                "Snubbull",
                "Granbull",
                "Shuckle",
                "Teddiursa",
                "Ursaring",
                "Remoraid",
                "Octillery",
                "Houndour",
                "Houndoom",
                "Stantler",
                "Smeargle",
                "Miltank",
            ][:])

        return pokemon

    def safari_pokemon(self) -> List[str]:
        pokemon: List[str] = self.safari_rse()[:]

        if self.has_emerald:
            pokemon.extend(self.safari_e()[:])

        return pokemon

    @staticmethod
    def poke_ball_types() -> List[str]:
        return [
            "Poké Ball",
            "Great Ball",
            "Ultra Ball",
            "Net Ball",
            "Dive Ball",
            "Nest Ball",
            "Repeat Ball",
            "Timer Ball",
            "Premier Ball",
            # Luxury and Master Balls *can* be found infinitely, but are too annoying
        ]

    @staticmethod
    def wild_rse() -> List[str]:
        return [
            "Poochyena",
            "Zigzagoon",
            "Linoone",
            "Wurmple",
            "Silcoon",
            "Cascoon",
            "Taillow",
            "Swellow",
            "Wingull",
            "Pelipper",
            "Ralts",
            "Shroomish",
            "Slakoth",
            "Abra",
            "Nincada",
            "Whismur",
            "Loudred",
            "Makuhita",
            "Hariyama",
            "Goldeen",
            "Magikarp",
            "Gyarados",
            "Marill",
            "Geodude",
            "Graveler",
            "Nosepass",
            "Skitty",
            "Zubat",
            "Golbat",
            "Tentacool",
            "Tentacruel",
            "Aron",
            "Lairon",
            "Machop",
            "Electrike",
            "Manectric",
            "Plusle",
            "Minun",
            "Magnemite",
            "Magneton",
            "Voltorb",
            "Electrode",
            "Volbeat",
            "Illumise",
            "Oddish",
            "Gloom",
            "Gulpin",
            "Carvanha",
            "Sharpedo",
            "Wailmer",
            "Wailord",
            "Numel",
            "Slugma",
            "Torkoal",
            "Grimer",
            "Koffing",
            "Spoink",
            "Sandshrew",
            "Spinda",
            "Skarmory",
            "Trapinch",
            "Cacnea",
            "Swablu",
            "Altaria",
            "Barboach",
            "Whiscash",
            "Corphish",
            "Baltoy",
            "Claydol",
            "Jigglypuff",
            # "Feebas", # Absolutely a difficult objective
            "Staryu",
            "Kecleon",
            "Shuppet",
            "Duskull",
            "Tropius",
            "Chimecho",
            "Absol",
            "Vulpix",
            # "Wynaut", # Mirage Island exclusive, not even a good difficult objective
            "Snorunt",
            "Spheal",
            "Clamperl",
            "Relicanth",
            "Corsola",
            "Chinchou",
            "Luvdisc",
            "Horsea",
            "Bagon",
        ]

    @staticmethod
    def wild_rs() -> List[str]:
        return [
            "Surskit",
            "Meditite",
            "Medicham",
            "Roselia",
        ]

    @staticmethod
    def wild_r() -> List[str]:
        return [
            "Zangoose",
            "Dusclops",
        ]

    @staticmethod
    def wild_re() -> List[str]:
        return [
            "Seedot",
            "Nuzleaf",
            "Mawile",
            "Solrock",
        ]

    @staticmethod
    def wild_s() -> List[str]:
        return [
            "Lunatone",
        ]

    @staticmethod
    def wild_se() -> List[str]:
        return [
            "Lotad",
            "Lombre",
            "Sableye",
            "Seviper",
            "Banette",
        ]

    @staticmethod
    def wild_e() -> List[str]:
        return [
            # Hoenn Dex
            "Mightyena",
            # National Dex
            "Ditto",
            "Smeargle"
        ]

    @staticmethod
    def safari_rse() -> List[str]:
        return [
            "Goldeen",
            "Seaking",
            "Magikarp",
            "Geodude",
            "Oddish",
            "Gloom",
            "Doduo",
            "Dodrio",
            "Pikachu",
            "Psyduck",
            "Golduck",
            "Wobbuffet",
            "Natu",
            "Xatu",
            "Girafarig",
            "Phanpy",
            "Pinsir",
            "Heracross",
            "Rhyhorn",
        ]

    @staticmethod
    def safari_e() -> List[str]:
        return [
            # Hoenn Dex
            "Marill",
            # National Dex
            "Hoothoot",
            "Ledyba",
            "Spinarak",
            "Mareep",
            "Aipom",
            "Sunkern",
            "Wooper",
            "Quagsire",
            "Pineco",
            "Gligar",
            "Snubbull",
            "Shuckle",
            "Teddiursa",
            "Remoraid",
            "Octillery",
            "Houndour",
            "Stantler",
            "Smeargle",
            "Miltank",
        ]

    @staticmethod
    def common_pokeblock_types() -> List[str]:
        return [
            "Red",
            "Blue",
            "Pink",
            "Green",
            "Yellow",
        ]

    @staticmethod
    def rare_pokeblock_types() -> List[str]:
        return [
            "Black",
            "Gold",
            "Purple",
            "Indigo",
            "Brown",
            "LiteBlue",
            "Olive",
            "Gray",
            "White",
        ]

    @staticmethod
    def base_contest_ranks() -> List[str]:
        return [
            "Normal",
            "Super",
            # "Hyper",  # Hyper is separated out as time-consuming
            # "Master", # Master is separated out as difficult and time-consuming
        ]

    @staticmethod
    def contest_types() -> List[str]:
        return [
            "Cool",
            "Beauty",
            "Cute",
            "Smart",
            "Tough"
        ]

    @staticmethod
    def cities() -> List[str]:
        return [
            "Littleroot Town",
            "Oldale Town",
            "Petalburg City",
            "Rustboro City",
            "Dewford Town",
            "Slateport City",
            "Mauville City",
            "Verdanturf Town",
            "Fallarbor Town",
            "Lavaridge Town",
            "Fortree City",
            "Lilycove City",
            "Mossdeep City",
            "Sootopolis City",
            "Pacifidlog Town",
            "Ever Grande City (South)",
            "Ever Grande City (North)",
        ]

    @staticmethod
    def battle_tents() -> List[str]:
        return [
            "Battle Tent Slateport Site",
            "Battle Tent Verdanturf Site",
            "Battle Tent Fallarbor Site",
        ]

    @staticmethod
    def battle_frontier_facilities() -> List[str]:
        return [
            "Battle Factory",
            "Battle Arena",
            "Battle Dome",
            "Battle Pike",
            "Battle Palace",
            # "Battle Pyramid", # Different objective than the others
            "Battle Tower",
        ]

    @staticmethod
    def battle_frontier_brains() -> List[str]:
        return [
            "Factory Head Noland",
            "Arena Tycoon Greta",
            "Dome Ace Tucker",
            "Pike Queen Lucy",
            "Palace Maven Spenser",
            "Pyramid King Brandon",
            "Salon Maiden Anabel"
        ]

# Archipelago Options
class RSEOwnedGames(OptionSet):
    """
    Indicates which versions of the games the player owns between Pokémon Ruby/Sapphire/Emerald.
    """

    display_name = "Pokémon Ruby/Sapphire/Emerald Owned Games"
    valid_keys = [
        "Ruby",
        "Sapphire",
        "Emerald"
    ]

    default = valid_keys

class RSEObjectives(OptionSet):
    """
    Indicates which objective types the player would like to engage in for Pokémon Ruby/Sapphire/Emerald.
    """
    display_name = "Pokémon Ruby/Sapphire/Emerald Objective Types"
    valid_keys = [
        "Catching",
        "Contests",
        "Battles",
        "Battle Frontier",
    ]

    default = valid_keys

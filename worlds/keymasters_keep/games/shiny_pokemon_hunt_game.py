from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import OptionSet

@dataclass
class ShinyPokemonHuntArchipelagoOptions:
    shiny_pokemon_hunt_owned_games: ShinyPokemonHuntOwnedGames

GEN_2_PRIMARY = "Gold/Silver/Crystal"
GEN_3_PRIMARY = "Ruby/Sapphire/Emerald"
GEN_3_REMAKE = "FireRed/LeafGreen"
GEN_3_SECONDARY = "Colosseum/XD"
GEN_4_PRIMARY = "Diamond/Pearl/Platinum"
GEN_4_REMAKE = "HeartGold/SoulSilver"
GEN_5_PRIMARY = "Black/White/Black 2/White 2"
GEN_6_PRIMARY = "X/Y"
GEN_6_REMAKE = "Omega Ruby/Alpha Sapphire"
GEN_7_PRIMARY = "Sun/Moon"
GEN_7_SECONDARY = "Ultra Sun/Ultra Moon"
GEN_7_REMAKE = "Let's Go Pikachu/Eevee"
GEN_8_PRIMARY = "Sword/Shield"
GEN_8_DLC = "Sword/Shield Expansion Pass"
GEN_8_REMAKE = "Brilliant Diamond/Shining Pearl"
GEN_8_SECONDARY = "Legends Arceus"
GEN_9_PRIMARY = "Scarlet/Violet"
GEN_9_DLC = "Scarlet/Violet - The Treasure of Area Zero"

masuda_games = [
    GEN_4_PRIMARY,
    GEN_4_REMAKE,
    GEN_5_PRIMARY,
    GEN_6_PRIMARY,
    GEN_6_REMAKE,
    GEN_7_PRIMARY,
    GEN_7_SECONDARY,
    GEN_8_PRIMARY,
    GEN_8_DLC,
    GEN_8_REMAKE,
    GEN_9_PRIMARY,
    GEN_9_DLC
]

poke_radar = [
    GEN_4_PRIMARY,
    GEN_6_PRIMARY
]

chain_fishing = [
    GEN_6_PRIMARY,
    GEN_6_REMAKE
]

sos_chaining = [
    GEN_7_PRIMARY,
    GEN_7_SECONDARY
]

outbreaks = [
    GEN_8_SECONDARY,
    GEN_9_PRIMARY,
    GEN_9_DLC
]

class ShinyPokemonHuntGame(Game):
    name = "Shiny Pokémon Hunt"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = [
        KeymastersKeepGamePlatforms.GBC,
        KeymastersKeepGamePlatforms.GBA,
        KeymastersKeepGamePlatforms.GC,
        KeymastersKeepGamePlatforms.NDS,
        KeymastersKeepGamePlatforms._3DS,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False
    is_metagame = True

    options_cls = ShinyPokemonHuntArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [GameObjectiveTemplate(
            label="Complete at least one hunt in GAME",
            data={"GAME": (self.games, 1)}
        )]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives = [
            GameObjectiveTemplate(
                label="Encounter and capture a Shiny Pokémon",
                data={},
                is_time_consuming=True,
            ),
            GameObjectiveTemplate(
                label="Encounter and capture a Shiny Pokémon by soft-resetting a static encounter",
                data={},
                is_difficult=True, # it's not but it's exponentially more time consuming than the rest
                is_time_consuming=True,
            )
        ]
        if any(game in masuda_games for game in self.archipelago_options.shiny_pokemon_hunt_owned_games) or \
                (self.archipelago_options.include_modern_console_games and
                 GEN_8_REMAKE in self.archipelago_options.shiny_pokemon_hunt_owned_games):
            objectives.append(GameObjectiveTemplate(
                label="Hatch a Shiny Pokémon from an Egg",
                data={},
                is_time_consuming=True,
            ))
        if any(game in poke_radar for game in self.archipelago_options.shiny_pokemon_hunt_owned_games):
            objectives.append(GameObjectiveTemplate(
                label="Encounter and capture a Shiny Pokémon using the Poké Radar",
                data={},
                is_time_consuming=True,
            ))
        if any(game in chain_fishing for game in self.archipelago_options.shiny_pokemon_hunt_owned_games):
            objectives.extend([
                GameObjectiveTemplate(
                    label="Encounter and capture a Shiny Pokémon by chain fishing",
                    data={},
                    is_time_consuming=True,
                ),
                GameObjectiveTemplate(
                    label="Encounter and capture a Shiny Pokémon during a horde encounter",
                    data={},
                    is_time_consuming=True,
                )
            ])
        if GEN_6_PRIMARY in self.archipelago_options.shiny_pokemon_hunt_owned_games:
            objectives.append(GameObjectiveTemplate(
                label="Encounter and capture a Shiny Pokémon in the Friend Safari",
                data={},
                is_time_consuming=True,
            ))
        if GEN_6_REMAKE in self.archipelago_options.shiny_pokemon_hunt_owned_games:
            objectives.append(GameObjectiveTemplate(
                label="Encounter and capture a Shiny Pokémon by using DexNav",
                data={},
                is_time_consuming=True,
            ))
        if any(game in sos_chaining for game in self.archipelago_options.shiny_pokemon_hunt_owned_games):
            objectives.append(GameObjectiveTemplate(
                label="Encounter and capture a Shiny Pokémon by chaining SOS calls",
                data={},
                is_time_consuming=True,
            ))
        if GEN_7_SECONDARY in self.archipelago_options.shiny_pokemon_hunt_owned_games:
            objectives.append(GameObjectiveTemplate(
                label="Encounter and capture a Shiny Pokémon within an Ultra Wormhole",
                data={},
                is_time_consuming=True,
            ))
        if self.archipelago_options.include_modern_console_games:
            if GEN_7_REMAKE in self.archipelago_options.shiny_pokemon_hunt_owned_games:
                objectives.append(GameObjectiveTemplate(
                    label="Encounter and capture a Shiny Pokémon by maintaining a catch combo",
                    data={},
                    is_time_consuming=True,
                ))
            if GEN_8_DLC in self.archipelago_options.shiny_pokemon_hunt_owned_games:
                objectives.append(GameObjectiveTemplate(
                    label="Encounter and capture a Shiny Pokémon within a Dynamax Adventure",
                    data={},
                    is_time_consuming=True,
                ))
            if any(game in outbreaks for game in self.archipelago_options.shiny_pokemon_hunt_owned_games):
                objectives.append(GameObjectiveTemplate(
                    label="Encounter and capture a Shiny Pokémon within a mass outbreak",
                    data={},
                    is_time_consuming=True,
                ))

        return objectives

    def games(self):
        return sorted(self.archipelago_options.shiny_pokemon_hunt_owned_games.value)


class ShinyPokemonHuntOwnedGames(OptionSet):
    """Which games should be considered for special shiny hunting methods"""

    valid_keys = [
        GEN_2_PRIMARY,
        GEN_3_PRIMARY,
        GEN_3_REMAKE,
        GEN_3_SECONDARY,
        GEN_4_PRIMARY,
        GEN_4_REMAKE,
        GEN_5_PRIMARY,
        GEN_6_PRIMARY,
        GEN_6_REMAKE,
        GEN_7_PRIMARY,
        GEN_7_SECONDARY,
        GEN_7_REMAKE,
        GEN_8_PRIMARY,
        GEN_8_DLC,
        GEN_8_REMAKE,
        GEN_8_SECONDARY,
        GEN_9_PRIMARY,
        GEN_9_DLC,
    ]

    default = valid_keys

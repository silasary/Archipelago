from typing import Dict, Type

from dataclasses import dataclass

from ..game import Game

# Game Imports
from .a_dance_of_fire_and_ice_game import ADanceOfFireAndIceGame, ADanceOfFireAndIceArchipelagoOptions
from .anger_foot_game import AngerFootGame, AngerFootArchipelagoOptions
from .halls_of_torment_game import HallsOfTormentGame, HallsOfTormentArchipelagoOptions
from .neon_white_game import NeonWhiteGame, NeonWhiteArchipelagoOptions
from .pinball_fx3_game import PinballFX3Game, PinballFX3ArchipelagoOptions

from .placid_plastic_duck_simulator_game import (
    PlacidPlasticDuckSimulatorGame, PlacidPlasticDuckSimulatorArchipelagoOptions
)

from .star_wars_battlefront_ii_classic_game import (
    StarWarsBattlefrontIIClassicGame, StarWarsBattlefrontIIClassicArchipelagoOptions
)

from .street_fighter_6_game import StreetFighter6Game, StreetFighter6ArchipelagoOptions
from .trackmania_game import TrackmaniaGame, TrackmaniaArchipelagoOptions
from .trombone_champ_game import TromboneChampGame, TromboneChampArchipelagoOptions
from .ultrakill_game import UltrakillGame, UltrakillArchipelagoOptions

# Metagame Imports
from .archipelago_multiworld_randomizer_game import (
    ArchipelagoMultiworldRandomizerGame, ArchipelagoMultiworldRandomizerArchipelagoOptions
)

from .game_backlog_game import GameBacklogGame, GameBacklogArchipelagoOptions
from .retro_achievements_game import RetroAchievementsGame, RetroAchievementsArchipelagoOptions


games: Dict[str, Type[Game]] = {
    ADanceOfFireAndIceGame.game_name_with_platforms(): ADanceOfFireAndIceGame,
    AngerFootGame.game_name_with_platforms(): AngerFootGame,
    HallsOfTormentGame.game_name_with_platforms(): HallsOfTormentGame,
    NeonWhiteGame.game_name_with_platforms(): NeonWhiteGame,
    PinballFX3Game.game_name_with_platforms(): PinballFX3Game,
    PlacidPlasticDuckSimulatorGame.game_name_with_platforms(): PlacidPlasticDuckSimulatorGame,
    StarWarsBattlefrontIIClassicGame.game_name_with_platforms(): StarWarsBattlefrontIIClassicGame,
    StreetFighter6Game.game_name_with_platforms(): StreetFighter6Game,
    TrackmaniaGame.game_name_with_platforms(): TrackmaniaGame,
    TromboneChampGame.game_name_with_platforms(): TromboneChampGame,
    UltrakillGame.game_name_with_platforms(): UltrakillGame,
}

metagames: Dict[str, Type[Game]] = {
    ArchipelagoMultiworldRandomizerGame.game_name_with_platforms(): ArchipelagoMultiworldRandomizerGame,
    GameBacklogGame.game_name_with_platforms(): GameBacklogGame,
    RetroAchievementsGame.game_name_with_platforms(): RetroAchievementsGame,
}


@dataclass
class GameArchipelagoOptions(
    # Add in reverse alphabetical order
    UltrakillArchipelagoOptions,
    TromboneChampArchipelagoOptions,
    TrackmaniaArchipelagoOptions,
    StreetFighter6ArchipelagoOptions,
    StarWarsBattlefrontIIClassicArchipelagoOptions,
    RetroAchievementsArchipelagoOptions,
    PlacidPlasticDuckSimulatorArchipelagoOptions,
    PinballFX3ArchipelagoOptions,
    NeonWhiteArchipelagoOptions,
    HallsOfTormentArchipelagoOptions,
    GameBacklogArchipelagoOptions,
    ArchipelagoMultiworldRandomizerArchipelagoOptions,
    AngerFootArchipelagoOptions,
    ADanceOfFireAndIceArchipelagoOptions,
):
    pass

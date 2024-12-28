from typing import Dict, Type

from dataclasses import dataclass

from ..game import Game

# Game Imports
from .anger_foot_game import AngerFootGame, AngerFootArchipelagoOptions

from .archipelago_multiworld_randomizer_game import (
    ArchipelagoMultiworldRandomizerGame, ArchipelagoMultiworldRandomizerArchipelagoOptions
)

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

# Metagame Imports
from .game_backlog_game import GameBacklogGame, GameBacklogArchipelagoOptions


games: Dict[str, Type[Game]] = {
    AngerFootGame.game_name_with_platforms(): AngerFootGame,
    ArchipelagoMultiworldRandomizerGame.game_name_with_platforms(): ArchipelagoMultiworldRandomizerGame,
    NeonWhiteGame.game_name_with_platforms(): NeonWhiteGame,
    PinballFX3Game.game_name_with_platforms(): PinballFX3Game,
    PlacidPlasticDuckSimulatorGame.game_name_with_platforms(): PlacidPlasticDuckSimulatorGame,
    StarWarsBattlefrontIIClassicGame.game_name_with_platforms(): StarWarsBattlefrontIIClassicGame,
    StreetFighter6Game.game_name_with_platforms(): StreetFighter6Game,
    TrackmaniaGame.game_name_with_platforms(): TrackmaniaGame,
    TromboneChampGame.game_name_with_platforms(): TromboneChampGame,
}

metagames: Dict[str, Type[Game]] = {
    GameBacklogGame.game_name_with_platforms(): GameBacklogGame,
}


@dataclass
class GameArchipelagoOptions(
    # Add in reverse alphabetical order
    TromboneChampArchipelagoOptions,
    TrackmaniaArchipelagoOptions,
    StreetFighter6ArchipelagoOptions,
    StarWarsBattlefrontIIClassicArchipelagoOptions,
    PlacidPlasticDuckSimulatorArchipelagoOptions,
    PinballFX3ArchipelagoOptions,
    NeonWhiteArchipelagoOptions,
    GameBacklogArchipelagoOptions,
    ArchipelagoMultiworldRandomizerArchipelagoOptions,
    AngerFootArchipelagoOptions,
):
    pass

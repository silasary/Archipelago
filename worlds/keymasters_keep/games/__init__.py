from typing import Dict, Type

from dataclasses import dataclass

from ..game import Game

# Game Imports
from .archipelago_multiworld_randomizer_game import (
    ArchipelagoMultiworldRandomizerGame, ArchipelagoMultiworldRandomizerArchipelagoOptions
)

from .street_fighter_6_game import StreetFighter6Game, StreetFighter6ArchipelagoOptions

# Metagame Imports
from .game_backlog_game import GameBacklogGame, GameBacklogArchipelagoOptions


games: Dict[str, Type[Game]] = {
    ArchipelagoMultiworldRandomizerGame.game_name_with_platforms(): ArchipelagoMultiworldRandomizerGame,
    StreetFighter6Game.game_name_with_platforms(): StreetFighter6Game,
}

metagames: Dict[str, Type[Game]] = {
    GameBacklogGame.game_name_with_platforms(): GameBacklogGame,
}


@dataclass
class GameArchipelagoOptions(
    # Add in reverse alphabetical order
    StreetFighter6ArchipelagoOptions,
    GameBacklogArchipelagoOptions,
    ArchipelagoMultiworldRandomizerArchipelagoOptions,
):
    pass

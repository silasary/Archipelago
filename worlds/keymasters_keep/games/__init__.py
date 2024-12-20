from typing import Dict, Type

from dataclasses import dataclass

from ..game import Game

from .street_fighter_6_game import StreetFighter6Game, StreetFighter6ArchipelagoOptions

from .game_backlog_game import GameBacklogGame, GameBacklogArchipelagoOptions


games: Dict[str, Type[Game]] = {
    StreetFighter6Game.game_name_with_platforms(): StreetFighter6Game,
}

metagames: Dict[str, Type[Game]] = {
    GameBacklogGame.game_name_with_platforms(): GameBacklogGame,
}


@dataclass
class GameArchipelagoOptions(
    GameBacklogArchipelagoOptions,
    StreetFighter6ArchipelagoOptions
):
    pass

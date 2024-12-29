import pkgutil
from typing import List, Type

from dataclasses import dataclass

from ..game import AutoGameRegister

from pkgutil import iter_modules
from importlib import import_module

for game in iter_modules(__path__):
    import_module(f".{game.name}", __package__)


option_classes: List[Type] = []

for name, game in [*sorted(AutoGameRegister.games.items(), reverse=True),
                   *sorted(AutoGameRegister.metagames.items(), reverse=True)]:
    if game.options_cls:
        option_classes.append(game.options_cls)


@dataclass
class GameArchipelagoOptions(
    # Add in reverse alphabetical order
    *option_classes
):
    pass

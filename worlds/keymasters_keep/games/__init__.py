from typing import List, Type

from dataclasses import dataclass
from importlib import import_module
from pkgutil import iter_modules

from ..game import AutoGameRegister, Game

for game_module_info in iter_modules(__path__):
    import_module(f".{game_module_info.name}", __package__)


option_classes: List[Type] = list()

# Reverse order here is needed so that the options are added in alphabetical order in the YAML
game_cls: Type[Game]
for _, game_cls in sorted(AutoGameRegister.games.items(), reverse=True):
    option_classes.append(game_cls.options_cls)


@dataclass
class GameArchipelagoOptions(*option_classes):
    pass

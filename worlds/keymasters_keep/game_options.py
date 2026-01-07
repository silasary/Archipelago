import dataclasses
import sys
import typing

from Options import OptionGroup

from .games import AutoGameRegister, Game

# We need to "move" options classes into a file that ends with options.py because Utils.restricted_dumps complains if we don't
this = sys.modules[__name__]

option_classes: list[type] = []
game_option_groups: list[OptionGroup] = []

game_cls: type[Game]
for name, game_cls in sorted(AutoGameRegister.games.items()):
    option_classes.append(game_cls.options_cls)
    options = list(typing.get_type_hints(game_cls.options_cls).values())
    if options:
        game_option_groups.append(OptionGroup(name, options))
        for opt in options:
            if not hasattr(this, opt.__name__):
                setattr(this, opt.__name__, opt)
                mod = sys.modules[opt.__module__]
                opt.__module__ = __name__
    setattr(this, game_cls.options_cls.__name__, game_cls.options_cls)
    game_cls.options_cls.__module__ = __name__

@dataclasses.dataclass
class GameArchipelagoOptions(*option_classes):
    pass


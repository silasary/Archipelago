from typing import List, Type

import dataclasses
import importlib.machinery
import importlib.util
import pathlib
import pkgutil
import sys
import types

from importlib import import_module
import typing

from Options import OptionGroup
from Utils import user_path

from ..game import AutoGameRegister, Game

# Bundled games
for game_module_info in pkgutil.iter_modules(__path__):
    import_module(f".{game_module_info.name}", __package__)

# External games
games_path: pathlib.Path = pathlib.Path(user_path("keymasters_keep"))

broken_games: List[str] = list()
broken_games_path: pathlib.Path = games_path / "_broken_games.txt"

game_path: pathlib.Path
for game_path in games_path.glob("*.py"):
    module_name: str = f"worlds.keymasters_keep.games.{game_path.stem}"
    module_spec: importlib.machinery.ModuleSpec = importlib.util.spec_from_file_location(module_name, str(game_path))
    module: types.ModuleType = importlib.util.module_from_spec(module_spec)

    try:
        sys.modules[module_name] = module
        module_spec.loader.exec_module(module)
    except Exception:
        broken_games.append(game_path.name)

if broken_games_path.exists():
    broken_games_path.unlink()

if len(broken_games):
    with open(broken_games_path, "w") as f:
        f.write(
            f"The following Keymaster's Keep games could not be loaded and are likely broken:\n\n" +
            "\n".join(broken_games)
        )

    raise RuntimeError("Some Keymaster's Keep games could not be loaded. See broken_games.txt for details.")

# Archipelago options
option_classes: list[type] = []
game_option_groups: list[OptionGroup] = []

game_cls: type[Game]
for name, game_cls in sorted(AutoGameRegister.games.items()):
    option_classes.append(game_cls.options_cls)
    options = list(typing.get_type_hints(game_cls.options_cls).values())
    if options:
        game_option_groups.append(OptionGroup(name, options))


@dataclasses.dataclass
class GameArchipelagoOptions(*option_classes):
    pass

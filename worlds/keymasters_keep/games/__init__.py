import importlib.machinery
import importlib.util
import logging
import pathlib
import pkgutil
import sys
import types
from importlib import import_module

from Utils import user_path

bundled_names: list[str] = []

# Bundled games
for game_module_info in pkgutil.iter_modules(__path__):
    import_module(f".{game_module_info.name}", __package__)
    bundled_names.append(game_module_info.name)

# External games
games_path: pathlib.Path = pathlib.Path(user_path("keymasters_keep"))

broken_games: list[str] = []
broken_games_path: pathlib.Path = games_path / "_broken_games.txt"

game_path: pathlib.Path
for game_path in games_path.glob("*.py"):
    if game_path.stem in bundled_names:
        logging.warning(f"Overriding bundled Keymaster's Keep game: {game_path.stem} with external version.")
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

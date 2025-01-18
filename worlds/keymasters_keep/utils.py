from typing import Dict, List, Type

from .data.mapping_data import label_mapping
from .enums import KeymastersKeepGamePlatforms
from .game import Game
from .games import AutoGameRegister


def generate_docs_supported_games() -> None:
    count_games: int = len(AutoGameRegister.games)
    count_metagames: int = len(AutoGameRegister.metagames)
    count_modded_games: int = len(AutoGameRegister.modded_games)

    count_total: int = count_games + count_metagames + count_modded_games

    with open("worlds/keymasters_keep/Supported Games.md", "w", encoding="utf-8") as f:
        f.truncate(0)

        f.write("# Keymaster's Keep Supported Games\n\n")

        f.write(
            f"Keymaster's Keep currently supports {count_total} games "
            f"({count_games} + {count_metagames} metagames + {count_modded_games} modded games).\n\n"
        )

        f.write(f"### Metagames Supported ({count_metagames})\n")

        game: str
        for game in sorted(AutoGameRegister.metagames.keys()):
            f.write(f"* {game}\n")

        f.write("\n")

        f.write(f"### Games Supported ({count_games})\n")

        game: str
        for game in sorted(AutoGameRegister.games.keys()):
            f.write(f"* {game}\n")

        f.write("\n")

        f.write(f"### Modded Games Supported ({count_modded_games})\n")

        game: str
        for game in sorted(AutoGameRegister.modded_games.keys()):
            f.write(f"* {game}\n")


def generate_docs_supported_games_by_platform() -> None:
    count_games: int = len(AutoGameRegister.games)
    count_metagames: int = len(AutoGameRegister.metagames)
    count_modded_games: int = len(AutoGameRegister.modded_games)

    count_total: int = count_games + count_metagames + count_modded_games

    games_by_platform: Dict[KeymastersKeepGamePlatforms, List[str]] = dict()

    item: KeymastersKeepGamePlatforms
    for item in KeymastersKeepGamePlatforms:
        games_by_platform[item] = list()

    games: Dict[str, Type[Game]] = AutoGameRegister.games

    games.update(AutoGameRegister.metagames)
    games.update(AutoGameRegister.modded_games)

    game: Type[Game]
    for game in games.values():
        games_by_platform[game.platform].append(game.name)

        if game.platforms_other is not None:
            platform: KeymastersKeepGamePlatforms
            for platform in game.platforms_other:
                games_by_platform[platform].append(game.name)

    filtered_games_by_platform: Dict[KeymastersKeepGamePlatforms, List[str]] = dict()

    platform: KeymastersKeepGamePlatforms
    games: List[str]
    for platform, games in games_by_platform.items():
        if len(games):
            filtered_games_by_platform[platform] = games

    platform_labels: Dict[KeymastersKeepGamePlatforms, str] = dict()

    platform: KeymastersKeepGamePlatforms
    for platform in filtered_games_by_platform.keys():
        platform_labels[label_mapping[platform]] = platform

    with open("worlds/keymasters_keep/Supported Games by Platform.md", "w", encoding="utf-8") as f:
        f.truncate(0)

        f.write("# Keymaster's Keep Supported Games by Platform\n\n")

        f.write(
            f"Keymaster's Keep currently supports {count_total} games "
            f"({count_games} + {count_metagames} metagames + {count_modded_games} modded games).\n\n"
        )

        platform_label: str
        for platform_label in sorted(platform_labels.keys()):
            f.write(f"### {platform_label} ({len(filtered_games_by_platform[platform_labels[platform_label]])})\n")

            game: str
            for game in sorted(filtered_games_by_platform[platform_labels[platform_label]]):
                f.write(f"* {game}\n")

            f.write("\n")

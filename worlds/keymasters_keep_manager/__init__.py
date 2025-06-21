import os

import worlds.LauncherComponents as LauncherComponents

from Utils import user_path


games_path: str = user_path("keymasters_keep")

if not os.path.exists(games_path):
    os.makedirs(games_path)

repositories_path: str = os.path.join(games_path, "repositories.txt")

if not os.path.exists(repositories_path):
    with open(repositories_path, "w") as repositories_file:
        repositories_file.writelines([
            "SerpentAI/KeymastersKeepGames\n",
            "SerpentAI/KeymastersKeepGameArchive",
        ])


downloads_path: str = os.path.join(games_path, "downloads")

if not os.path.exists(downloads_path):
    os.makedirs(downloads_path)


def launch_app() -> None:
    from .app import main
    LauncherComponents.launch(main, name="KeymastersKeepManager")


LauncherComponents.components.append(
    LauncherComponents.Component(
        "Keymaster's Keep Manager",
        func=launch_app,
        component_type=LauncherComponents.Type.TOOL
    )
)

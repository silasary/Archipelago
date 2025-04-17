from typing import ClassVar
from settings import Group
from worlds.LauncherComponents import Component, Type, components, launch_subprocess

from worlds.AutoWorld import World

class ManagerSettings(Group):
    """
    repositories: A list of Repository URLs and whether they're enabled or not.
    github_token: A github Personal Access Token with the `repo` scope to allow for more requests to the GitHub API. This lets you avoid rate limits if you use GitHub repos."""
    repositories: dict = {"https://raw.githubusercontent.com/silasary/apworlds/refs/heads/main/index.json": True}
    github_token: str = ""

class RepoWorld(World):
    """
    Package manager for Archipelago Worlds
    """
    settings: ClassVar[ManagerSettings]
    settings_key = "apworld_manager"
    world_version = "0.0.7"

    # to make auto world register happy so we can register our settings
    game = "APWorld Manager"
    hidden = True
    item_name_to_id = {}
    location_name_to_id = {}

def launch_client():
    from .kv_app import launch
    launch_subprocess(launch, name="APManager")

components.append(Component("Install/Update Apworlds", None, func=launch_client, component_type=Type.TOOL))

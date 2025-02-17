from typing import ClassVar, List
from settings import Group
from worlds.LauncherComponents import Component, Type, components, launch_subprocess

from worlds.AutoWorld import World

class ManagerSettings(Group):
    repositories: dict = {"https://raw.githubusercontent.com/silasary/apworlds/refs/heads/main/index.json": True}

class RepoWorld(World):
    settings: ClassVar[ManagerSettings]
    settings_key = "apworld_manager"

    # to make auto world register happy so we can register our settings
    game = "APWorld Manager"
    hidden = True
    item_name_to_id = {}
    location_name_to_id = {}

def launch_client():
    from .kv_app import launch
    launch_subprocess(launch, name="APManager")

components.append(Component("Install/Update Apworlds", None, func=launch_client, component_type=Type.TOOL))

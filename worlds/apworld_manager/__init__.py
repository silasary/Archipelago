from worlds.LauncherComponents import Component, Type, components

from worlds.AutoWorld import World


class RepoWorld(World):
    # settings: ClassVar[ManagerSettings]
    # settings_key = "apworld_manager"

    # to make auto world register happy so we can register our settings
    game = "APWorld Manager"
    hidden = True
    item_name_to_id = {}
    location_name_to_id = {}

def launch_client():
    from .apworld_directory import launch
    launch()

components.append(Component("Install/Update Apworlds", None, func=launch_client, component_type=Type.TOOL))


from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client():
    from .TrackerClient import launch as TCMain
    launch_subprocess(TCMain, name="Universal Tracker client")

class TrackerWorld:
    pass

components.append(Component("Universal Tracker", "Univeral Tracker client", func=launch_client, component_type=Type.CLIENT))

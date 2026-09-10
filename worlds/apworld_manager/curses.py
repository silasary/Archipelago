from utils.curses_utils import curses_select
from .world_manager import SortStages, install_world, RepositoryManager, parse_version, refresh_apworld_table, repositories


def launch(apworlds):
    worlds_list = [
        "{0:<50}|{1:<45}|{2:<25}".format(
            w["title"][:50],
            w["description"][:45],
            w["install_text"][:25],
        ) for w in apworlds]
    key = lambda index: apworlds[index]

    world = curses_select(worlds_list, key=key, max_height=30, max_length=120)
    if world is None:
        return

    install_world(world)
    print(f"updated {world['title']} to version {world['latest_version'].data['metadata']['world_version']}")

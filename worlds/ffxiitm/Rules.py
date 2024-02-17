from typing import TYPE_CHECKING

from BaseClasses import CollectionState, MultiWorld, LocationProgressType
from worlds.generic.Rules import add_rule, set_rule
from .Locations import get_locations_by_category

if TYPE_CHECKING:
    from worlds.ffxiitm import FFXIITMWorld

def has_item(state: CollectionState, player: int, item) -> bool:
    return state.has(item, player)

def set_rules(world: "FFXIITMWorld", player: int):
    # Win condition.
    world.multiworld.completion_condition[player] = lambda state: state.has_all({"Victory"}, player)
    max_floor = world.get_setting("trial_victory")

    def get_entrance(entrance: str):
        return world.multiworld.get_entrance(entrance, world.player)

    if max_floor > 10:
        set_rule(
            get_entrance("Trial 010"),
            lambda state: state.has("Second Job", world.player)
        )
    if max_floor > 20:
        set_rule(
            get_entrance("Trial 020"),
            lambda state: state.count_group("Equipment", world.player) >= 4
        )
    if max_floor > 30:
        set_rule(
            get_entrance("Trial 030"),
            lambda state: state.count_group("Magick", world.player) >= 4
        )
    if max_floor > 40:
        set_rule(
            get_entrance("Trial 040"),
            lambda state: state.count_group("Technick", world.player) >= 4
        )

    if max_floor > 50:
        for floor in range(2, max_floor // 10):
            set_rule(
                get_entrance(f"Trial {str(floor * 10).rjust(3, '0')}"),
                lambda state: state.count_group("Equipment", world.player) + state.count_group("Magick", world.player) + state.count_group("Technick", world.player) + state.count_group("Mist", world.player) >= floor
            )

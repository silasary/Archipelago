from BaseClasses import CollectionState, MultiWorld, LocationProgressType
from .Locations import get_locations_by_category

def has_item(state: CollectionState, player: int, item) -> bool:
    return state.has(item, player)

def set_rules(multiworld: MultiWorld, player: int):
    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has_all({"Victory"}, player)

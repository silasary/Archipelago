from typing import Dict, List, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import FFXIITMLocation, location_table, get_locations_by_category, chests, event_location_table

if TYPE_CHECKING:
    from . import FFXIITMWorld

class FFXIITMRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, world: "FFXIITMWorld", player: int, max_trial_floor: int):
    regions: Dict[str, FFXIITMRegionData] = {
        "Menu":        FFXIITMRegionData(None ,["Trial 001"]),
        }
    for trial in range(1, 101):
        if trial > max_trial_floor:
            break
        trial_padded = str(trial).rjust(3, "0")
        if trial > 1:
            regions[f"Trial {str(trial - 1).rjust(3, '0')}"].region_exits.append(f"Trial {trial_padded}")
        regions[f"Trial {trial_padded}"] = FFXIITMRegionData([],[])
        for chest in range(1, chests[trial] + 1):
            regions[f"Trial {trial_padded}"].locations.append(f"Trial {trial_padded} Chest {chest}-1")
            regions[f"Trial {trial_padded}"].locations.append(f"Trial {trial_padded} Chest {chest}-2")

    # Set up the regions correctly.
    for name, data in regions.items():
        print(name)
        multiworld.regions.append(create_region(multiworld, world, player, name, data))

    for trial in range(1, 101):
        if trial > max_trial_floor:
            break
        trial_padded = str(trial).rjust(3, "0")
        multiworld.get_entrance(f"Trial {trial_padded}", player).connect(multiworld.get_region(f"Trial {trial_padded}", player))

def create_region(multiworld: MultiWorld, world: "FFXIITMWorld", player: int, name: str, data: FFXIITMRegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = FFXIITMLocation(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)
    # if name != "Menu":
    #     event = FFXIITMLocation(player, f'Reach {name}', None, region)
    #     event.place_locked_item(world.create_event(f'Reach {name}'))
    #     region.locations.append(event)

    if data.region_exits:
        for exit in data.region_exits:
            entrance = Entrance(player, exit, region)
            region.exits.append(entrance)

    return region

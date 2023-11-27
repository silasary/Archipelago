from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import FFXIITMLocation, location_table, get_locations_by_category


class FFXIITMRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int):
    regions: Dict[str, RLRegionData] = {
        "Menu":        FFXIITMRegionData(None, ["Trial Mode"]),
        "Trial Mode":  FFXIITMRegionData([], []),
    }

    # Set up locations
    
    regions["Trial Mode"].locations.append("Trial 001 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 001 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 002 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 002 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 003 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 003 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 004 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 004 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 005 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 005 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 006 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 006 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 007 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 007 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 008 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 008 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 009 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 009 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 010 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 010 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 011 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 011 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 012 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 012 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 013 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 013 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 014 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 014 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 015 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 015 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 016 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 016 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 017 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 017 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 018 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 018 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 019 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 019 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 020 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 020 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 021 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 021 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 022 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 022 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 023 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 023 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 024 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 024 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 025 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 025 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 026 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 026 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 027 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 027 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 028 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 028 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 029 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 029 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 030 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 030 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 030 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 031 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 031 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 031 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 031 Chest 4"),
    regions["Trial Mode"].locations.append("Trial 031 Chest 5"),
    regions["Trial Mode"].locations.append("Trial 032 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 032 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 032 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 033 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 033 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 034 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 034 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 035 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 035 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 035 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 035 Chest 4"),
    regions["Trial Mode"].locations.append("Trial 036 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 036 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 036 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 037 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 037 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 038 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 038 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 039 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 039 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 040 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 040 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 041 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 041 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 042 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 042 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 043 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 043 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 044 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 044 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 045 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 045 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 046 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 046 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 047 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 047 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 048 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 048 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 049 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 049 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 050 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 050 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 051 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 051 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 052 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 052 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 053 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 053 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 054 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 054 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 055 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 055 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 056 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 056 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 057 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 057 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 058 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 058 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 059 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 059 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 060 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 060 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 061 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 061 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 062 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 062 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 062 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 062 Chest 4"),
    regions["Trial Mode"].locations.append("Trial 063 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 063 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 064 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 064 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 065 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 065 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 066 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 066 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 067 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 067 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 068 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 068 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 069 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 069 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 070 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 070 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 071 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 071 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 072 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 072 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 073 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 073 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 074 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 074 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 075 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 075 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 076 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 076 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 077 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 077 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 078 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 078 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 079 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 079 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 080 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 080 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 081 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 081 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 082 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 082 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 082 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 083 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 083 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 083 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 084 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 084 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 084 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 085 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 085 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 085 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 086 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 086 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 086 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 087 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 087 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 087 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 087 Chest 4"),
    regions["Trial Mode"].locations.append("Trial 088 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 088 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 088 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 089 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 089 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 090 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 090 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 091 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 091 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 091 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 091 Chest 4"),
    regions["Trial Mode"].locations.append("Trial 092 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 092 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 092 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 093 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 093 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 094 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 094 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 094 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 095 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 096 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 096 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 097 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 097 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 097 Chest 3"),
    regions["Trial Mode"].locations.append("Trial 097 Chest 4"),
    regions["Trial Mode"].locations.append("Trial 099 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 100 Chest 1"),
    regions["Trial Mode"].locations.append("Trial 100 Chest 2"),
    regions["Trial Mode"].locations.append("Trial 100 Chest 3"),
    
    # Set up the regions correctly.
    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))

    multiworld.get_entrance("Trial Mode", player).connect(multiworld.get_region("Trial Mode", player))


def create_region(multiworld: MultiWorld, player: int, name: str, data: FFXIITMRegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = FFXIITMLocation(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)

    if data.region_exits:
        for exit in data.region_exits:
            entrance = Entrance(player, exit, region)
            region.exits.append(entrance)

    return region
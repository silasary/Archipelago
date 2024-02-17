from typing import Dict, NamedTuple, Optional
import typing


from BaseClasses import Location


class FFXIITMLocation(Location):
    game: str = "Final Fantasy XII Trial Mode"

    @property
    def hint_text(self) -> str:
        return "at " + self.name.replace("_", " ")


class FFXIITMLocationData(NamedTuple):
    category: str
    code: Optional[int] = None


def get_locations_by_category(category: str) -> Dict[str, FFXIITMLocationData]:
    location_dict: Dict[str, FFXIITMLocationData] = {}
    for name, data in location_table.items():
        if data.category == category:
            location_dict.setdefault(name, data)

    return location_dict

chests = {i: 2 for i in range(1, 101)}
chests[30] = 3
chests[31] = 5
chests[32] = 3
chests[35] = 4
chests[36] = 3
chests[62] = 4
chests[82] = 3
chests[83] = 3
chests[84] = 3
chests[85] = 3
chests[86] = 3
chests[87] = 4
chests[88] = 3
chests[91] = 4
chests[92] = 3
chests[94] = 3
chests[95] = 1
chests[97] = 4
chests[98] = 0
chests[99] = 1
chests[100] = 3

location_table: Dict[str, FFXIITMLocationData] = {}
for trial, chest_count in chests.items():
    for chest in range(1, chest_count + 1):
        trial_padded = str(trial).rjust(3, "0")
        location_name = f"Trial {trial_padded} Chest {chest}"
        location_table[location_name + '-1'] = FFXIITMLocationData(f"Trial {trial_padded}", 45_0000 + trial * 10 + chest)
        location_table[location_name + '-2'] = FFXIITMLocationData(f"Trial {trial_padded}", 45_0000 + trial * 10 + chest + 5)

event_location_table: Dict[str, FFXIITMLocationData] = {f'Reach Trial {str(trial).rjust(3, "0")}': FFXIITMLocationData("Event", None)
                                                        for trial in range(1, 101)
}


lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}

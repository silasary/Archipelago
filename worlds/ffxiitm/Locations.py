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

map_ids = {
    1155: 1,
    1156: 2,
    1157: 3,
    1158: 4,
    1159: 5,
    1163: 6,
    1164: 7,
    1165: 8,
    1166: 9,
    1167: 10,
    1171: 11,
    1172: 12,
    1173: 13,
    1174: 14,
    1175: 15,
    1179: 16,
    1180: 17,
    1181: 18,
    1182: 19,
    1183: 20,
    1187: 21,
    1188: 22,
    1189: 23,
    1190: 24,
    1191: 25,
    1195: 26,
    1196: 27,
    1197: 28,
    1198: 29,
    1199: 30,
    1203: 31,
    1204: 32,
    1205: 33,
    1206: 34,
    1207: 35,
    1211: 36,
    1212: 37,
    1213: 38,
    1214: 39,
    1215: 40,
    1219: 41,
    1220: 42,
    1221: 43,
    1222: 44,
    1223: 45,
    1227: 46,
    1228: 47,
    1229: 48,
    1230: 49,
    1231: 50,
    1235: 51,
    1236: 52,
    1237: 53,
    1238: 54,
    1239: 55,
    1243: 56,
    1244: 57,
    1245: 58,
    1246: 59,
    1247: 60,
    1251: 61,
    1252: 62,
    1253: 63,
    1254: 64,
    1255: 65,
    1259: 66,
    1260: 67,
    1261: 68,
    1262: 69,
    1263: 70,
    1267: 71,
    1268: 72,
    1269: 73,
    1270: 74,
    1271: 75,
    1275: 76,
    1276: 77,
    1277: 78,
    1278: 79,
    1279: 80,
    1283: 81,
    1284: 82,
    1285: 83,
    1286: 84,
    1287: 85,
    1291: 86,
    1292: 87,
    1293: 88,
    1294: 89,
    1295: 90,
    1299: 91,
    1300: 92,
    1301: 93,
    1302: 94,
    1303: 95,
    1307: 96,
    1308: 97,
    1309: 98,
    1310: 99,
    1311: 100,
}

location_table: Dict[str, FFXIITMLocationData] = {}
for trial, chest_count in chests.items():
    for chest in range(1, chest_count + 1):
        trial_padded = str(trial).rjust(3, "0")
        location_name = f"Trial {trial_padded} Chest {chest}"
        location_table[location_name + '-1'] = FFXIITMLocationData(f"Trial {trial_padded}", 45_0000 + trial * 10 + chest)
        location_table[location_name + '-2'] = FFXIITMLocationData(f"Trial {trial_padded}", 45_0000 + trial * 10 + chest + 5)

# progress_locations: Dict[str, FFXIITMLocationData] = {f'Reach Trial {str(trial).rjust(3, "0")}': FFXIITMLocationData("Event", 45_0000 + trial * 10)
#                                                         for trial in range(1, 101)
# }
# location_table.update(progress_locations)

event_location_table: Dict[str, FFXIITMLocationData] = {}


lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}

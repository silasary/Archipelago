from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, ItemClassification


FF12OW_BASE_ID = 760701597784


class FF12OpenWorldItem(Item):
    game: str = "Final Fantasy 12 Open World"


class FF12OpenWorldItemData(NamedTuple):
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    weight: int = 0
    amount: int = 1
    duplicateAmount: int = 1


item_data_table: Dict[str, FF12OpenWorldItemData] = {
    "Potion": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 0,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Hi-Potion": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 1,
        classification=ItemClassification.filler,
        weight=5
    ),
    "X-Potion": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 2,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Ether": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 3,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Hi-Ether": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Elixir": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 5,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Phoenix Down": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 6,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Gold Needle": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 7,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Echo Herbs": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Antidote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 9,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Eye Drops": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 10,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Prince's Kiss": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 11,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Handkerchief": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Chronos Tear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 13,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Nu Khai Sand": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 14,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Serum": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 15,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Remedy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Soleil Fang": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 17,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Rime Fang": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 18,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Lightning Fang": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 19,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Bacchus's Wine": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 20,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Megalixir": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 21,
        classification=ItemClassification.filler
    ),
    "Baltoro Seed": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 22,
        classification=ItemClassification.filler
    ),
    "Domaine Calvados": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 23,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Dark Energy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 24,
        classification=ItemClassification.filler
    ),
    "Meteorite A": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 25,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Meteorite B": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 26,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Meteorite C": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 27,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Meteorite D": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 28,
        classification=ItemClassification.filler
    ),
    "Reverse Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 42,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Dark Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 43,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Aero Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 44,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Aquara Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 45,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Bio Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 46,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Shock Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 47,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Holy Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 48,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Scathe Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Balance Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 50,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Gravity Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 51,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Cura Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 52,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Dispel Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 53,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Aeroga Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 54,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Warp Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 55,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Bubble Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 56,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Hastega Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 57,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Reflectga Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 58,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Vanishga Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 59,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Float Mote": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 60,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Eksir Berries": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 61,
        classification=ItemClassification.filler,
        weight=20
    ),
    "Dark Matter": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 62,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Knot of Rust": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 63,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Broadsword": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4097,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Longsword": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4098,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Iron Sword": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4099,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Zwill Blade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4100,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Ancient Sword": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4101,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Blood Sword": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4102,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Lohengrin": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4103,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Flametongue": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4104,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Demonsbane": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4105,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Icebrand": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4106,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Platinum Sword": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4107,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Bastard Sword": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4108,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Diamond Sword": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4109,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Runeblade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4110,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Deathbringer": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4111,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Stoneblade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4112,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Durandal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4113,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Claymore": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4114,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Defender": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4115,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Save the Queen": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4116,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Ragnarok": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4117,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Ultima Blade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4118,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Excalibur": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4119,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Tournesol": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4120,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Kotetsu": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4121,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Osafune": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4122,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Kogarasumaru": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4123,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Magoroku": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4124,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Murasame": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4125,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Kiku-ichimonji": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4126,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Yakei": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4127,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Ame-no-Murakumo": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4128,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Muramasa": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4129,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Masamune": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4130,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ashura": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4131,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Sakura-saezuri": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4132,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Kagenui": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4133,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Koga Blade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4134,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Iga Blade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4135,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Orochi": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4136,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Yagyu Darkblade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4137,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Javelin": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4138,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Spear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4139,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Partisan": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4140,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Heavy Lance": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4141,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Storm Spear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4142,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Obelisk": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4143,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Halberd": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4144,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Trident": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4145,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Holy Lance": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4146,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Gungnir": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4147,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Dragon Whisker": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4148,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Zodiac Spear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4149,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Oaken Pole": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4150,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Cypress Pole": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4151,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Battle Bamboo": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4152,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Musk Stick": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4153,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Iron Pole": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4154,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Six-fluted Pole": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4155,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Gokuu Pole": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4156,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Zephyr Pole": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4157,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Ivory Pole": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4158,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Sweep": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4159,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Eight-fluted Pole": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4160,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Whale Whisker": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4161,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Shortbow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4162,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Silver Bow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4163,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Aevis Killer": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4164,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Killer Bow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4165,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Longbow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4166,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Elfin Bow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4167,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Loxley Bow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4168,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Giant Stonebow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4169,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Burning Bow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4170,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Traitor's Bow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4171,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Yoichi Bow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4172,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Perseus Bow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4173,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Artemis Bow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4174,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Sagittarius": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4175,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Bowgun": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4176,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Crossbow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4177,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Paramina Crossbow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4178,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Recurve Crossbow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4179,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Hunting Crossbow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4180,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Penetrator Crossbow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4181,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Gastrophetes": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4182,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Altair": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4183,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Capella": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4184,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Vega": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4185,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Sirius": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4186,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Betelgeuse": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4187,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Ras Algethi": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4188,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Aldebaran": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4189,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Spica": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4190,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Antares": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4191,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Arcturus": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4192,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Fomalhaut": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4193,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Handaxe": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4194,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Broadaxe": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4195,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Slasher": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4196,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Hammerhead": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4197,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Francisca": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4198,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Greataxe": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4199,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Golden Axe": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4200,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Iron Hammer": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4201,
        classification=ItemClassification.filler,
        weight=10
    ),
    "War Hammer": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4202,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Sledgehammer": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4203,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Morning Star": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4204,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Scorpion Tail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4205,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Dagger": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4206,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Mage Masher": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4207,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Assassin's Dagger": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4208,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Chopper": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4209,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Main Gauche": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4210,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Gladius": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4211,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Avenger": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4212,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Orichalcum Dirk": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4213,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Platinum Dagger": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4214,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Zwill Crossblade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4215,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Shikari Nagasa": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4216,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Rod": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4217,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Serpent Rod": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4218,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Healing Rod": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4219,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Gaia Rod": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4220,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Power Rod": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4221,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Empyrean Rod": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4222,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Holy Rod": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4223,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Rod of Faith": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4224,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Oak Staff": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4225,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Cherry Staff": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4226,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Wizard's Staff": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4227,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Flame Staff": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4228,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Storm Staff": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4229,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Glacial Staff": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4230,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Golden Staff": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4231,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Judicer's Staff": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4232,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Cloud Staff": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4233,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Staff of the Magi": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4234,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Mace": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4235,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Bronze Mace": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4236,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Bhuj": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4237,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Miter": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4238,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Thorned Mace": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4239,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Chaos Mace": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4240,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Doom Mace": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4241,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Zeus Mace": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4242,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Grand Mace": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4243,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Gilt Measure": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4244,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Arc Scale": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4245,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Multiscale": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4246,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Cross Scale": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4247,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Caliper": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4248,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Euclid's Sextant": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4249,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Hornito": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4250,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Fumarole": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4251,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Tumulus": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4252,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Caldera": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4253,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Volcano": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4254,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Bonebreaker": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4255,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Mythril Sword": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4256,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Mythril Blade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4264,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Kumbha": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4266,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Mesa": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4267,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Mina": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4268,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Wyrmhero Blade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4269,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Vrsabha": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4270,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Bone of Byblos": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4271,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Tula": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4272,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Great Trango": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4273,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Seitengrat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4274,
        classification=ItemClassification.filler
    ),
    "Karkata": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4288,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Excalipur": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4289,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Simha": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4290,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Makara": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4291,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Vrscika": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4292,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Mithuna": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4293,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Kanya": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4294,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Dhanusha": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4295,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Gendarme": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4296,
        classification=ItemClassification.filler
    ),
    "Leather Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4297,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Buckler": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4298,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Bronze Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4299,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Round Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4300,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Shell Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4301,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Golden Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4302,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Ice Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4303,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Flame Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4304,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Diamond Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4305,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Platinum Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4306,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Dragon Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4307,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Crystal Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4308,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Genji Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4309,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Kaiser Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4310,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Aegis Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4311,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Demon Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4312,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Venetian Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4313,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Zodiac Escutcheon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4314,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ensanguined Shield": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4315,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Leather Cap": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4316,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Headgear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4317,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Headguard": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4318,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Leather Headgear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4319,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Horned Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4320,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Balaclava": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4321,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Soldier's Cap": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4322,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Green Beret": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4323,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Red Cap": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4324,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Headband": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4325,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Pirate Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4326,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Goggle Mask": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4327,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Adamant Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4328,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Officer's Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4329,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Chakra Band": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4330,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Thief's Cap": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4331,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Gigas Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4332,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Chaperon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4333,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Crown of Laurels": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4334,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Renewing Morion": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4335,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Dueling Mask": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4336,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Cotton Cap": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4337,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Magick Curch": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4338,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Pointy Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4339,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Topkapi Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4340,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Calot Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4341,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Wizard's Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4342,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Lambent Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4343,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Feathered Cap": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4344,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Mage's Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4345,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Lamia's Tiara": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4346,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Sorcerer's Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4347,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Black Cowl": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4348,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Astrakhan Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4349,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Gaia Hat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4350,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Hypnocrown": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4351,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Gold Hairpin": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4352,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Celebrant's Miter": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4353,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Black Mask": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4354,
        classification=ItemClassification.filler,
        weight=2
    ),
    "White Mask": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4355,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Golden Skullcap": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4356,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Circlet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4357,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Leather Helm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4358,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Bronze Helm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4359,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Sallet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4360,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Iron Helm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4361,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Barbut": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4362,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Winged Helm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4363,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Golden Helm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4364,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Burgonet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4365,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Close Helmet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4366,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Bone Helm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4367,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Diamond Helm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4368,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Steel Mask": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4369,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Platinum Helm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4370,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Giant's Helmet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4371,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Dragon Helm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4372,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Genji Helm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4373,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Magepower Shishak": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4374,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Grand Helm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4375,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Leather Clothing": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4376,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Chromed Leathers": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4377,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Leather Breastplate": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4378,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Bronze Chestplate": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4379,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Ringmail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4380,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Windbreaker": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4381,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Heavy Coat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4382,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Survival Vest": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4383,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Brigandine": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4384,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Jujitsu Gi": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4385,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Viking Coat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4386,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Metal Jerkin": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4387,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Adamant Vest": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4388,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Barrel Coat": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4389,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Power Vest": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4390,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Ninja Gear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4391,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Gigas Chestplate": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4392,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Minerva Bustier": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4393,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Rubber Suit": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4394,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Mirage Vest": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4395,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Brave Suit": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4396,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Cotton Shirt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4397,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Light Woven Shirt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4398,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Silken Shirt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4399,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Kilimweave Shirt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4400,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Shepherd's Bolero": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4401,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Wizard's Robes": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4402,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Chanter's Djellaba": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4403,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Traveler's Vestment": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4404,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Mage's Habit": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4405,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Enchanter's Habit": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4406,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Sorcerer's Habit": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4407,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Black Garb": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4408,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Carmagnole": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4409,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Maduin Gear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4410,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Jade Gown": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4411,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Gaia Gear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4412,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Cleric's Robes": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4413,
        classification=ItemClassification.filler,
        weight=2
    ),
    "White Robes": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4414,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Black Robes": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4415,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Glimmering Robes": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4416,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Lordly Robes": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4417,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Leather Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4418,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Bronze Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4419,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Scale Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4420,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Iron Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4421,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Linen Cuirass": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4422,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Chainmail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4423,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Golden Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4424,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Shielded Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4425,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Demon Mail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4426,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Bone Mail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4427,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Diamond Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4428,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Mirror Mail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4429,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Platinum Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4430,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Carabineer Mail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4431,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Dragon Mail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4432,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Genji Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4433,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Maximillian": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4434,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Grand Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4435,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Opal Ring": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4436,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Ruby Ring": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4437,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Tourmaline Ring": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4438,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Sage's Ring": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4439,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Ring of Renewal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4440,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Agate Ring": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4441,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Bangle": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4442,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Orrachea Armlet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4443,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Power Armlet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4444,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Argyle Armlet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4445,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Diamond Armlet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4446,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Amber Armlet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4447,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Berserker Bracers": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4448,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Magick Gloves": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4449,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Thief's Cuffs": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4450,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Blazer Gloves": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4451,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Genji Gloves": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4452,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Gauntlets": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4453,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Turtleshell Choker": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4454,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Nihopalaoa": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4455,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Embroidered Tippet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4456,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Leather Gorget": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4457,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Jade Collar": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4458,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Steel Gorget": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4459,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Rose Corsage": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4460,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Pheasant Netsuke": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4461,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Indigo Pendant": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4462,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Golden Amulet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4463,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Bowline Sash": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4464,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Firefly": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4465,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Sash": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4466,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Bubble Belt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4467,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Cameo Belt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4468,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Nishijin Belt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4469,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Black Belt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4470,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Battle Harness": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4471,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Germinas Boots": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4472,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Hermes Sandals": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4473,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Gillie Boots": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4474,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Steel Poleyns": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4475,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Winged Boots": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4476,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Quasimodo Boots": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4477,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Cat-ear Hood": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4479,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Fuzzy Miter": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4480,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Ribbon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4481,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Onion Arrows": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4484,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Parallel Arrows": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4485,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Fiery Arrows": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4486,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Bamboo Arrows": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4487,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Lightning Arrows": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4488,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Assassin's Arrows": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4489,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Icecloud Arrows": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4490,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Artemis Arrows": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4491,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Onion Bolts": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4492,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Long Bolts": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4493,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Stone Bolts": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4494,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Lead Bolts": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4495,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Black Bolts": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4496,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Time Bolts": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4497,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Sapping Bolts": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4498,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Grand Bolts": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4499,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Onion Shot": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4500,
        classification=ItemClassification.filler,
        weight=14
    ),
    "Silent Shot": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4501,
        classification=ItemClassification.filler,
        weight=10
    ),
    "Aqua Shot": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4502,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Wyrmfire Shot": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4503,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Mud Shot": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4504,
        classification=ItemClassification.filler,
        weight=7
    ),
    "Windslicer Shot": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4505,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Dark Shot": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4506,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Stone Shot": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4507,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Onion Bombs": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4508,
        classification=ItemClassification.filler,
        weight=5
    ),
    "Poison Bombs": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4509,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Stun Bombs": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4510,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Oil Bombs": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4511,
        classification=ItemClassification.filler,
        weight=3
    ),
    "Chaos Bombs": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4512,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Stink Bombs": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4513,
        classification=ItemClassification.filler,
        weight=4
    ),
    "Water Bombs": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4514,
        classification=ItemClassification.filler,
        weight=2
    ),
    "Castellanos": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 4515,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Cure": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12288,
        classification=ItemClassification.useful
    ),
    "Blindna": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12289,
        classification=ItemClassification.useful
    ),
    "Vox": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12290,
        classification=ItemClassification.useful
    ),
    "Poisona": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12291,
        classification=ItemClassification.useful
    ),
    "Cura": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12292,
        classification=ItemClassification.useful
    ),
    "Raise": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12293,
        classification=ItemClassification.useful
    ),
    "Curaga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12294,
        classification=ItemClassification.useful
    ),
    "Stona": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12295,
        classification=ItemClassification.useful
    ),
    "Regen": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12296,
        classification=ItemClassification.useful
    ),
    "Cleanse": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12297,
        classification=ItemClassification.useful
    ),
    "Esuna": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12298,
        classification=ItemClassification.useful
    ),
    "Curaja": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12299,
        classification=ItemClassification.useful
    ),
    "Dispel": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12300,
        classification=ItemClassification.useful
    ),
    "Dispelga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12301,
        classification=ItemClassification.useful
    ),
    "Renew": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12302,
        classification=ItemClassification.useful
    ),
    "Arise": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12303,
        classification=ItemClassification.useful
    ),
    "Esunaga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12304,
        classification=ItemClassification.useful
    ),
    "Holy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12305,
        classification=ItemClassification.useful
    ),
    "Fire": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12306,
        classification=ItemClassification.useful
    ),
    "Thunder": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12307,
        classification=ItemClassification.useful
    ),
    "Blizzard": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12308,
        classification=ItemClassification.useful
    ),
    "Aqua": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12309,
        classification=ItemClassification.useful
    ),
    "Aero": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12310,
        classification=ItemClassification.useful
    ),
    "Fira": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12311,
        classification=ItemClassification.useful
    ),
    "Thundara": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12312,
        classification=ItemClassification.useful
    ),
    "Blizzara": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12313,
        classification=ItemClassification.useful
    ),
    "Bio": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12314,
        classification=ItemClassification.useful
    ),
    "Aeroga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12315,
        classification=ItemClassification.useful
    ),
    "Firaga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12316,
        classification=ItemClassification.useful
    ),
    "Thundaga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12317,
        classification=ItemClassification.useful
    ),
    "Blizzaga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12318,
        classification=ItemClassification.useful
    ),
    "Shock": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12319,
        classification=ItemClassification.useful
    ),
    "Scourge": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12320,
        classification=ItemClassification.useful
    ),
    "Flare": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12321,
        classification=ItemClassification.useful
    ),
    "Ardor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12322,
        classification=ItemClassification.useful
    ),
    "Scathe": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12323,
        classification=ItemClassification.useful
    ),
    "Haste": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12324,
        classification=ItemClassification.useful
    ),
    "Float": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12325,
        classification=ItemClassification.useful
    ),
    "Hastega": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12326,
        classification=ItemClassification.useful
    ),
    "Slow": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12327,
        classification=ItemClassification.useful
    ),
    "Immobilize": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12328,
        classification=ItemClassification.useful
    ),
    "Disable": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12329,
        classification=ItemClassification.useful
    ),
    "Bleed": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12330,
        classification=ItemClassification.useful
    ),
    "Break": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12331,
        classification=ItemClassification.useful
    ),
    "Stop": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12332,
        classification=ItemClassification.useful
    ),
    "Slowga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12333,
        classification=ItemClassification.useful
    ),
    "Countdown": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12334,
        classification=ItemClassification.useful
    ),
    "Reflect": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12335,
        classification=ItemClassification.useful
    ),
    "Reflectga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12336,
        classification=ItemClassification.useful
    ),
    "Balance": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12337,
        classification=ItemClassification.useful
    ),
    "Warp": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12338,
        classification=ItemClassification.useful
    ),
    "Protect": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12339,
        classification=ItemClassification.useful
    ),
    "Shell": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12340,
        classification=ItemClassification.useful
    ),
    "Bravery": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12341,
        classification=ItemClassification.useful
    ),
    "Faith": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12342,
        classification=ItemClassification.useful
    ),
    "Protectga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12343,
        classification=ItemClassification.useful
    ),
    "Shellga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12344,
        classification=ItemClassification.useful
    ),
    "Blind": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12345,
        classification=ItemClassification.useful
    ),
    "Oil": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12346,
        classification=ItemClassification.useful
    ),
    "Poison": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12347,
        classification=ItemClassification.useful
    ),
    "Silence": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12348,
        classification=ItemClassification.useful
    ),
    "Sleep": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12349,
        classification=ItemClassification.useful
    ),
    "Blindga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12350,
        classification=ItemClassification.useful
    ),
    "Toxify": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12351,
        classification=ItemClassification.useful
    ),
    "Silencega": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12352,
        classification=ItemClassification.useful
    ),
    "Sleepga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12353,
        classification=ItemClassification.useful
    ),
    "Reverse": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12354,
        classification=ItemClassification.useful
    ),
    "Berserk": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12355,
        classification=ItemClassification.useful
    ),
    "Death": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12356,
        classification=ItemClassification.useful
    ),
    "Confuse": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12357,
        classification=ItemClassification.useful
    ),
    "Decoy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12358,
        classification=ItemClassification.useful
    ),
    "Vanish": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12359,
        classification=ItemClassification.useful
    ),
    "Vanishga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12360,
        classification=ItemClassification.useful
    ),
    "Drain": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12361,
        classification=ItemClassification.useful
    ),
    "Syphon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12362,
        classification=ItemClassification.useful
    ),
    "Bubble": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12363,
        classification=ItemClassification.useful
    ),
    "Dark": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12364,
        classification=ItemClassification.useful
    ),
    "Darkra": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12365,
        classification=ItemClassification.useful
    ),
    "Darkga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12366,
        classification=ItemClassification.useful
    ),
    "Gravity": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12367,
        classification=ItemClassification.useful
    ),
    "Graviga": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 12368,
        classification=ItemClassification.useful
    ),
    "First Aid": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16384,
        classification=ItemClassification.useful
    ),
    "Shades of Black": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16385,
        classification=ItemClassification.useful
    ),
    "Horology": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16386,
        classification=ItemClassification.useful
    ),
    "Stamp": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16387,
        classification=ItemClassification.useful
    ),
    "Achilles": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16388,
        classification=ItemClassification.useful
    ),
    "Charge": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16389,
        classification=ItemClassification.useful
    ),
    "Infuse": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16390,
        classification=ItemClassification.useful
    ),
    "Souleater": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16391,
        classification=ItemClassification.useful
    ),
    "Wither": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16392,
        classification=ItemClassification.useful
    ),
    "Addle": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16393,
        classification=ItemClassification.useful
    ),
    "Bonecrusher": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16394,
        classification=ItemClassification.useful
    ),
    "Steal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16395,
        classification=ItemClassification.useful
    ),
    "Telekinesis": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16396,
        classification=ItemClassification.useful
    ),
    "Expose": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16397,
        classification=ItemClassification.useful
    ),
    "Shear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16398,
        classification=ItemClassification.useful
    ),
    "Charm": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16399,
        classification=ItemClassification.useful
    ),
    "Revive": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16400,
        classification=ItemClassification.useful
    ),
    "Sight Unseeing": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16401,
        classification=ItemClassification.useful
    ),
    "Numerology": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16402,
        classification=ItemClassification.useful
    ),
    "Libra": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16403,
        classification=ItemClassification.useful
    ),
    "Poach": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16404,
        classification=ItemClassification.useful
    ),
    "1000 Needles": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16405,
        classification=ItemClassification.useful
    ),
    "Traveler": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16406,
        classification=ItemClassification.useful
    ),
    "Gil Toss": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 16407,
        classification=ItemClassification.useful
    ),
    "Teleport Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8192,
        classification=ItemClassification.filler,
        weight=20
    ),
    "Earth Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8224,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Wind Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8225,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Water Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8226,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Fire Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8227,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ice Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8228,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Storm Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8229,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Holy Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8230,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Dark Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8231,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Earth Magicite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8232,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Wind Magicite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8233,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Water Magicite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8234,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Fire Magicite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8235,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ice Magicite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8236,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Storm Magicite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8237,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Holy Magicite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8238,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Dark Magicite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8239,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Earth Crystal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8240,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Wind Crystal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8241,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Water Crystal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8242,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Fire Crystal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8243,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ice Crystal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8244,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Storm Crystal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8245,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Holy Crystal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8246,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Dark Crystal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8247,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Aries Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8248,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Taurus Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8249,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Gemini Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8250,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Cancer Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8251,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Leo Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8252,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Virgo Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8253,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Libra Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8254,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Scorpio Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8255,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Sagittarius Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8256,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Capricorn Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8257,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Aquarius Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8258,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Pisces Gem": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8259,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Salamand Halcyon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8260,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Mardu Halcyon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8261,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Leshach Halcyon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8262,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Gnoma Halcyon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8263,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Undin Halcyon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8264,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Sylphi Halcyon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8265,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Diakon Halcyon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8266,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Leamonde Halcyon": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8267,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Arcana": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8268,
        classification=ItemClassification.filler,
        weight=1
    ),
    "High Arcana": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8269,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Turtle Shell": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8270,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Aged Turtle Shell": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8271,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ancient Turtle Shell": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8272,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Molting": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8273,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Iron Carapace": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8274,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Wyrm Carapace": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8275,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Insect Husk": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8276,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Battlewyrm Carapace": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8277,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Destrier Barding": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8278,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Charger Barding": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8279,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Fish Scale": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8280,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Yensa Scale": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8281,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ichthon Scale": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8282,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ring Wyrm Scale": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8283,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Drab Wool": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8284,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Braid Wool": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8285,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Fine Wool": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8286,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Blood Wool": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8287,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Rat Pelt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8288,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Snake Skin": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8289,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Tyrant Hide": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8290,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Quality Hide": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8291,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Beastlord Hide": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8292,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Tanned Hide": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8293,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Tanned Giantskin": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8294,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Tanned Tyrant Hide": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8295,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Prime Tanned Hide": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8296,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Wolf Pelt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8297,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Coeurl Pelt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8298,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Quality Pelt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8299,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Prime Pelt": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8300,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Small Feather": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8301,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Large Feather": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8302,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Chocobo Feather": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8303,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Giant Feather": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8304,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Bundle of Feathers": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8305,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Windslicer Pinion": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8306,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Horn": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8307,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Pointed Horn": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8308,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Solid Horn": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8309,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Bat Fang": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8310,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Crooked Fang": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8311,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Spiral Incisor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8312,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Wyvern Fang": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8313,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Cactus Fruit": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8314,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Succulent Fruit": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8315,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Screamroot": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8316,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Malboro Vine": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8317,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Malboro Fruit": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8318,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Malboro Flower": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8319,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Bone Fragment": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8320,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Sturdy Bone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8321,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Blood-darkened Bone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8322,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Lumber": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8323,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Quality Lumber": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8324,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Solid Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8325,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Quality Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8326,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Iron Scraps": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8327,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Iron Ore": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8328,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Green Liquid": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8329,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Yellow Liquid": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8330,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Silver Liquid": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8331,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Glass Jewel": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8332,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Sky Jewel": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8333,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Demon Eyeball": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8334,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Demon Feather": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8335,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Demon Tail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8336,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Grimoire Togail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8337,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Grimoire Aidhed": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8338,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Bomb Ashes": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8339,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Bomb Shell": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8340,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Book of Orgain": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8341,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Book of Orgain-Cent": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8342,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Book of Orgain-Mille": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8343,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Foul Flesh": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8344,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Festering Flesh": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8345,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Maggoty Flesh": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8346,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Forbidden Flesh": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8347,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Feystone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8348,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Pebble": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8349,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Broken Sword": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8350,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Broken Greataxe": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8351,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Broken Spear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8352,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Bent Staff": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8353,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Moon Ring": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8354,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Bundle of Needles": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8355,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Coeurl Whisker": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8356,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Mallet": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8357,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Tattered Garment": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8358,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Split Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8359,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Chimera Head": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8360,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Rat Tail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8361,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Slaven Harness": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8362,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Blood-stained Necklace": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8363,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Destrier Mane": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8364,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Wargod's Band": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8365,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Soul of Thamasa": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8366,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Beastlord Horn": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8367,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Vampyr Fang": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8368,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Great Serpent's Fang": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8369,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Death's-Head": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8370,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ancient Bone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8371,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Wyrm Bone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8372,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Tyrant Bone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8373,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Mirror Scale": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8374,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Emperor Scale": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8375,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Mythril": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8376,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Adamantite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8377,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Scarletite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8378,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Damascus Steel": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8379,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Orichalcum": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8380,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Mystletainn": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8381,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Einherjarium": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8382,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Electrum": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8383,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Dorsal Fin": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8384,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Yensa Fin": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8385,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ring Wyrm Liver": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8386,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Eye of the Hawk": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8387,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Serpent Eye": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8388,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ambrosia": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8389,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Foul Liquid": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8390,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Putrid Liquid": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8391,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Caramel": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8392,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Slime Oil": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8393,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Unpurified Ether": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8394,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Demon Drink": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8395,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Death Powder": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8396,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Soul Powder": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8397,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Zombie Powder": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8398,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Snowfly": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8399,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Corpse Fly": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8400,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Bat Wing": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8401,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Wyvern Wing": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8402,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Bomb Fragment": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8403,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Throat Wolf Blood": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8404,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Frogspawn": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8405,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Frog Oil": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8406,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Behemoth Steak": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8407,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Gysahl Greens": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8408,
        classification=ItemClassification.filler,
        weight=1
    ),
    "White Incense": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8409,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Antarctic Wind": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8410,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Arctic Wind": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8411,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Wrath of the Gods": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8412,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Charged Gizzard": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8413,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Lifewick": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8414,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Ketu Board": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8415,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Magick Lamp": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8416,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Hell-Gate's Flame": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8417,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Sickle-Blade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8418,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Stardust": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8419,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Moondust": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8420,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Rainbow Egg": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8421,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Four-leaf Clover": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8422,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Gimble Stalk": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8423,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Onion": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8424,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Jack-o'-Lantern": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8425,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Tomato Stalk": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8426,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Demon's Sigh": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8427,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Omega Badge": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8428,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Empyreal Soul": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8429,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Serpentarius": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8430,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Gemsteel": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8431,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Centurio Hero's Badge": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8432,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Horakhty's Flame": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8433,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Phobos Glaze": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8434,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Deimos Clay": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8435,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Godslayer's Badge": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8436,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Lu Shang's Badge": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8437,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Empty Bottle": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8448,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Common Fish": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8449,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Delicious Fish": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8450,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Nebra Succulent": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8451,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Peach Tuft": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8452,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Green Tuft": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8453,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Orange Tuft": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8454,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Brown Tuft": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8455,
        classification=ItemClassification.filler,
        weight=1
    ),
    "White Tuft": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8456,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Valeblossom Dew": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8457,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Semclam Shell": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8458,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Nebralim": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8459,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Great Serpentskin": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8460,
        classification=ItemClassification.filler,
        weight=1
    ),
    "Sandalwood Chop": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8466,
        classification=ItemClassification.progression
    ),
    "Pinewood Chop": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8467,
        classification=ItemClassification.progression_skip_balancing,
        duplicateAmount=28
    ),
    "Black Orb": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 8470,
        classification=ItemClassification.progression_skip_balancing,
        duplicateAmount=24
    ),
    "Writ of Transit": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32880,
        classification=ItemClassification.progression
    ),
    "Clan Primer": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32881,
        classification=ItemClassification.progression
    ),
    "Cactus Flower": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32883,
        classification=ItemClassification.progression
    ),
    "Tube Fuse": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32884,
        classification=ItemClassification.progression
    ),
    "Sword of the Order": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32885,
        classification=ItemClassification.progression
    ),
    "No. 1 Brig Key": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32886,
        classification=ItemClassification.progression
    ),
    "Systems Access Key": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32887,
        classification=ItemClassification.progression
    ),
    "Dawn Shard": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32888,
        classification=ItemClassification.progression
    ),
    "Shadestone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32889,
        classification=ItemClassification.progression
    ),
    "Sunstone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32890,
        classification=ItemClassification.progression
    ),
    "Ring of the Toad": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32892,
        classification=ItemClassification.progression
    ),
    "Silent Urn": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32893,
        classification=ItemClassification.progression
    ),
    "Site 3 Key": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32894,
        classification=ItemClassification.progression
    ),
    "Site 11 Key": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32895,
        classification=ItemClassification.progression
    ),
    "Crescent Stone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32896,
        classification=ItemClassification.progression
    ),
    "Medallion of Bravery": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32897,
        classification=ItemClassification.progression
    ),
    "Medallion of Might": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32898,
        classification=ItemClassification.progression
    ),
    "Medallion of Love": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32899,
        classification=ItemClassification.progression
    ),
    "Lusterless Medallion": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32900,
        classification=ItemClassification.progression
    ),
    "Stone of the Condemner": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32901,
        classification=ItemClassification.progression
    ),
    "Errmonea Leaf": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32902,
        classification=ItemClassification.progression
    ),
    "Rabbit's Tail": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32903,
        classification=ItemClassification.progression
    ),
    "Ann's Letter": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32904,
        classification=ItemClassification.progression
    ),
    "Manufacted Nethicite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32905,
        classification=ItemClassification.progression
    ),
    "Rusted Scrap of Armor": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32906,
        classification=ItemClassification.progression
    ),
    "Sword of Kings": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32907,
        classification=ItemClassification.progression
    ),
    "Treaty-Blade": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32908,
        classification=ItemClassification.progression
    ),
    "Dusty Letter": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32909,
        classification=ItemClassification.progression
    ),
    "Serpentwyne Must": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32910,
        classification=ItemClassification.progression
    ),
    "Dull Fragment": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32911,
        classification=ItemClassification.progression
    ),
    "Blackened Fragment": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32912,
        classification=ItemClassification.progression
    ),
    "Grimy Fragment": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32913,
        classification=ItemClassification.progression
    ),
    "Stolen Articles": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32914,
        classification=ItemClassification.progression
    ),
    "Barheim Key": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32915,
        classification=ItemClassification.progression
    ),
    "Merchant's Armband": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32920,
        classification=ItemClassification.progression
    ),
    "Pilika's Diary": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32921,
        classification=ItemClassification.progression
    ),
    "Ring of the Light": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32922,
        classification=ItemClassification.progression
    ),
    "Viera Rucksack": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32923,
        classification=ItemClassification.progression
    ),
    "Lab Access Card": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32926,
        classification=ItemClassification.progression
    ),
    "Moonsilver Medallion": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32931,
        classification=ItemClassification.progression
    ),
    "Goddess's Magicite": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32940,
        classification=ItemClassification.progression
    ),
    "Broken Key": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32942,
        classification=ItemClassification.progression
    ),
    "Sluice Gate Key": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32943,
        classification=ItemClassification.progression
    ),
    "Wind Globe": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32945,
        classification=ItemClassification.progression
    ),
    "Windvane": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32946,
        classification=ItemClassification.progression
    ),
    "Dragon Scale": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32948,
        classification=ItemClassification.progression
    ),
    "Ageworn Key": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32949,
        classification=ItemClassification.progression
    ),
    "Soul Ward Key": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32950,
        classification=ItemClassification.progression
    ),
    "Lente's Tear": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32951,
        classification=ItemClassification.progression
    ),
    "Shelled Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32952,
        classification=ItemClassification.progression
    ),
    "Fur-scaled Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32953,
        classification=ItemClassification.useful
    ),
    "Bony Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32954,
        classification=ItemClassification.useful
    ),
    "Fanged Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32955,
        classification=ItemClassification.useful
    ),
    "Hide-covered Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32956,
        classification=ItemClassification.useful
    ),
    "Maned Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32957,
        classification=ItemClassification.useful
    ),
    "Fell Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32958,
        classification=ItemClassification.useful
    ),
    "Accursed Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32959,
        classification=ItemClassification.useful
    ),
    "Beaked Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32960,
        classification=ItemClassification.useful
    ),
    "Maverick Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32961,
        classification=ItemClassification.useful
    ),
    "Soulless Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32962,
        classification=ItemClassification.useful
    ),
    "Leathern Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32963,
        classification=ItemClassification.useful
    ),
    "Sickle Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32964,
        classification=ItemClassification.useful
    ),
    "Vengeful Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32965,
        classification=ItemClassification.useful
    ),
    "Gravesoil Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32966,
        classification=ItemClassification.useful
    ),
    "Metallic Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32967,
        classification=ItemClassification.useful
    ),
    "Slimy Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32968,
        classification=ItemClassification.useful
    ),
    "Scythe Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32969,
        classification=ItemClassification.useful
    ),
    "Feathered Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32970,
        classification=ItemClassification.useful
    ),
    "Skull Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32971,
        classification=ItemClassification.useful
    ),
    "Mind Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32972,
        classification=ItemClassification.useful
    ),
    "Eternal Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32973,
        classification=ItemClassification.useful
    ),
    "Clawed Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32974,
        classification=ItemClassification.useful
    ),
    "Odiferous Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32975,
        classification=ItemClassification.useful
    ),
    "Whiskered Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32976,
        classification=ItemClassification.useful
    ),
    "Frigid Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32977,
        classification=ItemClassification.useful
    ),
    "Ensanguined Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32978,
        classification=ItemClassification.useful
    ),
    "Cruel Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32979,
        classification=ItemClassification.useful
    ),
    "Adamantine Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32980,
        classification=ItemClassification.useful
    ),
    "Reptilian Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32981,
        classification=ItemClassification.useful
    ),
    "Vile Trophy": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32982,
        classification=ItemClassification.useful
    ),
    "Rainstone": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32992,
        classification=ItemClassification.progression
    ),
    "Rabanastre Aeropass": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32993,
        classification=ItemClassification.progression
    ),
    "Nalbina Aeropass": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32994,
        classification=ItemClassification.progression
    ),
    "Bhujerba Aeropass": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32995,
        classification=ItemClassification.progression
    ),
    "Archades Aeropass": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32996,
        classification=ItemClassification.progression
    ),
    "Balfonheim Aeropass": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 32997,
        classification=ItemClassification.progression
    ),
    "Belias": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49170,
        classification=ItemClassification.progression
    ),
    "Mateus": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49171,
        classification=ItemClassification.progression
    ),
    "Adrammelech": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49172,
        classification=ItemClassification.progression
    ),
    "Hashmal": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49173,
        classification=ItemClassification.progression
    ),
    "Cuchulainn": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49174,
        classification=ItemClassification.progression
    ),
    "Famfrit": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49175,
        classification=ItemClassification.progression
    ),
    "Zalera": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49176,
        classification=ItemClassification.progression
    ),
    "Shemhazai": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49177,
        classification=ItemClassification.progression
    ),
    "Chaos": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49178,
        classification=ItemClassification.progression
    ),
    "Zeromus": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49179,
        classification=ItemClassification.progression
    ),
    "Exodus": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49180,
        classification=ItemClassification.progression
    ),
    "Ultima": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49181,
        classification=ItemClassification.progression
    ),
    "Zodiark": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49182,
        classification=ItemClassification.progression
    ),
    "Second Board": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 49183,
        classification=ItemClassification.progression
    ),
    "1 Gil": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 98304,
        classification=ItemClassification.filler,
        weight=60,
        duplicateAmount=0
    ),
    "500 Gil": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 98305,
        classification=ItemClassification.filler,
        weight=100,
        amount=500,
        duplicateAmount=0
    ),
    "1000 Gil": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 98306,
        classification=ItemClassification.filler,
        weight=120,
        amount=1000,
        duplicateAmount=0
    ),
    "5000 Gil": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 98307,
        classification=ItemClassification.filler,
        weight=90,
        amount=5000,
        duplicateAmount=0
    ),
    "10000 Gil": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 98308,
        classification=ItemClassification.filler,
        weight=40,
        amount=10000,
        duplicateAmount=0
    ),
    "25000 Gil": FF12OpenWorldItemData(
        code=FF12OW_BASE_ID + 98309,
        classification=ItemClassification.filler,
        weight=30,
        amount=25000,
        duplicateAmount=0
    ),
}

item_table = {name: data.code for name, data in item_data_table.items()}
inv_item_table = {data.code: name for name, data in item_data_table.items()}

filler_items = [name for name, data in item_data_table.items()
                if data.classification == ItemClassification.filler and data.weight > 0]
filler_weights = [item_data_table[name].weight for name in filler_items]

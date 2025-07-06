"""
Pulls data from JSON files in worlds/pokemon_emerald/data/ into classes.
This also includes marrying automatically extracted data with manually
defined data (like location labels or usable pokemon species), some cleanup
and sorting, and Warp methods.
"""

from dataclasses import dataclass
from enum import IntEnum, Enum
import orjson
from typing import Dict, List, NamedTuple, Optional, Set, FrozenSet, Tuple, Any, Union
import pkgutil
import pkg_resources

from BaseClasses import ItemClassification

from .data_consts import all_species, all_abilities, all_moves, all_legendary_pokemon

BASE_OFFSET = 3860000
POKEDEX_OFFSET = 10000

IGNORABLE_MAPS = {
    "MAP_ALTERING_CAVE",
    "MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP1",
    "MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP2",
    "MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP3",
}
"""These maps exist but don't show up in the rando or are unused, and so should be discarded"""

OUT_OF_LOGIC_MAPS = {
    "MAP_DESERT_UNDERPASS",
    "MAP_SAFARI_ZONE_NORTHEAST",
    "MAP_SAFARI_ZONE_SOUTHEAST",
    "MAP_METEOR_FALLS_STEVENS_CAVE",
    "MAP_MIRAGE_TOWER_1F",
    "MAP_MIRAGE_TOWER_2F",
    "MAP_MIRAGE_TOWER_3F",
    "MAP_MIRAGE_TOWER_4F",
}
"""
These maps have encounters and are locked behind beating the champion or are missable.
Those encounter slots should be ignored for logical access to a species.
"""

NUM_REAL_SPECIES = 1024


class Warp:
    """
    Represents warp events in the game like doorways or warp pads
    """
    is_one_way: bool
    source_map: str
    source_ids: List[int]
    dest_map: str
    dest_ids: List[int]
    parent_region: Optional[str]

    def __init__(self, encoded_string: Optional[str] = None, parent_region: Optional[str] = None) -> None:
        if encoded_string is not None:
            decoded_warp = Warp.decode(encoded_string)
            self.is_one_way = decoded_warp.is_one_way
            self.source_map = decoded_warp.source_map
            self.source_ids = decoded_warp.source_ids
            self.dest_map = decoded_warp.dest_map
            self.dest_ids = decoded_warp.dest_ids
        self.parent_region = parent_region

    def encode(self) -> str:
        """
        Returns a string encoding of this warp
        """
        source_ids_string = ""
        for source_id in self.source_ids:
            source_ids_string += str(source_id) + ","
        source_ids_string = source_ids_string[:-1]  # Remove last ","

        dest_ids_string = ""
        for dest_id in self.dest_ids:
            dest_ids_string += str(dest_id) + ","
        dest_ids_string = dest_ids_string[:-1]  # Remove last ","

        return f"{self.source_map}:{source_ids_string}/{self.dest_map}:{dest_ids_string}{'!' if self.is_one_way else ''}"

    def connects_to(self, other: "Warp") -> bool:
        """
        Returns true if this warp sends the player to `other`
        """
        return self.dest_map == other.source_map and set(self.dest_ids) <= set(other.source_ids)

    @staticmethod
    def decode(encoded_string: str) -> "Warp":
        """
        Create a Warp object from an encoded string
        """
        warp = Warp()
        warp.is_one_way = encoded_string.endswith("!")
        if warp.is_one_way:
            encoded_string = encoded_string[:-1]

        warp_source, warp_dest = encoded_string.split("/")
        warp_source_map, warp_source_indices = warp_source.split(":")
        warp_dest_map, warp_dest_indices = warp_dest.split(":")

        warp.source_map = warp_source_map
        warp.dest_map = warp_dest_map

        warp.source_ids = [int(index) for index in warp_source_indices.split(",")]
        warp.dest_ids = [int(index) for index in warp_dest_indices.split(",")]

        return warp


class ItemData(NamedTuple):
    label: str
    item_id: int
    modern_id: Optional[int]
    classification: ItemClassification
    tags: FrozenSet[str]


class LocationCategory(IntEnum):
    BADGE = 0
    HM = 1
    KEY = 2
    ROD = 3
    BIKE = 4
    TICKET = 5
    OVERWORLD_ITEM = 6
    HIDDEN_ITEM = 7
    GIFT = 8
    BERRY_TREE = 9
    TRAINER = 10
    POKEDEX = 11


class LocationData(NamedTuple):
    name: str
    label: str
    parent_region: str
    default_item: int
    address: Union[int, List[int]]
    flag: int
    category: LocationCategory
    tags: FrozenSet[str]


class EncounterTableData(NamedTuple):
    slots: List[int]
    address: int


# class EncounterType(StrEnum):  # StrEnum introduced in python 3.11
class EncounterType(Enum):
    LAND = "LAND"
    WATER = "WATER"
    FISHING = "FISHING"
    ROCK_SMASH = "ROCK_SMASH"


@dataclass
class MapData:
    name: str
    label: str
    header_address: int
    encounters: Dict[EncounterType, EncounterTableData]


class EventData(NamedTuple):
    name: str
    parent_region: str


class RegionData:
    name: str
    parent_map: MapData
    has_grass: bool
    has_water: bool
    has_fishing: bool
    exits: List[str]
    warps: List[str]
    locations: List[str]
    events: List[EventData]

    def __init__(self, name: str, parent_map: MapData, has_grass: bool, has_water: bool, has_fishing: bool):
        self.name = name
        self.parent_map = parent_map
        self.has_grass = has_grass
        self.has_water = has_water
        self.has_fishing = has_fishing
        self.exits = []
        self.warps = []
        self.locations = []
        self.events = []


class BaseStats(NamedTuple):
    hp: int
    attack: int
    defense: int
    speed: int
    special_attack: int
    special_defense: int


class LearnsetMove(NamedTuple):
    level: int
    move_id: int


class EvolutionMethodEnum(IntEnum):
    LEVEL = 0
    LEVEL_ATK_LT_DEF = 1
    LEVEL_ATK_EQ_DEF = 2
    LEVEL_ATK_GT_DEF = 3
    LEVEL_SILCOON = 4
    LEVEL_CASCOON = 5
    LEVEL_NINJASK = 6
    LEVEL_SHEDINJA = 7
    ITEM = 8
    FRIENDSHIP = 9
    FRIENDSHIP_DAY = 10
    FRIENDSHIP_NIGHT = 11


class EvolutionData(NamedTuple):
    method: EvolutionMethodEnum
    param: int  # Level/item id/friendship/etc.; depends on method
    species_id: int


class MiscPokemonData(NamedTuple):
    species_id: int
    address: int


@dataclass
class SpeciesData:
    name: str
    label: str
    species_id: int
    national_dex_number: int
    base_stats: BaseStats
    types: Tuple[int, int]
    abilities: Tuple[int, int, int]  # Hidden ability is the third ability
    evolutions: List[EvolutionData]
    pre_evolution: Optional[int]
    catch_rate: int
    friendship: int
    learnset: List[LearnsetMove]
    tm_hm_compatibility: int
    learnset_address: int
    address: int


class AbilityData(NamedTuple):
    ability_id: int
    label: str


class TrainerPokemonDataTypeEnum(IntEnum):
    NO_ITEM_DEFAULT_MOVES = 0
    ITEM_DEFAULT_MOVES = 1
    NO_ITEM_CUSTOM_MOVES = 2
    ITEM_CUSTOM_MOVES = 3


def _str_to_pokemon_data_type(string: str) -> TrainerPokemonDataTypeEnum:
    if string == "NO_ITEM_DEFAULT_MOVES":
        return TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES
    if string == "ITEM_DEFAULT_MOVES":
        return TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES
    if string == "NO_ITEM_CUSTOM_MOVES":
        return TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES
    if string == "ITEM_CUSTOM_MOVES":
        return TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES
    raise ValueError(f"Unknown TrainerPokemonDataTypeEnum string: {string}")


class TrainerPokemonData(NamedTuple):
    species_id: int
    level: int
    moves: Optional[Tuple[int, int, int, int]]


class TrainerPartyData(NamedTuple):
    pokemon: List[TrainerPokemonData]
    pokemon_data_type: TrainerPokemonDataTypeEnum
    address: int


@dataclass
class TrainerData:
    trainer_id: int
    party: TrainerPartyData
    address: int
    script_address: int
    battle_type: int


class PokemonEmeraldData:
    starters: Tuple[int, int, int]
    constants: Dict[str, int]
    ram_addresses: Dict[str, int]
    rom_addresses: Dict[str, int]
    regions: Dict[str, RegionData]
    locations: Dict[str, LocationData]
    items: Dict[int, ItemData]
    species: Dict[int, SpeciesData]
    legendary_encounters: List[MiscPokemonData]
    misc_pokemon: List[MiscPokemonData]
    tmhm_moves: List[int]
    abilities: List[AbilityData]
    move_labels: Dict[str, int]
    maps: Dict[str, MapData]
    warps: Dict[str, Warp]
    warp_map: Dict[str, Optional[str]]
    trainers: List[TrainerData]

    def __init__(self) -> None:
        self.starters = (277, 280, 283)
        self.constants = {}
        self.ram_addresses = {}
        self.rom_addresses = {}
        self.regions = {}
        self.locations = {}
        self.items = {}
        self.species = {}
        self.legendary_encounters = []
        self.misc_pokemon = []
        self.tmhm_moves = []
        self.abilities = []
        self.move_labels = {}
        self.maps = {}
        self.warps = {}
        self.warp_map = {}
        self.trainers = []


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))


def _init() -> None:
    import re

    extracted_data: Dict[str, Any] = load_json_data("extracted_data.json")
    data.constants = extracted_data["constants"]
    data.ram_addresses = extracted_data["misc_ram_addresses"]
    data.rom_addresses = extracted_data["misc_rom_addresses"]

    location_attributes_json = load_json_data("locations.json")

    # Create map data
    for map_name, map_json in extracted_data["maps"].items():
        assert isinstance(map_name, str)
        if map_name in IGNORABLE_MAPS:
            continue

        encounter_tables: Dict[EncounterType, EncounterTableData] = {}
        if "land_encounters" in map_json:
            encounter_tables[EncounterType.LAND] = EncounterTableData(
                map_json["land_encounters"]["slots"],
                map_json["land_encounters"]["address"]
            )
        if "water_encounters" in map_json:
            encounter_tables[EncounterType.WATER] = EncounterTableData(
                map_json["water_encounters"]["slots"],
                map_json["water_encounters"]["address"]
            )
        if "fishing_encounters" in map_json:
            encounter_tables[EncounterType.FISHING] = EncounterTableData(
                map_json["fishing_encounters"]["slots"],
                map_json["fishing_encounters"]["address"]
            )
        if "rock_smash_encounters" in map_json:
            encounter_tables[EncounterType.ROCK_SMASH] = EncounterTableData(
                map_json["rock_smash_encounters"]["slots"],
                map_json["rock_smash_encounters"]["address"]
            )

        # Derive a user-facing label
        label = []
        for word in map_name[4:].split("_"):
            # 1F, B1F, 2R, etc.
            re_match = re.match(r"^B?\d+[FRP]$", word)
            if re_match:
                label.append(word)
                continue

            # Route 103, Hall 1, House 5, etc.
            re_match = re.match(r"^([A-Z]+)(\d+)$", word)
            if re_match:
                label.append(re_match.group(1).capitalize())
                label.append(re_match.group(2).lstrip("0"))
                continue

            if word == "OF":
                label.append("of")
                continue

            if word == "SS":
                label.append("S.S.")
                continue

            label.append(word.capitalize())

        data.maps[map_name] = MapData(
            map_name,
            " ".join(label),
            map_json["header_address"],
            encounter_tables
        )

    # Load/merge region json files
    region_json_list = []
    for file in pkg_resources.resource_listdir(__name__, "data/regions"):
        if not pkg_resources.resource_isdir(__name__, "data/regions/" + file):
            region_json_list.append(load_json_data("regions/" + file))

    regions_json = {}
    for region_subset in region_json_list:
        for region_name, region_json in region_subset.items():
            if region_name in regions_json:
                raise AssertionError("Region [{region_name}] was defined multiple times")
            regions_json[region_name] = region_json

    # Create region data
    claimed_locations: Set[str] = set()
    claimed_warps: Set[str] = set()

    data.regions = {}
    for region_name, region_json in regions_json.items():
        new_region = RegionData(
            region_name,
            data.maps[region_json["parent_map"]],
            region_json["has_grass"],
            region_json["has_water"],
            region_json["has_fishing"]
        )

        # Locations
        for location_name in region_json["locations"]:
            if location_name in claimed_locations:
                raise AssertionError(f"Location [{location_name}] was claimed by multiple regions")

            location_json = extracted_data["locations"][location_name]
            if location_name.startswith("TRAINER_BRENDAN_") or location_name.startswith("TRAINER_MAY_"):
                import re
                locale = re.match("TRAINER_BRENDAN_([A-Z0-9_]+)_MUDKIP_REWARD", location_name).group(1)
                alternate_rival_jsons = [extracted_data["locations"][alternate] for alternate in [
                    f"TRAINER_BRENDAN_{locale}_TORCHIC_REWARD",
                    f"TRAINER_BRENDAN_{locale}_TREECKO_REWARD",
                    f"TRAINER_MAY_{locale}_MUDKIP_REWARD",
                    f"TRAINER_MAY_{locale}_TORCHIC_REWARD",
                    f"TRAINER_MAY_{locale}_TREECKO_REWARD",
                ]]
                new_location = LocationData(
                    location_name,
                    location_attributes_json[location_name]["label"],
                    region_name,
                    location_json["default_item"],
                    [location_json["address"]] + [j["address"] for j in alternate_rival_jsons],
                    location_json["flag"],
                    LocationCategory[location_attributes_json[location_name]["category"]],
                    frozenset(location_attributes_json[location_name]["tags"])
                )
            else:
                new_location = LocationData(
                    location_name,
                    location_attributes_json[location_name]["label"],
                    region_name,
                    location_json["default_item"],
                    location_json["address"],
                    location_json["flag"],
                    LocationCategory[location_attributes_json[location_name]["category"]],
                    frozenset(location_attributes_json[location_name]["tags"])
                )
            new_region.locations.append(location_name)
            data.locations[location_name] = new_location
            claimed_locations.add(location_name)

        new_region.locations.sort()

        # Events
        for event in region_json["events"]:
            new_region.events.append(EventData(event, region_name))

        # Exits
        for region_exit in region_json["exits"]:
            new_region.exits.append(region_exit)

        # Warps
        for encoded_warp in region_json["warps"]:
            if encoded_warp in claimed_warps:
                raise AssertionError(f"Warp [{encoded_warp}] was claimed by multiple regions")
            new_region.warps.append(encoded_warp)
            data.warps[encoded_warp] = Warp(encoded_warp, region_name)
            claimed_warps.add(encoded_warp)

        new_region.warps.sort()

        data.regions[region_name] = new_region

    # Create item data
    items_json = load_json_data("items.json")

    data.items = {}
    for item_constant_name, attributes in items_json.items():
        item_classification = None
        if attributes["classification"] == "PROGRESSION":
            item_classification = ItemClassification.progression
        elif attributes["classification"] == "USEFUL":
            item_classification = ItemClassification.useful
        elif attributes["classification"] == "FILLER":
            item_classification = ItemClassification.filler
        elif attributes["classification"] == "TRAP":
            item_classification = ItemClassification.trap
        else:
            raise ValueError(f"Unknown classification {attributes['classification']} for item {item_constant_name}")

        data.items[data.constants[item_constant_name]] = ItemData(
            attributes["label"],
            data.constants[item_constant_name],
            attributes["modern_id"],
            item_classification,
            frozenset(attributes["tags"])
        )

    # Create species data

    # Excludes extras like copies of Unown and special species values like SPECIES_EGG.
    max_species_id = 0
    for species_name, species_label, species_dex_number in all_species:
        species_id = data.constants[species_name]
        max_species_id = max(species_id, max_species_id)
        species_data = extracted_data["species"][species_id]

        learnset = [LearnsetMove(item["level"], item["move_id"]) for item in species_data["learnset"]["moves"]]

        data.species[species_id] = SpeciesData(
            species_name,
            species_label,
            species_id,
            species_dex_number,
            BaseStats(
                species_data["base_stats"][0],
                species_data["base_stats"][1],
                species_data["base_stats"][2],
                species_data["base_stats"][3],
                species_data["base_stats"][4],
                species_data["base_stats"][5]
            ),
            (species_data["types"][0], species_data["types"][1]),
            (
                species_data["abilities"][0],
                species_data["abilities"][1],
                species_data["abilities"][2],
            ),
            [
                EvolutionData(
                    EvolutionMethodEnum[evolution_json["method"]],
                    evolution_json["param"],
                    evolution_json["species"],
                )
                for evolution_json in species_data["evolutions"]
            ],
            None,
            species_data["catch_rate"],
            species_data["friendship"],
            learnset,
            int(species_data["tmhm_learnset"], 16),
            species_data["learnset"]["address"],
            species_data["address"]
        )

    for species in data.species.values():
        for evolution in species.evolutions:
            data.species[evolution.species_id].pre_evolution = species.species_id

    # Replace default item for dex entry locations based on evo stage of species
    evo_stage_to_ball_map: Dict[int, int] = {
        0: data.constants["ITEM_POKE_BALL"],
        1: data.constants["ITEM_GREAT_BALL"],
        2: data.constants["ITEM_ULTRA_BALL"],
    }

    for species in data.species.values():
        default_item: Optional[int] = None
        pre_evolution = species.pre_evolution

        if pre_evolution is not None:
            evo_data = next(evo for evo in data.species[pre_evolution].evolutions if evo.species_id == species.species_id)
            if evo_data.method == EvolutionMethodEnum.ITEM:
                default_item = evo_data.param

        evo_stage = 0
        if default_item is None:
            while pre_evolution is not None:
                evo_stage += 1
                pre_evolution = data.species[pre_evolution].pre_evolution
            default_item = evo_stage_to_ball_map[evo_stage]

        dex_location_name = f"POKEDEX_REWARD_{str(species.national_dex_number).zfill(3)}"
        data.locations[dex_location_name] = LocationData(
            data.locations[dex_location_name].name,
            data.locations[dex_location_name].label,
            data.locations[dex_location_name].parent_region,
            default_item,
            data.locations[dex_location_name].address,
            data.locations[dex_location_name].flag,
            data.locations[dex_location_name].category,
            data.locations[dex_location_name].tags
        )

    # Create legendary encounter data
    for legendary_encounter_json in extracted_data["legendary_encounters"]:
        data.legendary_encounters.append(MiscPokemonData(
            legendary_encounter_json["species"],
            legendary_encounter_json["address"]
        ))

    for misc_pokemon_json in extracted_data["misc_pokemon"]:
        data.misc_pokemon.append(MiscPokemonData(
            misc_pokemon_json["species"],
            misc_pokemon_json["address"]
        ))

    # TM moves
    data.tmhm_moves = extracted_data["tmhm_moves"]
    # Create ability data
    data.abilities = [
        AbilityData(data.constants[ability_data[0]], ability_data[1])
        for ability_data in all_abilities
    ]

    # Move labels
    data.move_labels = {r: data.constants[l] for l, r in all_moves}

    # Create warp map
    for warp, destination in extracted_data["warps"].items():
        data.warp_map[warp] = None if destination == "" else destination

    # Create trainer data
    for i, trainer_json in enumerate(extracted_data["trainers"]):
        party_json = trainer_json["party"]
        pokemon_data_type = _str_to_pokemon_data_type(trainer_json["data_type"])
        data.trainers.append(TrainerData(
            i,
            TrainerPartyData(
                [TrainerPokemonData(
                    p["species"],
                    p["level"],
                    (p["moves"][0], p["moves"][1], p["moves"][2], p["moves"][3]) if "moves" in p else None
                ) for p in party_json],
                pokemon_data_type,
                trainer_json["party_address"]
            ),
            trainer_json["address"],
            trainer_json["script_address"],
            trainer_json["battle_type"]
        ))


data = PokemonEmeraldData()
_init()

"""Species IDs of legendary pokemon"""

UNEVOLVED_POKEMON = frozenset({
    species.species_id
    for species in data.species.values()
    if len(species.evolutions) > 0
})
"""Species IDs of pokemon which have further evolution stages in the vanilla game"""

NATIONAL_ID_TO_SPECIES_ID = {species.national_dex_number: i for i, species in data.species.items()}
LEGENDARY_POKEMON = frozenset(
    [data.constants[species] for species in all_legendary_pokemon]
)

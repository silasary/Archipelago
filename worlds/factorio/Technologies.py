import itertools
from collections import defaultdict, Counter
from dataclasses import dataclass
from enum import IntEnum, IntFlag

from .data import (
    get_data,
    Entity as RawEntity,
    Item as RawItem,
    Fluid as RawFluid,
    Tile as RawTile,
    Recipe as RawRecipe,
    SpaceLocation as RawSpaceLocation,
    Technology as RawTechnology,
)

# TODO: complicated things not done yet:
# * steam is both a power type and an ingredient, but it's only considered a power type currently. consider acid neutralization, coal liquifaction, steam condensation, etc.
# * aquilo freezing buildings matters for performing ammoniacal solution separation, but the logic doesn't know that that requires heating buildings. the logic is incorrectly assuming that access to ammoniacal ocean allows you to craft arbitrarily with the item, perhaps as though shipping it offworld were possible, which it is not.
# * there's no logic for generating power in space, which does not allow chemical combustion. solar panels need to be required somehow.
# * fusion reactor is missing the fluoroketone requirement. probably need to add a capability.
# * spoiling is a process that's not included in the logic. e.g. fish is a source of spoilage, and copper bacteria produces copper.

# TODO: delete these notes: 
"""
# These are the exports we're expected to provide:
from .Technologies import free_sample_exclusions, tech_to_progressive_lookup, base_tech_table, all_product_sources, required_technologies, get_rocket_requirements, get_science_pack_pools, Recipe, recipes, technology_table, tech_table, factorio_base_id, useless_technologies, progressive_technology_table, fluids, valid_ingredients
"""
# TODO: redo these:
required_technologies: dict[str, frozenset["Technology"]] = {}
base_tech_table = {}
progressive_technology_table: dict[str, "Technology"] = {}
tech_to_progressive_lookup: dict[str, str] = {}
useless_technologies: set[str] = {}
valid_ingredients: set[str] = {}
all_product_sources: dict[str, set["Recipe"]] = {}
free_sample_exclusions: set[str] = set()
tech_table: dict[str, int] = {}
technology_table: dict[str, "Technology"] = {}


factorio_base_id = 2 ** 17

class Capability(IntFlag):
    """
    Represents global milestones in the player's abilities
    """
    automate_mining                    = 1<< 0 # burner mining drill
    mine_with_fluid                    = 1<< 1 # uranium mining technology + electric mining drills
    mine_hard_solids                   = 1<< 2 # big mining drill
    pump_tiles                         = 1<< 3 # offshore pump
    pump_entities                      = 1<< 4 # pumpjack
    automate_planting                  = 1<< 5 # agricultural tower
    harness_lightning                  = 1<< 6 # lightning rod
    capture_biter_spawners             = 1<< 7 # capture robot rocket + some rocket launcher on nauvis
    heat_buildings                     = 1<< 8 # heating tower or nuclear reactor
    build_on_ice_platforms             = 1<< 9 # ice platform + concrete
    collect_asteroids                  = 1<<10 # asteroid collector
    travel_space                       = 1<<11 # thruster
    generate_electricity_in_space      = 1<<12 # solar panel
    generate_electricity_in_dark_space = 1<<13 # nuclear or fusion
    destroy_medium_asteroids           = 1<<14 # gun turret
    destroy_big_asteroids              = 1<<15 # rocket turret
    destroy_huge_asteroids             = 1<<16 # railgun turret

    destroy_big_and_smaller_asteroids = destroy_big_asteroids | destroy_medium_asteroids
    destroy_huge_and_smaller_asteroids = destroy_huge_asteroids | destroy_big_and_smaller_asteroids


class PowerType(IntFlag):
    """
    Buildings almost always require exactly 1 power type,
    except for the fusion reactor which consumes both electricity and fusion fuel,
    and some machines operate for free, e.g. offshore-pump.
    """
    chemical_fuel = 1<< 0 # satisfied by foraged coal, required by boiler
    steam_165C    = 1<< 1 # produced by boiler, required by steam engine
    steam_500C    = 1<< 2 # produced by heat exchanger, usable in steam turbine and steam engine
    electricity   = 1<< 3 # produced by solar panel, required by assembling machine
    heat          = 1<< 4 # produced by heating tower, required by heat exchanger
    nutrients     = 1<< 5 # satisfied by nutrients, required by biochamber
    food          = 1<< 6 # satisfied by bioflux, required by captive biter spawner
    nuclear_fuel  = 1<< 7 # satisfied by uranium fuel cell, required by nuclear reactor
    fusion_fuel   = 1<< 8 # satisfied by fusion power cell, required by fusion reactor
    fusion_plasma = 1<< 9 # produced by fusion reactor, required by fusion generator
    thruster_fuel = 1<<10 # both fuel and oxidizer, required by thruster
    free          = 0 # offshore pump requires no power.

class HeatBufferMode(IntEnum):
    conduct = 0, # heat pipe
    produce = 1, # nuclear reactor, heating tower
    consume = 2, # heat exchanger
    editor_only = -1, # heat interface

class RecipeClassification(IntEnum):
    standard = 0 # Produce "better" items.
    breeding = 1 # Produce more of the same items.
    conversion = 2 # Lossless conversion of items into other items.
    dead_end_recycling = 3 # 75% chance to destroy item in a recycler.

@dataclass
class ResearchRequirement:
    ingredients: dict[str, int]
    """ the keys are the science pack names for 1 unit of research. the values are always 1. """
    units: int | None
    """ how many units of research, e.g. 'automation' costs 10. None means this is an infinite research with a cost formula. """
    energy: int
    """ lab time for 1 unit of research in seconds. """
@dataclass
class CraftRequirement:
    item: str
    """ e.g. 'steel-plate' """
    count: int
    """ e.g. 50 """
@dataclass
class MineRequirement:
    entity: str
    """ e.g. 'fulgoran-ruin-vault' """
@dataclass
class BuildRequirement:
    entity: str
    """ e.g. 'asteroid-collector' """
@dataclass
class CaptureSpawnerRequirement: pass
@dataclass
class CreateSpacePlatformRequirement: pass
@dataclass
class Technology:
    name: str
    """ e.g. 'lightning-collector', 'refined-flammables-1' """
    prerequisites: set[str]
    """ technology names required immediately prior to this one (not recursive). """
    requirement: (ResearchRequirement |
        CraftRequirement |
        MineRequirement |
        BuildRequirement |
        CaptureSpawnerRequirement |
        CreateSpacePlatformRequirement)
    """ usually a ResearchRequirement """

    def is_infinite(self):
        return type(self.requirement) == ResearchRequirement and self.requirement.units == None

@dataclass
class Recipe:
    name: str
    """ e.g. 'electronic-circuit', 'simple-coal-liquefaction' """
    inputs: dict[str, int]
    """
    e.g. {'copper-cable': 3, 'iron-place': 1}, {'raw-fish': 0, 'nutrients': 100, 'water': 100}
    an amount of 0 means the input is somehow "preserved" in the process.
    """
    outputs: dict[str, int]
    """
    e.g. {'electronic-circuit': 1}, {'empty-barrel': 0, 'water': 0}
    an amount of 0 means this is a lossless conversion.
    """
    energy: float
    """ the crafting time in seconds """
    classification: RecipeClassification
    """ useful for guiding traversal of the cyclic directed graph of what items yield what other items. """
    machines: set[str]
    """ this recipe can be performed in any of these machines, possibly including 'character' for hand crafting. """
    locations: set[str] | None
    """ this recipe must be performed in one of these locations. None means anywhere. """
    is_unusual_recipe: bool
    """ true for barreling/unbarreling, rocket part, and biter egg. these should be excluded from free samples. """

@dataclass
class Machine:
    """ an entity that performs some role in a factory """
    name: str
    """ e.g. 'assembling-machine-1', 'captive-biter-spawner', 'steam-turbine', 'character' """
    power_required: PowerType
    """ what type of power is required to operate this building? """
    locations: set[str] | None
    """ this machine can only operate in one of these locations. None means anywhere. the charcater cannot hand craft in space. """
    can_freeze: bool
    """ requires heating in locations with the Capability.heat_buildings threat. """

@dataclass
class Item:
    """ the item version of a thing can be placed on a belt and has a stack size. """
    name: str
    stack_size: int
    rocket_capacity: int
    """ how many fit on a rocket. e.g. 2000 for electronic-circuit, 50 for inserter. 0 for rocket-silo. """

@dataclass(frozen=True, order=True)
class SurfaceProperties:
    gravity: float
    magnetic_field: float
    pressure: float
    def satisfies(self, surface_conditions):
        for condition_data in surface_conditions:
            value = {
                "gravity": self.gravity,
                "magnetic-field": self.magnetic_field,
                "pressure": self.pressure,
            }[condition_data["property"]]
            if not (condition_data["min"] <= value <= condition_data["max"]):
                return False
        return True
SPACE_SURFACE = SurfaceProperties(0, 0, 0)

@dataclass
class SpaceLocation:
    name: str
    """ e.g. 'nauvis', 'solar-system-edge', 'fulgora-aquilo', 'aquilo_orbit' """
    surface_properties: SurfaceProperties
    unlock_names: set[str]
    """ the names of space locations mentioned in research. all are required to access this location. """
    drop_to: str | None
    """ if this is orbit above a planet, which planet? """
    launch_to: str | None
    """ if this is a planet, what's the location name of the orbit above? """
    thrust_to: list[str]
    """ where would thrusters be able to fly us from here? """
    threats: Capability
    """ what size asteroids do we encounter here, and do buildings freeze? """
    def __init__(self, name: str, surface_properties: SurfaceProperties, unlock_names: set[str]):
        self.name = name
        self.surface_properties = surface_properties
        self.unlock_names = unlock_names
        self.drop_to = None
        self.launch_to = None
        self.thrust_to = []
        self.threats = Capability(0)

ORBIT_SUFFIX = "_orbit"

@dataclass(frozen=True, order=True)
class MiningSource:
    """
    A source of an item the player can collect in automated abundance provided they have the right equipment and technology.
    E.g. stone on Nauvis (requires mining drills), sulfuric acid on vulcanus (requires pumpjacks),
    yumako on gleba (requires agricultural towers), carbonic asteroid chunk in space (requires asteroid collector).
    """
    name: str
    """ item or fluid name """
    location: str
    """ e.g. 'fulgora' """
    required_capabilities: Capability
    """ e.g. Capability.automate_mining|mine_with_fluid """
    required_ingredients: tuple[str, ...]
    """ e.g. 'sulfuric-acid' """

# =============
# Exported data
# =============

items: dict[str, Item] = {}
machines: dict[str, Machine] = {}
recipes: dict[str, Recipe] = {}
technologies: dict[str, Technology] = {}
progressive_technology_chains: dict[str, dict[int, str]] = defaultdict(dict)
""" e.g. {'advanced-material-processing': {1:'advanced-material-processing', 2:'advanced-material-processing-2'}} """
empty_technologies: set[str] = set()
fluids: set[str] = set()
logic_events = {}
"""
mapping from event name to expression. Expression is either an event name,
or {"or": [expression, ...]} or {"and": [expression, ...]}
"""

# ==================
# Hardcoded constants that we don't have a good way to derrive from the data:
# ==================

_parameter_names = {
    RawItem.parameter_0,
    RawItem.parameter_1,
    RawItem.parameter_2,
    RawItem.parameter_3,
    RawItem.parameter_4,
    RawItem.parameter_5,
    RawItem.parameter_6,
    RawItem.parameter_7,
    RawItem.parameter_8,
    RawItem.parameter_9,
    # Same as RawFluid.parameter_0...
}

_additional_autoplace_entities = {
    # Most entities are configured in the autoplace settings for space locations,
    # but some are missing. fill them in here.
    RawSpaceLocation.nauvis: {
        RawEntity.tree_01,
        RawEntity.tree_02,
        RawEntity.tree_02_red,
        RawEntity.tree_03,
        RawEntity.tree_04,
        RawEntity.tree_05,
        RawEntity.tree_06,
        RawEntity.tree_06_brown,
        RawEntity.tree_07,
        RawEntity.tree_08,
        RawEntity.tree_08_brown,
        RawEntity.tree_08_red,
        RawEntity.tree_09,
        RawEntity.tree_09_brown,
        RawEntity.tree_09_red,
        RawEntity.dead_dry_hairy_tree,
        RawEntity.dead_grey_trunk,
        RawEntity.dead_tree_desert,
        RawEntity.dry_hairy_tree,
        RawEntity.dry_tree,
        RawEntity.tree_plant, # Unclear if this actually spawns naturally, but it's equivalent to the other trees anyway.
    },
    RawSpaceLocation.gleba: {
        RawEntity.jellystem,
        RawEntity.yumako_tree,
        RawEntity.slipstack,
        RawEntity.funneltrunk,
        RawEntity.hairyclubnub,
        RawEntity.teflilly,
        RawEntity.lickmaw,
        RawEntity.stingfrond,
        RawEntity.boompuff,
        RawEntity.sunnycomb,
        RawEntity.cuttlepop,
        RawEntity.water_cane,
        RawEntity.gleba_spawner,
        RawEntity.gleba_spawner_small,
        RawEntity.small_stomper_shell,
        RawEntity.medium_stomper_shell,
        RawEntity.big_stomper_shell,
    },
    RawSpaceLocation.vulcanus: {
        RawEntity.small_demolisher_corpse,
        RawEntity.medium_demolisher_corpse,
        RawEntity.big_demolisher_corpse,
    },
    RawSpaceLocation.fulgora: {
        RawEntity.fulgurite_small,
        RawEntity.lightning,
    },
}
_additional_autoplace_tiles = {
    RawSpaceLocation.nauvis: {
        RawTile.water_green,
        RawTile.deepwater_green,
    },
    RawSpaceLocation.gleba: {
        RawTile.water_shallow,
        RawTile.water_mud,
    }
}

_surfaces_with_lightning = {
    RawSpaceLocation.fulgora,
}
_surfaces_requiring_ice_platforms = {
    RawSpaceLocation.aquilo,
}

# Nauvis is missing its surface properties for some reason.
_default_gravity = 10
_default_magnetic_field = 90
_default_pressure =  1000
# This would lock a recipe/building to Nauvis.
_navis_surface_conditions = [{"property": "pressure", "min": _default_pressure, "max": _default_pressure}]

_asteroid_info_table = {
    RawEntity.medium_metallic_asteroid: (Capability.destroy_medium_asteroids,             RawItem.metallic_asteroid_chunk),
    RawEntity.medium_carbonic_asteroid: (Capability.destroy_medium_asteroids,             RawItem.carbonic_asteroid_chunk),
    RawEntity.medium_oxide_asteroid:    (Capability.destroy_medium_asteroids,             RawItem.oxide_asteroid_chunk),
    RawEntity.big_metallic_asteroid:    (Capability.destroy_big_and_smaller_asteroids,    RawItem.metallic_asteroid_chunk),
    RawEntity.big_carbonic_asteroid:    (Capability.destroy_big_and_smaller_asteroids,    RawItem.carbonic_asteroid_chunk),
    RawEntity.big_oxide_asteroid:       (Capability.destroy_big_and_smaller_asteroids,    RawItem.oxide_asteroid_chunk),
    RawEntity.huge_metallic_asteroid:   (Capability.destroy_huge_and_smaller_asteroids,   RawItem.metallic_asteroid_chunk),
    RawEntity.huge_carbonic_asteroid:   (Capability.destroy_huge_and_smaller_asteroids,   RawItem.carbonic_asteroid_chunk),
    RawEntity.huge_oxide_asteroid:      (Capability.destroy_huge_and_smaller_asteroids,   RawItem.oxide_asteroid_chunk),
    RawEntity.huge_promethium_asteroid: (Capability.destroy_huge_and_smaller_asteroids,   RawItem.promethium_asteroid_chunk),
}

_resource_category_to_capbility = {
   "basic-solid": Capability.automate_mining,
   "hard-solid":  Capability.mine_hard_solids,
   "basic-fluid": Capability.pump_entities,
}

_indirect_recycling_recipes = {
    # breaks multi-step loops in crafting dependencies.
    # TODO: is this really needed?
    RawRecipe.nuclear_fuel_reprocessing,
    RawRecipe.nutrients_from_spoilage,
}

_automated_planting_machines = {
    RawEntity.agricultural_tower,
}
_lightning_harnessing_machines = {
    RawEntity.lightning_rod,
    RawEntity.lightning_collector,
}
_asteroid_collecting_machines = {
    RawEntity.asteroid_collector,
}
_tile_mining_machines = {
    RawEntity.offshore_pump,
}

_fluid_conduit_machines = {
    RawEntity.pipe,
}

_electricity_conduit_machines = {
    RawEntity.small_electric_pole,
    RawEntity.medium_electric_pole,
    RawEntity.big_electric_pole,
    RawEntity.substation,
}

_entity_heat_buffer_mode = {
    RawEntity.nuclear_reactor: HeatBufferMode.produce,
    RawEntity.heating_tower:   HeatBufferMode.produce,
    RawEntity.heat_exchanger:  HeatBufferMode.consume,
    RawEntity.heat_pipe:       HeatBufferMode.conduct,
    RawEntity.heat_interface:  HeatBufferMode.editor_only,
}
_steam_165C_consuming_machines = {
    RawEntity.steam_engine,
}
_steam_500C_consuming_machines = {
    RawEntity.steam_turbine,
}

_ice_platform_items = {
    # Also the names of the entities.
    RawItem.ice_platform,
}
_heat_insulation_flooring_items = {
    RawItem.concrete,
    RawItem.hazard_concrete,
    RawItem.refined_concrete,
    RawItem.refined_hazard_concrete,
}

_power_producing_usage_priorities = {
    "primary-output", # lightning rod
    "secondary-output", # steam engine, steam turbine, fusion generator
    "solar", # solar panel
}
_power_consuming_usage_priorities = {
    "lamp", # small lamp
    "primary-input", # combinators, fusion reactor, rocket silo, ...
    "secondary-input", # assembling machine, pumpjack, ...
}

_fusion_plasma_producing_machines = {
    RawEntity.fusion_reactor,
}
_fusion_plasma_consuming_machines = {
    RawEntity.fusion_generator,
}

_override_recipe_data = {
    # I think it's actually a bug that bacteria cultivation doesn't ignore stats for catalysts like pentapod egg breading does.
    RawRecipe.copper_bacteria_cultivation: {
        "ingredients": [
            { "type": "item", "name": "copper-bacteria", "amount": 1,
                "ignored_by_stats": 1, # Added this.
            },
            { "type": "item", "name": "bioflux", "amount": 1, },
        ],
        "products": [
            { "type": "item", "name": "copper-bacteria", "probability": 1, "amount": 4,
                "ignored_by_stats": 1, # Added this.
                "ignored_by_productivity": 1, # Added this.
            },
        ],
    },
    RawRecipe.iron_bacteria_cultivation: {
        "ingredients": [
            { "type": "item", "name": "iron-bacteria", "amount": 1,
                "ignored_by_stats": 1, # Added this.
            },
            { "type": "item", "name": "bioflux", "amount": 1, },
        ],
        "products": [
            { "type": "item", "name": "iron-bacteria", "probability": 1, "amount": 4,
                "ignored_by_stats": 1, # Added this.
                "ignored_by_productivity": 1, # Added this.
            },
        ],
    },
}

# TODO: this is unimplemented, and also do we care?
_effective_technology_name_for_progressive_grouping = {
    RawTechnology.turbo_transport_belt: "logistics-4",
    RawTechnology.epic_quality: "quality-upgrade-1", # Really it's quality-upgrade-3. quality-module gives the first two builtin.
    RawTechnology.legendary_quality: "quality-upgrade-2",
}

def _get_asteroid_info(spawn_data):
    if spawn_data["type"] == "asteroid-chunk":
        # Just a free floating chunk.
        return Capability(0), spawn_data["asteroid"]
    if spawn_data["type"] == "entity":
        # Need to break it open.
        return _asteroid_info_table[spawn_data["asteroid"]]
    assert False, "what's this asteroid data: " + repr(spawn_data)

_fuel_category_to_power_type = {
    "chemical":  PowerType.chemical_fuel,
    "nutrients": PowerType.nutrients,
    "food":      PowerType.food,
    "nuclear":   PowerType.nuclear_fuel,
    "fusion":    PowerType.fusion_fuel,
}
def _get_machine_power_type(entity) -> PowerType:
    result = PowerType.free
    if "burner_prototype" in entity:
        [fuel_category] = entity["burner_prototype"]["fuel_categories"].keys()
        result |= _fuel_category_to_power_type[fuel_category]
    if "electric_energy_source_prototype" in entity and entity["electric_energy_source_prototype"]["usage_priority"] in _power_consuming_usage_priorities:
        result |= PowerType.electricity
    return result

def init():
    factorio_tech_id = factorio_base_id

    global fluids
    fluids = get_data()["fluid"].keys() - _parameter_names

    # Throughout this code, we assume there's no ambiguity between item and fluid names. Assert that assumption.
    fluid_item_name_collisions = fluids & get_data()["item"].keys()
    assert len(fluid_item_name_collisions) == 0, "so it's come to this, has it. we need to add 'type' fields to fluid and item references due to name collisions. :NotLikeThis: " + repr(fluid_item_name_collisions)

    # ===============
    # Space Locations
    # ===============
    item_to_mining_sources: dict[str, set[MiningSource]] = defaultdict(set)
    item_to_forage_locations: dict[str, set[str]] = defaultdict(set)

    natural_entity_to_locations: dict[str, set[str]] = defaultdict(set)
    natural_tile_to_locations: dict[str, set[str]] = defaultdict(set)
    space_locations: dict[str, SpaceLocation] = {}
    for location_name, space_location_data in get_data()["space_location"].items():
        unlock_names = {location_name}
        if "surface_properties" in space_location_data:
            # There is a surface here.
            props = space_location_data["surface_properties"]
            surface_properties = SurfaceProperties(
                gravity=props.get("gravity", _default_gravity),
                magnetic_field=props.get("magnetic-field", _default_magnetic_field),
                pressure=props.get("pressure", _default_pressure),
            )

            # This is a pair of locations.
            surface_location = SpaceLocation(location_name, surface_properties, unlock_names)
            space_location = SpaceLocation(location_name + ORBIT_SUFFIX, SPACE_SURFACE, unlock_names)
            space_locations[surface_location.name] = surface_location
            space_locations[space_location.name] = space_location
            surface_location.launch_to = space_location.name
            space_location.drop_to = surface_location.name

            # Surface features.
            if space_location_data.get("entities_require_heating", False):
                surface_location.threats |= Capability.heat_buildings
            if location_name in _surfaces_requiring_ice_platforms:
                surface_location.threats |= Capability.build_on_ice_platforms
            if location_name in _surfaces_with_lightning:
                surface_location.threats |= Capability.harness_lightning
            for entity_name in itertools.chain(
                space_location_data["map_gen_settings"]["autoplace_settings"]["entity"]["settings"].keys(),
                _additional_autoplace_entities.get(location_name, set()),
            ):
                natural_entity_to_locations[entity_name].add(surface_location.name)
            for tile_name in (
                space_location_data["map_gen_settings"]["autoplace_settings"]["tile"]["settings"].keys() |
                _additional_autoplace_tiles.get(location_name, set())
            ):
                natural_tile_to_locations[tile_name].add(surface_location.name)
        else:
            # There is no surface here. e.g. solar-system-edge.
            space_location = SpaceLocation(location_name, SPACE_SURFACE, unlock_names)
            space_locations[space_location.name] = space_location
        # Asteroid info.
        for spawn_data in space_location_data.get("asteroid_spawn_definitions", []):
            threats, item = _get_asteroid_info(spawn_data)
            space_location.threats |= threats
            # Add a natural resource for this now, because we already know everything.
            item_to_mining_sources[item].add(MiningSource(item, space_location.name, threats | Capability.collect_asteroids, ()))
        space_location.threats |= Capability.generate_electricity_in_space
        if space_location_data["solar_power_in_space"] < 100:
            # This is true for aquilo and beyond.
            space_location.threats |= Capability.generate_electricity_in_dark_space

    for location_name, space_connection_data in get_data()["space_connection"].items():
        connection_names = [
            space_connection_data["from"]["name"],
            space_connection_data["to"]["name"],
        ]
        unlock_names = set(connection_names)
        # We actually connect to the orbit above the planets, not directly to the surface.
        for i, name in enumerate(connection_names):
            if name + ORBIT_SUFFIX in space_locations.keys():
                connection_names[i] = name + ORBIT_SUFFIX
        space_location = SpaceLocation(location_name, SPACE_SURFACE, unlock_names)
        space_locations[space_location.name] = space_location
        # Connect
        space_location.thrust_to = connection_names
        for name in connection_names:
            space_locations[name].thrust_to.append(space_location.name)
        # Asteroid info.
        for spawn_data in space_connection_data.get("asteroid_spawn_definitions", []):
            capabilities, item = _get_asteroid_info(spawn_data)
            space_location.threats |= capabilities
            # Add a natural resource for this now, because we already know everything.
            item_to_mining_sources[item].add(MiningSource(item, space_location.name, threats | Capability.collect_asteroids, ()))
        space_location.threats |= Capability.generate_electricity_in_space
        solar_power_in_space = min(
            get_data()["space_location"][space_connection_data["from"]["name"]]["solar_power_in_space"],
            get_data()["space_location"][space_connection_data["to"]  ["name"]]["solar_power_in_space"],
        )
        if solar_power_in_space < 100:
            # This is true for all of aquilo's connections and beyond.
            space_location.threats |= Capability.generate_electricity_in_dark_space

    # =================
    # Natural Resources
    # =================
    # Find mineable and forageable resources.
    for entity_name, entity in get_data()["entity"].items():
        if "autoplace_specification" not in entity: continue # We're looking for natural features.
        if entity["mineable_properties"]["minable"]:
            products = [p["name"] for p in entity["mineable_properties"]["products"]]
            required_capabilities = Capability(0)
            required_ingredients = ()
            if "resource_category" in entity:
                # Mineable
                required_capabilities |= _resource_category_to_capbility[entity["resource_category"]]
                if "required_fluid" in entity["mineable_properties"]:
                    required_ingredients = (entity["mineable_properties"]["required_fluid"],)
                    required_capabilities |= Capability.mine_with_fluid
                for product in products:
                    for home in natural_entity_to_locations.get(entity_name, ()):
                        item_to_mining_sources[product].add(MiningSource(item, home, required_capabilities, required_ingredients))
            else:
                # Foragable
                for product in products:
                    for home in natural_entity_to_locations.get(entity_name, ()):
                        item_to_forage_locations[product].add(home)
                if "items_to_place_this" in entity:
                    # Can additionally be automated with agriculture.
                    # This is probably the wrong logic for determining what the agricultural tower is willing to plant,
                    # but it gets the answer right for Space Age: yumako, jellynut, tree.
                    # Other ideas:
                    #  * entity["surface_conditions"] -- for tree-plant
                    #  * entity["autoplace_specification"]["tile_restriction"] -- for jellystem
                    for ingredient_data in entity["items_to_place_this"]:
                        ingredient = ingredient_data["name"]
                        for product in products:
                            for home in natural_entity_to_locations.get(entity_name, ()):
                                item_to_mining_sources[product].add(MiningSource(item, home, Capability.automate_planting, (ingredient,)))
        elif "loot" in entity:
            # Pentapod eggs from gleba spawners (aka egg rafts) use .loot instead of .mineable_properties.
            products = [p["item"] for p in entity["loot"]]
            for product in products:
                for home in natural_entity_to_locations.get(entity_name, ()):
                    item_to_forage_locations[product].add(home)
        else: continue

    # Offshore pump yields fluids sourced from tiles.
    for tile_name, tile_data in get_data()["tile"].items():
        if "fluid" not in tile_data: continue
        fluid_name = tile_data["fluid"]["name"]
        for home in natural_tile_to_locations.get(tile_name, ()):
            item_to_mining_sources[fluid_name].add(MiningSource(fluid_name, home, Capability.pump_tiles, ()))

    # =====
    # Items
    # =====

    ammo_category_to_weapon_items = defaultdict(set)
    ammo_category_to_ammo_items = defaultdict(set)
    power_type_to_fuel_items = defaultdict(set)
    ice_platform_items = set()
    heat_insulation_flooring_items = set()
    for item_name, item_data in get_data()["item"].items():
        stack_size = item_data["stack_size"]
        weight_in_g = item_data["weight"]
        if weight_in_g <= 100:
            # All items with the default weight are not "real" items except for pistol.
            # Let's also ignore pistol, unless we want to make it logically relevant somehow.
            continue
        rocket_capacity = 1_000_000 // weight_in_g
        items[item_name] = Item(item_name, stack_size, rocket_capacity)

        # Handheld weapons are logically relevant for capturing biter spawners.
        if "attack_parameters" in item_data:
            # We're really only looking for rocket-launcher here.
            for ammo_category in item_data["attack_parameters"]["ammo_categories"]:
                ammo_category_to_weapon_items[ammo_category].add(item_name)
        # Ammo is logically relevant for destroying asteroids of various sizes.
        if "ammo_category" in item_data:
            ammo_category_to_ammo_items[item_data["ammo_category"]["name"]].add(item_name)
        # Fuel
        if "fuel_category" in item_data:
            power_type_to_fuel_items[_fuel_category_to_power_type[item_data["fuel_category"]]].add(item_name)
        # Ice platforms
        if item_name in _ice_platform_items:
            ice_platform_items.add(item_name)
        if item_name in _heat_insulation_flooring_items:
            heat_insulation_flooring_items.add(item_name)

    # ========
    # Machines
    # ========

    crafting_category_to_machines = defaultdict(set)
    mining_capability_to_machines = defaultdict(set)
    automated_planting_machines = set()
    lightning_harnessing_machines = set()
    asteroid_collecting_machines = set()
    tile_mining_machines = set()
    fluid_conduit_machines = set()
    water_boiling_machines_165C = set()
    water_boiling_machines_500C = set()
    electricity_producing_machines = set()
    electricity_conduit_machines = set()
    heat_producing_machines = set()
    heat_conduit_machines = set()
    fusion_plasma_producing_machines = set()
    thruster_machines = set()
    lab_machines = set()
    science_pack_to_labs = defaultdict(set)
    ammo_category_to_weapon_entities = defaultdict(set)
    for entity_name, entity in get_data()["entity"].items():
        is_machine = False
        # What powers this machine?
        power_required = _get_machine_power_type(entity)
        # Crafting buildings and the character:
        for category in entity.get("crafting_categories", ()):
            crafting_category_to_machines[category].add(entity_name)
            is_machine = True
        # Mining buildings and the character:
        for category in entity.get("resource_categories", ()):
            mining_capability_to_machines[_resource_category_to_capbility[category]].add(entity_name)
            is_machine = True
        # agricultural tower:
        if entity_name in _automated_planting_machines:
            automated_planting_machines.add(entity_name)
            is_machine = True
        # lightning rods:
        if entity_name in _lightning_harnessing_machines:
            lightning_harnessing_machines.add(entity_name)
            is_machine = True
        # asteroid collector:
        if entity_name in _asteroid_collecting_machines:
            asteroid_collecting_machines.add(entity_name)
            is_machine = True
        # Offshore pump:
        if entity_name in _tile_mining_machines:
            tile_mining_machines.add(entity_name)
            is_machine = True
        # Fluid conduits:
        if entity_name in _fluid_conduit_machines:
            fluid_conduit_machines.add(entity_name)
            is_machine = True
        # Water boiling:
        if "boiler_mode" in entity:
            if entity["target_temperature"] == 165:
                water_boiling_machines_165C.add(entity_name)
            elif entity["target_temperature"] == 500:
                water_boiling_machines_500C.add(entity_name)
            else: assert False, "unrecognized boiled water temperature: " + repr(entity["target_temperature"])
            is_machine = True
        # Steam consuming:
        if entity_name in _steam_165C_consuming_machines:
            power_required |= PowerType.steam_165C
        elif entity_name in _steam_500C_consuming_machines:
            power_required |= PowerType.steam_500C
        # Electricity producers:
        if "electric_energy_source_prototype" in entity and entity["electric_energy_source_prototype"]["usage_priority"] in _power_producing_usage_priorities:
            electricity_producing_machines.add(entity_name)
            is_machine = True
        # Electricity conduits:
        if entity_name in _electricity_conduit_machines:
            electricity_conduit_machines.add(entity_name)
            is_machine = True
        # Heat producers, consumers, and conduits:
        if "heat_buffer_prototype" in entity:
            mode = _entity_heat_buffer_mode[entity_name]
            if mode == HeatBufferMode.produce:
                heat_producing_machines.add(entity_name)
                is_machine = True
            elif mode == HeatBufferMode.consume:
                power_required |= PowerType.heat
                is_machine = True
            elif mode == HeatBufferMode.conduct:
                heat_conduit_machines.add(entity_name)
                is_machine = True
            elif mode == HeatBufferMode.editor_only:
                pass # ignore
            else: assert False
        # Fusion reactor:
        if entity_name in _fusion_plasma_producing_machines:
            fusion_plasma_producing_machines.add(entity_name)
            is_machine = True
        # Fusion generator:
        if entity_name in _fusion_plasma_consuming_machines:
            power_required |= PowerType.fusion_plasma
            is_machine = True
        # Thruster:
        if "max_performance" in entity:
            thruster_machines.add(entity_name)
            power_required |= PowerType.thruster_fuel
            is_machine = True
        # Labs:
        if "lab_inputs" in entity:
            lab_machines.add(entity_name)
            for science_pack_name in entity["lab_inputs"]:
                science_pack_to_labs[science_pack_name].add(entity_name)
            is_machine = True
        # Turrets and vehicles:
        if "indexed_guns" in entity:
            # Some entities describe their weapon abilities as gun items, which is more comprehensive and reliable when present.
            # e.g. tank has 3 different gun types, and the tank's own attack_parameters only represent one of them.
            for gun_data in entity["indexed_guns"]:
                for ammo_category in get_data()["item"][gun_data["name"]]["attack_parameters"]["ammo_categories"]:
                    ammo_category_to_weapon_entities[ammo_category].add(entity_name)
            is_machine = True
        elif "attack_parameters" in entity and "items_to_place_this" in entity:
            # This entity can be placed by the player (it is not an enemy), it can attack, and it's attacks are not specified by items.
            # E.g. gun-turret
            for ammo_category in entity["attack_parameters"]["ammo_categories"]:
                ammo_category_to_weapon_entities[ammo_category].add(entity_name)
            is_machine = True

        # Where can this machine operate?
        if "surface_conditions" in entity:
            locations = set(
                location_name for location_name, location in space_locations.items()
                if location.surface_properties.satisfies(entity["surface_conditions"])
            )
        else:
            locations = None
        can_freeze = entity.get("heating_energy", 0) != 0

        # Do we care?
        if not is_machine:
            continue

        if entity_name != RawEntity.character:
            # Assume a 1:1 correspondance between items and entities.
            assert len(entity.get("items_to_place_this", [])) == 1, "weirdly placed machine: " + entity_name
            assert entity["items_to_place_this"][0]["count"] == 1, "a machine shouldn't spread out like a curved rail: " + entity_name
            assert entity["items_to_place_this"][0]["name"] == entity_name, "expected building entity and item to have matching names: " + entity_name
            # Note this assumption isn't exactly correct for launching capture bot rockets to create captive biter spawners.
            # The pseudo recipes below work around this.

        machines[entity_name] = Machine(entity_name, power_required, locations, can_freeze)

    assert all(labs == next(iter(science_pack_to_labs.values())) for labs in science_pack_to_labs.values()), "labs that take a subset of science packs are not supported"

    # =======
    # Recipes
    # =======

    starting_recipes: set[str] = set()
    for recipe_name, recipe_data in get_data()["recipe"].items():
        if recipe_data["enabled"]:
            starting_recipes.add(recipe_name)
        energy = recipe_data["energy"] # crafting time in seconds.
        override_data = _override_recipe_data.get(recipe_name, recipe_data)

        inputs = {
            i["name"]: i["amount"] - i.get("ignored_by_stats", 0)
            for i in override_data["ingredients"]
        }
        outputs = {
            p["name"]: p["amount"] * p.get("probability", 1) + p.get("extra_count_fraction", 0) - p.get("ignored_by_stats", 0)
            for p in override_data["products"]
        }

        if any(amount < 0 for amount in outputs.values()):
            # This only happens for dead-end recycling recipes, such as copper-ore-recycling.
            assert (
                recipe_data["category"] == "recycling" and
                len(inputs) == 1 and
                inputs.keys() == outputs.keys() and
                all(amount == 0 for amount in inputs.values())
            ), "expected a negative byproduct to be part of a dead-end recycling recipe"
            classification = RecipeClassification.dead_end_recycling
        elif all(amount == 0 for amount in inputs.values()) and all(amount == 0 for amount in outputs.values()):
            # This is a lossless conversion recipe, such as barreling/unbarreling or fluoroketone cooling.
            # Thematically the recipe respects conservation of mass, if you like.
            classification = RecipeClassification.conversion
        elif any(amount == 0 and name in outputs and outputs[name] > 0 for name, amount in inputs.items()):
            # Use an item (and something else surely) to produce more of the item (and something else possibly).
            # e.g. kovarex, pentapod egg breeding, coal liquefaction
            classification = RecipeClassification.breeding
        else:
            # e.g. electronic circuit, cryogenic science pack
            classification = RecipeClassification.standard

        # What machines can perform this recipe?
        valid_machines = crafting_category_to_machines[recipe_data["category"]]
        # Where can this recipe be performed?
        if "surface_conditions" in recipe_data:
            locations = set(
                location_name for location_name, location in space_locations.items()
                if location.surface_properties.satisfies(recipe_data["surface_conditions"])
            )
        else:
            locations = None
        # Should this be excluded from free samples?
        is_unusual_recipe = recipe_data["hidden_from_player_crafting"]

        recipes[recipe_name] = Recipe(recipe_name, inputs, outputs, energy, classification, valid_machines, locations, is_unusual_recipe)
    product_to_recipes: dict[str, set[str]] = defaultdict(set)
    for recipe_name, recipe in recipes.items():
        for product in recipe.outputs.keys():
            product_to_recipes[product].add(recipe_name)

    # ============
    # Technologies
    # ============
    recipe_to_unlocking_technologies: dict[str, set[str]] = defaultdict(set)
    space_location_to_unlocking_technologies: dict[str, set[str]] = defaultdict(set)
    mining_with_fluid_unlocking_technologies = set()
    for technology_name, technology_data in get_data()["technology"].items():
        prerequisites = set(technology_data["prerequisites"].keys())
        ingredients = {i["name"]: i["amount"] for i in technology_data["research_unit_ingredients"] }
        if len(ingredients) > 0:
            # Research technology (using science packs and labs).
            assert set(ingredients.values()) == {1}, "update comment on ResearchRequirement.ingredients to no longer claim the amount is always 1"
            if "research_unit_count_formula" in technology_data:
                units = None # infinite
            else:
                units = technology_data["research_unit_count"]
            energy_in_ticks = technology_data["research_unit_energy"]
            assert energy_in_ticks % 60 == 0, "update Technology.energy type from int to float"
            energy = energy_in_ticks // 60
            requirement = ResearchRequirement(ingredients, units, energy)
        elif "research_trigger" in technology_data:
            # Trigger technology.
            trigger = technology_data["research_trigger"]
            if trigger["type"] == "craft-item":
                requirement = CraftRequirement(trigger["item"]["name"], trigger["count"])
            elif trigger["type"] == "mine-entity":
                requirement = MineRequirement(trigger["entity"])
            elif trigger["type"] == "build-entity":
                requirement = BuildRequirement(trigger["entity"])
            elif trigger["type"] == "capture-spawner":
                requirement = CaptureSpawnerRequirement()
            elif trigger["type"] == "create-space-platform":
                requirement = CreateSpacePlatformRequirement()
            else: assert False, "unrecognized research trigger type: " + repr(trigger["type"])
        else: assert False, "technology appears to have no cost or trigger: " + technology_name

        technology = Technology(technology_name, prerequisites, requirement)
        technologies[technology_name] = technology

        does_something_important = False
        for effect in technology_data["effects"]:
            if effect["type"] == "unlock-recipe":
                recipe_to_unlocking_technologies[effect["recipe"]].add(technology_name)
                does_something_important = True
            elif effect["type"] == "unlock-space-location":
                space_location_to_unlocking_technologies[effect["space_location"]].add(technology_name)
                does_something_important = True
            elif effect["type"] == "mining-with-fluid":
                mining_with_fluid_unlocking_technologies.add(technology_name)
                does_something_important = True
            else:
                pass # It does something else not relevant to logic.
        if not technology_data["effects"]:
            empty_technologies.add(technology_name)

        if type(requirement) != ResearchRequirement:
            continue # No more complexity to consider for now.

        # Technology with levels is usually something we want to make progressive.
        level = technology_data["level"]
        try:
            # The tech name ending with "-1" or another number is actually meaningful.
            # This is documented here: https://lua-api.factorio.com/latest/types/TechnologyUnit.html#count_formula
            progressive_group_name, level_from_name = technology_name.rsplit("-", 1)
            level_from_name = int(level_from_name)
        except ValueError: # It doesn't end with a number.
            progressive_group_name = None
        else:
            assert level_from_name == level, "technology name lies about the level: " + technology_name
        if level != 1:
            assert progressive_group_name != None, "leveled technology doesn't have a number in the name: " + technology_name
        # Infinite research.
        if technology.is_infinite():
            assert technology_data["max_level"] == 4294967295, "consider evaluating the cost at each finite level instead of using an 'infinite' formula"
            assert not does_something_important, "infinite research is doing something important: " + technology_name
            if progressive_group_name == None:
                # The technology that starts infinite from level 1 doesn't include numbers in the names.
                # e.g. 'steel-plate-productivity', 'health'
                progressive_group_name = technology_name
        if progressive_group_name != None:
            progressive_technology_chains[progressive_group_name][level] = technology_name
    # Fill in sneaky progressive technologies like 'automation' as level 1 despite not being called 'automation-1'.
    for progressive_group_name, progressive_chain in progressive_technology_chains.items():
        if 2 in progressive_chain and 1 not in progressive_chain:
            assert progressive_group_name in technologies, "why is there a 2 if there's no 1? " + progressive_group_name
            progressive_chain[1] = progressive_group_name
        # Make sure our assumptions are correct about the way progressive technologies are defined.
        assert set(progressive_chain.keys()) == set(range(1, len(progressive_chain)+1)), "skipped progressive levels: " + progressive_group_name
        if len(progressive_chain) == 1:
            assert technologies[progressive_chain[1]].is_infinite(), "technology ends with -1 without any other levels: " + progressive_chain[1]
        assert not any(technologies[progressive_chain[level]].is_infinite() for level in range(1, len(progressive_chain)+1-1)), "infinite technology must be the highest level defined in the group: " + progressive_group_name




    # =====
    # Logic
    # =====
    # Thanks to an assertion above, we can conflate item names with machine names here for simplicity.
    fmt_discover_location = "Discover {}".format
    fmt_reach_location = "Reach {}".format
    fmt_access_item = "Access {}".format
    fmt_automate_item = "Automate {}".format
    fmt_capability = lambda capability: "Can {}".format(capability.name.replace("_", " "))
    fmt_operate_machine = "Operate {}".format
    fmt_supply_power = lambda power_type: "Supply {}".format(power_type.name.replace("_", " "))
    fmt_unlock_research = lambda name: name # These are proper Archipelago items.
    fmt_learn_recipe = "Learn {}".format

    can_launch_rockets = fmt_automate_item(RawItem.rocket_part)

    all_ingredient_items = set(itertools.chain.from_iterable(
        recipe.inputs.keys() for recipe in recipes.values()
        if recipe.classification != RecipeClassification.dead_end_recycling
    ))

    # Reach locations.
    for space_location in space_locations.values():
        # Inbound connections
        logic_events[fmt_reach_location(space_location.name)] = {"and": [
            {"and": [fmt_discover_location(name) for name in space_location.unlock_names]},
            {"or": [
                *[{"and": [
                    # Thrust from each thrust_to location.
                    fmt_reach_location(connection_location),
                    fmt_capability(Capability.travel_space),
                    *[fmt_capability(threat) for threat in space_locations[connection_location].threats],
                ]} for connection_location in space_location.thrust_to],
                *([{"and": [
                    # Launch from the drop_to location.
                    fmt_reach_location(space_location.drop_to),
                    can_launch_rockets,
                ]}] if space_location.drop_to else []),
                *([
                    # Drop from the launch_to location.
                    fmt_reach_location(space_location.launch_to),
                ] if space_location.launch_to else []),
            ]},
        ]}
    # Discover them too.
    for name, techs in space_location_to_unlocking_technologies.items():
        logic_events[fmt_discover_location(name)] = {"or": [fmt_unlock_research(technology) for technology in techs]}
    # Start on Nauvis
    logic_events[fmt_discover_location(RawSpaceLocation.nauvis)] = ALWAYS
    logic_events[fmt_reach_location(RawSpaceLocation.nauvis)] = ALWAYS

    # Capabilities.
    for capability in Capability:
        if capability in mining_capability_to_machines:
            expr = {"or": [
                fmt_operate_machine(name) for name in mining_capability_to_machines[capability]
                if name != RawEntity.character # Smacking rocks does not count as automating mining.
            ]}
        elif capability == Capability.mine_with_fluid:
            expr = {"or": [fmt_unlock_research(name) for name in mining_with_fluid_unlocking_technologies]}
        elif capability == Capability.pump_tiles:
            expr = {"or": [fmt_operate_machine(name) for name in tile_mining_machines]}
        elif capability == Capability.automate_planting:
            expr = {"or": [fmt_operate_machine(name) for name in automated_planting_machines]}
        elif capability == Capability.harness_lightning:
            expr = {"or": [fmt_operate_machine(name) for name in lightning_harnessing_machines]}
        elif capability == Capability.capture_biter_spawners:
            expr = {"and": [
                fmt_reach_location(RawSpaceLocation.nauvis),
                fmt_access_item(RawItem.capture_robot_rocket),
                {"or": [
                    *[fmt_access_item(item) for item in ammo_category_to_weapon_items["rocket"]],
                    *[fmt_access_item(entity) for entity in ammo_category_to_weapon_entities["rocket"]],
                ]}
            ]}
        elif capability == Capability.heat_buildings:
            expr = {"and": [
                {"or": [fmt_operate_machine(name) for name in heat_producing_machines]},
                {"or": [fmt_access_item(name) for name in heat_conduit_machines]},
            ]}
        elif capability == Capability.build_on_ice_platforms:
            expr = {"and": [
                {"or": [fmt_automate_item(name) for name in ice_platform_items]},
                {"or": [fmt_automate_item(name) for name in heat_insulation_flooring_items]},
            ]}
        elif capability == Capability.collect_asteroids:
            expr = {"or": [fmt_operate_machine(name) for name in asteroid_collecting_machines]}
        elif capability == Capability.travel_space:
            expr = {"or": [fmt_operate_machine(name) for name in thruster_machines]}
        elif capability == Capability.generate_electricity_in_space:
            expr = "TODO" # TODO
        elif capability == Capability.generate_electricity_in_dark_space:
            expr = "TODO" # TODO
        elif capability == Capability.destroy_medium_asteroids:
            expr = "TODO" # TODO
        elif capability == Capability.destroy_big_asteroids:
            expr = "TODO" # TODO
        elif capability == Capability.destroy_huge_asteroids:
            expr = "TODO" # TODO
        else: assert False, "forgot a capability: " + repr(capability)

        logic_events[fmt_capability(capability)] = expr
        del expr # give me a NameError if i forget to assign to expr in this loop.

    # Machines
    for machine_name, machine in machines.items():
        # Craft the machine.
        obtain_expr = fmt_access_item(machine_name)
        if machine_name == RawEntity.captive_biter_spawner:
            # There's an alternate way to get this.
            obtain_expr = {"or": [
                fmt_capability(Capability.capture_biter_spawners),
                obtain_expr,
            ]}
        expr = {"and": [
            obtain_expr,
            # Power it.
            *[fmt_supply_power(power_type) for power_type in machine.power_required],
            # Place it.
            *([{"or": [
                fmt_reach_location(space_location) for space_location in machine.locations
            ]}] if machine.locations != None else []),
        ]}
        logic_events[fmt_operate_machine(machine_name)] = expr

    # Power
    for power_type in PowerType:
        if power_type in power_type_to_fuel_items:
            expr = {"or": [fmt_access_item(item) for item in power_type_to_fuel_items[power_type]]}
        elif power_type == PowerType.steam_165C:
            expr = {"and": [
                # Steam too hot still works.
                {"or": [fmt_operate_machine(machine) for machine in itertools.chain(water_boiling_machines_165C, water_boiling_machines_500C)]},
                {"or": [fmt_access_item(machine)     for machine in fluid_conduit_machines]},
            ]}
        elif power_type == PowerType.steam_500C:
            expr = {"and": [
                {"or": [fmt_operate_machine(machine) for machine in water_boiling_machines_500C]},
                {"or": [fmt_access_item(machine)     for machine in fluid_conduit_machines]},
            ]}
        elif power_type == PowerType.electricity:
            expr = {"and": [
                {"or": [fmt_operate_machine(machine) for machine in electricity_producing_machines]},
                {"or": [fmt_access_item(machine)     for machine in electricity_conduit_machines]},
            ]}
        elif power_type == PowerType.heat:
            expr = {"and": [
                {"or": [fmt_operate_machine(machine) for machine in heat_producing_machines]},
                {"or": [fmt_access_item(machine)     for machine in heat_conduit_machines]},
            ]}
        elif power_type == PowerType.fusion_plasma:
            expr = {"and": [
                {"or": [fmt_operate_machine(machine) for machine in fusion_plasma_producing_machines]},
                # No conduits for fusion plasma
            ]}
        elif power_type == PowerType.thruster_fuel:
            expr = {"and": [
                fmt_automate_item(RawFluid.thruster_fuel),
                fmt_automate_item(RawFluid.thruster_oxidizer),
                {"or": [fmt_access_item(machine) for machine in fluid_conduit_machines]},
            ]}
        else: assert False, "forgot a PowerType: " + repr(power_type)
        logic_events[fmt_supply_power(power_type)] = expr
        del expr # give me a NameError if i forget to assign to expr in this loop.

    # Research
    for technology_name, technology in technologies.items():
        if type(technology.requirement) == ResearchRequirement:
            expr = {"and": [
                {"or": [fmt_operate_machine(lab) for lab in lab_machines]},
                *[fmt_automate_item(science_pack) for science_pack in technology.requirement.ingredients.keys()],
            ]}
        elif type(technology.requirement) == CraftRequirement:
            # FIXME: This assumes that mining up the item counts as crafting it, which i think is wrong, but i don't think it ever matters.
            expr = fmt_access_item(technology.requirement.item)
        elif type(technology.requirement) == BuildRequirement:
            # FIXME: This also requires that you power the thing, which is not correct,
            # but it's more correct than just crafting it.
            # (building an asteroid collector requires launching a space platform starter pack, but not having solar panels.)
            # This incorrect logic inflicts unnecessary logical requirements,
            # which at least is erring in the right direction.
            expr = fmt_operate_machine(technology.requirement.entity)
        elif type(technology.requirement) == MineRequirement:
            expr = {"or": [fmt_reach_location(space_location) for space_location in natural_entity_to_locations[technology.requirement.entity]]}
        elif type(technology.requirement) == CaptureSpawnerRequirement:
            expr = fmt_capability(Capability.capture_biter_spawners)
        elif type(technology.requirement) == CreateSpacePlatformRequirement:
            expr = {"and": [
                can_launch_rockets,
                fmt_access_item(RawItem.space_platform_starter_pack),
            ]}
        else: assert False, "forgot a requirement type: " + repr(technology.requirement)
        logic_events[fmt_unlock_research(technology_name)] = expr
        del expr # give me a NameError if i forget to assign to expr in this loop.

    # Recipes
    for recipe_name, recipe in recipes.items():
        if recipe_name in starting_recipes:
            expr = ALWAYS
        else:
            expr = {"or": [
                fmt_unlock_research(technology_name)
                for technology_name in recipe_to_unlocking_technologies.get(recipe_name, [])
            ]}
        logic_events[fmt_learn_recipe(recipe_name)] = expr

    # Items
    for item_name in itertools.chain(items.keys(), fluids):
        for fmt_automate_or_access in [fmt_access_item, fmt_automate_item]:
            source_exprs = []
            # Foraging sources only count for accessing the item, not for automating it.
            if fmt_automate_or_access is fmt_access_item:
                for home in item_to_forage_locations.get(item_name, []):
                    source_exprs.append(fmt_reach_location(home))
            # Mining
            for mining_source in item_to_mining_sources.get(item_name, []):
                source_exprs.append({"and": [
                    fmt_reach_location(mining_source.location),
                    *[fmt_capability(capability) for capability in mining_source.required_capabilities],
                    *[fmt_access_item(ingredient) for ingredient in mining_source.required_ingredients],
                ]})
            # Crafting
            for recipe_name in product_to_recipes.get(item_name, []):
                recipe = recipes[recipe_name]
                if recipe.classification == RecipeClassification.dead_end_recycling:
                    continue # e.g. steel recycling is not a source of steel.
                amount_of_this_product = recipe.outputs[item_name]
                if amount_of_this_product == 0 and recipe.classification != RecipeClassification.conversion:
                    continue # e.g. quantum-processor is not a source of fluoroketone-hot
                # This recipe works.
                recipe_exprs = [
                    fmt_learn_recipe(recipe_name),
                ]
                needs_pipes = False
                for ingredient, amount in recipe.inputs.items():
                    if amount <= 0 and recipe.classification != RecipeClassification.conversion:
                        # This item must be present, but isn't "consumed" so to speak by the recipe.
                        # Automating this recipe only needs limited access to the ingredient.
                        recipe_exprs.append(fmt_access_item(ingredient))
                    else:
                        recipe_exprs.append(fmt_automate_or_access(ingredient))
                    if ingredient in fluids:
                        needs_pipes = True
                if needs_pipes:
                    recipe_exprs.append({"or": [fmt_access_item(machine) for machine in fluid_conduit_machines]})
                machine_exprs = []
                for machine in recipe.machines:
                    if machine == RawEntity.character:
                        # The character can only create limited quantities. Not proper automation.
                        if fmt_automate_or_access is fmt_access_item:
                            machine_expr = ALWAYS
                        else:
                            machine_expr = NEVER
                    else:
                        machine_expr = fmt_operate_machine(machine)
                    machine_exprs.append(machine_expr)
                recipe_exprs.append({"or": machine_exprs})
                if recipe.locations != None:
                    recipe_exprs.append({"or": [fmt_reach_location(location_name) for location_name in recipe.locations]})
                source_exprs.append({"and": recipe_exprs})
            logic_events[fmt_automate_or_access(item_name)] = {"or": source_exprs}

    import os, json
    with open(os.path.join(os.path.dirname(__file__), "data", "logic.json"), "w") as f:
        f.write(json.dumps({k: optimize_expr(v) for k, v in logic_events.items()}, indent=2, sort_keys=True))
        f.write("\n")

    import pdb; pdb.set_trace()
    import json; print(json.dumps({k: optimize_expr(v) for k, v in logic_events.items()}, indent=2))
    import pdb; pdb.set_trace()

    return None

ALWAYS = "(always)"
NEVER = "(never)"

def optimize_expr(expr):
    def recurse(expr):
        if type(expr) != dict: return expr
        if "or" in expr:
            clauses = expr["or"]
            if len(clauses) == 0: return NEVER
            if len(clauses) == 1: return recurse(clauses[0])
            new_clauses = []
            for clause in clauses:
                clause = recurse(clause)
                if clause == NEVER: continue # A or False == A
                if clause == ALWAYS: return ALWAYS # A or True == True
                if type(clause) == dict and "or" in clause:
                    # A or (B or C) == A or B or C
                    new_clauses.extend(clause["or"])
                else:
                    new_clauses.append(clause)
            # (A and B) or (A and C) == A and (B or C)
            counter = Counter(itertools.chain.from_iterable(
                (sub_clause for sub_clause in sub_expr["and"] if type(sub_clause) == str)
                for sub_expr in new_clauses if type(sub_expr) == dict and "and" in sub_expr
            ))
            omnipresent_sub_clauses = set(sub_clause for sub_clause, count in counter.items() if count == len(new_clauses))
            if len(omnipresent_sub_clauses) > 0:
                return {"and": [
                    *omnipresent_sub_clauses,
                    {"or": [
                        {"and": [
                            sub_clause for sub_clause in clause["and"]
                            if not (type(sub_clause) == str and sub_clause in omnipresent_sub_clauses)
                        ]} for clause in new_clauses
                    ]},
                ]}
            return {"or": new_clauses}

        elif "and" in expr:
            clauses = expr["and"]
            if len(clauses) == 0: return ALWAYS
            if len(clauses) == 1: return recurse(clauses[0])
            new_clauses = []
            for clause in clauses:
                clause = recurse(clause)
                if clause == ALWAYS: continue # A and True == A
                if clause == NEVER: return NEVER # A and False == False
                if type(clause) == dict and "and" in clause:
                    # A and (B and C) == A and B and C
                    new_clauses.extend(clause["and"])
                else:
                    new_clauses.append(clause)

            # (A or B) and (A or C) == A or (B and C)
            counter = Counter(itertools.chain.from_iterable(
                (sub_clause for sub_clause in sub_expr["or"] if type(sub_clause) == str)
                for sub_expr in new_clauses if type(sub_expr) == dict and "or" in sub_expr
            ))
            omnipresent_sub_clauses = set(sub_clause for sub_clause, count in counter.items() if count == len(new_clauses))
            if len(omnipresent_sub_clauses) > 0:
                import pdb; pdb.set_trace() # Test this logic and then delete this breakpoint.
                return {"or": [
                    *omnipresent_sub_clauses,
                    {"and": [
                        {"or": [
                            sub_clause for sub_clause in clause["or"]
                            if not (type(sub_clause) == str and sub_clause in omnipresent_sub_clauses)
                        ]} for clause in new_clauses
                    ]},
                ]}
            return {"and": new_clauses}

        else: assert False
        return expr

    import json
    original_expr = json.dumps(expr,sort_keys=True,separators=(',', ':'))
    while True:
        expr = recurse(expr)
        new_expr = json.dumps(expr,sort_keys=True,separators=(',', ':'))
        if original_expr == new_expr: break
        original_expr = new_expr


    def sorted_recursive(expr):
        if type(expr) != dict: return expr
        expr = {k: (sorted_recursive(x) for x in v) for k, v in expr.items()}
        expr = {k: sorted(v, key=json.dumps) for k, v in expr.items()}
        return expr
    return sorted_recursive(expr)
init()

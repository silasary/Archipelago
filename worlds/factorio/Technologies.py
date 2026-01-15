from __future__ import annotations

import functools, itertools
import string
from collections import Counter, defaultdict
from typing import Dict, Set, FrozenSet, Tuple, Union, List, Any, Optional
from dataclasses import dataclass
from enum import IntEnum, IntFlag

import orjson

import Utils
from . import Options
from .data import get_data, Entity as RawEntity, Item as RawItem, Tile as RawTile, Recipe as RawRecipe, SpaceLocation as RawSpaceLocation

# TODO: delete this 
"""
# These are the exports we're expected to provide:
from .Technologies import free_sample_exclusions, tech_to_progressive_lookup, base_tech_table, all_product_sources, required_technologies, get_rocket_requirements, get_science_pack_pools, Recipe, recipes, technology_table, tech_table, factorio_base_id, useless_technologies, progressive_technology_table, fluids, valid_ingredients
"""

factorio_base_id = 2 ** 17


class Capability(IntFlag):
    """
    Represents global milestones in the player's abilities
    """
    generate_power               = 1<< 0 # boiler + steam engine
    generate_power_in_space      = 1<< 1 # solar panel
    generate_power_in_dark_space = 1<< 2 # nuclear or fusion
    automate_mining              = 1<< 3 # burner mining drill
    mine_with_fluid              = 1<< 4 # uranium mining technology + electric mining drills
    mine_hard_solids             = 1<< 5 # big mining drill
    pump_tiles                   = 1<< 6 # offshore pump
    pump_entities                = 1<< 7 # pumpjack
    automate_planting            = 1<< 8 # agricultural tower
    harness_lightning            = 1<< 9 # lightning rod
    heat_buildings               = 1<<10 # heating tower or nuclear reactor
    build_on_ocean_planet        = 1<<11 # ice platform + concrete
    collect_asteroids            = 1<<12 # asteroid collector
    travel_space                 = 1<<13 # thruster
    destroy_medium_asteroids     = 1<<14 # gun turret
    destroy_big_asteroids        = 1<<15 # rocket turret
    destroy_huge_asteroids       = 1<<16 # railgun turret

    destroy_big_and_smaller_asteroids = destroy_big_asteroids | destroy_medium_asteroids
    destroy_huge_and_smaller_asteroids = destroy_huge_asteroids | destroy_big_and_smaller_asteroids

class PowerType(IntFlag):
    """
    Effectively 0-count ingredients for every recipe/operation a machine performs.
    Except for the fusion reactor which consumes both electricty and fusion fuel,
    buildings almost always require exactly 1 power type.
    """
    electricity = 1<<0 # produced by solar panel, required by assembling machine.
    heat        = 1<<1 # produced by heating tower, required by heat exchanger.
    chemical    = 1<<2 # satisfied by foraged coal, required by boiler.
    nutrients   = 1<<3 # satisfied by nutrients, required by biochamber.
    food        = 1<<4 # satisfied by bioflux, required by captive biter spawner.
    nuclear     = 1<<5 # satisfied by uranium fuel cell, required by nuclear reactor
    fusion      = 1<<6 # satisfied by fusion power cell, required by fusion reactor
    free        = 0 # offshore pump requires no power.

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
class Technology:
    name: str
    """ e.g. 'lightning-collector', 'refined-flammables-1' """
    ingredients: Dict[str, int]
    """ the keys are the science pack names for 1 unit of research. the values are always 1. """
    units: int | None
    """ how many units of research, e.g. 'automation' costs 10. None means this is an infinite research with a cost formula. """
    energy: int
    """ lab time for 1 unit of research in seconds. """
    prerequisites: Set[str]
    """ technology names required immediately prior to this one (not recursive). """
    unlock_recipes: Set[str]
    unlock_space_locations: Set[str]
    unlock_mining_with_fluid: bool


class CustomTechnology(Technology):
    """A particularly configured Technology for a world."""
    ingredients: Set[str]

    def __init__(self, origin: Technology, world, allowed_packs: Set[str], player: int):
        ingredients = allowed_packs
        self.player = player
        if origin.name not in world.special_nodes:
            ingredients = set(world.random.sample(list(ingredients), world.random.randint(1, len(ingredients))))
        self.ingredients = ingredients
        super(CustomTechnology, self).__init__(origin.name, origin.factorio_id)

    def get_prior_technologies(self) -> Set[Technology]:
        """Get Technologies that have to precede this one to resolve tree connections."""
        technologies = set()
        for ingredient in self.ingredients:
            technologies |= required_technologies[ingredient]  # technologies that unlock the recipes
        return technologies


@dataclass
class Recipe:
    name: str
    """ e.g. 'electronic-circuit', 'simple-coal-liquefaction' """
    inputs: Dict[str, int]
    """
    e.g. {'copper-cable': 3, 'iron-place': 1}, {'raw-fish': 0, 'nutrients': 100, 'water': 100}
    an amount of 0 means the input is somehow "preserved" in the process.
    """
    outputs: Dict[str, int]
    """
    e.g. {'electronic-circuit': 1}, {'empty-barrel': 0, 'water': 0}
    an amount of 0 means this is a lossless conversion.
    """
    energy: float
    """ the crafting time in seconds """
    classification: RecipeClassification
    """ useful for guiding traversal of the cyclic directed graph of what items yield what other items. """
    machines: Set[str]
    """ this recipe can be performed in any of these machines, possibly including 'character' for hand crafting. """
    locations: Set[str] | None
    """ this recipe must be performed in one of these locations. None means anywhere. """
    is_unusual_recipe: bool
    """ true for barreling/unbarreling, rocket part, and biter egg. these should be excluded from free samples. """

@dataclass
class Machine:
    name: str
    """ e.g. 'assembling-machine-1', 'captive-biter-spawner', 'steam-turbine', 'character' """
    power_type: PowerType
    locations: Set[str] | None
    """ this machine can only operate in one of these locations. None means anywhere. the charcater cannot hand craft in space. """
    can_freeze: bool
    """ requires heating in locations with the Capability.heat_buildings threat. """

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
    drop_to: str | None
    """ if this is orbit above a planet, which planet? """
    launch_to: str | None
    """ if this is a planet, what's the location name of the orbit above? """
    thrust_to: List[str]
    """ where would thrusters be able to fly us from here? """
    threats: Capability
    """ what size asteroids do we encounter here, and do buildings freeze? """

    mineable_resources: Set[MineableResource]
    forageable_resources: Set[ForageableResource]

    def __init__(self, name: str, surface_properties: SurfaceProperties):
        self.name = name
        self.surface_properties = surface_properties
        self.drop_to = None
        self.launch_to = None
        self.thrust_to = []
        self.threats = Capability(0)
        self.mineable_resources = set()
        self.forageable_resources = set()

ORBIT_SUFFIX = "_orbit"

@dataclass(frozen=True, order=True)
class MineableResource:
    """
    A resource the player can collect in automated abundance provided they have the right equipment and technology.
    E.g. stone on Nauvis (requires mining drills), sulfuric acid on vulcanus (requires pumpjacks),
    yumako on gleba (requires agricultural towers), carbonic asteroid chunk in space (required asteroid collector).
    """
    name: str
    """ item or fluid name """
    required_capabilities: Capability
    """ e.g. Capability.automate_mining|mine_with_fluid """
    required_ingredients: Tuple[str]
    """ e.g. 'sulfuric-acid' """
    def __init__(self, name: str, required_capabilities=0, required_ingredients=None):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "required_capabilities", Capability(required_capabilities))
        object.__setattr__(self, "required_ingredients", tuple(sorted(required_ingredients or ())))

@dataclass(frozen=True, order=True)
class ForageableResource:
    """
    A resource the player can collect manually in small quantities. Never requires special equipment.
    Does not logically satisfy automation ingredients, but can be used for trigger techs,
    automation machine ingredients, and bootstrapping circular recipes like pentapod egg breeding.
    e.g. fish on Nauvis, iron stick on fulgora, yumako on gleba (even without agricultural towers).
    """
    name: str
    """ item or fluid name """

# Exported data
machines: Dict[str, Machine] = {}
recipes: Dict[str, Recipe] = {}
technologies: Dict[str, Technology] = {}
progressive_technology_chains: Dict[str, Dict[int, str]] = defaultdict(dict)
""" e.g. {'advanced-material-processing': {1:'advanced-material-processing', 2:'advanced-material-processing-2'}} """
empty_technologies: Set[str] = set()
fluids: Set[str] = set()

# TODO: redo these:
machine_per_category: Dict[str: str] = {} # One machine for each category. TODO: determinism.
required_technologies: Dict[str, FrozenSet[Technology]] = {}
base_tech_table = {}
progressive_technology_table: Dict[str, Technology] = {}
tech_to_progressive_lookup: Dict[str, str] = {}
useless_technologies: Set[str] = {}
valid_ingredients: Set[str] = {}
all_product_sources: Dict[str, Set[Recipe]] = {}
free_sample_exclusions: Set[str] = set()
tech_table: Dict[str, int] = {}
technology_table: Dict[str, Technology] = {}

# Hardcoded constants that we don't have a good way to derrive from the data:

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

# Nauvis is missing its surface properties for some reason.
_default_gravity = 10
_default_magnetic_field = 90
_default_pressure =  1000

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

_assteroid_collecting_entities = {
    RawEntity.asteroid_collector,
}
_automated_planting_entities = {
    RawEntity.agricultural_tower,
}
_tile_mining_machines = {
    RawEntity.offshore_pump,
}

_electricity_conducting_machines = {
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

def _get_asteroid_info(spawn_data):
    if spawn_data["type"] == "asteroid-chunk":
        # Just a free floating chunk.
        return Capability(0), spawn_data["asteroid"]
    if spawn_data["type"] == "entity":
        # Need to break it open.
        return _asteroid_info_table[spawn_data["asteroid"]]
    assert False, "what's this asteroid data: " + repr(spawn_data)

def _get_machine_power_type(entity) -> PowerType:
    result = PowerType.free
    if "burner_prototype" in entity:
        [fuel_category] = entity["burner_prototype"]["fuel_categories"].keys()
        result |= {
            "chemical":  PowerType.chemical,
            "nutrients": PowerType.nutrients,
            "food":      PowerType.food,
            "nuclear":   PowerType.nuclear,
            "fusion":    PowerType.fusion,
        }[fuel_category]
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

    natural_entity_to_locations: Dict[str, Set[str]] = defaultdict(set)
    space_locations: Dict[str, SpaceLocation] = {}
    for location_name, space_location_data in get_data()["space_location"].items():
        if "surface_properties" in space_location_data:
            # There is a surface here.
            props = space_location_data["surface_properties"]
            surface_properties = SurfaceProperties(
                gravity=props.get("gravity", _default_gravity),
                magnetic_field=props.get("magnetic-field", _default_magnetic_field),
                pressure=props.get("pressure", _default_pressure),
            )

            # This is a pair of locations.
            surface_location = SpaceLocation(location_name, surface_properties)
            space_location = SpaceLocation(location_name + ORBIT_SUFFIX, SPACE_SURFACE)
            space_locations[surface_location.name] = surface_location
            space_locations[space_location.name] = space_location
            surface_location.launch_to = space_location.name
            space_location.drop_to = surface_location.name

            # Surface features.
            if space_location_data.get("entities_require_heating", False):
                surface_location.threats |= Capability.heat_buildings
            if location_name in _surfaces_with_lightning:
                surface_location.threats |= Capability.harness_lightning
            for entity_name in (
                space_location_data["map_gen_settings"]["autoplace_settings"]["entity"]["settings"].keys() |
                _additional_autoplace_entities.get(location_name, set())
            ):
                natural_entity_to_locations[entity_name].add(surface_location.name)
            for tile_name in (
                space_location_data["map_gen_settings"]["autoplace_settings"]["tile"]["settings"].keys() |
                _additional_autoplace_tiles.get(location_name, set())
            ):
                natural_tile_to_locations[tile_name].add(surface_location.name)
        else:
            # There is no surface here. e.g. solar-system-edge.
            space_location = SpaceLocation(location_name, SPACE_SURFACE)
            space_locations[space_location.name] = space_location
        # Asteroid info.
        for spawn_data in space_location_data.get("asteroid_spawn_definitions", []):
            threats, item = _get_asteroid_info(spawn_data)
            space_location.threats |= threats
            # Add a natural resource for this now, because we already know everything.
            space_location.mineable_resources.add(MineableResource(item, threats | Capability.collect_asteroids))

    for location_name, space_connection_data in get_data()["space_connection"].items():
        connection_names = [
            space_connection_data["from"]["name"],
            space_connection_data["to"]["name"],
        ]
        # We actually connect to the orbit above the planets, not directly to the surface.
        for i, name in enumerate(connection_names):
            if name + ORBIT_SUFFIX in space_locations.keys():
                connection_names[i] = name + ORBIT_SUFFIX
        space_location = SpaceLocation(location_name, SPACE_SURFACE)
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
            space_location.mineable_resources.add(MineableResource(item, threats | Capability.collect_asteroids))

    # =================
    # Natural Resources
    # =================
    # Find mineable and forageable resources.
    for entity_name, entity in get_data()["entity"].items():
        if "autoplace_specification" not in entity: continue # We're looking for natural features.
        mineable_resources = set()
        forageable_resources = set()
        if entity["mineable_properties"]["minable"]:
            products = [p["name"] for p in entity["mineable_properties"]["products"]]
            required_capabilities = Capability(0)
            required_ingredients = []
            if "resource_category" in entity:
                # Mineable
                required_capabilities |= _resource_category_to_capbility[entity["resource_category"]]
                if "required_fluid" in entity["mineable_properties"]:
                    required_ingredients.append(entity["mineable_properties"]["required_fluid"])
                    required_capabilities |= Capability.mine_with_fluid
                for product in products:
                    mineable_resources.add(MineableResource(product, required_capabilities, required_ingredients))
            else:
                # Foragable
                for product in products:
                    forageable_resources.add(ForageableResource(product))
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
                            mineable_resources.add(MineableResource(product, Capability.automate_planting, [ingredient]))
        elif "loot" in entity:
            # Pentapod eggs from gleba spawners (aka egg rafts) use .loot instead of .mineable_properties.
            products = [p["item"] for p in entity["loot"]]
            for product in products:
                forageable_resources.add(ForageableResource(product))
        else: continue

        # Where does this resource appear in the uninverse?
        homes = natural_entity_to_locations.get(entity_name, None)
        if homes != None:
            for space_location in homes:
                space_location.mineable_resources.update(mineable_resources)
                space_location.forageable_resources.update(forageable_resources)
        else:
            print("WARNING: missing home for natural resource entity: " + entity_name)
    # Offshore pump yields fluids sourced from tiles.
    for tile_name, tile_data in get_data()["tile"].items():
        if "fluid" not in tile_data: continue
        mineable_resource = MineableResource(tile_data["fluid"]["name"], Capability.pump_tiles)
        homes = natural_tile_to_locations.get(tile_name, None)
        if homes != None:
            for space_location in homes:
                space_location.mineable_resources.update(mineable_resources)
        else:
            print("WARNING: missing home for natural resource tile: " + tile_name)

    # ========
    # Machines
    # ========

    crafting_category_to_machines = defaultdict(set)
    resource_category_to_machines = defaultdict(set)
    tile_mining_machines = set()
    electricity_producing_machines = set()
    electricity_conducting_machines = set()
    heat_producing_machines = set()
    heat_conducting_machines = set()
    machine_to_power_type: Dict[str, PowerType] = {}
    for entity_name, entity in get_data()["entity"].items():
        is_machine = False
        # What powers this machine?
        power_type = _get_machine_power_type(entity)
        # Crafting buildings and the character:
        for category in entity.get("crafting_categories", ()):
            crafting_category_to_machines[category].add(entity_name)
            is_machine = True
        # Mining buildings and the character:
        for category in entity.get("resource_categories", ()):
            resource_category_to_machines[category].add(entity_name)
            is_machine = True
        # Offshore pump:
        if entity_name in _tile_mining_machines:
            tile_mining_machines.add(entity_name)
            is_machine = True
        # Electricity producers:
        if "electric_energy_source_prototype" in entity and entity["electric_energy_source_prototype"]["usage_priority"] in _power_producing_usage_priorities:
            electricity_producing_machines.add(entity_name)
            is_machine = True
        # Electricity conductors:
        if entity_name in _electricity_conducting_machines:
            electricity_conducting_machines.add(entity_name)
            is_machine = True
        # Heat producers, consumers, and conductors:
        if "heat_buffer_prototype" in entity:
            mode = _entity_heat_buffer_mode[entity_name]
            if mode == HeatBufferMode.produce:
                heat_producing_machines.add(entity_name)
                is_machine = True
            elif mode == HeatBufferMode.consume:
                power_type |= PowerType.heat
                is_machine = True
            elif mode == HeatBufferMode.conduct:
                heat_conducting_machines.add(entity_name)
                is_machine = True
            elif mode == HeatBufferMode.editor_only:
                pass # ignore
            else: assert False
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
        if is_machine:
            machines[entity_name] = Machine(entity_name, power_type, locations, can_freeze)

    # =======
    # Recipes
    # =======

    starting_recipes: Set[str] = set()
    for recipe_name, recipe_data in get_data()["recipe"].items():
        if recipe_data["enabled"]:
            starting_recipes.add(recipe_name)
        energy = recipe_data["energy"] # crafting time in seconds.
        allows_productivity = recipe_data["allowed_effects"]["productivity"]
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

    import pdb; pdb.set_trace()

    # ============
    # Technologies
    # ============
    recipe_to_technologies: Dict[str, Set[Technology]] = defaultdict(set)
    for technology_name, technology in get_data()["technology"].items():
        ingredients = {i["name"]: i["amount"] for i in technology["research_unit_ingredients"] }
        assert set(ingredients.values()) == {1}, "update comment on Technology.ingredients to no longer claim the amount is always 1"
        if "research_unit_count_formula" in technology:
            units = None # infinite
        else:
            units = technology["research_unit_count"]
        energy_in_ticks = technology["research_unit_energy"]
        assert energy_in_ticks % 60 == 0, "update Technology.energy type from int to float"
        energy = energy_in_ticks // 60
        prerequisites = set(technology["prerequisites"].keys())

        unlock_recipes = set()
        unlock_space_locations = set()
        unlock_mining_with_fluid = False
        does_anything = False
        for effect in technology["effects"]:
            if effect["type"] == "unlock-recipe":
                unlock_recipes.add(effect["recipe"])
            elif effect["type"] == "unlock-space-location":
                unlock_space_locations.add(effect["space_location"])
            elif effect["type"] == "mining-with-fluid":
                unlock_mining_with_fluid = True
            else:
                pass # It does something else not relevant to logic.
            does_anything = True
        if not does_anything:
            empty_technologies.add(technology_name)

        technologies[technology_name] = Technology(technology_name,
            ingredients, units, energy, prerequisites, 
            unlock_recipes, unlock_space_locations, unlock_mining_with_fluid,
        )

        # Technology with levels is usually something we want to make progressive.
        level = technology["level"]
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
        if units == None:
            assert technology["max_level"] == 4294967295, "consider evaluating the cost at each finite level instead of using an 'infinite' formula"
            assert len(unlock_recipes) + len(unlock_space_locations) + unlock_mining_with_fluid == 0, "infinite research is doing something important: " + technology_name
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
            assert technologies[progressive_chain[1]].units == None, "technology ends with -1 without any other levels: " + progressive_chain[1]
        assert not any(progressive_chain[level].units != None for level in range(1, len(progressive_chain)+1-1)), "infinite technology must be the highest level defined in the group: " + progressive_group_name

init()

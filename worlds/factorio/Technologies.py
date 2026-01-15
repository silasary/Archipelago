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

tech_table: Dict[str, int] = {}
technology_table: Dict[str, Technology] = {}


class FactorioElement:
    name: str

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __hash__(self):
        return hash(self.name)


# TODO: These should probably be "event" location/items in AP.
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

class Technology(FactorioElement):  # maybe make subclass of Location?
    factorio_id: int
    progressive: Tuple[str]
    unlocks: Union[Set[str], bool]  # bool case is for progressive technologies
    modifiers: list[str]

    def __init__(self, technology_name: str, factorio_id: int, progressive: Tuple[str] = (),
                 modifiers: list[str] = None, unlocks: Union[Set[str], bool] = None):
        self.name = technology_name
        self.factorio_id = factorio_id
        self.progressive = progressive
        if modifiers is None:
            modifiers = []
        self.modifiers =  modifiers
        if unlocks:
            self.unlocks = unlocks
        else:
            self.unlocks = set()

    def __hash__(self):
        return self.factorio_id

    @property
    def has_modifier(self) -> bool:
        return bool(self.modifiers)

    def get_custom(self, world, allowed_packs: Set[str], player: int) -> CustomTechnology:
        return CustomTechnology(self, world, allowed_packs, player)

    def useful(self) -> bool:
        return self.has_modifier or self.unlocks


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


class Recipe(FactorioElement):
    name: str
    category: str
    """ determines the required machine. e.g. 'metallurgy' for casting pipe from molten iron """
    ingredients: Dict[str, int]
    products: Dict[str, int]
    energy: float

    def __init__(self, name: str, category: str, ingredients: Dict[str, int], products: Dict[str, int], energy: float):
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.products = products
        self.energy = energy

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    @property
    def crafting_machine(self) -> str:
        """cheapest crafting machine name able to run this recipe"""
        return machine_per_category[self.category]

    @property
    def unlocking_technologies(self) -> Set[Technology]:
        """Unlocked by any of the returned technologies. Empty set indicates a starting recipe."""
        return {technology_table[tech_name] for tech_name in recipe_sources.get(self.name, ())}

    @property
    def recursive_unlocking_technologies(self) -> Set[Technology]:
        base = {technology_table[tech_name] for tech_name in recipe_sources.get(self.name, ())}
        for ingredient in self.ingredients:
            base |= required_technologies[ingredient]
        base |= required_technologies[self.crafting_machine]
        return base

    @property
    def rel_cost(self) -> float:
        ingredients = sum(self.ingredients.values())
        return min(ingredients / amount for product, amount in self.products.items())

    @functools.cached_property
    def base_cost(self) -> Dict[str, int]:
        ingredients = Counter()
        try:
            for ingredient, cost in self.ingredients.items():
                if ingredient in all_product_sources:
                    for recipe in all_product_sources[ingredient]:
                        if recipe.ingredients:
                            ingredients.update({name: amount * cost / recipe.products[ingredient] for name, amount in
                                                recipe.base_cost.items()})
                        else:
                            ingredients[ingredient] += recipe.energy * cost / recipe.products[ingredient]
                else:
                    ingredients[ingredient] += cost
        except RecursionError as e:
            raise Exception(f"Infinite recursion in ingredients of {self}.") from e
        return ingredients

    @property
    def total_energy(self) -> float:
        """Total required energy (crafting time) for single craft"""
        # TODO: multiply mining energy by 2 since drill has 0.5 speed
        total_energy = self.energy
        for ingredient, cost in self.ingredients.items():
            if ingredient in all_product_sources:
                selected_recipe_energy = float('inf')
                for ingredient_recipe in all_product_sources[ingredient]:
                    craft_count = max((n for name, n in ingredient_recipe.products.items() if name == ingredient))
                    recipe_energy = ingredient_recipe.total_energy / craft_count * cost
                    if recipe_energy < selected_recipe_energy:
                        selected_recipe_energy = recipe_energy
                total_energy += selected_recipe_energy
        return total_energy

#TODO: delete the above definition of class Recipe
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

class Machine(FactorioElement):
    def __init__(self, name, categories):
        self.name: str = name
        self.categories: set = categories

# TODO: delete the above definition of class Machine.
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

    natural_entities: Set[str]
    """ e.g. iron-ore, sulfuric-acid-geyser, ashland-lichen-tree-flaming """
    natural_tiles: Set[str]
    """ relevant for offshore pumps and agriculture """
    mineable_resources: Set[MineableResource]
    forageable_resources: Set[ForageableResource]

    def __init__(self, name: str, surface_properties: SurfaceProperties):
        self.name = name
        self.surface_properties = surface_properties
        self.drop_to = None
        self.launch_to = None
        self.thrust_to = []
        self.threats = Capability(0)
        self.natural_entities = set()
        self.natural_tiles = set()
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
machine_per_category: Dict[str: str] = {} # One machine for each category. TODO: determinism.
required_technologies: Dict[str, FrozenSet[Technology]] = {}
free_sample_exclusions: Set[str] = set()
base_tech_table = {}
progressive_technology_table: Dict[str, Technology] = {}
tech_to_progressive_lookup: Dict[str, str] = {}
useless_technologies: Set[str] = {}
fluids: Set[str] = {}
valid_ingredients: Set[str] = {}
all_product_sources: Dict[str, Set[Recipe]] = {}

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
            surface_location.natural_entities.update(space_location_data["map_gen_settings"]["autoplace_settings"]["entity"]["settings"].keys())
            surface_location.natural_entities.update(_additional_autoplace_entities.get(location_name, ()))
            surface_location.natural_tiles.update(space_location_data["map_gen_settings"]["autoplace_settings"]["tile"]["settings"].keys())
            surface_location.natural_tiles.update(_additional_autoplace_tiles.get(location_name, ()))
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
        found_a_home = False
        for space_location in space_locations.values():
            if entity_name in space_location.natural_entities:
                space_location.mineable_resources.update(mineable_resources)
                space_location.forageable_resources.update(forageable_resources)
                found_a_home = True
        if not found_a_home:
            print("WARNING: missing home for natural resource entity: " + entity_name)
    # Offshore pump yields fluids sourced from tiles.
    for tile_name, tile_data in get_data()["tile"].items():
        if "fluid" not in tile_data: continue
        mineable_resource = MineableResource(tile_data["fluid"]["name"], Capability.pump_tiles)
        found_a_home = False
        for space_location in space_locations.values():
            if tile_name in space_location.natural_tiles:
                space_location.mineable_resources.add(mineable_resource)
                found_a_home = True
        if not found_a_home:
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
        recipes[recipe_name] = Recipe(recipe_name, inputs, outputs, energy, classification, valid_machines, locations)

    import pdb; pdb.set_trace()


    # ============
    # Technologies
    # ============

    raw_recipes = get_data()["recipe"]
    assert all(recipe_name in raw_recipes for recipe_name in _start_unlocked_recipes), "Unknown Recipe defined."

    # recipes and technologies can share names in Factorio
    recipe_sources: Dict[str, Set[str]] = {}  # recipe_name -> technology source
    mining_with_fluid_sources: set[str] = set()
    for technology_name, data in sorted(get_data()["technology"].items()):
        modifiers = []
        unlocks = []
        for effect in data.get("effects", {}) or []:
            if "modifier" in effect:
                modifiers.append(effect["type"])
            if effect["type"] == "unlock-recipe":
                unlocks.append(effect["recipe"])
        technology = Technology(
            technology_name,
            factorio_tech_id,
            modifiers=modifiers,
            # By depriving some base game technologies of purpose (e.g. electronics, usually unlocked by crafting 10 copper plates),
            # the technologies become "useless" (like flammables), and the mod will unlock them at the start.
            # It is critical to unlock these "useless" technologies so that the foundational items are craftable.
            unlocks=set(unlocks) - _start_unlocked_recipes,
        )
        factorio_tech_id += 1
        tech_table[technology_name] = technology.factorio_id
        technology_table[technology_name] = technology
        for recipe_name in technology.unlocks:
            recipe_sources.setdefault(recipe_name, set()).add(technology_name)
        if "mining-with-fluid" in technology.modifiers:
            mining_with_fluid_sources.add(technology_name)


    # =======
    # Recipes
    # =======


    import pdb; pdb.set_trace()
    for recipe_name, recipe_data in raw_recipes.items():
        # example:
        # [{"type":"item", "name":"iron-plate", "amount":1}, {"type":"item", "name":"copper-cable", "amount":3}]
        # => {"iron-plate":1, "copper-cable":3}
        ingredients = {x["name"]: x["count"] for x in recipe_data["ingredients"]}
        products = {x["name"]: x["count"] for x in recipe_data["products"]}
        energy = recipe_data["energy"]

        recipes[recipe_name] = Recipe(recipe_name, recipe_data["category"], ingredients, products, energy)

    # add uranium mining to logic graph. TODO: are we sure a Recipe is the right tool for the job here?
    #for resource_name, mineable_resource in mineable_resources.items():
    #    # TODO
    #    recipes[f"_mining-{resource_name}"] = Recipe(...)
    #    if "required_fluid" in resource_data:
    #        recipe_sources.setdefault(f"mining-{resource_name}", set()).update(mining_with_fluid_sources)

    for recipe_name, recipe in recipes.items():
        # kovarex, asteroid crushing, fish breeding, etc.
        # TODO: we actually do need a source of pentapod eggs for swamp science, but it's overlooked here for being circular.
        is_circular = not recipe.products.keys().isdisjoint(recipe.ingredients.keys())
        # pumpjack-recycling, empty-water-barrel, etc.
        # TODO: we actually do need to craft backwards on fulgora.
        is_backwards = not recipe_data["unlock_results"]
        # nuclear-fuel-reprocessing
        is_indirect_recycling = recipe_name in _indirect_recycling_recipes
        if is_circular or is_backwards or is_indirect_recycling: continue

        for product_name in recipe.products.keys():
            all_product_sources.setdefault(product_name, set()).add(recipe)

    # build requirements graph for all technology ingredients

    # TODO: reduce the number of passes over the entity data list.
    all_science_pack_names = set(itertools.chain(*(
        entity_data["lab_inputs"] for entity_data in get_data()["entity"].values()
        if "lab_inputs" in entity_data
    )))
    all_science_pack_names: Set[str] = set(Options.MaxSciencePack.get_ordered_science_packs())


    def unlock_just_tech(recipe: Recipe, _done) -> Set[Technology]:
        current_technologies = recipe.unlocking_technologies
        for ingredient_name in recipe.ingredients:
            current_technologies |= recursively_get_unlocking_technologies(ingredient_name, _done,
                                                                           unlock_func=unlock_just_tech)
        return current_technologies


    def unlock(recipe: Recipe, _done) -> Set[Technology]:
        current_technologies = recipe.unlocking_technologies
        for ingredient_name in recipe.ingredients:
            current_technologies |= recursively_get_unlocking_technologies(ingredient_name, _done, unlock_func=unlock)
        current_technologies |= required_category_technologies[recipe.category]

        return current_technologies


    def recursively_get_unlocking_technologies(ingredient_name, _done=None, unlock_func=unlock_just_tech) -> Set[Technology]:
        if _done:
            if ingredient_name in _done:
                return set()
            else:
                _done.add(ingredient_name)
        else:
            _done = {ingredient_name}
        recipes = all_product_sources.get(ingredient_name)
        if not recipes:
            return set()
        current_technologies = set()
        for recipe in recipes:
            current_technologies |= unlock_func(recipe, _done)

        return current_technologies


    required_machine_technologies: Dict[str, FrozenSet[Technology]] = {}
    for ingredient_name in machines:
        required_machine_technologies[ingredient_name] = frozenset(recursively_get_unlocking_technologies(ingredient_name))

    machine_tech_cost = {}
    for machine in machines.values():
        for category in machine.categories:
            current_cost, current_machine = machine_tech_cost.get(category, (10000, "character"))
            machine_cost = len(required_machine_technologies[machine.name])
            if machine_cost < current_cost:
                machine_tech_cost[category] = machine_cost, machine.name

    for category, (cost, machine_name) in machine_tech_cost.items():
        machine_per_category[category] = machine_name

    # required technologies to be able to craft recipes from a certain category
    required_category_technologies: Dict[str, FrozenSet[FrozenSet[Technology]]] = {}
    for category_name, machine_name in machine_per_category.items():
        techs = set()
        techs |= recursively_get_unlocking_technologies(machine_name)
        required_category_technologies[category_name] = frozenset(techs)

    global required_technologies
    required_technologies = Utils.KeyedDefaultDict(lambda ingredient_name: frozenset(
        recursively_get_unlocking_technologies(ingredient_name, unlock_func=unlock)))


    global get_rocket_requirements # TODO: super weird to declare a global function this way.
    def get_rocket_requirements(silo_recipe: Optional[Recipe], part_recipe: Optional[Recipe],
                                satellite_recipe: Optional[Recipe], cargo_landing_pad_recipe: Optional[Recipe]) -> Set[str]:
        techs = set()
        if silo_recipe:
            for ingredient in silo_recipe.ingredients:
                techs |= recursively_get_unlocking_technologies(ingredient)
        if part_recipe:
            for ingredient in part_recipe.ingredients:
                techs |= recursively_get_unlocking_technologies(ingredient)
        if cargo_landing_pad_recipe:
            for ingredient in cargo_landing_pad_recipe.ingredients:
                techs |= recursively_get_unlocking_technologies(ingredient)
        if satellite_recipe:
            techs |= satellite_recipe.unlocking_technologies
            for ingredient in satellite_recipe.ingredients:
                techs |= recursively_get_unlocking_technologies(ingredient)
        return {tech.name for tech in techs}


    global free_sample_exclusions
    free_sample_exclusions = all_science_pack_names | {"rocket-part"}

    # progressive technologies
    # auto-progressive
    progressive_rows: Dict[str, Union[List[str], Tuple[str, ...]]] = {}
    progressive_incs = set()
    for tech_name in tech_table:
        if tech_name.endswith("-1"):
            progressive_rows[tech_name] = []
        elif tech_name[-2] == "-" and tech_name[-1] in string.digits:
            progressive_incs.add(tech_name)

    for root, progressive in progressive_rows.items():
        seeking = root[:-1] + str(int(root[-1]) + 1)
        while seeking in progressive_incs:
            progressive.append(seeking)
            progressive_incs.remove(seeking)
            seeking = seeking[:-1] + str(int(seeking[-1]) + 1)

    # make root entry the progressive name
    for old_name in set(progressive_rows):
        prog_name = "progressive-" + old_name.rsplit("-", 1)[0]
        progressive_rows[prog_name] = tuple([old_name] + progressive_rows[old_name])
        del (progressive_rows[old_name])

    # no -1 start
    base_starts = set()
    for remnant in progressive_incs:
        if remnant[-1] == "2":
            base_starts.add(remnant[:-2])

    for root in base_starts:
        seeking = root + "-2"
        progressive = [root]
        while seeking in progressive_incs:
            progressive.append(seeking)
            seeking = seeking[:-1] + str(int(seeking[-1]) + 1)
        progressive_rows["progressive-" + root] = tuple(progressive)

    # science packs
    progressive_rows["progressive-science-pack"] = tuple(Options.MaxSciencePack.get_ordered_science_packs())[1:]

    # manual progressive
    progressive_rows["progressive-processing"] = (
        "steel-processing",
        "oil-processing", "sulfur-processing", "advanced-oil-processing", "coal-liquefaction",
        "uranium-processing", "kovarex-enrichment-process", "nuclear-fuel-reprocessing")
    progressive_rows["progressive-rocketry"] = ("rocketry", "explosive-rocketry", "atomic-bomb")
    progressive_rows["progressive-vehicle"] = ("automobilism", "tank", "spidertron")
    progressive_rows["progressive-fluid-handling"] = ("fluid-handling", "fluid-wagon")
    progressive_rows["progressive-train-network"] = ("railway", "automated-rail-transportation")
    progressive_rows["progressive-engine"] = ("engine", "electric-engine")
    progressive_rows["progressive-armor"] = ("heavy-armor", "modular-armor", "power-armor", "power-armor-mk2")
    progressive_rows["progressive-personal-battery"] = ("battery-equipment", "battery-mk2-equipment")
    progressive_rows["progressive-energy-shield"] = ("energy-shield-equipment", "energy-shield-mk2-equipment")
    progressive_rows["progressive-wall"] = ("stone-wall", "gate")
    progressive_rows["progressive-follower"] = ("defender", "distractor", "destroyer")
    progressive_rows["progressive-inserter"] = ("fast-inserter", "bulk-inserter")
    progressive_rows["progressive-turret"] = ("gun-turret", "laser-turret")
    progressive_rows["progressive-flamethrower"] = ("flamethrower",)  # leaving out flammables, as they do nothing
    progressive_rows["progressive-personal-roboport-equipment"] = ("personal-roboport-equipment",
                                                                   "personal-roboport-mk2-equipment")

    sorted_rows = sorted(progressive_rows)

    # integrate into
    source_target_mapping: Dict[str, str] = {
        "progressive-braking-force": "progressive-train-network",
        "progressive-inserter-capacity-bonus": "progressive-inserter",
        "progressive-refined-flammables": "progressive-flamethrower",
    }

    for source, target in source_target_mapping.items():
        progressive_rows[target] += progressive_rows[source]

    global base_tech_table
    base_tech_table = tech_table.copy()  # without progressive techs

    progressive_tech_table: Dict[str, int] = {}
    global progressive_technology_table
    progressive_technology_table = {}

    for root in sorted_rows:
        progressive = progressive_rows[root]
        assert all(tech in tech_table for tech in progressive), \
            (f"Declared a progressive technology ({root}) without base technology. "
             f"Missing: f{tuple(tech for tech in progressive if tech not in tech_table)}")
        factorio_tech_id += 1
        progressive_technology = Technology(root, factorio_tech_id,
                                            tuple(progressive),
                                            modifiers=sorted(set.union(
                                                *(set(technology_table[tech].modifiers) for tech in progressive)
                                            )),
                                            unlocks=any(technology_table[tech].unlocks for tech in progressive),)
        progressive_tech_table[root] = progressive_technology.factorio_id
        progressive_technology_table[root] = progressive_technology

    global tech_to_progressive_lookup
    tech_to_progressive_lookup = {}
    for technology in progressive_technology_table.values():
        if technology.name not in source_target_mapping:
            for progressive in technology.progressive:
                tech_to_progressive_lookup[progressive] = technology.name

    tech_table.update(progressive_tech_table)
    technology_table.update(progressive_technology_table)

    # techs that are never progressive
    common_tech_table: Dict[str, int] = {tech_name: tech_id for tech_name, tech_id in base_tech_table.items()
                                         if tech_name not in progressive_tech_table}

    global useless_technologies
    useless_technologies = {
        tech_name for tech_name in common_tech_table
        if not technology_table[tech_name].useful()
    }

    rel_cost = {
        # TODO: use ForageableResource and MineableResource instead of this hardcoded list.
        "wood": 10000,
        "iron-ore": 1,
        "copper-ore": 1,
        "stone": 1,
        "crude-oil": 0.5,
        "water": 0.001,
        "coal": 1,
        "raw-fish": 1000,
        "steam": 0.01,
        "used-up-uranium-fuel-cell": 1000 # TODO: should this be "depleted-uranium-fuel-cell"?
    }

    exclusion_list: Set[str] = all_science_pack_names | {"rocket-part", "used-up-uranium-fuel-cell"}


    global get_science_pack_pools # TODO: jank
    @Utils.cache_argsless
    def get_science_pack_pools() -> Dict[str, Set[str]]:
        def get_estimated_difficulty(recipe: Recipe):
            base_ingredients = recipe.base_cost
            cost = 0

            for ingredient_name, amount in base_ingredients.items():
                cost += rel_cost.get(ingredient_name, 1) * amount
            return cost

        science_pack_pools: Dict[str, Set[str]] = {}
        already_taken = exclusion_list.copy()
        current_difficulty = 5
        for science_pack in Options.MaxSciencePack.get_ordered_science_packs():
            current = science_pack_pools[science_pack] = set()
            for name, recipe in recipes.items():
                if (science_pack != "automation-science-pack" or not recipe.recursive_unlocking_technologies) \
                        and get_estimated_difficulty(recipe) < current_difficulty:
                    current |= set(recipe.products)

            if science_pack == "automation-science-pack":
                # Can't handcraft automation science if fluids end up in its recipe, making the seed impossible.
                current -= fluids
            elif science_pack == "logistic-science-pack":
                current |= {"steam"}

            current -= already_taken
            already_taken |= current
            current_difficulty *= 2

        return science_pack_pools


    item_stack_sizes: Dict[str, int] = items_future.result()
    non_stacking_items: Set[str] = {item for item, stack in item_stack_sizes.items() if stack == 1}
    stacking_items: Set[str] = set(item_stack_sizes) - non_stacking_items
    global valid_ingredients
    valid_ingredients = stacking_items | fluids

init()

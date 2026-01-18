import itertools
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum, IntFlag

from .data import (
    get_data,
    Entity as RawEntity,
    Item as RawItem,
    Tile as RawTile,
    Recipe as RawRecipe,
    SpaceLocation as RawSpaceLocation,
    Technology as RawTechnology,
)

# TODO: complicated things not done yet:
# * capture-bot-rocket + (rocket launcher | rocket turret | spidertron) @ nauvis = captive-biter-spawner
#   ^ this is the only example of a building that is not necessarily placed by an item of the same name.
# * boiler not registering as a machine. boiling water is not a Recipe 
# * acid neutralization produces 500C steam. that's functionally a different item from regular steam, but only for steam-turbine. otherwise it's compatible with steam, e.g. for coal liquifaction and steam condensation.

# TODO: delete these notes: 
"""
# These are the exports we're expected to provide:
from .Technologies import free_sample_exclusions, tech_to_progressive_lookup, base_tech_table, all_product_sources, required_technologies, get_rocket_requirements, get_science_pack_pools, Recipe, recipes, technology_table, tech_table, factorio_base_id, useless_technologies, progressive_technology_table, fluids, valid_ingredients
"""
# TODO: redo these:
machine_per_category: dict[str: str] = {} # One machine for each category.
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
    automate_mining              = 1<< 0 # burner mining drill
    mine_with_fluid              = 1<< 1 # uranium mining technology + electric mining drills
    mine_hard_solids             = 1<< 2 # big mining drill
    pump_tiles                   = 1<< 3 # offshore pump
    pump_entities                = 1<< 4 # pumpjack
    automate_planting            = 1<< 5 # agricultural tower
    harness_lightning            = 1<< 6 # lightning rod
    heat_buildings               = 1<< 7 # heating tower or nuclear reactor
    build_on_ocean_planet        = 1<< 8 # ice platform + concrete
    collect_asteroids            = 1<< 9 # asteroid collector
    travel_space                 = 1<<10 # thruster
    destroy_medium_asteroids     = 1<<11 # gun turret
    destroy_big_asteroids        = 1<<12 # rocket turret
    destroy_huge_asteroids       = 1<<13 # railgun turret

    destroy_big_and_smaller_asteroids = destroy_big_asteroids | destroy_medium_asteroids
    destroy_huge_and_smaller_asteroids = destroy_huge_asteroids | destroy_big_and_smaller_asteroids

class PowerType(IntFlag):
    """
    Buildings almost always require exactly 1 power type,
    except for the fusion reactor which consumes both electricty and fusion fuel,
    and some machines operate for free, e.g. offshore-pump.
    """
    electricity   = 1<<0 # produced by solar panel, required by assembling machine.
    heat          = 1<<1 # produced by heating tower, required by heat exchanger.
    chemical      = 1<<2 # satisfied by foraged coal, required by boiler.
    nutrients     = 1<<3 # satisfied by nutrients, required by biochamber.
    food          = 1<<4 # satisfied by bioflux, required by captive biter spawner.
    nuclear       = 1<<5 # satisfied by uranium fuel cell, required by nuclear reactor
    fusion_fuel   = 1<<6 # satisfied by fusion power cell, required by fusion reactor
    fusion_plasma = 1<<7 # produced by fusion reactor, required by fusion generator
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
    unlock_recipes: set[str]
    unlock_space_locations: set[str]
    unlock_mining_with_fluid: bool

    def is_infinite(self):
        return type(self.requirement) == ResearchRequirement and self.requirement.units == None

class CustomTechnology(Technology):
    """A particularly configured Technology for a world."""
    ingredients: set[str]

    def __init__(self, origin: Technology, world, allowed_packs: set[str], player: int):
        ingredients = allowed_packs
        self.player = player
        if origin.name not in world.special_nodes:
            ingredients = set(world.random.sample(list(ingredients), world.random.randint(1, len(ingredients))))
        self.ingredients = ingredients
        super(CustomTechnology, self).__init__(origin.name, origin.factorio_id)

    def get_prior_technologies(self) -> set[Technology]:
        """Get Technologies that have to precede this one to resolve tree connections."""
        technologies = set()
        for ingredient in self.ingredients:
            technologies |= required_technologies[ingredient]  # technologies that unlock the recipes
        return technologies


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
    drop_to: str | None
    """ if this is orbit above a planet, which planet? """
    launch_to: str | None
    """ if this is a planet, what's the location name of the orbit above? """
    thrust_to: list[str]
    """ where would thrusters be able to fly us from here? """
    threats: Capability
    """ what size asteroids do we encounter here, and do buildings freeze? """

    mineable_resources: set["MineableResource"]
    forageable_resources: set["ForageableResource"]

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
    required_ingredients: tuple[str, ...]
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
_asteroid_collecting_machines = {
    RawEntity.asteroid_collector,
}
_tile_mining_machines = {
    RawEntity.offshore_pump,
}

_fluid_conduit_machines = {
    RawEntity.pipe,
    RawEntity.pipe_to_ground,
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

# Psuedo recipes functions in logic like a normal recipe, but Factorio doesn't consider them proper recipes.
_ROCKET_LAUNCHER_CATEGORY = "_rocket-launcher"
_pseudo_recipes = {
    "_capture-spawner-with-rocket": {
        # This says it creates a captive biter spawner as an item, which is not exactly right, but it makes the logic flow as we want.
        # (Unless the captive-biter-spawner-recycling recipe somehow becomes a non-dead-end recycling recipe, then this logic would be broken.)
        "enabled": True,
        "category": _ROCKET_LAUNCHER_CATEGORY,
        "energy": 0.5,
        "hidden_from_player_crafting": True,
        "ingredients": [{"type": "item", "name": RawItem.capture_robot_rocket, "amount": 1}],
        "products": [{"type": "item", "name": RawItem.captive_biter_spawner, "amount": 1}],
        "surface_conditions": _navis_surface_conditions,
    },
}


# TODO: this is unimplemented, and also do we care?
_effective_technology_name_for_progressive_grouping = {
    RawTechnology.turbo_transport_belt: "logistics-4",
    RawTechnology.epic_quality: "quality-upgrade-1",
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

def _get_machine_power_type(entity) -> PowerType:
    result = PowerType.free
    if "burner_prototype" in entity:
        [fuel_category] = entity["burner_prototype"]["fuel_categories"].keys()
        result |= {
            "chemical":  PowerType.chemical,
            "nutrients": PowerType.nutrients,
            "food":      PowerType.food,
            "nuclear":   PowerType.nuclear,
            "fusion":    PowerType.fusion_fuel,
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

    natural_entity_to_locations: dict[str, set[str]] = defaultdict(set)
    natural_tile_to_locations: dict[str, set[str]] = defaultdict(set)
    space_locations: dict[str, SpaceLocation] = {}
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
            for name in homes:
                space_location = space_locations[name]
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
            for name in homes:
                space_location = space_locations[name]
                space_location.mineable_resources.update(mineable_resources)
        else:
            print("WARNING: missing home for natural resource tile: " + tile_name)

    # =====
    # Items
    # =====

    ammo_category_to_weapon_items = defaultdict(set)
    ammo_category_to_ammo_items = defaultdict(set)
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

    # ========
    # Machines
    # ========

    crafting_category_to_machines = defaultdict(set)
    resource_category_to_machines = defaultdict(set)
    automated_planting_machines = set()
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
            resource_category_to_machines[category].add(entity_name)
            is_machine = True
        # agricultural tower:
        if entity_name in _automated_planting_machines:
            automated_planting_machines.add(entity_name)
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

    # =======
    # Recipes
    # =======

    starting_recipes: set[str] = set()
    for recipe_name, recipe_data in itertools.chain(get_data()["recipe"].items(), _pseudo_recipes.items()):
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

    # ============
    # Technologies
    # ============
    recipe_to_technologies: dict[str, set[Technology]] = defaultdict(set)
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


        unlock_recipes = set()
        unlock_space_locations = set()
        unlock_mining_with_fluid = False
        does_anything = False
        for effect in technology_data["effects"]:
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

        technology = Technology(technology_name,
            prerequisites, requirement,
            unlock_recipes, unlock_space_locations, unlock_mining_with_fluid,
        )
        technologies[technology_name] = technology

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
            assert technologies[progressive_chain[1]].is_infinite(), "technology ends with -1 without any other levels: " + progressive_chain[1]
        assert not any(technologies[progressive_chain[level]].is_infinite() for level in range(1, len(progressive_chain)+1-1)), "infinite technology must be the highest level defined in the group: " + progressive_group_name

    import pdb; pdb.set_trace()
    TODO()
    return None

init()

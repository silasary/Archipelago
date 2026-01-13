from __future__ import annotations

import functools, itertools
import string
from collections import Counter
from typing import Dict, Set, FrozenSet, Tuple, Union, List, Any, Optional
from dataclasses import dataclass
from enum import IntFlag

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


class Capability(IntFlag):
    """ The player has the ability to do something. """
    automate_mining = 1<<0 # burner mining drill
    mine_with_fluid = 1<<1 # uranium mining technology
    mine_hard_solids = 1<<2 # big mining drill
    pump_tiles = 1<<3 # offshore pump
    pump_entities = 1<<4 # pumpjack
    automate_planting = 1<<5 # agricultural tower
    heat_buildings = 1<<6 # heating tower, nuclear reactor
    collect_asteroids = 1<<7 # asteroid collector
    travel_space = 1<<8 # thruster

    # big becomes medium, so chain the capabilities.
    destroy_medium_asteroids           = 1<<9 # gun turret
    destroy_big_asteroids        = 1<<10|1<<9 # rocket turret
    destroy_huge_asteroids = 1<<11|1<<10|1<<9 # railgun turret

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


class Machine(FactorioElement):
    def __init__(self, name, categories):
        self.name: str = name
        self.categories: set = categories

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

class SpaceLocation: # TODO subclass AP Region
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
    def __repr__(self):
        return "{}({})".format(type(self).__name__, ", ".join("{}={}".format(name, repr(value)) for name, value in self.__dict__.items()))

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
recipes = {}
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
        RawEntity.gleba_spawner,
        RawEntity.gleba_spawner_small,
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
    },
    RawSpaceLocation.vulcanus: {
        # These don't spawn naturally per se.
        RawEntity.small_demolisher_corpse,
        RawEntity.medium_demolisher_corpse,
        RawEntity.big_demolisher_corpse,
    },
    RawSpaceLocation.fulgora: {
        RawEntity.fulgurite_small,
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

# Nauvis is missing its surface properties for some reason.
_default_gravity = 10
_default_magnetic_field = 90
_default_pressure =  1000

_asteroid_info_table = {
    RawEntity.medium_metallic_asteroid: (Capability.destroy_medium_asteroids, RawItem.metallic_asteroid_chunk),
    RawEntity.medium_carbonic_asteroid: (Capability.destroy_medium_asteroids, RawItem.carbonic_asteroid_chunk),
    RawEntity.medium_oxide_asteroid:    (Capability.destroy_medium_asteroids, RawItem.oxide_asteroid_chunk),
    RawEntity.big_metallic_asteroid:    (Capability.destroy_big_asteroids,    RawItem.metallic_asteroid_chunk),
    RawEntity.big_carbonic_asteroid:    (Capability.destroy_big_asteroids,    RawItem.carbonic_asteroid_chunk),
    RawEntity.big_oxide_asteroid:       (Capability.destroy_big_asteroids,    RawItem.oxide_asteroid_chunk),
    RawEntity.huge_metallic_asteroid:   (Capability.destroy_huge_asteroids,   RawItem.metallic_asteroid_chunk),
    RawEntity.huge_carbonic_asteroid:   (Capability.destroy_huge_asteroids,   RawItem.carbonic_asteroid_chunk),
    RawEntity.huge_oxide_asteroid:      (Capability.destroy_huge_asteroids,   RawItem.oxide_asteroid_chunk),
    RawEntity.huge_promethium_asteroid: (Capability.destroy_huge_asteroids,   RawItem.promethium_asteroid_chunk),
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

_start_unlocked_recipes = {
    # TODO: Derrive this from get_data() and/or make this one or more Options.
    # This relates to whether trigger techs are shuffled, vanilla, skipped, or something else.
    RawRecipe.offshore_pump,
    RawRecipe.boiler,
    RawRecipe.steam_engine,
    RawRecipe.automation_science_pack,
    RawRecipe.inserter,
    RawRecipe.small_electric_pole,
    RawRecipe.copper_cable,
    RawRecipe.lab,
    RawRecipe.electronic_circuit,
    RawRecipe.electric_mining_drill,
    RawRecipe.pipe,
    RawRecipe.pipe_to_ground,
}

def _get_asteroid_info(spawn_data):
    if spawn_data["type"] == "asteroid-chunk":
        # Just a free floating chunk.
        return Capability(0), spawn_data["asteroid"]
    if spawn_data["type"] == "entity":
        # Need to break it open.
        return _asteroid_info_table[spawn_data["asteroid"]]
    assert False, "what's this asteroid data: " + repr(spawn_data)

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
                category = entity["resource_category"]
                if category == "basic-solid":
                    required_capabilities |= Capability.automate_mining
                elif category == "hard-solid":
                    required_capabilities |= Capability.mine_hard_solids
                elif category == "basic-fluid":
                    required_capabilities |= Capability.pump_entities
                else: assert False, "new .resource_category needs to be added to class Capability(IntFlag): " + repr(category)
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
                    # TODO: this is probably the wrong logic for determining what the agricultural tower is willing to plant,
                    # but it gets the answer right for space age: yumako, jellynut, tree.
                    # TODO: determine the valid surface by checking both:
                    #  * entity["surface_conditions"] -- needed for tree-plant
                    #  * entity["autoplace_specification"]["tile_restriction"] -- needed for jellystem
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
    # Note: This does not count drops from stomper shells
    # (i couldn't find a compelling connection between the enemies and their corpses in the data.),
    # but it's all overshadowed by other options on the same surface anyway.

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

    # Collect all crafting entities.
    for entity_name, entity in get_data()["entity"].items():
        if "crafting_categories" not in entity: continue # We're looking for crafting buildings (and "character").
        machines[entity_name] = Machine(entity_name, set(entity["crafting_categories"]))

    # add electric mining drill as a crafting machine to resolve basic-solid (mining)
    #machines["electric-mining-drill"] = Machine("electric-mining-drill", {"basic-solid"})
    #machines["pumpjack"] = Machine("pumpjack", {"basic-fluid"})
    #machines["assembling-machine-1"].categories.add("crafting-with-fluid")  # mod enables this

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

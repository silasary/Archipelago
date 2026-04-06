# This module translates a (pruned) export of data from factorio into a static description of the logic for a given set of options.

# These are the only "public" exports of this module.
__all__ = ["FactorioData", "parse_level_from_technology_prototype_name"]

import itertools, typing
from functools import lru_cache
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum, IntFlag

from .data import generated_names as names
from .Logic import (
    inline_exprs, optimize_expr, ALWAYS, NEVER, EXTERNAL,
)


def parse_level_from_technology_prototype_name(prototype_name):
    # https://lua-api.factorio.com/latest/types/TechnologyUnit.html#count_formula
    try:
        [_, level_str] = prototype_name.rsplit("-", 1)
    except ValueError:
        return 1
    try:
        return int(level_str)
    except ValueError:
        return 1

class FactorioData:
    """
    This class represents all the recipes, technologies, etc. in Factorio,
    and supports making changes, such as recipe randomization, and then can compute derrived info,
    such as logical dependencies.
    """
    the_data: dict[str, dict[str, dict]]
    starting_planet: str
    technology_name_to_progressive_group_name: dict[str, str]
    unrandomized_technologies: set[str]
    skipped_locations: set[str]
    # Derrived:
    infinite_technology_names: set[str]
    empty_technology_names: set[str]
    def __init__(self, the_data,
        technology_name_to_progressive_group_name,
        starting_planet,
        unrandomized_technologies,
        skipped_locations,
    ):
        self.the_data = the_data
        self.starting_planet = starting_planet
        self.technology_name_to_progressive_group_name = technology_name_to_progressive_group_name
        self.unrandomized_technologies = unrandomized_technologies
        self.skipped_locations = skipped_locations
        # Derrived:
        self.infinite_technology_names = {
            name for name, prototype in self.the_data["technology"].items()
            if prototype.get("max_level", "") == "infinite"
        }
        self.empty_technology_names = {
            name for name, prototype in self.the_data["technology"].items()
            if len(prototype.get("effects", [])) == 0
        }

        self.combined_items: dict[str, dict] = {}
        for prototype_type in [
            "ammo",
            "armor",
            "capsule",
            "fluid", # This is technically a different namespace.
            "gun",
            "item",
            "item-with-entity-data",
            "module",
            "rail-planner",
            "repair-tool",
            "space-platform-starter-pack",
            "tool",
        ]:
            for prototype_name, prototype_data in the_data[prototype_type].items():
                if prototype_data.get("parameter", False): continue
                # Throughout this code, we assume there's no ambiguity between item and fluid names. Assert that assumption.
                assert prototype_name not in self.combined_items, "so it's come to this, has it. we need to add 'type' fields to fluid and item references due to name collisions. :NotLikeThis: " + repr(prototype_name)
                self.combined_items[prototype_name] = prototype_data

    def unrecognized_recipe_names(self, possible_names: set[str]) -> set[str]:
        return self._unrecognized_names(possible_names, self.the_data["recipe"])
    def unrecognized_item_names(self, possible_names: set[str]) -> set[str]:
        return self._unrecognized_names(possible_names, self.combined_items)
    def _unrecognized_names(self, possible_names: set[str], prototypes: dict[str, dict]) -> set[str]:
        bad_names = possible_names - prototypes.keys()
        for name in (possible_names & prototypes.keys()):
            prototype_data = prototypes[name]
            if prototype_data.get("hidden", False) or prototype_data.get("parameter", False):
                bad_names.add(name)
        return bad_names

    def get_location_dupe_candidates(self) -> list[str]:
        return [
            name for name, prototype_data in self.the_data["technology"].items()
            if not prototype_data.get("hidden", False) # Not removed by Any Planet Start
            and prototype_data.get("unit", None) # Not a trigger tech
            and prototype_data.get("max_level", None) != "infinite" # Not infinite
        ]


    def build_logic(self, *,
        bypass_technology_prerequisites: bool,
        burner_mining_drill_is_good_enough: bool,
        inserter_balancing_is_good_enough: bool,
        water_barrel_is_good_enough: bool,
        launching_metal_is_good_enough: bool,
        backwards_recycling_is_interesting: bool,
        unbarreling_is_interesting: bool,
        walls_to_destroy_medium_asteroids_is_good_enough: bool,
        small_electric_pole_is_good_enough: bool,
        wait_hours_for_fish_to_spoil: bool,
        storing_seeds_is_good_eough: bool,
        lightning_schmightning: bool,
        solar_panels_into_darkness: bool,
        slow_inserter_is_good_enough: bool,
        assembling_machine_1_is_good_enough: bool,
        direct_pipes_is_good_enough: bool,
        hand_building_is_good_enough: bool,
        belt_logistics_is_good_enough: bool,
        basic_asteroid_processing_is_good_enough: bool,
        nuclear_heating_is_good_enough: bool,

        enemies_enabled: bool,
        demolisher_killers: dict[str, bool],
        pentapod_killers: dict[str, bool],
        medium_asteroid_upgrade_requirements: set[str],

        energy_link_bridge_recipe: dict | None,
        energy_link_bridge_technology: bool,
        energy_link_bridge_required_for: str | None,
        allow_energy_link_to_satisfy_logic: bool,
    ):
        the_data = self.the_data
        combined_items = self.combined_items

        # These will be used for logic later.
        item_to_mining_sources: dict[str, set[MiningSource]] = defaultdict(set)
        item_to_forage_locations: dict[str, set[str]] = defaultdict(set)
        entity_to_mining_sources: dict[str, set[MiningSource]] = defaultdict(set)
        entity_to_forage_locations: dict[str, set[str]] = defaultdict(set)
        natural_entity_to_locations: dict[str, set[str]] = defaultdict(set)
        natural_tile_to_locations: dict[str, set[str]] = defaultdict(set)

        # ===============
        # Space Locations
        # ===============
        surface_property_defaults = {
            prop_name: prop_data["default_value"]
            for prop_name, prop_data in the_data["surface-property"].items()
        }
        control_variable_to_autoplace_things: dict[str, set[str]] = defaultdict(set)
        for prototypes in the_data.values():
            for name, data in prototypes.items():
                try:
                    control_variable = data["autoplace"]["control"]
                except KeyError:
                    continue
                assert name not in control_variable_to_autoplace_things[control_variable], "name collision: " + name
                control_variable_to_autoplace_things[control_variable].add(name)
        @lru_cache()
        def get_asteroid_info(asteroid_name: str) -> tuple[Capability, tuple[str, ...]]:
            if asteroid_name in the_data["asteroid-chunk"]:
                # Just a free floating chunk.
                return Capability(0), (the_data["asteroid-chunk"][asteroid_name]["minable"]["result"],)
            if asteroid_name in the_data["asteroid"]:
                # Need to break it open.
                threats = asteroid_to_capability[asteroid_name]
                items = set()
                # What it does it turn into?
                for effect_data in the_data["asteroid"][asteroid_name]["dying_trigger_effect"]:
                    if effect_data["type"] == "create-asteroid-chunk":
                        sub_name = effect_data["asteroid_name"]
                    elif effect_data["type"] == "create-entity":
                        sub_name = effect_data["entity_name"]
                    else:
                        continue # Ignore create-explosion aesthetic effects.
                    sub_threats, sub_items = get_asteroid_info(sub_name)
                    threats |= sub_threats
                    items.update(sub_items)
                return threats, tuple(sorted(items))
            assert False, "what's this asteroid data: " + repr(spawn_data)

        asteroid_chunk_and_location_to_mining_sources: dict[tuple[str, str], set[MiningSource]] = defaultdict(set)
        space_locations: dict[str, SpaceLocation] = {}
        space_location_to_solar_power: dict[str, int|float] = {}
        for location_name, space_location_data in itertools.chain(
            the_data["planet"].items(),
            the_data["space-location"].items(),
        ):
            if space_location_data.get("hidden", False): continue
            unlock_names = {location_name}
            if "surface_properties" in space_location_data:
                # There is a surface here.
                props = space_location_data["surface_properties"]
                surface_properties = SurfaceProperties(
                    gravity=props.get("gravity", surface_property_defaults["gravity"]),
                    magnetic_field=props.get("magnetic-field", surface_property_defaults["magnetic-field"]),
                    pressure=props.get("pressure", surface_property_defaults["pressure"]),
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
                if location_name in surfaces_requiring_ice_platforms:
                    surface_location.threats |= Capability.build_on_ice_platforms
                if "lightning_properties" in space_location_data:
                    surface_location.threats |= Capability.harness_lightning
                # Natural resources.
                for entity_name in space_location_data["map_gen_settings"]["autoplace_settings"]["entity"]["settings"].keys():
                    natural_entity_to_locations[entity_name].add(surface_location.name)
                for tile_name in space_location_data["map_gen_settings"]["autoplace_settings"]["tile"]["settings"].keys():
                    if "fluid" not in the_data["tile"][tile_name]:
                        continue # Most tiles are not logically relevant.
                    natural_tile_to_locations[tile_name].add(surface_location.name)
                for control_variable in space_location_data["map_gen_settings"]["autoplace_controls"].keys():
                    for thing_name in control_variable_to_autoplace_things.get(control_variable, []):
                        assert thing_name not in the_data["tile"], "change this code to work with control-based autoplace tiles"
                        natural_entity_to_locations[thing_name].add(surface_location.name)
                for unit_name in space_location_data["map_gen_settings"].get("territory_settings", {}).get("units", []):
                    # Demolishers
                    corpse_name = the_data["segmented-unit"][unit_name]["corpse"]
                    natural_entity_to_locations[corpse_name].add(surface_location.name)
                # Missing: stomper shells from stompers from unit spawners.
            else:
                # There is no surface here. e.g. solar-system-edge.
                space_location = SpaceLocation(location_name, SPACE_SURFACE, unlock_names)
                space_locations[space_location.name] = space_location
            # Asteroid info.
            for spawn_data in space_location_data.get("asteroid_spawn_definitions", []):
                threats, items = get_asteroid_info(spawn_data["asteroid"])
                space_location.threats |= threats
                # Add a natural resource for this now, because we already know everything.
                for item in items:
                    asteroid_chunk_and_location_to_mining_sources[(item, space_location.name)].add(MiningSource(item, space_location.name, threats | Capability.collect_asteroids, ()))
            space_location.threats |= Capability.generate_electricity_in_space
            solar_power_in_space = space_location_data.get("solar_power_in_space", 1)
            space_location_to_solar_power[space_location.name] = solar_power_in_space
            if solar_power_in_space < 100:
                # This is true for aquilo and beyond.
                space_location.threats |= Capability.generate_electricity_in_dark_space

        for location_name, space_connection_data in the_data["space-connection"].items():
            connection_names = [
                space_connection_data["from"],
                space_connection_data["to"],
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
                threats, items = get_asteroid_info(spawn_data["asteroid"])
                space_location.threats |= threats
                # Add a natural resource for this now, because we already know everything.
                for item in items:
                    asteroid_chunk_and_location_to_mining_sources[(item, space_location.name)].add(MiningSource(item, space_location.name, threats | Capability.collect_asteroids, ()))
            space_location.threats |= Capability.generate_electricity_in_space
            solar_power_in_space = min(
                space_location_to_solar_power[connection_name]
                for connection_name in connection_names
            )
            if solar_power_in_space < 100:
                # This is true for all of aquilo's connections and beyond.
                space_location.threats |= Capability.generate_electricity_in_dark_space

        # The generic expression optimizer has trouble with the complexity of asteroid chunk sourcing.
        # Do a little bit of simplification now.
        for (item, space_location_name), sources in asteroid_chunk_and_location_to_mining_sources.items():
            sources = sorted(sources, key=lambda mining_source: mining_source.required_capabilities)
            easiest_source = sources[0]
            item_to_mining_sources[item].add(easiest_source)
            for mining_source in sources[1:]:
                if mining_source.required_capabilities & easiest_source.required_capabilities == easiest_source.required_capabilities:
                    # This is strictly harder. Logic only needs to know about the easiest one.
                    continue
                # This never happens, but would mean that mining some sources of asteroid chunks aren't strictly easier or harder than other sources.
                assert False, "incomparable asteroid mining capabilities? if this really happens, just delete this assertion"
                item_to_mining_sources[item].add(mining_source)
        del asteroid_chunk_and_location_to_mining_sources # This intermediate form is done.

        def get_allowed_locations(surface_conditions) -> set[str] | None:
            if surface_conditions == None: return None
            return set(
                location_name for location_name, location in space_locations.items()
                if location.surface_properties.satisfies(surface_conditions)
            )

        # =================
        # Natural Resources
        # =================
        def get_mine_results(prototype_data):
            if "results" in prototype_data["minable"]:
                return [result["name"] for result in prototype_data["minable"]["results"]]
            if "result" in prototype_data["minable"]:
                return [prototype_data["minable"]["result"]]
            return []
        # Mining (drills and pumpjacks)
        for prototype_name, prototype_data in the_data["resource"].items():
            # https://lua-api.factorio.com/latest/prototypes/ResourceEntityPrototype.html
            if "autoplace" not in prototype_data: continue # We're looking for natural features.
            if "minable" not in prototype_data: continue # We're looking for things we can mine.
            required_capabilities = resource_category_to_capbility[prototype_data.get("category", "basic-solid")]
            required_ingredients = ()
            if "required_fluid" in prototype_data["minable"]:
                required_ingredients = (prototype_data["minable"]["required_fluid"],)
                required_capabilities |= Capability.mine_with_fluid
            results = get_mine_results(prototype_data)
            for home in natural_entity_to_locations.get(prototype_name, ()):
                for result in results:
                    home_threats = space_locations[home].threats
                    mining_source = MiningSource(result, home, required_capabilities|home_threats, required_ingredients)
                    item_to_mining_sources[result].add(mining_source)
                    entity_to_mining_sources[prototype_name].add(mining_source)
        # Foraging
        for prototype_name, prototype_data in itertools.chain(
            the_data["fish"].items(),
            the_data["lightning-attractor"].items(),
            the_data["simple-entity"].items(), # rocks, etc.
            the_data["tree"].items(), # Does not include automatable plants. Those are in "plant" below.
        ):
            # https://lua-api.factorio.com/latest/prototypes/EntityPrototype.html
            if "autoplace" not in prototype_data: continue # We're looking for natural features.
            if "minable" not in prototype_data: continue # We're looking for things we can mine.
            results = get_mine_results(prototype_data)
            for home in natural_entity_to_locations.get(prototype_name, ()):
                entity_to_forage_locations[prototype_name].add(home)
                for result in results:
                    item_to_forage_locations[result].add(home)
        # Plants: yumako-tree, jellystem, tree-plant.
        plant_to_seed = {
            prototype_data["plant_result"]: prototype_name
            for prototype_name, prototype_data in combined_items.items()
            if "plant_result" in prototype_data
        }
        for prototype_name, prototype_data in the_data["plant"].items():
            # https://lua-api.factorio.com/latest/prototypes/PlantPrototype.html
            assert "autoplace" in prototype_data, prototype_name
            assert "minable" in prototype_data, prototype_name
            results = get_mine_results(prototype_data)
            # Foraging
            for home in natural_entity_to_locations.get(prototype_name, ()):
                entity_to_forage_locations[prototype_name].add(home)
                for result in results:
                    item_to_forage_locations[result].add(home)
            # Automation
            seed_name = plant_to_seed[prototype_name]
            for result in results:
                for home in plant_to_valid_surfaces[prototype_name]:
                    home_threats = space_locations[home].threats
                    item_to_mining_sources[result].add(MiningSource(result, home, Capability.automate_planting|home_threats, (seed_name,)))
        # Enemy bases: gleba-spawner yields pentapod-egg
        for prototype_name, prototype_data in the_data["unit-spawner"].items():
            # https://lua-api.factorio.com/latest/prototypes/EnemySpawnerPrototype.html
            if "loot" not in prototype_data: continue # Not logically interesting
            results = [p["item"] for p in prototype_data["loot"]]
            for home in natural_entity_to_locations.get(prototype_name, ()):
                for result in results:
                    item_to_forage_locations[result].add(home)
        # Tiles: water, lava, ammoniacal solution
        for tile_name, tile_data in the_data["tile"].items():
            if "autoplace" not in prototype_data: continue # We're looking for natural features.
            if "fluid" not in tile_data: continue
            fluid_name = tile_data["fluid"]
            for home in natural_tile_to_locations.get(tile_name, ()):
                # This claims that pumping ammoniacal solution with an offshore pump requires heating buildings, which is not quite right,
                # but it's tricky to find a more correct place for the threat logic.
                home_threats = space_locations[home].threats
                item_to_mining_sources[fluid_name].add(MiningSource(fluid_name, home, Capability.pump_tiles|home_threats, ()))

        # =====
        # Items
        # =====
        # Handheld weapons are logically relevant for capturing biter spawners.
        ammo_category_to_weapon_items = defaultdict(set)
        for item_name, item_data in the_data["gun"].items():
            # https://lua-api.factorio.com/latest/types/BaseAttackParameters.html
            if "ammo_categories" in item_data["attack_parameters"]:
                ammo_categories = item_data["attack_parameters"]["ammo_categories"]
            elif "ammo_category" in item_data["attack_parameters"]:
                ammo_categories = [item_data["attack_parameters"]["ammo_category"]]
            else: assert False, "attack_parameters missing ammo category"
            for ammo_category in ammo_categories:
                ammo_category_to_weapon_items[ammo_category].add(item_name)
        # Ammo is logically relevant for destroying asteroids of various sizes.
        ammo_category_to_ammo_items = defaultdict(set)
        for item_name, item_data in the_data["ammo"].items():
            # https://lua-api.factorio.com/latest/prototypes/AmmoItemPrototype.html#ammo_category
            ammo_category_to_ammo_items[item_data["ammo_category"]].add(item_name)
        # Fuel
        power_type_to_fuel_items = defaultdict(set)
        for item_name, item_data in combined_items.items():
            # https://lua-api.factorio.com/latest/prototypes/ItemPrototype.html
            if "fuel_category" in item_data:
                power_type_to_fuel_items[fuel_category_to_power_type[item_data["fuel_category"]]].add(item_name)

        # ========
        # Machines
        # ========
        machines: dict[str, Machine] = {}
        crafting_category_to_machines = defaultdict(set)
        mining_capability_to_machines = defaultdict(set)
        mining_drills_with_fluid_connections = set()
        automated_planting_machines = set()
        lightning_harnessing_machines = set()
        asteroid_collecting_machines = set()
        tile_mining_machines = set()
        water_boilers_165C = set()
        water_boilers_500C = set()
        electricity_producing_machines = set()
        heat_producing_machines = set()
        fusion_plasma_producing_machines = set()
        thruster_machines = set()
        lab_machines = set()
        all_science_pack_names = set()
        ammo_category_to_weapon_entities = defaultdict(set)

        for prototype_type in [
            "agricultural-tower",
            "ammo-turret",
            "assembling-machine",
            "asteroid-collector",
            "boiler",
            "car",
            "character",
            "electric-turret",
            "fluid-turret",
            "furnace",
            "fusion-generator",
            "fusion-reactor",
            "generator",
            "lab",
            "lightning-attractor",
            "mining-drill",
            "offshore-pump",
            "pump",
            "reactor",
            "roboport",
            "rocket-silo",
            "solar-panel",
            "spider-vehicle",
            "thruster",
        ]:
            for prototype_name, prototype_data in the_data[prototype_type].items():
                if prototype_data.get("hidden", False): continue

                # What powers this machine?
                # What is this machine's consumption/production of different forms of power?
                power_required = PowerType.free
                if "energy_source" in prototype_data:
                    if prototype_data["energy_source"]["type"] == "burner":
                        # stone-furnace, biochamber, nuclear-reactor, etc.
                        [fuel_category] = prototype_data["energy_source"]["fuel_categories"]
                        power_required |= fuel_category_to_power_type[fuel_category]
                    elif prototype_data["energy_source"]["type"] == "electric":
                        usage_priority = prototype_data["energy_source"]["usage_priority"]
                        # https://lua-api.factorio.com/latest/types/ElectricUsagePriority.html
                        if usage_priority in (
                            "lamp", # small lamp
                            "primary-input", # combinators, fusion reactor, rocket silo, ...
                            "secondary-input", # assembling machine, pumpjack, ...
                        ):
                            # assembling-machine, etc.
                            power_required |= PowerType.electricity
                        elif usage_priority in (
                            "primary-output", # lightning rod
                            "secondary-output", # steam engine, steam turbine, fusion generator
                            "solar", # solar panel
                        ):
                            # steam-engine, etc.
                            electricity_producing_machines.add(prototype_name)
                        elif usage_priority == "tertiary":
                            pass # An accumulator's effect on the power grid is not logically relevant.
                        else: assert False, "unrecognized electric usage_priority: " + prototype_name
                    elif prototype_data["energy_source"]["type"] == "heat":
                        power_required |= PowerType.heat
                    elif prototype_data["energy_source"]["type"] == "void":
                        pass # Why even specify this?
                    else: assert False, "unrecognized energy source type: " + prototype_name
                if "burner" in prototype_data:
                    # fusion-reactor
                    [fuel_category] = prototype_data["burner"]["fuel_categories"]
                    power_required |= fuel_category_to_power_type[fuel_category]
                # Steam powered:
                if prototype_type == "generator":
                    # https://lua-api.factorio.com/latest/prototypes/GeneratorPrototype.html
                    if prototype_data["maximum_temperature"] == 165:
                        power_required |= PowerType.steam_165C
                    elif prototype_data["maximum_temperature"] == 500:
                        power_required |= PowerType.steam_500C
                    else: assert False, "unrecognized generator maximum_temperature: " + prototype_name

                # Can't figure out where water consumption and steam production is in the data.
                if prototype_type == "boiler":
                    if prototype_data["target_temperature"] == 165:
                        water_boilers_165C.add(prototype_name)
                    elif prototype_data["target_temperature"] == 500:
                        water_boilers_500C.add(prototype_name)
                    else: assert False, "unrecognized boiled water temperature: " + prototype_name
                # Can't find where plasma production/consumption is in the data.
                if prototype_type == "fusion-reactor":
                    fusion_plasma_producing_machines.add(prototype_name)
                if prototype_type == "fusion-generator":
                    power_required |= PowerType.fusion_plasma
                # Can't find where heat production is in the data.
                if prototype_type == "reactor":
                    # nuclear-reactor, heating-tower
                    heat_producing_machines.add(prototype_name)

                # Crafting machines.
                if prototype_type in (
                    "assembling-machine",
                    "character",
                    "furnace",
                    "rocket-silo",
                ):
                    for category in prototype_data["crafting_categories"]:
                        crafting_category_to_machines[category].add(prototype_name)
                # Mining drills, pumpjacks, and the character:
                if prototype_type in ("mining-drill", "character"):
                    for category in prototype_data[{
                        "mining-drill": "resource_categories",
                        "character": "mining_categories",
                    }[prototype_type]]:
                        mining_capability_to_machines[resource_category_to_capbility[category]].add(prototype_name)
                        if "input_fluid_box" in prototype_data:
                            mining_drills_with_fluid_connections.add(prototype_name)
                # Machines with specialized functions:
                if prototype_type == "agricultural-tower":
                    automated_planting_machines.add(prototype_name)
                if prototype_type == "lightning-attractor":
                    if prototype_data["efficiency"] == 0:
                        # fulgoran-ruin-attractor doesn't count.
                        continue
                    lightning_harnessing_machines.add(prototype_name)
                if prototype_type == "asteroid-collector":
                    asteroid_collecting_machines.add(prototype_name)
                if prototype_type == "offshore-pump":
                    tile_mining_machines.add(prototype_name)

                # Thruster:
                if prototype_type == "thruster":
                    thruster_machines.add(prototype_name)
                    power_required |= PowerType.thruster_fuel
                # Labs:
                if prototype_type == "lab":
                    lab_machines.add(prototype_name)
                    for science_pack_name in prototype_data["inputs"]:
                        all_science_pack_names.add(science_pack_name)

                # Turrets and vehicles:
                if prototype_type == "ammo-turret":
                    # E.g. gun-turret
                    ammo_category_to_weapon_entities[prototype_data["attack_parameters"]["ammo_category"]].add(prototype_name)
                if prototype_type in ("car", "spider-vehicle"):
                    # e.g. tank
                    for gun_name in prototype_data["guns"]:
                        gun_data = the_data["gun"][gun_name]
                        ammo_category_to_weapon_entities[gun_data["attack_parameters"]["ammo_category"]].add(prototype_name)

                # Where can this machine operate?
                locations = get_allowed_locations(prototype_data.get("surface_conditions", None))
                can_freeze = "heating_energy" in prototype_data

                machines[prototype_name] = Machine(prototype_name, power_required, locations, can_freeze)

        assert all(all_science_pack_names == set(the_data["lab"][lab_name]["inputs"]) for lab_name in lab_machines), "labs that take a subset of science packs are not supported"
        # Assume a 1:1 correspondance between items and machine entities.
        for item_name, item_data in combined_items.items():
            if "place_result" not in item_data: continue
            entity_name = item_data["place_result"]
            if entity_name not in machines:
                # e.g. stone-brick places stone-path, yumako-seed places yumako-tree, etc.
                # But those aren't placing machines, so ignore them.
                continue
            # This is an item that places a machine that we care about.
            assert entity_name == item_name, "non-bijective item to machine naming: " + item_name
            # Mining the machine will probably result in this item, but don't bother checking.
            # There's at least one example of a violation of this: captive-biter-spawner.
            # And it's not even really logically relevant what happens when you pick up a machine;
            # the important thing is how do you build it.
        fluid_conduit_machines = set()
        for prototype_name, prototype_data in the_data["pipe"].items():
            if prototype_data.get("hidden", False): continue
            fluid_conduit_machines.add(prototype_name)
        electricity_conduit_machines = set()
        for prototype_name, prototype_data in the_data["electric-pole"].items():
            if prototype_data.get("hidden", False): continue
            electricity_conduit_machines.add(prototype_name)
        heat_conduit_machines = set()
        for prototype_name, prototype_data in the_data["heat-pipe"].items():
            if prototype_data.get("hidden", False): continue
            heat_conduit_machines.add(prototype_name)

        # =======
        # Recipes
        # =======

        recipes: dict[str, Recipe] = {}
        starting_recipes: set[str] = set()
        unbarreling_recipes: set[str] = set()
        for recipe_name, recipe_data in the_data["recipe"].items():
            if recipe_data.get("parameter", False): continue
            energy = recipe_data.get("energy_required", 0.5) # crafting time in seconds.
            category = recipe_data.get("category", "crafting")

            override_data = override_recipe_data.get(recipe_name, recipe_data)
            extra_products = []
            for p in override_data["results"]:
                if p["name"] == names.steam and "temperature" in p:
                    assert p["temperature"] == 500, "unrecognized steam temperature in recipe output: " + recipe_name
                    extra_products.append({
                        # This steam also satisfies the 500C steam requirement.
                        # Effectively produce both to make it work with the logic.
                        "name": STEAM_500C,
                        "amount": p["amount"],
                    })

            inputs = {
                i["name"]: i["amount"] - i.get("ignored_by_stats", 0)
                for i in override_data["ingredients"]
            }
            outputs = {
                p["name"]: p["amount"] * p.get("probability", 1) + p.get("extra_count_fraction", 0) - p.get("ignored_by_stats", 0)
                for p in itertools.chain(override_data["results"], extra_products)
            }

            if len(inputs) == len(outputs) == 0:
                # Ignore recipe-unknown.
                continue
            elif any(amount < 0 for amount in outputs.values()):
                # This only happens for dead-end recycling recipes, such as copper-ore-recycling.
                assert (
                    category == "recycling" and
                    len(inputs) == 1 and
                    inputs.keys() == outputs.keys() and
                    all(amount == 0 for amount in inputs.values())
                ), "expected a negative byproduct to be part of a dead-end recycling recipe: " + recipe_name
                classification = RecipeClassification.dead_end_recycling
            elif category == "recycling":
                # Uncrafting an item.
                assert len(inputs) == 1 and sum(inputs.values()) == 1, "is this not an un-crafting recipe?: " + recipe_name
                classification = RecipeClassification.backwards_recycling
            elif all(amount == 0 for amount in inputs.values()) and all(amount == 0 for amount in outputs.values()):
                # This is a lossless conversion recipe, such as barreling/unbarreling or fluoroketone cooling.
                # Thematically the recipe respects conservation of mass, if you like.
                classification = RecipeClassification.conversion
                if names.barrel in outputs.keys():
                    unbarreling_recipes.add(recipe_name)
            elif any(amount == 0 and name in outputs and outputs[name] > 0 for name, amount in inputs.items()):
                # Use an item (and something else surely) to produce more of the item (and something else possibly).
                # e.g. kovarex, pentapod egg breeding, coal liquefaction
                classification = RecipeClassification.breeding
            else:
                # e.g. electronic circuit, cryogenic science pack
                classification = RecipeClassification.standard

            # What machines can perform this recipe?
            valid_machines = crafting_category_to_machines[category]
            # Where can this recipe be performed?
            locations = get_allowed_locations(recipe_data.get("surface_conditions", None))

            recipes[recipe_name] = Recipe(recipe_name, inputs, outputs, energy, classification, valid_machines, locations)

            if recipe_data.get("enabled", True):
                starting_recipes.add(recipe_name)

        # Spoiling is like a recipe.
        for item_name, item_data in combined_items.items():
            if "spoil_result" not in item_data: continue
            product = item_data["spoil_result"]
            recipe_name = item_name + SPOILING_SUFFIX
            recipes[recipe_name] = Recipe(recipe_name,
                inputs={item_name:1}, outputs={product:1},
                energy=item_data["spoil_ticks"] / 60,
                classification=RecipeClassification.spoilage,
                machines=None, locations=None,
            )
            starting_recipes.add(recipe_name)

        # Water boiling is like a recipe.
        for machine_name in water_boilers_165C:
            recipe_name = machine_name + OPERATION_SUFFIX
            recipes[recipe_name] = Recipe(recipe_name,
                inputs={names.water: 6}, outputs={names.steam: 60},
                energy=1, classification=RecipeClassification.standard,
                machines={machine_name}, locations=None,
            )
            starting_recipes.add(recipe_name)
        for machine_name in water_boilers_500C:
            recipe_name = machine_name + OPERATION_SUFFIX
            recipes[recipe_name] = Recipe(recipe_name,
                inputs={names.water: 10.3}, outputs={
                    STEAM_500C: 103,
                    # 500C steam also works as plain steam for coal liquefaction and steam engine operation.
                    # The math here is a lie, because we're not really producing twice as much steam,
                    # but our logic doesn't consider managing unwanted byproducts, so the result is correct here.
                    # (Note that STEAM_500C is not counted as a fluid when determining if a recipe requires pipes.)
                    names.steam: 103,
                },
                energy=1, classification=RecipeClassification.standard,
                machines={machine_name}, locations=None,
            )
            starting_recipes.add(recipe_name)

        # TODO: pseduo recipes for burnt_result (depleted_uranium_fuel_cell)
        # TODO: pseudo recipes for fusion_reactor producing fusion_plasma.

        product_to_recipes: dict[str, set[str]] = defaultdict(set)
        for recipe_name, recipe in recipes.items():
            for product in recipe.outputs.keys():
                product_to_recipes[product].add(recipe_name)

        # ============
        # Technologies
        # ============
        technologies: dict[str, Technology] = {}
        technology_props_lua: dict[str, dict] = {}
        empty_technologies: set[str] = set()
        infinite_technologies: set[str] = set()
        recipe_to_unlocking_technologies: dict[str, set[str]] = defaultdict(set)
        space_location_to_unlocking_technologies: dict[str, set[str]] = defaultdict(set)
        mining_with_fluid_unlocking_technologies = set()
        for prototype_name, prototype_data in the_data["technology"].items():
            if prototype_data.get("hidden", False): continue # any-planet-start hides disocvery of your starting planet.
            # https://lua-api.factorio.com/latest/prototypes/TechnologyPrototype.html
            assert " " not in prototype_name, "spaces are used to prefix event types. a space in a technology name creates ambiguity"
            prerequisites = set(prototype_data.get("prerequisites", []))
            prerequisites -= self.skipped_locations
            technology_props = {
                "prerequisites": sorted(prerequisites),
            }
            is_infinite = False
            if "unit" in prototype_data:
                ingredients = {name: amount for (name, amount) in prototype_data["unit"]["ingredients"]}
                # Research technology (using science packs and labs).
                assert set(ingredients.values()) == {1}, "update comment on ResearchRequirement.ingredients to no longer claim the amount is always 1"
                requirement = ResearchRequirement(tuple(ingredients.keys()), not prototype_data.get("ignore_tech_cost_multiplier", False))
                technology_props["unit"] = prototype_data["unit"]
                is_infinite = prototype_data.get("max_level", None) == "infinite"
                assert is_infinite == ("count_formula" in prototype_data["unit"]), "conflicting signals on whether this is infinite tech: " + prototype_name
                if is_infinite:
                    # laser-weapons-damage goes infinite at level 7,
                    # and the count formula assumes L=7 will be the first instantiation.
                    technology_props["level"] = parse_level_from_technology_prototype_name(prototype_name)
                    technology_props["max_level"] = prototype_data["max_level"]
                    # The effects can be shuffled later.
                    technology_props["effects"] = prototype_data["effects"]
            elif "research_trigger" in prototype_data:
                # Trigger technology.
                trigger = prototype_data["research_trigger"]
                technology_props["research_trigger"] = trigger
                if trigger["type"] == "craft-item":
                    requirement = CraftRequirement(trigger["item"], trigger.get("count", 1))
                elif trigger["type"] == "craft-fluid":
                    requirement = CraftRequirement(trigger["fluid"], trigger.get("count", 1))
                elif trigger["type"] == "mine-entity":
                    requirement = MineRequirement(trigger["entity"])
                elif trigger["type"] == "build-entity":
                    requirement = BuildRequirement(trigger["entity"])
                elif trigger["type"] == "capture-spawner":
                    requirement = CaptureSpawnerRequirement()
                elif trigger["type"] == "create-space-platform":
                    requirement = CreateSpacePlatformRequirement()
                else: assert False, "unrecognized research trigger type: " + repr(trigger["type"])
            else: assert False, "technology has no cost or trigger: " + prototype_name

            technology = Technology(prototype_name, prerequisites, requirement)
            technologies[prototype_name] = technology
            technology_props_lua[prototype_name] = technology_props

            does_something_important = False
            if "effects" in prototype_data:
                for effect in prototype_data["effects"]:
                    if effect["type"] == "unlock-recipe":
                        recipe_to_unlocking_technologies[effect["recipe"]].add(prototype_name)
                        does_something_important = True
                    elif effect["type"] == "unlock-space-location":
                        space_location_to_unlocking_technologies[effect["space_location"]].add(prototype_name)
                        does_something_important = True
                    elif effect["type"] == "mining-with-fluid":
                        mining_with_fluid_unlocking_technologies.add(prototype_name)
                        does_something_important = True
                    else:
                        pass # It does something else not relevant to logic.
            else:
                empty_technologies.add(prototype_name)

            if is_infinite:
                assert not does_something_important, "infinite research is doing something important: " + prototype_name
                infinite_technologies.add(prototype_name)

        # =====
        # Logic
        # =====
        logic_events = {}

        # Thanks to an assertion above, we can conflate item names with machine names here for simplicity.
        fmt_discover_location = "Discover {}".format
        fmt_reach_location = "Reach {}".format
        fmt_access_item = "Access {}".format
        fmt_automate_item = "Automate {}".format
        fmt_capability = lambda capability: "Can {}".format(capability.name.replace("_", " "))
        fmt_operate_machine = "Operate {}".format
        fmt_supply_power = lambda power_type: "Supply {}".format(power_type.name.replace("_", " "))
        fmt_technology_location = "{}_location".format # These are proper Archipelago items.
        fmt_unlock_technology = lambda name: name # These are proper Archipelago items.
        fmt_learn_recipe = "Learn {}".format

        can_launch_rockets = fmt_automate_item(names.rocket_part)
        if launching_metal_is_good_enough:
            automate_iron_plates_in_space = ALWAYS
        else:
            automate_iron_plates_in_space = {"and": [
                fmt_operate_machine(names.asteroid_collector),
                fmt_operate_machine(names.crusher),
                {"or": [
                    # The normal way.
                    fmt_operate_machine(names.electric_furnace),
                    # The Vulcanus way.
                    {"and": [
                        fmt_operate_machine(names.foundry),
                        fmt_unlock_technology(names.advanced_asteroid_processing),
                    ]},
                ]},
            ]}
        if direct_pipes_is_good_enough:
            optionally_access_pumps_and_tanks = ALWAYS
        else:
            optionally_access_pumps_and_tanks = {"and": [
                fmt_access_item(names.pump),
                fmt_access_item(names.storage_tank),
            ]}
        if belt_logistics_is_good_enough:
            optionally_operate_requester_chests = ALWAYS
        else:
            optionally_operate_requester_chests = {"and": [
                fmt_access_item(names.requester_chest),
                fmt_access_item(names.roboport),
                fmt_access_item(names.logistic_robot),
            ]}
        if hand_building_is_good_enough:
            optionally_operate_construction_robots = ALWAYS
        else:
            optionally_operate_construction_robots = {"and": [
                fmt_access_item(names.storage_chest), # I think this is always redundant with roboport, but included for completeness.
                fmt_access_item(names.roboport),
                fmt_access_item(names.construction_robot),
            ]}
        can_get_water_in_space = {"or": [
            # Probably this one.
            {"and": [
                fmt_learn_recipe(names.ice_melting),
                fmt_automate_item(names.ice),
                fmt_operate_machine(names.chemical_plant),
            ]},
        ]}
        if water_barrel_is_good_enough:
            # Technically this also works.
            can_get_water_in_space["or"].append({"and": [
                fmt_learn_recipe(names.empty_water_barrel),
                fmt_automate_item(names.water_barrel),
                {"or": [
                    fmt_operate_machine(names.assembling_machine_2),
                    fmt_operate_machine(names.assembling_machine_3),
                ]},
            ]})
            # The offshore pump sources of water don't count, and neither does steam condensation.

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
            logic_events[fmt_discover_location(name)] = {"or": [fmt_unlock_technology(technology) for technology in techs]}
        # Start on a planet
        if self.starting_planet == 'all_simultaneously':
            for planet in [names.nauvis, names.fulgora, names.gleba, names.vulcanus]:
                logic_events[fmt_discover_location(planet)] = ALWAYS
                logic_events[fmt_reach_location(planet)] = ALWAYS
        else:
            logic_events[fmt_discover_location(self.starting_planet)] = ALWAYS
            logic_events[fmt_reach_location(self.starting_planet)] = ALWAYS

        # Capabilities.
        for capability in Capability:
            if capability in mining_capability_to_machines:
                expr = {"or": [
                    fmt_operate_machine(name) for name in mining_capability_to_machines[capability]
                    if name != names.character # Smacking rocks does not count as automating mining.
                ]}
            elif capability == Capability.mine_with_fluid:
                expr = {"and": [
                    {"or": [fmt_unlock_technology(name) for name in mining_with_fluid_unlocking_technologies]},
                    {"or": [fmt_operate_machine(name) for name in mining_drills_with_fluid_connections]},
                ]}
            elif capability == Capability.pump_tiles:
                expr = {"or": [fmt_operate_machine(name) for name in tile_mining_machines]}
            elif capability == Capability.automate_planting:
                expr = {"or": [fmt_operate_machine(name) for name in automated_planting_machines]}
            elif capability == Capability.harness_lightning:
                if lightning_schmightning:
                    expr = ALWAYS
                else:
                    expr = {"or": [
                        *[fmt_operate_machine(name) for name in lightning_harnessing_machines],
                    ]}
            elif capability == Capability.build_space_platforms:
                expr = {"and": [
                    can_launch_rockets,
                    fmt_access_item(names.space_platform_starter_pack),
                ]}
            elif capability == Capability.capture_biter_spawners:
                expr = {"and": [
                    fmt_reach_location(names.nauvis),
                    fmt_access_item(names.capture_robot_rocket),
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
                if not nuclear_heating_is_good_enough:
                    expr["and"].append(fmt_operate_machine(names.heating_tower))
            elif capability == Capability.build_on_ice_platforms:
                expr = {"or": [fmt_automate_item(name) for name in heat_insulation_flooring_items]}
            elif capability == Capability.collect_asteroids:
                expr = {"or": [fmt_operate_machine(name) for name in asteroid_collecting_machines]}
            elif capability == Capability.travel_space:
                expr = {"and": [
                    {"or": [fmt_operate_machine(name) for name in thruster_machines]},
                    # Also need to automate bullets probably.
                    automate_iron_plates_in_space,
                    # It'd be nice to have robots at this point too.
                    optionally_access_pumps_and_tanks,
                    optionally_operate_requester_chests,
                    optionally_operate_construction_robots,
                ]}
            elif capability == Capability.generate_electricity_in_space:
                expr = {"or": [
                    # In order to infer this from the data, we would need to understand that unbarreling water always requires power,
                    # and that water is required for every other form of power. (And fusion requires power to turn on.)
                    # This logic has a very poor understanding of the separation between surfaces, so special casing power
                    # is a simple way to mostly get everything else to click into place.
                    fmt_operate_machine(names.solar_panel),
                ]}
                if allow_energy_link_to_satisfy_logic:
                    expr["or"].append(fmt_access_item(names.ap_energy_link_bridge))
            elif capability == Capability.generate_electricity_in_dark_space:
                # See above comment about inferring why certain power sources are hard to infer not working in space.
                expr = {"or": [
                    # Nuclear reactor power.
                    {"and": [
                        fmt_operate_machine(names.nuclear_reactor),
                        fmt_operate_machine(names.steam_turbine), # includes heat exchanger and stuff.
                        # And get water in space.
                        can_get_water_in_space,
                    ]},
                    # Fusion power.
                    {"and": [
                        fmt_operate_machine(names.fusion_generator),
                        # You must barrel the coolant to get it into space.
                        fmt_access_item(names.fluoroketone_cold_barrel),
                    ]},
                ]}
                if solar_panels_into_darkness:
                    # Or if you really want to try to make this work.
                    expr["or"].append(fmt_operate_machine(names.solar_panel))
                if allow_energy_link_to_satisfy_logic:
                    # The Easy Way(TM).
                    expr["or"].append(fmt_access_item(names.ap_energy_link_bridge))
            elif capability == Capability.destroy_medium_asteroids:
                ammo_category = "bullet"
                expr = {"or": [
                    {"and": [
                        # Pewpew is the usual way.
                        {"or": [
                            fmt_operate_machine(machine) for machine in ammo_category_to_weapon_entities[ammo_category]
                            # Car and tank don't work in space, and aren't automated.
                            # Just hardcoding the answer i guess.
                            if machine == names.gun_turret
                        ]},
                        {"or": [fmt_automate_item(item) for item in ammo_category_to_ammo_items[ammo_category]]},
                        *[fmt_unlock_technology(bonus) for bonus in medium_asteroid_upgrade_requirements],
                    ]},
                ]}
                if walls_to_destroy_medium_asteroids_is_good_enough:
                    # Consult your local speedrunner to find out if wall ships are right for you.
                    expr["or"].append(fmt_automate_item(names.stone_wall))
                    # No repair packs in logic for you. Be grateful you get walls.
            elif capability == Capability.destroy_big_asteroids:
                ammo_category = "rocket"
                expr = {"and": [
                    {"or": [
                        fmt_operate_machine(machine) for machine in ammo_category_to_weapon_entities[ammo_category]
                        # Spidertron can't be placed in space.
                        # Just hardcoding the answer i guess.
                        if machine == names.rocket_turret
                    ]},
                    {"or": [
                        fmt_automate_item(item) for item in ammo_category_to_ammo_items[ammo_category]
                        # atomic bomb and capture robot rocket are not what you need.
                        # Just hardcoding the answer i guess.
                        if item in (names.rocket, names.explosive_rocket)
                    ]},
                ]}
                if not basic_asteroid_processing_is_good_enough:
                    expr["and"].extend([
                        fmt_unlock_technology(names.asteroid_reprocessing),
                        fmt_unlock_technology(names.advanced_asteroid_processing),
                    ])
            elif capability == Capability.destroy_huge_asteroids:
                ammo_category = "railgun"
                expr = {"and": [
                    {"or": [fmt_operate_machine(machine) for machine in ammo_category_to_weapon_entities[ammo_category]]},
                    {"or": [fmt_automate_item(item) for item in ammo_category_to_ammo_items[ammo_category]]},
                ]}
            elif capability == Capability.kill_demolishers:
                source_exprs = []
                for setting, value in demolisher_killers.items():
                    if not value: continue
                    if setting == "poison capsule":
                        source_exprs.append(fmt_access_item(names.poison_capsule))
                    elif setting == "land mine":
                        source_exprs.append(fmt_access_item(names.land_mine))
                    elif setting == "gun turret and firearm magazine":
                        source_exprs.append({"and": [
                            fmt_access_item(names.gun_turret),
                            fmt_access_item(names.firearm_magazine),
                        ]})
                    elif setting == "gun turret and piercing rounds magazine":
                        source_exprs.append({"and": [
                            fmt_access_item(names.gun_turret),
                            fmt_access_item(names.piercing_rounds_magazine),
                        ]})
                    elif setting == "gun turret and uranium rounds magazine":
                        source_exprs.append({"and": [
                            fmt_access_item(names.gun_turret),
                            fmt_access_item(names.uranium_rounds_magazine),
                        ]})
                    elif setting == "rocket turret and rocket":
                        source_exprs.append({"and": [
                            fmt_access_item(names.rocket_turret),
                            fmt_access_item(names.rocket),
                        ]})
                    elif setting == "rocket turret and explosive rocket":
                        source_exprs.append({"and": [
                            fmt_access_item(names.rocket_turret),
                            fmt_access_item(names.explosive_rocket),
                        ]})
                    elif setting == "tesla turret":
                        source_exprs.append(fmt_operate_machine(names.tesla_turret))
                    elif setting == "atomic bomb":
                        source_exprs.append({"and": [
                            fmt_access_item(names.rocket_launcher),
                            fmt_access_item(names.atomic_bomb),
                        ]})
                    elif setting == "railgun":
                        source_exprs.append({"and": [
                            fmt_access_item(names.railgun),
                            fmt_access_item(names.railgun_ammo),
                        ]})
                    else: assert False
                expr = {"or": source_exprs}
            elif capability == Capability.kill_pentapods:
                source_exprs = []
                for setting, value in pentapod_killers.items():
                    if not value: continue
                    if setting == "land mine":
                        source_exprs.append(fmt_automate_item(names.land_mine))
                    elif setting == "rocket turret":
                        source_exprs.append({"and": [
                            fmt_access_item(names.rocket_turret),
                            fmt_automate_item(names.rocket),
                        ]})
                    elif setting == "gun turret and firearm magazine":
                        source_exprs.append({"and": [
                            fmt_access_item(names.gun_turret),
                            fmt_automate_item(names.firearm_magazine),
                        ]})
                    elif setting == "gun turret and piercing rounds magazine":
                        source_exprs.append({"and": [
                            fmt_access_item(names.gun_turret),
                            fmt_automate_item(names.piercing_rounds_magazine),
                        ]})
                    elif setting == "gun turret and uranium rounds magazine":
                        source_exprs.append({"and": [
                            fmt_access_item(names.gun_turret),
                            fmt_automate_item(names.uranium_rounds_magazine),
                        ]})
                    elif setting == "tesla turret":
                        source_exprs.append(fmt_operate_machine(names.tesla_turret))
                    elif setting == "railgun":
                        source_exprs.append({"and": [
                            fmt_access_item(names.railgun),
                            fmt_automate_item(names.railgun_ammo),
                        ]})
                    else: assert False
                expr = {"or": source_exprs}
            else: assert False, "forgot a capability: " + repr(capability)

            logic_events[fmt_capability(capability)] = expr
            del expr # give me a NameError if i forget to assign to expr in this loop.

        # Machines
        for machine_name, machine in machines.items():
            if machine_name == names.character: continue # You can access yourself from the beginning.
            # Craft the machine.
            obtain_expr = fmt_access_item(machine_name)
            if machine_name == names.captive_biter_spawner:
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
            if machine_name in fusion_plasma_producing_machines:
                # You also need coolant for this machine.
                expr["and"].append(fmt_access_item(names.fluoroketone_cold))
            if (
                machine.locations != None and
                all(space_locations[name].surface_properties.gravity == 0 for name in machine.locations) and
                PowerType.electricity in machine.power_required
            ):
                # Space requires special electricity.
                expr["and"].append(fmt_capability(Capability.generate_electricity_in_space))
            logic_events[fmt_operate_machine(machine_name)] = expr

        # Power
        for power_type in PowerType:
            if power_type in power_type_to_fuel_items:
                expr = {"or": [fmt_access_item(item) for item in power_type_to_fuel_items[power_type]]}
            elif power_type == PowerType.steam_165C:
                expr = fmt_access_item(names.steam)
            elif power_type == PowerType.steam_500C:
                expr = fmt_access_item(STEAM_500C)
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
                    fmt_automate_item(names.thruster_fuel),
                    fmt_automate_item(names.thruster_oxidizer),
                    {"or": [fmt_access_item(machine) for machine in fluid_conduit_machines]},
                    # Also need water in space.
                    can_get_water_in_space,
                ]}
            else: assert False, "forgot a PowerType: " + repr(power_type)
            logic_events[fmt_supply_power(power_type)] = expr
            del expr # give me a NameError if i forget to assign to expr in this loop.

        # Research
        def get_logic_expr_for_requirement(requirement):
            if type(requirement) == ResearchRequirement:
                fmt_automate_or_access = fmt_automate_item if requirement.uses_tech_cost_multiplier else fmt_access_item
                expr = {"and": [
                    {"or": [fmt_operate_machine(lab) for lab in lab_machines]},
                    *[fmt_automate_or_access(science_pack) for science_pack in requirement.ingredients],
                ]}
            elif type(requirement) == CraftRequirement:
                # FIXME: This assumes that mining up the item counts as crafting it, which i think is wrong, but i don't think it ever matters.
                if requirement.count < 100:
                    # e.g. 50 iron plates for steam power, 25 bioflux for rocket-fuel-from-jelly.
                    expr = fmt_access_item(requirement.item)
                else:
                    # e.g. 100 nutrients for agricultural-science-pack, 500 nutrients for artificial soil.
                    expr = fmt_automate_item(requirement.item)
            elif type(requirement) == BuildRequirement:
                # FIXME: This also requires that you power the thing, which is not correct,
                # but it's more correct than just crafting it.
                # (building an asteroid collector requires launching a space platform starter pack, but not having solar panels.)
                # This incorrect logic inflicts unnecessary logical requirements,
                # which at least is erring in the right direction.
                expr = fmt_operate_machine(requirement.entity)
            elif type(requirement) == MineRequirement:
                source_exprs = []
                if requirement.entity in entity_to_mining_sources:
                    for mining_source in entity_to_mining_sources[requirement.entity]:
                        required_capabilities = mining_source.required_capabilities
                        if not (required_capabilities & Capability.mine_with_fluid):
                            # The character can hand-mine basic-solid ore patches.
                            required_capabilities &= ~Capability.automate_mining
                        source_exprs.append({"and": [
                            fmt_reach_location(mining_source.location),
                            *[fmt_capability(capability) for capability in required_capabilities],
                            *[fmt_access_item(ingredient) for ingredient in mining_source.required_ingredients],
                        ]})
                elif requirement.entity in entity_to_forage_locations:
                    source_exprs.extend(fmt_reach_location(home) for home in entity_to_forage_locations[requirement.entity])
                else: assert False, "no way to mine for trigger tech: " + requirement.entity
                expr = {"or": source_exprs}
            elif type(requirement) == CaptureSpawnerRequirement:
                expr = fmt_capability(Capability.capture_biter_spawners)
            elif type(requirement) == CreateSpacePlatformRequirement:
                expr = fmt_capability(Capability.build_space_platforms)
            else: assert False, "forgot a requirement type: " + repr(requirement)
            return expr
        @lru_cache(maxsize=None)
        def get_prerequisite_requirements(later_technology_name) -> set["Requirement"]:
            """
            returns all prerequisite requirements, not the reqirements of the technology itself.
            returns a set of requirement objects.
            """
            recursive_requirements = set()
            for prerequisite_technology_name in technologies[later_technology_name].prerequisites:
                if prerequisite_technology_name in self.skipped_locations:
                    continue
                recursive_requirements.update(get_prerequisite_requirements(prerequisite_technology_name))
                prerequisite_technology = technologies[prerequisite_technology_name]
                recursive_requirements.add(prerequisite_technology.requirement)
            return recursive_requirements
        for technology_name, technology in technologies.items():
            expr = get_logic_expr_for_requirement(technology.requirement)

            # add prerequisites into logic.
            prerequisite_requirements = get_prerequisite_requirements(technology_name)
            if len(prerequisite_requirements) > 0 and not bypass_technology_prerequisites:
                expr = {"and": [
                    expr,
                    {"and": [
                        get_logic_expr_for_requirement(requirement)
                        for requirement in prerequisite_requirements
                    ]},
                ]}

            if technology_name not in self.skipped_locations:
                logic_events[fmt_technology_location(technology_name)] = expr
            if technology_name in self.unrandomized_technologies:
                # Tell the optimizer how to inline these.
                logic_events[fmt_unlock_technology(technology_name)] = expr
            else:
                # The multiworld decides how to get it.
                logic_events[fmt_unlock_technology(technology_name)] = EXTERNAL
            del expr # give me a NameError if i forget to assign to expr in this loop.
        # EnergyLink technology, victory technologies.
        if energy_link_bridge_technology:
            logic_events[fmt_unlock_technology(names.ap_energy_link_bridge)] = EXTERNAL
        # This isn't ever randomized, but no need to describe the details to the optimizer.
        logic_events[fmt_unlock_technology(names.victory)] = EXTERNAL

        # Recipes
        for recipe_name, recipe in recipes.items():
            if recipe_name.endswith(pseudo_recipe_suffixes): continue # not a real recipe.
            if recipe_name in starting_recipes:
                expr = ALWAYS
            elif recipe_name == names.iron_stick:
                # Prevent circuit-network from getting flagged as advancmenet because it could be a provider of the iron stick recipe for refined concrete.
                # Really every recipe that needs sticks also comes with the sticks, so just remove this recipe from logical consideration.
                expr = ALWAYS
            else:
                expr = {"or": [
                    fmt_unlock_technology(technology_name)
                    for technology_name in recipe_to_unlocking_technologies.get(recipe_name, [])
                ]}
            logic_events[fmt_learn_recipe(recipe_name)] = expr

        # Items
        for item_name, prototype_data in itertools.chain(
            combined_items.items(),
            [(STEAM_500C, {})],
        ):
            for fmt_automate_or_access in [fmt_access_item, fmt_automate_item]:
                source_exprs = []
                # Foraging sources only count for accessing the item, not for automating it.
                if fmt_automate_or_access is fmt_access_item:
                    for home in item_to_forage_locations.get(item_name, []):
                        source_exprs.append(fmt_reach_location(home))
                # Mining
                for mining_source in item_to_mining_sources.get(item_name, []):
                    required_capabilities = mining_source.required_capabilities
                    if not (required_capabilities & Capability.mine_with_fluid) and fmt_automate_or_access is fmt_access_item:
                        # The character can hand-mine basic-solid ore patches.
                        required_capabilities &= ~Capability.automate_mining
                    if self.starting_planet == names.vulcanus and enemies_enabled and item_name == names.tungsten_ore:
                        required_capabilities |= Capability.kill_demolishers
                    source_exprs.append({"and": [
                        fmt_reach_location(mining_source.location),
                        *[fmt_capability(capability) for capability in required_capabilities],
                        *[fmt_access_item(ingredient) for ingredient in mining_source.required_ingredients],
                    ]})
                # Crafting
                for recipe_name in product_to_recipes.get(item_name, []):
                    recipe = recipes[recipe_name]
                    if recipe.classification == RecipeClassification.dead_end_recycling:
                        continue # e.g. steel recycling is not a source of steel.
                    if recipe.outputs[item_name] == 0 and recipe.classification != RecipeClassification.conversion:
                        continue # e.g. quantum-processor is not a source of fluoroketone-hot
                    if item_name in recipe.inputs and recipe.outputs[item_name] - recipe.inputs[item_name] < 0:
                        continue # e.g. metallic-asteroid-crushing is not a source of metallic-asteroid-chunk
                    if recipe_name == names.nutrients_from_spoilage and fmt_automate_or_access is fmt_automate_item:
                        # Crafting nutrients from spoilage is not a viable source of automated nutrients.
                        # The reason is in the numbers in the data, so this could be possible to infer automatically,
                        # but it would need to consider many branching paths through bioflux and bacteria
                        # and also consider productivity bonuses at every step of the way.
                        # Instead of all that, hardcode this escape hatch where nutrients from spoilage is suitable only for getting a
                        # catalyst amount of nutrients.
                        continue
                    # This recipe works.
                    recipe_exprs = []
                    if not recipe_name.endswith(pseudo_recipe_suffixes):
                        recipe_exprs.append(fmt_learn_recipe(recipe_name))
                    for ingredient, amount in recipe.inputs.items():
                        if amount <= 0 and recipe.classification != RecipeClassification.conversion:
                            # This item must be present, but isn't "consumed" so to speak by the recipe.
                            # Automating this recipe only needs limited access to the ingredient.
                            recipe_exprs.append(fmt_access_item(ingredient))
                        else:
                            recipe_exprs.append(fmt_automate_or_access(ingredient))
                    needs_pipes = (
                        sum(ingredient in the_data["fluid"].keys() for ingredient in recipe.inputs.keys()) >= 2 or
                        sum(product    in the_data["fluid"].keys() for product    in recipe.outputs.keys()) >= 2
                    )
                    if needs_pipes:
                        recipe_exprs.append({"or": [fmt_access_item(machine) for machine in fluid_conduit_machines]})
                    if recipe.machines != None:
                        machine_exprs = []
                        for machine in recipe.machines:
                            if machine == names.character:
                                # The character can only create limited quantities. Not proper automation.
                                if fmt_automate_or_access is fmt_access_item:
                                    machine_expr = ALWAYS
                                else:
                                    machine_expr = NEVER
                            else:
                                machine_expr = fmt_operate_machine(machine)
                            machine_exprs.append(machine_expr)
                        recipe_exprs.append({"or": machine_exprs})
                    if recipe.classification == RecipeClassification.backwards_recycling:
                        if not backwards_recycling_is_interesting:
                            # Just cull this recipe from the logic if we're not doing something like a Fulgora start.
                            recipe_exprs.append(NEVER)
                    elif recipe.classification == RecipeClassification.spoilage and recipe.energy > 120:
                        if not wait_hours_for_fish_to_spoil:
                            recipe_exprs.append(NEVER)
                    if recipe.locations != None:
                        recipe_exprs.append({"or": [fmt_reach_location(location_name) for location_name in recipe.locations]})
                    # Logic option hooks
                    if item_name == names.logistic_science_pack and fmt_automate_or_access is fmt_automate_item:
                        if not burner_mining_drill_is_good_enough:
                            # Require electric mining drills to get out of the early game.
                            recipe_exprs.append(fmt_access_item(names.electric_mining_drill))
                        if not inserter_balancing_is_good_enough:
                            recipe_exprs.extend([
                                fmt_access_item(names.underground_belt),
                                fmt_access_item(names.splitter),
                            ])
                    if item_name == names.advanced_circuit and names.assembling_machine_2 in recipe.machines and fmt_automate_or_access is fmt_automate_item:
                        # Require faster machines to get through the blue science phase of the game.
                        if not slow_inserter_is_good_enough:
                            recipe_exprs.append(fmt_access_item(names.fast_inserter))
                        if not assembling_machine_1_is_good_enough:
                            recipe_exprs.append(fmt_access_item(names.assembling_machine_2))
                    if recipe_name in (names.advanced_oil_processing, names.coal_liquefaction):
                        # You could probably do without this, but it sure is easier with fluid handling.
                        recipe_exprs.append(optionally_access_pumps_and_tanks)
                    if item_name in (names.production_science_pack, names.utility_science_pack) and fmt_automate_or_access is fmt_automate_item:
                        # Require construction robots to scale up your factory for purple/yellow science.
                        recipe_exprs.append(optionally_operate_construction_robots)
                    if item_name == names.space_science_pack and fmt_automate_or_access is fmt_automate_item:
                        # Require electric furnaces to make space science.
                        recipe_exprs.append(automate_iron_plates_in_space)
                    if recipe_name in (names.metallurgic_science_pack, names.electromagnetic_science_pack) and fmt_automate_or_access is fmt_automate_item:
                        if not small_electric_pole_is_good_enough:
                            recipe_exprs.append(fmt_access_item(names.medium_electric_pole))
                    if recipe_name == names.agricultural_science_pack and fmt_automate_or_access is fmt_automate_item:
                        if not storing_seeds_is_good_eough:
                            recipe_exprs.append({"or": [
                                fmt_access_item(names.heating_tower),
                                fmt_access_item(names.recycler),
                            ]})
                        if enemies_enabled:
                            recipe_exprs.append(fmt_capability(Capability.kill_pentapods))
                    if self.starting_planet == names.gleba and enemies_enabled and recipe_name == names.chemical_science_pack and fmt_automate_or_access is fmt_automate_item:
                        recipe_exprs.append(fmt_capability(Capability.kill_pentapods))
                    if recipe_name in unbarreling_recipes:
                        if not unbarreling_is_interesting:
                            # Unbarreling is never a source of an item.
                            recipe_exprs.append(NEVER)
                    if energy_link_bridge_required_for == item_name and fmt_automate_or_access is fmt_automate_item:
                        recipe_exprs.append(fmt_access_item(names.ap_energy_link_bridge))
                    source_exprs.append({"and": recipe_exprs})
                logic_events[fmt_automate_or_access(item_name)] = {"or": source_exprs}

        # Access Archipelago EnergyLink Bridge
        if energy_link_bridge_recipe != None:
            expr = {"and": [
                # Craft it according to configurable recipe.
                fmt_access_item(ingredient_data["name"]) for ingredient_data in energy_link_bridge_recipe
            ]}
            if energy_link_bridge_technology:
                # Unlock the recipe.
                expr["and"].append(fmt_unlock_technology(names.ap_energy_link_bridge))
            logic_events[fmt_access_item(names.ap_energy_link_bridge)] = expr

        # Optimize.
        logic_events = {k: optimize_expr(v, k) for k, v in logic_events.items()}
        never_delete_events = {event_name for event_name in logic_events.keys() if " " not in event_name}
        never_inline_events = {
            # These are sometimes goals, which the logic needs to see in the final product:
            fmt_reach_location(names.aquilo),
            fmt_reach_location(names.solar_system_edge),
        }
        # It's nice to show these in the spoiler walkthrough:
        never_inline_events.update(fmt_automate_item(science_pack_name) for science_pack_name in all_science_pack_names)

        logic_events, all_used_names = inline_exprs(logic_events, never_delete_events, never_inline_events)
        advancement_technologies = set(name for name in all_used_names if " " not in name)
        advancement_technologies -= {ALWAYS, EXTERNAL}
        # If any one recipe in a progressive chain is advancement, then every progresive item is advancement.
        # e.g. progressive-automation is advancement even though automation-3 isn't.
        advancement_technologies.update(
            self.technology_name_to_progressive_group_name[technology_name]
            for technology_name in all_used_names
            if technology_name in self.technology_name_to_progressive_group_name
        )
        # Winning is indeed an advancement item.
        advancement_technologies.add(names.victory)

        return logic_events, advancement_technologies, technology_props_lua




class Capability(IntFlag):
    """
    Represents global milestones in the player's abilities
    """
    automate_mining                    = 1<< 0 # burner mining drill
    mine_with_fluid                    = 1<< 1 # uranium mining technology + electric mining drills
    mine_hard_solids                   = 1<< 2 # big mining drill
    pump_tiles                         = 1<< 3 # offshore pump
    pump_entities                      = 1<< 4 # pumpjack
    build_space_platforms              = 1<< 5 # launch rockets + craft start pack
    automate_planting                  = 1<< 6 # agricultural tower
    harness_lightning                  = 1<< 7 # lightning rod
    capture_biter_spawners             = 1<< 8 # capture robot rocket + some rocket launcher on nauvis
    heat_buildings                     = 1<< 9 # heating tower or nuclear reactor
    build_on_ice_platforms             = 1<<10 # concrete
    collect_asteroids                  = 1<<11 # asteroid collector
    travel_space                       = 1<<12 # thruster and either ice or water barrel
    generate_electricity_in_space      = 1<<13 # solar panel
    generate_electricity_in_dark_space = 1<<14 # nuclear or fusion
    destroy_medium_asteroids           = 1<<15 # gun turret
    destroy_big_asteroids              = 1<<16 # rocket turret
    destroy_huge_asteroids             = 1<<17 # railgun turret
    kill_demolishers                   = 1<<18 # configurable, e.g. poison capsule
    kill_pentapods                     = 1<<19 # configurable, e.g. land mine


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

class RecipeClassification(IntEnum):
    standard = 0 # Produce "better" items.
    breeding = 1 # Produce more of the same items.
    conversion = 2 # Lossless conversion of items into other items.
    backwards_recycling = 3 # Un-crafting an item via a recycler.
    dead_end_recycling = 4 # 75% chance to destroy item in a recycler.
    spoilage = 5 # Waiting.

@dataclass(frozen=True)
class ResearchRequirement:
    ingredients: tuple[str]
    """ the keys are the science pack names for 1 unit of research. the values are always 1. """
    uses_tech_cost_multiplier: bool
    """ whether the units scale with the tech cost multiplier map gen setting. """
@dataclass(frozen=True)
class CraftRequirement:
    item: str
    """ e.g. 'steel-plate' """
    count: int
    """ e.g. 50 """
@dataclass(frozen=True)
class MineRequirement:
    entity: str
    """ e.g. 'fulgoran-ruin-vault' """
@dataclass(frozen=True)
class BuildRequirement:
    entity: str
    """ e.g. 'asteroid-collector' """
@dataclass(frozen=True)
class CaptureSpawnerRequirement: pass
@dataclass(frozen=True)
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
    machines: set[str] | None
    """ this recipe can be performed in any of these machines, possibly including 'character' for hand crafting. None means this is a spoiling process. """
    locations: set[str] | None
    """ this recipe must be performed in one of these locations. None means anywhere. """

SPOILING_SUFFIX = "_spoiling"
OPERATION_SUFFIX = "_operation"
pseudo_recipe_suffixes = (SPOILING_SUFFIX, OPERATION_SUFFIX)

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

# Steam is both a power source and an "item" sometimes.
# There may be a way to infer where temperatures of which fluids are interesting by looking at fluid box filters and stuff,
# but I don't want to write a whole fluid temperature layer of data throughout this code,
# so we're just hardcoding steam at 2 temperatures, and putting in special case handling for them.
STEAM_500C = names.steam + "_500C"

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
            if "min" in condition_data and not (condition_data["min"] <= value):
                return False
            if "max" in condition_data and not (value <= condition_data["max"]):
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


# Map Factorio enums to our own.
resource_category_to_capbility = {
   "basic-solid": Capability.automate_mining,
   "hard-solid":  Capability.mine_hard_solids,
   "basic-fluid": Capability.pump_entities,
}
fuel_category_to_power_type = {
    "chemical":  PowerType.chemical_fuel,
    "nutrients": PowerType.nutrients,
    "food":      PowerType.food,
    "nuclear":   PowerType.nuclear_fuel,
    "fusion":    PowerType.fusion_fuel,
}


# Hard code the answers to certain questions that aren't inferred from the data.


surfaces_requiring_ice_platforms = {
    # If this were to be inferred from the data, it would mean noticing that the starting area is super small,
    # and also noticing that the ammoniacal ocean tiles allow only ice platform and not landfill
    # (from the ice platform / landfill item prototype .place_as_tile.tile_condition).
    # The latter isn't too bad, but noticing the size of the starting area being super
    # small would require evaluating the noise functions, which is waaaay too much effort
    # compared to just hardcoding the answer here.
    names.aquilo,
}

heat_insulation_flooring_items = {
    # I never figured out how this could be inferred from the data.
    # One clue is that stone-brick item prototype .place_as_tile.condition.layers includes "meltable",
    # whereas the concrete items do not include that layer.
    # Beyond that, I'm stumped.
    names.concrete,
    names.hazard_concrete,
    names.refined_concrete,
    names.refined_hazard_concrete,
}

asteroid_to_capability = {
    # If this were to be inferred from the data, it would mean checking the damage resistances of each entity type,
    # and then making a judgement call about what numeric thresholds and ratios were acceptable.
    names.small_metallic_asteroid:    Capability.destroy_medium_asteroids,
    names.small_carbonic_asteroid:    Capability.destroy_medium_asteroids,
    names.small_oxide_asteroid:       Capability.destroy_medium_asteroids,
    names.small_promethium_asteroid:  Capability.destroy_medium_asteroids,
    names.medium_metallic_asteroid:   Capability.destroy_medium_asteroids,
    names.medium_carbonic_asteroid:   Capability.destroy_medium_asteroids,
    names.medium_oxide_asteroid:      Capability.destroy_medium_asteroids,
    names.medium_promethium_asteroid: Capability.destroy_medium_asteroids,
    names.big_metallic_asteroid:      Capability.destroy_big_asteroids,
    names.big_carbonic_asteroid:      Capability.destroy_big_asteroids,
    names.big_oxide_asteroid:         Capability.destroy_big_asteroids,
    names.big_promethium_asteroid:    Capability.destroy_big_asteroids,
    names.huge_metallic_asteroid:     Capability.destroy_huge_asteroids,
    names.huge_carbonic_asteroid:     Capability.destroy_huge_asteroids,
    names.huge_oxide_asteroid:        Capability.destroy_huge_asteroids,
    names.huge_promethium_asteroid:   Capability.destroy_huge_asteroids,
}

plant_to_valid_surfaces = {
    # If this were to be inferred from the data, it would mean checking the surface conditions and autoplace tile restrictions,
    # and recursively discovering that gleba soil can only be placed on tiles that are only on gleba.
    names.yumako_tree: (names.gleba,),
    names.jellystem:   (names.gleba,),
    names.tree_plant:  (names.nauvis,),
}

override_recipe_data = {
    # The devs claim this is not a bug: https://forums.factorio.com/viewtopic.php?t=122288 .
    # But our logic requires that all circular recipes use the ignore fields to figure out how to automate them.
    names.copper_bacteria_cultivation: {
        "ingredients": [
            { "type": "item", "name": "copper-bacteria", "amount": 1,
                "ignored_by_stats": 1, # Added this.
            },
            { "type": "item", "name": "bioflux", "amount": 1, },
        ],
        "results": [
            { "type": "item", "name": "copper-bacteria", "probability": 1, "amount": 4,
                "ignored_by_stats": 1, # Added this.
                "ignored_by_productivity": 1, # Added this.
            },
        ],
    },
    names.iron_bacteria_cultivation: {
        "ingredients": [
            { "type": "item", "name": "iron-bacteria", "amount": 1,
                "ignored_by_stats": 1, # Added this.
            },
            { "type": "item", "name": "bioflux", "amount": 1, },
        ],
        "results": [
            { "type": "item", "name": "iron-bacteria", "probability": 1, "amount": 4,
                "ignored_by_stats": 1, # Added this.
                "ignored_by_productivity": 1, # Added this.
            },
        ],
    },
}


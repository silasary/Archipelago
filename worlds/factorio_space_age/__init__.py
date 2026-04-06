from __future__ import annotations

import typing
from collections import defaultdict

from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld

from .settings import FactorioSettings
from .Options import FactorioOptions, option_groups
from .data.generated_ids import (
    ap_item_name_to_id, ap_location_name_to_id,
)
# NOTE: avoid importing FactorioData and other large modules until someone actually instantiates a Factorio apworld.
# This improves startup time for the launcher.


def _register_client():
    from worlds.LauncherComponents import Component, components, Type, launch as launch_component
    def launch_client(*args: str):
        from .Client import launch
        launch_component(launch, name="Factorio: Space Age Client", args=args)
    components.append(Component("Factorio: Space Age Client", func=launch_client, component_type=Type.CLIENT))
_register_client()


class FactorioWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Factorio software on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Berserker, Farrak Kilhn, Josh Wolfe"]
    )]
    option_groups = option_groups


class FactorioItem(Item):
    game = "Factorio: Space Age"

class FactorioLocation(Location):
    game = "Factorio: Space Age"
    revealed: bool

    def __init__(self, player: int, name: str, address: int, parent: Region,
        access_rule_fn: typing.Callable[[dict[str, int]], bool],
    ):
        super().__init__(player, name, address, parent)
        self.revealed = False
        self.access_rule = lambda state: access_rule_fn(state.prog_items[player])


class Factorio(World):
    """
    Factorio is a game in which you build and maintain factories.

    You will be mining resources, researching technologies, building infrastructure,
    automating production, and fighting enemies. Use your imagination to design your factory,
    combine simple elements into ingenious structures, apply management skills to keep it working,
    and protect it from the creatures who don't really like you.

    https://www.factorio.com/
    """
    game = "Factorio: Space Age"
    required_client_version = (0, 6, 6)

    web = FactorioWeb()
    settings: typing.ClassVar[FactorioSettings]
    options_dataclass = FactorioOptions
    options: FactorioOptions

    item_name_to_id = ap_item_name_to_id
    location_name_to_id = ap_location_name_to_id
    item_name_groups = {}

    locations: list[FactorioLocation]
    recipe_changes: dict[str, dict[str, object]]
    rocket_parts_per_rocket: int
    asteroid_hp_changes: dict[str, float]
    technology_effect_additions: dict[str, dict]
    logic_events: dict
    advancement_technologies: set[str]
    infinite_technology_shuffle: dict[str, str] | None = None
    empty_technologies: list[str]
    starting_planet: str
    enemies_enabled: bool
    medium_asteroid_upgrade_requirements: set[str]
    early_unrandomized_technologies: set[str]
    skipped_locations: set[str]
    filler_weights_argv: tuple[list[str], list[int]]
    location_to_duplicates: dict[str, list[str]]

    def __init__(self, world, player: int):
        self.locations = []
        self.recipe_changes = {}
        self.asteroid_hp_changes = {}
        self.technology_effect_additions = defaultdict(list)
        self.skipped_locations = set()
        super().__init__(world, player)

    def generate_output(self, output_directory: str) -> None:
        from .Mod import generate_mod
        from .data import generated_names as names
        generate_mod(
            player=self.player,
            player_name=self.player_name,
            world_locations=self.locations,
            options=self.options,
            multiworld=self.multiworld,
            logic_events=self.logic_events,
            progressive_technology_stacks=self.progressive_technology_stacks,
            technology_name_to_progressive_group_name=self.technology_name_to_progressive_group_name,
            infinite_technology_names=self.factorio_data.infinite_technology_names,
            infinite_technology_shuffle=self.infinite_technology_shuffle,
            duplicate_location_to_original_location={
                duplicate: origin_location
                for origin_location, duplicates in self.location_to_duplicates.items()
                for duplicate in duplicates
            },
            technology_props_lua=self.technology_props_lua,
            recipe_changes=self.recipe_changes,
            rocket_parts_per_rocket=self.rocket_parts_per_rocket,
            asteroid_hp_changes=self.asteroid_hp_changes,
            technology_effect_additions=dict(self.technology_effect_additions),
            starting_planet=self.starting_planet,
            vulcanus_rock_multiplier=self.options.vulcanus_rocks.value,
            enable_alternate_explosives=self.starting_planet == names.gleba and self.options.gleba_coal.current_key == "alternate_explosives",
            output_directory=output_directory,
        )

    def generate_early(self) -> None:
        import json
        from .FactorioData import FactorioData
        from .data.ap_data import (
            trap_names, energy_link_bridge_recipes,
            small_progressive_groups, large_progressive_groups,
            starting_planet_to_unrandomized_technologies,
        )
        from .data import generated_names as names

        self.starting_planet = self.options.starting_planet.current_key
        self.enemies_enabled = (
            not self.options.world_gen_custom.value["basic"].get("no_enemies_mode", False)
            if self.options.world_gen.current_key == "custom" else
            self.options.world_gen_enemies.value
        )
        self.early_unrandomized_technologies = starting_planet_to_unrandomized_technologies[self.starting_planet]

        the_data = json.loads(read_local_path("data/ap-dump.json"))
        if self.starting_planet != names.nauvis:
            # Patch the logic data according to Any Planet Start mod.
            data_diff = json.loads(read_local_path("data/ap-dump-{}.json".format(self.starting_planet)))
            for prototype_type, prototype_diffs in data_diff.items():
                prototypes = the_data[prototype_type]
                for prototype_name, prototype_diff in prototype_diffs.items():
                    if prototype_diff == None:
                        del prototypes[prototype_name]
                    else:
                        prototypes[prototype_name] = prototype_diff

        if self.starting_planet == "all_simultaneously":
            # Planet picker automatically gives you discovery when a player first picks it, but that's not good enough for one person using respawn-to-any-planet.
            self.options.start_inventory.value.update({
                name: 1 for name in [
                    names.planet_discovery_nauvis,
                    names.planet_discovery_fulgora,
                    names.planet_discovery_gleba,
                    names.planet_discovery_vulcanus,
                ]
            })

        if self.options.skip_starting_trigger_techs.value:
            self.options.start_inventory.value.update({
                name: 1 for name in self.early_unrandomized_technologies
            })
            self.skipped_locations.update(self.early_unrandomized_technologies)

        infinite_scrap_recycling_productivity = names.scrap_recycling_productivity
        self.progressive_technology_stacks = {
            "only_related": small_progressive_groups,
            "large_groups": large_progressive_groups,
        }[self.options.progressive_technologies.current_key]
        # Remove unrandomized and removed technologies from progressive stacks.
        remove_from_progressive_stacks = {
             *self.early_unrandomized_technologies,
             *{
                 name for name, technology_data in the_data["technology"].items()
                 if technology_data.get("hidden", False)
             },
        }
        if self.starting_planet == names.nauvis:
            remove_from_progressive_stacks.add(names.planet_discovery_nauvis)
        self.progressive_technology_stacks = {
            group_name: [
                name for name in stack
                if name not in remove_from_progressive_stacks
            ]
            for group_name, stack in self.progressive_technology_stacks.items()
        }
        if self.starting_planet == names.fulgora:
            # any-planet-start instantiates 3 levels of scrap productivity, so the infinite one starts at 4.
            try:
                # progressive_technologies: only_related
                scrap_stack = self.progressive_technology_stacks[names.scrap_recycling_productivity]
            except KeyError:
                # progressive_technologies: large_groups
                scrap_stack = self.progressive_technology_stacks[names.progressive_fulgora]
            assert scrap_stack[-1] == infinite_scrap_recycling_productivity
            del scrap_stack[-1]
            scrap_stack.extend([
                names.scrap_recycling_productivity_1,
                names.scrap_recycling_productivity_2,
                names.scrap_recycling_productivity_3,
                names.scrap_recycling_productivity_4, # infinite
            ])
            infinite_scrap_recycling_productivity = scrap_stack[-1]

        # Now build the reverse index.
        self.technology_name_to_progressive_group_name = {
            technology_name: progressive_group_name
            for progressive_group_name, stack in self.progressive_technology_stacks.items()
            for technology_name in stack
        }

        if self.options.quick_start.value:
            # quick_start effectively modifies starting_items.
            # TODO: use the freeplay remote interface to load some of this stuff into the crashed ship instead,
            # so that newly joining multiplayers of the factorio world don't get all these starting items.
            # Something like this maybe: https://github.com/ouk-ouk/Factorio-NoRespawnGun/blob/c3f55d2dc5bf8a832ba8c110e23a71122252dd88/src/control.lua#L20C112-L20C129
            # See /path/to/factorio/data/base/script/freeplay.lua for the definition of the remote interface.
            for k, v in {
                # Run fast. Build fast. Fun fast.
                names.power_armor: 1,
                names.fission_reactor_equipment: 1,
                names.battery_equipment: 2,
                names.personal_roboport_equipment: 1,
                names.exoskeleton_equipment: 3,
                names.construction_robot: 50,
                # Also get through the burner phase faster.
                names.burner_mining_drill: 49, # +1 from scenario
                names.stone_furnace: 49,       # +1 from scenario
                names.wood: 99,                # +1 from scenario
                names.iron_plate: 500,
                names.iron_gear_wheel: 200,
                names.copper_cable: 200,       # +200 from free samples (if enabled)
                # Assembling machines cost 10 secience packs to unlock (not configurable).
                names.automation_science_pack: 10,
            }.items():
                try:
                    self.options.starting_items.value[k] += v
                except KeyError:
                    self.options.starting_items.value[k] = v
            # Quick start also makes bots faster.
            for k, v in {
                names.worker_robots_speed_7: 5
            }.items():
                try:
                    self.options.start_inventory.value[k] += v
                except KeyError:
                    self.options.start_inventory.value[k] = v

        # Data modifications.
        # Note that this modifies the_data in place.
        small_divisor = 1
        if self.options.space_technology_level.current_key != "vanilla":
            index = {"mid_game": 0, "early_game": 1}[self.options.space_technology_level.current_key]
            small_divisor = {"mid_game": 2, "early_game": 4}[self.options.space_technology_level.current_key]
            large_divisor = {"mid_game": 4, "early_game": 10}[self.options.space_technology_level.current_key]

            # Recipes
            ingredient_replacements = {
                names.processing_unit:       [names.advanced_circuit, names.electronic_circuit][index],
                names.advanced_circuit:      [names.advanced_circuit, names.electronic_circuit][index],
                names.low_density_structure: [names.plastic_bar,      names.copper_plate][index],
                names.rocket_fuel:           [names.sulfur,           names.coal][index],
                names.electric_engine_unit:  [names.engine_unit,      names.iron_gear_wheel][index],
                names.steel_plate:           [names.steel_plate,      names.iron_plate][index],
                names.concrete:              [names.concrete,         names.stone_brick][index],
            }
            recipes_to_modify = [
                names.rocket_silo, names.rocket_part, names.space_platform_foundation,
                names.space_platform_starter_pack, names.cargo_landing_pad, names.cargo_bay, names.asteroid_collector, names.crusher,
                names.thruster, names.chemical_plant, names.solar_panel,
            ]
            if self.options.require_self_sufficient_space_platform.value and self.starting_planet != names.vulcanus:
                recipes_to_modify.append(names.electric_furnace)
            recipes_to_shrink = {
                names.rocket_silo,
                names.space_platform_foundation,
            }

            if self.starting_planet == names.nauvis:
                pass
            elif self.starting_planet == names.vulcanus:
                # Sulfur is harder to get on vulcanus. Solid fuel requires only advanced-oil-processing.
                ingredient_replacements[names.rocket_fuel] = [names.solid_fuel, names.coal][index]
                # These are easy to get:
                del ingredient_replacements[names.steel_plate]
                del ingredient_replacements[names.concrete]
                # Automating tons of steel is actually fine,
                # (and you get assembling machine 2 unrandomized, so crafting speed is less of a concern).
                recipes_to_shrink.remove(names.space_platform_foundation)
            elif self.starting_planet == names.gleba:
                # Sulfur is not easier to get than rocket fuel on Gleba.
                ingredient_replacements[names.rocket_fuel] = [names.rocket_fuel, names.spoilage][index]
                # Otherwise, pretty similar to nauvis.
            elif self.starting_planet == names.fulgora:
                # A bunch of things are trivial on fulgora.
                del ingredient_replacements[names.processing_unit]
                del ingredient_replacements[names.advanced_circuit]
                del ingredient_replacements[names.low_density_structure]
                # Downgrade rocket fuel to trivial solid fuel.
                ingredient_replacements[names.rocket_fuel] = names.solid_fuel
                del ingredient_replacements[names.steel_plate]
                del ingredient_replacements[names.concrete]
            elif self.starting_planet == "all_simultaneously":
                pass
            else: assert False

            for recipe_name in recipes_to_modify:
                recipe_data = the_data["recipe"][recipe_name]
                made_any_change = False
                for ingredient_data in recipe_data["ingredients"]:
                    ingredient_name = ingredient_data["name"]
                    new_ingredient_name = ingredient_replacements.get(ingredient_name, ingredient_name)
                    if ingredient_name != new_ingredient_name:
                        ingredient_data["name"] = new_ingredient_name
                        made_any_change = True
                    if recipe_name in recipes_to_shrink:
                        ingredient_data["amount"] //= large_divisor
                        made_any_change = True
                if recipe_name in recipes_to_shrink:
                    made_any_change = True
                    recipe_data["energy_required"] /= small_divisor
                if made_any_change:
                    # Being minimal about this means avoiding the in-game display of which mods modified things (i think).
                    self.recipe_changes[recipe_name] = recipe_data
            the_data["rocket-silo"][names.rocket_silo]["rocket_parts_required"] //= large_divisor

            # Asteroid HP
            for asteroid_name in [
                names.small_metallic_asteroid,
                names.small_carbonic_asteroid,
                names.small_oxide_asteroid,
                names.medium_metallic_asteroid,
                names.medium_carbonic_asteroid,
                names.medium_oxide_asteroid,
            ]:
                self.asteroid_hp_changes[asteroid_name] = the_data["asteroid"][asteroid_name]["max_health"] / small_divisor

            # Technology
            if self.options.space_technology_level.current_key == "early_game" and self.starting_planet != names.vulcanus:
                # Thruster fuel requires chemical plant, so shortcut the recipe unlock if we wouldn't need it at this point anyway.
                self.technology_effect_additions[names.space_platform_thruster].append({
                    "type": "unlock-recipe",
                    "recipe": names.chemical_plant,
                })
        self.rocket_parts_per_rocket = the_data["rocket-silo"][names.rocket_silo]["rocket_parts_required"]
        self.technology_effect_additions[names.rocket_silo].append({
            # See https://github.com/thejoshwolfe/Archipelago/issues/9
            "type": "create-ghost-on-entity-death",
            "modifier": True,
        })

        # Balance for Gleba start.
        if self.starting_planet == names.gleba:
            if self.options.gleba_coal.current_key == "vanilla":
                pass
            elif self.options.gleba_coal.current_key == "buffed_ratio":
                # Change 6->1 to 3->2. With +50% from biochamber, it's a 1->1 ratio.
                recipe_data = the_data["recipe"][names.burnt_spoilage]
                recipe_data["ingredients"] = [{"type": "item", "name": "spoilage", "amount": 3}]
                recipe_data["results"] = [{"type": "item", "name": "carbon", "amount": 2}]
                self.recipe_changes[names.burnt_spoilage] = recipe_data
                # Change 5->1 to 5->5 (in chemical plant).
                recipe_data = the_data["recipe"][names.coal_synthesis]
                recipe_data["results"] = [{"type": "item", "name": "coal", "amount": 5}]
                self.recipe_changes[names.coal_synthesis] = recipe_data
            elif self.options.gleba_coal.current_key == "buffed_speed":
                # Change 12s -> 1s.
                recipe_data = the_data["recipe"][names.burnt_spoilage]
                recipe_data["energy_required"] = 1
                self.recipe_changes[names.burnt_spoilage] = recipe_data
            elif self.options.gleba_coal.current_key == "alternate_explosives":
                # This must be synchronized with data-updates.lua.
                recipe_data = json.loads(json.dumps(the_data["recipe"]["biosulfur"]))
                recipe_data["ingredients"] = [
                    dict(type="item",  name="sulfur",  amount=1),
                    dict(type="item",  name="bioflux", amount=1),
                    dict(type="fluid", name="water",   amount=10),
                ]
                recipe_data["results"] = [dict(type="item", name="explosives", amount=2)]
                the_data["recipe"]["explosives-from-bioflux"] = recipe_data
                the_data["technology"][names.explosives]["effects"].append(dict(type="unlock-recipe", recipe="explosives-from-bioflux"))

                recipe_data = json.loads(json.dumps(the_data["recipe"]["grenade"]))
                recipe_data["ingredients"] = [
                    dict(type="item", name="iron-plate", amount=5),
                    dict(type="item", name="explosives", amount=1),
                ]
                the_data["recipe"]["grenade-from-explosives"] = recipe_data
                the_data["technology"][names.military_2]["effects"].append({
                    "type": "unlock-recipe",
                    "recipe": "grenade-from-explosives",
                })
            else: assert False

        # Damage upgrades for medium asteroids.
        if self.options.require_gun_turret_upgrades.current_key == "easy":
            number_of_levels = 6
        elif self.options.require_gun_turret_upgrades.current_key == "medium":
            number_of_levels = 4
        elif self.options.require_gun_turret_upgrades.current_key == "hard":
            number_of_levels = 2
        elif self.options.require_gun_turret_upgrades.current_key == "none":
            number_of_levels = 0
        else: assert False
        self.medium_asteroid_upgrade_requirements = {
            *[
                names.physical_projectile_damage_1,
                names.physical_projectile_damage_2,
                names.physical_projectile_damage_3,
                names.physical_projectile_damage_4,
                names.physical_projectile_damage_5,
                names.physical_projectile_damage_6,
            ][:number_of_levels // small_divisor],
            *[
                names.weapon_shooting_speed_1,
                names.weapon_shooting_speed_2,
                names.weapon_shooting_speed_3,
                names.weapon_shooting_speed_4,
                names.weapon_shooting_speed_5,
                names.weapon_shooting_speed_6,
            ][:number_of_levels // small_divisor],
        }

        # Data analysis.
        self.factorio_data = FactorioData(the_data,
            self.technology_name_to_progressive_group_name,
            self.starting_planet,
            self.early_unrandomized_technologies,
            self.skipped_locations,
        )
        unrecognized_recipes = self.factorio_data.unrecognized_recipe_names(self.options.free_sample_excludes.value)
        if unrecognized_recipes:
            raise KeyError("free_sample_excludes contains unrecognized recipe names: " + repr(unrecognized_recipes))
        unrecognized_items = self.factorio_data.unrecognized_item_names(self.options.starting_items.value.keys())
        if unrecognized_items:
            raise KeyError("starting_items contains unrecognized item names: " + repr(unrecognized_items))
        if self.options.infinite_technologies.current_key == "shuffled":
            infinite_list = sorted(self.factorio_data.infinite_technology_names)
            target_list = list(infinite_list)
            self.random.shuffle(target_list)
            self.infinite_technology_shuffle = {src: dst for src, dst in zip(infinite_list, target_list)}
        else: assert self.options.infinite_technologies.current_key in ("removed", "vanilla")

        filler_weights = {
            names.artillery_shell_damage_1:           self.options.filler_artillery_shell_damage_weight.value,
            names.artillery_shell_range_1:            self.options.filler_artillery_shell_range_weight.value,
            names.artillery_shell_speed_1:            self.options.filler_artillery_shell_speed_weight.value,
            names.asteroid_productivity:              self.options.filler_asteroid_productivity_weight.value,
            names.electric_weapons_damage_4:          self.options.filler_electric_weapons_damage_weight.value,
            names.follower_robot_count_5:             self.options.filler_follower_robot_count_weight.value,
            names.health:                             self.options.filler_health_weight.value,
            names.laser_weapons_damage_7:             self.options.filler_laser_weapons_damage_weight.value,
            names.low_density_structure_productivity: self.options.filler_low_density_structure_productivity_weight.value,
            names.mining_productivity_3:              self.options.filler_mining_productivity_weight.value,
            names.physical_projectile_damage_7:       self.options.filler_physical_projectile_damage_weight.value,
            names.plastic_bar_productivity:           self.options.filler_plastic_bar_productivity_weight.value,
            names.processing_unit_productivity:       self.options.filler_processing_unit_productivity_weight.value,
            names.railgun_damage_1:                   self.options.filler_railgun_damage_weight.value,
            names.railgun_shooting_speed_1:           self.options.filler_railgun_shooting_speed_weight.value,
            names.refined_flammables_7:               self.options.filler_refined_flammables_weight.value,
            names.research_productivity:              self.options.filler_research_productivity_weight.value,
            names.rocket_fuel_productivity:           self.options.filler_rocket_fuel_productivity_weight.value,
            names.rocket_part_productivity:           self.options.filler_rocket_part_productivity_weight.value,
            infinite_scrap_recycling_productivity:    self.options.filler_scrap_recycling_productivity_weight.value,
            names.steel_plate_productivity:           self.options.filler_steel_plate_productivity_weight.value,
            names.stronger_explosives_7:              self.options.filler_stronger_explosives_weight.value,
            names.worker_robots_speed_7:              self.options.filler_worker_robots_speed_weight.value,
        }
        assert self.factorio_data.infinite_technology_names == filler_weights.keys(), "need to sync list of infinite technologies"
        assert all(
            name == self.progressive_technology_stacks[self.technology_name_to_progressive_group_name[name]][-1]
            for name in filler_weights.keys()
        ), "filler weight key needs to be the last item of a progressive stack"
        trap_filler_weights = {
            names.artillery_trap:            self.options.artillery_trap_weight.value,
            names.atomic_cliff_remover_trap: self.options.atomic_cliff_remover_trap_weight.value,
            names.atomic_rocket_trap:        self.options.atomic_rocket_trap_weight.value,
            names.attack_trap:               self.options.attack_trap_weight.value,
            names.cluster_grenade_trap:      self.options.cluster_grenade_trap_weight.value,
            names.evolution_trap:            self.options.evolution_trap_weight.value,
            names.grenade_trap:              self.options.grenade_trap_weight.value,
            names.inventory_spill_trap:      self.options.inventory_spill_trap_weight.value,
            names.teleport_trap:             self.options.teleport_trap_weight.value,
        }
        assert set(trap_names) == trap_filler_weights.keys(), "need to sync list of trap names"
        filler_weights.update(trap_filler_weights)
        filler_weights[""] = self.options.filler_nothing_weight.value

        if sum(filler_weights.values()) == 0:
            # If you ask for no filler, we'll give you nothing, which is filler.
            filler_weights[""] = 1
        self.filler_weights_argv = list(zip(*filler_weights.items()))

        self.empty_technologies = sorted(self.factorio_data.empty_technology_names)
        self.random.shuffle(self.empty_technologies)

        extra_location_count = self.options.filler_count.value + (
            - 4 # The builtin do-nothing technologies.
            + int(self.options.energy_link_technology.value)
            + 3*int(self.options.goal.current_key == "any_other_planet_science")
            - sum(self.options.start_inventory_from_pool.values())
        )
        assert extra_location_count < 1000, "didn't think this was possible"
        if extra_location_count > 0:
            location_candidates = sorted(self.factorio_data.get_location_dupe_candidates())
            self.location_to_duplicates = defaultdict(list)
            for i, dupe_target in enumerate(self.random.choices(location_candidates, k=extra_location_count)):
                self.location_to_duplicates[dupe_target].append("ap-{:03}_location".format(i))
        else:
            self.location_to_duplicates = {}

        # Generate logic.
        if self.options.energy_link.value:
            energy_link_bridge_recipe = energy_link_bridge_recipes[self.options.energy_link_recipe.current_key]
            energy_link_bridge_technology = bool(self.options.energy_link_technology.value)
            energy_link_bridge_required_for = {
                "early_game": names.logistic_science_pack,
                "mid_game": names.chemical_science_pack,
                "fulgora": names.electromagnetic_science_pack,
            }[self.options.energy_link_recipe.current_key]
            allow_energy_link_to_satisfy_logic = self.options.energy_link_satisfies_requirements
        else:
            energy_link_bridge_recipe = None
            energy_link_bridge_technology = False
            energy_link_bridge_required_for = None
            allow_energy_link_to_satisfy_logic = False

        self.logic_events, self.advancement_technologies, self.technology_props_lua = self.factorio_data.build_logic(
            bypass_technology_prerequisites=     self.options.technology_prerequisites.current_key == "removed",
            burner_mining_drill_is_good_enough=  not self.options.require_electric_mining_drill.value,
            inserter_balancing_is_good_enough=   not self.options.require_logistics.value,
            water_barrel_is_good_enough=         not self.options.require_ice_melting.value,
            launching_metal_is_good_enough=      not self.options.require_self_sufficient_space_platform.value,
            backwards_recycling_is_interesting=  self.starting_planet == names.fulgora,
            unbarreling_is_interesting=          False, # Full chaos recipe rando is not implemented.
            walls_to_destroy_medium_asteroids_is_good_enough= not self.options.require_gun_turret.value,
            small_electric_pole_is_good_enough=  not self.options.require_medium_electric_pole.value,
            wait_hours_for_fish_to_spoil=        not self.options.require_gleba_for_spoilage.value,
            storing_seeds_is_good_eough=         not self.options.require_seed_disposal,
            lightning_schmightning=              not self.options.require_lightning_rod.value,
            solar_panels_into_darkness=          not self.options.require_dark_power.value,
            slow_inserter_is_good_enough=        not self.options.require_fast_inserter.value,
            assembling_machine_1_is_good_enough= not self.options.require_assembling_machine_2.value,
            direct_pipes_is_good_enough=         not self.options.require_fluid_handling.value,
            hand_building_is_good_enough=        not self.options.require_construction_robots.value,
            belt_logistics_is_good_enough=       not self.options.require_logistic_robots.value,
            basic_asteroid_processing_is_good_enough= not self.options.require_asteroid_processing,
            nuclear_heating_is_good_enough=      not self.options.require_heating_tower,

            enemies_enabled=self.enemies_enabled,
            demolisher_killers=self.options.demolisher_killers.value,
            pentapod_killers=self.options.pentapod_killers.value,
            medium_asteroid_upgrade_requirements=self.medium_asteroid_upgrade_requirements,

            energy_link_bridge_recipe=energy_link_bridge_recipe,
            energy_link_bridge_technology=energy_link_bridge_technology,
            energy_link_bridge_required_for=energy_link_bridge_required_for,
            allow_energy_link_to_satisfy_logic=allow_energy_link_to_satisfy_logic,
        )

    def create_regions(self):
        """
        This implementation covers create_regions(), create_items(), and set_rules().
        """
        from .data import generated_names as names
        from .data.ap_data import (
            ap_item_names,
        )
        from .Logic import compile_expr
        player = self.player

        # Regions don't map well onto anything useful in Factorio, because all the AP Locations are globally unlocked research.
        # Even Space Age planets don't work as AP Regions, because the stuff you get there isn't Archipelago stuff
        # but rather items that help you globally unlock Archipelago stuff.
        # (And science packs aren't regions either, because you need combinations of science packs.)
        the_region = Region(self.origin_region_name, player, self.multiworld)
        self.multiworld.regions.append(the_region)

        def new_location(location_name, access_rule_fn):
            code = ap_location_name_to_id.get(location_name, None)
            location = FactorioLocation(player, location_name, code, the_region, access_rule_fn)
            the_region.locations.append(location)
            if code != None:
                self.locations.append(location)
            return location
        def new_event(location_name, item_name, access_rule_fn):
            location = new_location(location_name, access_rule_fn)
            event = self.create_item(item_name)
            location.place_locked_item(event)
        def lock_item(location, item):
            assert item != None
            location.place_locked_item(item)
            location.revealed = True

        unrandomized_technologies = set(self.early_unrandomized_technologies)
        lock_final_technology_name = None
        if self.options.goal.current_key in ("any_other_planet_science", "space_science"):
            victory_event = names.victory
        elif self.options.goal.current_key == "solar_system_edge":
            victory_event = "Reach solar-system-edge"
        elif self.options.goal.current_key == "solar_system_edge_11_science":
            victory_event = "Reach solar-system-edge"
            lock_final_technology_name = names.promethium_science_pack
        elif self.options.goal.current_key == "aquilo_orbit":
            victory_event = "Reach aquilo_orbit"
        elif self.options.goal.current_key == "aquilo_orbit_10_science":
            victory_event = "Reach aquilo_orbit"
            lock_final_technology_name = names.planet_discovery_aquilo
        else: assert False

        if lock_final_technology_name != None:
            # Lock the goal tech also.
            unrandomized_technologies.add(lock_final_technology_name)
        assert victory_event in self.logic_events, "event not found in logic: " + victory_event
        self.multiworld.completion_condition[player] = lambda state: state.has(victory_event, player)

        event_names = []
        location_names = []
        item_names = []
        for event_name in sorted(self.logic_events.keys()):
            if " " in event_name:
                # This is an abstract event.
                event_names.append(event_name)
            elif event_name.endswith("_location"):
                # This is a research objective location.
                location_names.append(event_name)
            else:
                # This is a receivable technology item.
                item_names.append(event_name)

        technology_name_to_location = {}
        for location_name in location_names:
            origin_technology_name = location_name[:-len("_location")]
            if origin_technology_name in self.skipped_locations:
                # Don't create a location for this. It's already obtained.
                continue
            access_rule_fn = compile_expr(self.logic_events[location_name])
            location = new_location(location_name, access_rule_fn)
            technology_name_to_location[origin_technology_name] = location
            for duplicate_name in self.location_to_duplicates.get(origin_technology_name, []):
                # Another one.
                new_location(duplicate_name, access_rule_fn)
        randomized_items = []
        for technology_name in item_names:
            # This is a receivable technology item.
            if technology_name in self.factorio_data.empty_technology_names:
                # Let filler fill in later.
                continue
            item_name = self.technology_name_to_progressive_group_name.get(technology_name, technology_name)
            item = self.create_item(item_name)
            # Where should it go?
            if technology_name in unrandomized_technologies or technology_name in self.factorio_data.infinite_technology_names:
                if technology_name in self.skipped_locations:
                    # It's already granted.
                    continue
                lock_item(technology_name_to_location[technology_name], item)
            elif item_name == names.victory:
                if self.options.goal.current_key == "space_science":
                    lock_item(technology_name_to_location[names.logistic_system], item)
                elif self.options.goal.current_key == "any_other_planet_science":
                    # We actually want 2 or 3 of these.
                    if self.starting_planet != names.vulcanus:
                        lock_item(technology_name_to_location[names.asteroid_reprocessing], self.create_item(names.victory))
                    if self.starting_planet != names.gleba:
                        lock_item(technology_name_to_location[names.carbon_fiber], self.create_item(names.victory))
                    if self.starting_planet != names.fulgora:
                        lock_item(technology_name_to_location[names.lightning_collector], self.create_item(names.victory))
                else:
                    pass # Don't create victory items for this goal.
            else:
                randomized_items.append(item)

        # Create filler items.
        empty_slots = sum(1 for location in self.locations if location.item == None)
        if empty_slots < len(randomized_items):
            assert False, "TODO: generate more locations"
        while len(randomized_items) < empty_slots:
            randomized_items.append(self.create_item(self.get_filler_item_name()))
        self.multiworld.itempool.extend(randomized_items)

        # Put these at the end of the spoiler log listing.
        for event_name in event_names:
            new_event(event_name, event_name, compile_expr(self.logic_events[event_name]))


    def generate_basic(self):
        if self.options.world_gen.current_key == "custom":
            map_basic_settings = self.options.world_gen_custom.value["basic"]
            if map_basic_settings.get("seed", None) is None: # allow seed 0
                map_basic_settings["seed"] = self.random.randint(0, 2 ** 32 - 1) # 32 bit uint

        start_location_hints: typing.Set[str] = self.options.start_location_hints.value
        for location in self.locations:
            if location.name in start_location_hints:
                location.revealed = True

    def collect_item(self, state, item, remove=False):
        # Convert a progressive technology name into what it would be at this state.
        try:
            stack = self.progressive_technology_stacks[item.name]
        except KeyError:
            # Normal item
            return super().collect_item(state, item, remove)
        # Progressive item
        if remove:
            # We're uncollecting an item during some backtracking in generation.
            # It will be collected again later.
            for actual_item in reversed(stack):
                if state.has(actual_item, item.player):
                    return actual_item
        else:
            for actual_item in stack:
                if not state.has(actual_item, item.player):
                    return actual_item
        return None

    def get_filler_item_name(self) -> str:
        [item_name] = self.random.choices(*self.filler_weights_argv)
        if item_name == "":
            # Use the next name in a (shuffled) rotation so you always see all 4 before any repeats.
            self.empty_technologies.append(self.empty_technologies.pop(0))
            item_name = self.empty_technologies[-1]
        return item_name

    def create_item(self, item_name: str) -> FactorioItem:
        from .data.ap_data import trap_names
        code = ap_item_name_to_id.get(item_name, None)
        if code == None or item_name in self.advancement_technologies:
            # Events are always advancement (that's the point.).
            classification = ItemClassification.progression
        elif item_name in self.empty_technologies:
            classification = ItemClassification.filler
        elif item_name in trap_names:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.useful
        return FactorioItem(item_name, classification, code, self.player)

def read_local_path(name: str) -> bytes:
    import pkgutil
    return pkgutil.get_data(__name__, name)

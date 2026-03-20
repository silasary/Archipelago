from __future__ import annotations

import typing

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
    logic_events: dict
    advancement_technologies: set[str]
    infinite_technology_shuffle: dict[str, str] | None = None
    empty_technologies: list[str]
    filler_weights_argv: tuple[list[str], list[int]]
    locations_to_duplicate: set[str]

    def __init__(self, world, player: int):
        self.locations = []
        super().__init__(world, player)

    def generate_output(self, output_directory: str) -> None:
        from .Mod import generate_mod
        generate_mod(
            player=self.player,
            player_name=self.player_name,
            world_locations=self.locations,
            options=self.options,
            multiworld=self.multiworld,
            logic_events=self.logic_events,
            progressive_technology_stacks=self.progressive_technology_stacks,
            technology_name_to_progressive_group_name=self.technology_name_to_progressive_group_name,
            infinite_technology_shuffle=self.infinite_technology_shuffle,
            technology_props_lua=self.technology_props_lua,
            output_directory=output_directory,
        )

    def generate_early(self) -> None:
        import json
        the_data = json.loads(read_local_path("data/ap-dump.json"))
        from .FactorioData import FactorioData
        from .data.ap_data import (
            trap_names, energy_link_bridge_recipes,
            small_progressive_groups, large_progressive_groups,
        )
        from .data import generated_names as names

        self.progressive_technology_stacks = {
            "only_related": small_progressive_groups,
            "large_groups": large_progressive_groups,
        }[self.options.progressive_technologies.current_key]
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

        self.factorio_data = FactorioData(the_data, self.technology_name_to_progressive_group_name)
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
            names.scrap_recycling_productivity:       self.options.filler_scrap_recycling_productivity_weight.value,
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

        assert self.factorio_data.empty_technology_names == {
            names.laser,
            names.flammables,
            names.biter_egg_handling,
            names.modules,
        }, "we have assumptions in __init__.py about the set of empty technologies"
        self.empty_technologies = sorted(self.factorio_data.empty_technology_names)
        self.random.shuffle(self.empty_technologies)

        extra_location_count = self.options.filler_count.value + (
            - 4 # The builtin do-nothing technologies.
            + int(self.options.energy_link_technology.value)
            + 3*int(self.options.goal.current_key == "any_other_planet_science")
            - sum(self.options.start_inventory_from_pool.values())
        )
        if extra_location_count > 0:
            other_location_names = [name for name in ap_location_name_to_id.keys() if name.endswith("_other_location")]
            chosen_other_locations = self.random.sample(other_location_names, extra_location_count)
            self.locations_to_duplicate = {name.replace("_other_location", "_location") for name in chosen_other_locations}
        else:
            self.locations_to_duplicate = set()

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
            launching_metal_is_good_enough=      not self.options.require_electric_furnace.value,
            backwards_recycling_is_interesting=  False, # Fulgora start is not implemented.
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

            any_other_planet_science=self.options.goal.current_key == "any_other_planet_science",

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
            unrandomized_technologies as base_unrandomized_technologies
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

        unrandomized_technologies = set(base_unrandomized_technologies)
        if self.options.goal.current_key == "any_other_planet_science":
            victory_events = (
                names.vulcanus_victory,
                names.gleba_victory,
                names.fulgora_victory,
            )
            assert all(event_name in self.logic_events for event_name in victory_events), "goal techs not in logic"
            self.multiworld.completion_condition[player] = lambda state: state.has_any(victory_events, player)
        else:
            if self.options.goal.current_key == "solar_system_edge":
                victory_event = "Reach solar-system-edge"
                final_technology_name = names.promethium_science_pack
            elif self.options.goal.current_key == "aquilo_orbit":
                victory_event = "Reach aquilo_orbit"
                final_technology_name = names.planet_discovery_aquilo
            elif self.options.goal.current_key == "space_platform":
                victory_event = "Can build space platforms"
                final_technology_name = names.rocket_silo
            else: assert False
            assert victory_event in self.logic_events, "event not found in logic: " + victory_event
            self.multiworld.completion_condition[player] = lambda state: state.has(victory_event, player)

            if not self.options.shuffle_final_technology.value:
                # Lock the goal tech also.
                unrandomized_technologies.add(final_technology_name)

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
            access_rule_fn = compile_expr(self.logic_events[location_name])
            location = new_location(location_name, access_rule_fn)
            origin_technology_name = location_name[:-len("_location")]
            technology_name_to_location[origin_technology_name] = location
            if location_name in self.locations_to_duplicate:
                # Another one.
                new_location(origin_technology_name + "_other_location", access_rule_fn)
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
                lock_item(technology_name_to_location[technology_name], item)
            elif item_name == names.vulcanus_victory:
                lock_item(technology_name_to_location[names.asteroid_reprocessing], item)
            elif item_name == names.gleba_victory:
                lock_item(technology_name_to_location[names.carbon_fiber], item)
            elif item_name == names.fulgora_victory:
                lock_item(technology_name_to_location[names.lightning_collector], item)
            else:
                randomized_items.append(item)

        # Create filler items.
        empty_slots = sum(1 for location in self.locations if location.item == None)
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

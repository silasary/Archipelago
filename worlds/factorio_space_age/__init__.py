from __future__ import annotations

import typing

from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld

from .settings import FactorioSettings
from .Options import FactorioOptions, option_groups
from .data.Logic import (
    LogicOption,
    compile_expr, instantiate_options,
)
from .data.generated1 import (
    ap_item_name_to_id, ap_location_name_to_id,
)
# NOTE: avoid importing .data.generated2 and 3 until someone actually instantiates a Factorio apworld.
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
    required_client_version = (0, 6, 0)

    web = FactorioWeb()
    settings: typing.ClassVar[FactorioSettings]
    options_dataclass = FactorioOptions
    options: FactorioOptions

    item_name_to_id = ap_item_name_to_id
    location_name_to_id = ap_location_name_to_id
    item_name_groups = {
        # TODO: progressive item groups here?
    }

    locations: list[FactorioLocation]
    logic_events: dict

    def __init__(self, world, player: int):
        self.locations = []
        super().__init__(world, player)

    def generate_output(self, output_directory: str) -> None:
        from .Mod import generate_mod
        generate_mod(
            player=self.player,
            player_name=self.player_name,
            world_zip_path=self.zip_path,
            world_locations=self.locations,
            options=self.options,
            multiworld=self.multiworld,
            logic_events=self.logic_events,
            output_directory=output_directory,
        )

    def generate_early(self) -> None:
        # if max < min, then swap max and min
        from .data.generated2 import all_recipe_names, all_item_names
        unrecognized_recipes = self.options.free_sample_excludes.value - all_recipe_names
        if unrecognized_recipes:
            raise KeyError("free_sample_excludes contains unrecognized recipe names: " + repr(unrecognized_recipes))
        unrecognized_items = self.options.starting_items.value.keys() - all_item_names
        if unrecognized_items:
            raise KeyError("starting_items contains unrecognized item names: " + repr(unrecognized_items))
        if self.options.energy_link_technology.value:
            raise NotImplementedError("TODO: energy_link_technology must be 'false'")

    def create_regions(self):
        """
        This implementation covers create_regions(), create_items(), and set_rules().
        TODO: create traps.
        """
        from .data.generated2 import (
            infinite_technologies,
            technology_name_to_location_name,
            technology_name_to_progressive_group_name, progressive_group_name_to_category,
            never_inline_events,
        )
        from .data.generated3 import raw_logic_events
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

        if self.options.goal.current_key == "solar_system_edge":
            victory_event_name = "Reach solar-system-edge"
        elif self.options.goal.current_key == "aquilo_orbit":
            victory_event_name = "Reach aquilo_orbit"
        elif self.options.goal.current_key == "space_platform":
            victory_event_name = "Can build space platforms"
        else: raise NotImplementedError("TODO: goal not supported: " + self.options.goal.current_key)
        self.multiworld.completion_condition[player] = lambda state: state.has(victory_event_name, player)

        el_enabled = self.options.energy_link.value
        el_recipe = self.options.energy_link_recipe.current_key
        el_logic = self.options.require_energy_link.value
        self.logic_events = instantiate_options(raw_logic_events, never_inline_events, {
            LogicOption.bypass_technology_prerequisites:     self.options.technology_prerequisites.current_key == "removed",
            LogicOption.burner_mining_drill_is_good_enough:  not self.options.require_electric_mining_drill.value,
            LogicOption.inserter_balancing_is_good_enough:   not self.options.require_logistics.value,
            LogicOption.water_barrel_is_good_enough:         not self.options.require_ice_melting.value,
            LogicOption.launching_metal_is_good_enough:      not self.options.require_electric_furnace.value,
            LogicOption.backwards_recycling_is_interesting:  False, # Fulgora start is not implemented.
            LogicOption.walls_to_destroy_medium_asteroids_is_good_enough: not self.options.require_gun_turret.value,
            LogicOption.wait_hours_for_fish_to_spoil:        not self.options.require_gleba_for_spoilage.value,
            LogicOption.lightning_schmightning:              not self.options.require_lightning_rod.value,
            LogicOption.solar_panels_into_darkness:          not self.options.require_dark_power.value,
            LogicOption.slow_inserter_is_good_enough:        not self.options.require_fast_inserter.value,
            LogicOption.assembling_machine_1_is_good_enough: not self.options.require_assembling_machine_2.value,
            LogicOption.direct_pipes_is_good_enough:         not self.options.require_fluid_handling.value,
            LogicOption.hand_building_is_good_enough:        not self.options.require_construction_robots.value,
            LogicOption.belt_logistics_is_good_enough:       not self.options.require_logistic_robots.value,

            LogicOption.energy_link_recipe_early_game:       el_enabled and el_recipe == "early_game",
            LogicOption.energy_link_recipe_mid_game:         el_enabled and el_recipe == "mid_game",
            LogicOption.energy_link_recipe_fulgora:          el_enabled and el_recipe == "fulgora",
            LogicOption.energy_link_unlocked_from_the_start: el_enabled and not self.options.energy_link_technology.value,
            LogicOption.playing_without_energy_link_early_game_is_good_enough: not (el_enabled and el_logic and el_recipe == "early_game"),
            LogicOption.playing_without_energy_link_mid_game_is_good_enough:   not (el_enabled and el_logic and el_recipe == "mid_game"),
            LogicOption.playing_without_energy_link_fulgora_is_good_enough:    not (el_enabled and el_logic and el_recipe == "fulgora"),
        })

        enabled_progressive_categories = {
            "off": (),
            "bonuses": ("bonuses",),
            "all": ("bonuses", "recipes"),
        }[self.options.progressive_technologies.current_key]

        found_victory_event = False
        for event_name, expr in sorted(self.logic_events.items(), key=lambda kv: (" " in kv[0], kv[0])):
            try:
                event_type, sub_name = event_name.split(" ", 1)
            except ValueError:
                event_type, sub_name = "Technology", event_name
            if event_type == "Technology":
                # This is a proper item and corresponding location.
                # TODO: shuffle infinite techs.
                locked = sub_name in (
                    # These are critical at the start.
                    # The algorithm might swap things around, but starting with these vanilla location/item locks
                    # prevents a naive shuffle from failing to find a path out of early game.
                    "steam-power",
                    "electronics",
                    "automation-science-pack",
                    "automation",
                )
                if sub_name in infinite_technologies:
                    if self.options.infinite_technologies.current_key == "removed":
                        continue
                    else:
                        raise NotImplementedError("infinite_technologies must be set to 'removed' for now")
                progressive_group_name = technology_name_to_progressive_group_name.get(sub_name, None)
                if progressive_group_name != None and progressive_group_name_to_category[progressive_group_name] in enabled_progressive_categories:
                    item_name = progressive_group_name
                else:
                    item_name = sub_name
                location = new_location(technology_name_to_location_name[sub_name], compile_expr(expr))
                item = self.create_item(item_name)
                if locked:
                    location.place_locked_item(item)
                    location.revealed = True
                else:
                    self.multiworld.itempool.append(item)
            else:
                # This is an abstract event.
                event = new_event(event_name, event_name, compile_expr(expr))
            if event_name == victory_event_name:
                found_victory_event = True
        assert found_victory_event, "event not found in logic: " + victory_event_name


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
        from .data.generated2 import progressive_technology_stacks
        # Convert a progressive technology name into what it would be at this state.
        try:
            stack = progressive_technology_stacks[item.name]
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
        # TODO: option for infinite techs to be filler items instead of nothing technologies.
        from .data.generated2 import empty_technologies
        empty_technologies_list = sorted(empty_technologies)
        return self.random.choice(empty_technologies_list)

    def create_item(self, item_name: str) -> FactorioItem:
        from .data.generated2 import advancement_technologies, empty_technologies
        code = ap_item_name_to_id.get(item_name, None)
        if code == None or item_name in advancement_technologies:
            # Events are always advancement (that's the point.).
            classification = ItemClassification.progression
        elif item_name in empty_technologies:
            classification = ItemClassification.filler
        else:
            classification = ItemClassification.useful
        return FactorioItem(item_name, classification, code, self.player)


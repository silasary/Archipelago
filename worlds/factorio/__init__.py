from __future__ import annotations

import typing

from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld

from .settings import FactorioSettings
from .Options import FactorioOptions, option_groups
from .Technologies import (
    compile_expr, logic_events,
    ap_item_name_to_id, ap_location_name_to_id,
    advancement_technologies, never_give_free_samples_from_recipes,
    progressive_technology_stacks,
)


def _register_client():
    from worlds.LauncherComponents import Component, components, Type, launch as launch_component
    def launch_client(*args: str):
        from .Client import launch
        launch_component(launch, name="Factorio Client", args=args)
    components.append(Component("Factorio Client", func=launch_client, component_type=Type.CLIENT))
_register_client()


class FactorioWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Factorio software on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Berserker, Farrak Kilhn"]
    )]
    option_groups = option_groups


class FactorioItem(Item):
    game = "Factorio"

class FactorioLocation(Location):
    game = "Factorio"

    def __init__(self, player: int, name: str, address: int, parent: Region,
        access_rule_fn: typing.Callable[[dict[str, int]], bool],
    ):
        super().__init__(player, name, address, parent)
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
    game = "Factorio"
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

    def __init__(self, world, player: int):
        super().__init__(world, player)

    def generate_output(self, output_directory: str) -> None:
        from .Mod import generate_mod
        generate_mod(
            player=self.player,
            player_name=self.player_name,
            world_zip_path=self.zip_path,
            world_locations=[], # TODO
            options=self.options,
            multiworld=self.multiworld,
            output_directory=output_directory,
        )

    def generate_early(self) -> None:
        # if max < min, then swap max and min
        if self.options.max_tech_cost < self.options.min_tech_cost:
            self.options.min_tech_cost.value, self.options.max_tech_cost.value = \
                self.options.max_tech_cost.value, self.options.min_tech_cost.value

    def create_regions(self):
        """
        This implementation covers create_regions(), create_items(), and set_rules().
        TODO: create traps.
        """
        player = self.player
        random = self.random

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
            return location
        def new_item(item_name, classification, add_to_pool=True):
            code = ap_item_name_to_id.get(item_name, None)
            item = FactorioItem(item_name, classification, code, player)
            if code != None and add_to_pool:
                self.multiworld.itempool.append(item)
            return item
        def new_event(location_name, item_name, access_rule_fn):
            location = new_location(location_name, access_rule_fn)
            event = new_item(item_name, ItemClassification.progression)
            location.place_locked_item(event)

        victory_event_name = "Reach solar-system-edge"
        self.multiworld.completion_condition[player] = lambda state: state.has(victory_event_name, player)

        found_victory_event = False
        for event_name, expr in sorted(logic_events.items(), key=lambda kv: (" " in kv[0], kv[0])):
            try:
                event_type, sub_name = event_name.split(" ", 1)
            except ValueError:
                event_type, sub_name = "Technology", event_name
            if event_type == "Technology":
                # This is a proper item and corresponding location.
                locked = sub_name in (
                    # These are critical at the start.
                    # The algorithm might swap things around, but starting with these vanilla location/item locks
                    # prevents a naive shuffle from failing to find a path out of early game.
                    "steam-power",
                    "elecetronics",
                    "automation-science-pack",
                    "automation",
                )
                location = new_location(sub_name, compile_expr(expr))
                item = new_item(sub_name,
                    ItemClassification.progression if event_name in advancement_technologies else ItemClassification.useful,
                    add_to_pool=not locked,
                )
                if locked:
                    location.place_locked_item(item)
            else:
                # This is an abstract event.
                event = new_event(event_name, event_name, compile_expr(expr))
                if event_name == victory_event_name:
                    found_victory_event = True
        assert found_victory_event, "event not found in logic: " + victory_event_name


    def generate_basic(self):
        map_basic_settings = self.options.world_gen.value["basic"]
        if map_basic_settings.get("seed", None) is None:  # allow seed 0
            # 32 bit uint
            map_basic_settings["seed"] = self.random.randint(0, 2 ** 32 - 1)

        start_location_hints: typing.Set[str] = self.options.start_location_hints.value
        # TODO: implement start_location_hints

    def collect_item(self, state, item, remove=False):
        # Convert a progressive technology name into what it would be at this state.
        try:
            stack = progressive_technology_stacks[item.name]
        except KeyError:
            # Normal item
            return super().collect_item(state, item, remove)
        # Progressive item
        if remove:
            # If we're culling items out of the multiworld, lose the last progressive item we have.
            for actual_item in reversed(stack):
                if state.has(actual_item, item.player):
                    return actual_item
            # If we didn't find anything, don't remove anything.
            return None
        else:
            for actual_item in stack:
                if not state.has(actual_item, item.player):
                    break
            # If we didn't find any we're missing, grant the last one again. It's probably an infinite tech.
            return actual_item

    def get_filler_item_name(self) -> str:
        import pdb; pdb.set_trace()
        raise NotImplementedError
    def create_item(self, name: str) -> FactorioItem:
        import pdb; pdb.set_trace()
        raise NotImplementedError


from typing import List
import typing

import settings
from BaseClasses import ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import FFXIITMItem, FFXIITMItemData, event_item_table, get_items_by_category, item_table
from .Locations import FFXIITMLocation, location_table, get_locations_by_category
from .Options import FF12TMOptions
from .Regions import create_regions
from .Rules import set_rules
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
import random


class FFXIITMSettings(settings.Group):
    class InstallScript(settings.Bool):
        """Automatically install/update the lua script when you launch the client.  If false, you will need to manually install the script from data/lua."""

    install_script: typing.Union[InstallScript, bool] = True

def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="FFXIITM Client")


components.append(Component("FFXIITM Client", "FFXIITMClient", func=launch_client, component_type=Type.CLIENT))

class FFXIITMWeb(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Final Fantasy XII Trial Mode Randomizer software on your computer. This guide covers single-player, "
        "multiworld, and related software.",
        "English",
        "ffxiitm_en.md",
        "ffxiitm/en",
        ["Gicu"]
    )]

class FFXIITMWorld(World):
    """
    Final Fantasy XII is JRPG developed by Square Enix.  The Trial Mode involves 100 consecutive battles, each more challenging than the last.
    """
    game = "Final Fantasy XII Trial Mode"
    options_dataclass = FF12TMOptions
    options: FF12TMOptions
    topology_present = False
    data_version = 4
    required_client_version = (0, 3, 5)
    web = FFXIITMWeb()
    settings: typing.ClassVar[FFXIITMSettings]

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    item_name_groups = {
        # "Item": {name for name, data in item_table.items() if data.category == "Item"},
        "Equipment": {name for name, data in item_table.items() if data.category == "Equipment"},
        "Magick": {name for name, data in item_table.items() if data.category == "Magick"},
        "Technick": {name for name, data in item_table.items() if data.category == "Technick"},
        "Mist": {name for name, data in item_table.items() if data.category == "Mist"},
    }

    # TODO: Replace calls to this function with "options-dict", once that PR is completed and merged.
    def get_setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        return {
            "trial_victory": self.options.trial_victory.value,
        }

    def create_items(self):
        victory_location_name = random.sample(list(get_locations_by_category("Trial " + str(self.options.trial_victory.value).rjust(3, "0")).keys()),1)[0]
        self.multiworld.get_location(victory_location_name, self.player).place_locked_item(self.create_item("Victory"))
        item_pool: List[FFXIITMItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        equipment = list(self.item_name_groups["Equipment"])
        magick = list(self.item_name_groups["Magick"])
        technick = list(self.item_name_groups["Technick"])
        mist = list(self.item_name_groups["Mist"])

        self.random.shuffle(equipment)
        self.random.shuffle(magick)
        self.random.shuffle(technick)
        self.random.shuffle(mist)

        progressive = [n for n, i in item_table.items()
                       if i.classification in [ItemClassification.progression, ItemClassification.progression_skip_balancing]
                       and i.category not in ["Victory", "Guest"]
                      ]

        for i in range(1, self.options.trial_victory.value // 10):
            # progressive.append(equipment.pop())
            # progressive.append(magick.pop())
            # progressive.append(technick.pop())
            # if i // 2 == 0:
            progressive.append(mist.pop())

        progressive_items_left_to_be_added = len(progressive)
        useful = [n for n, i in item_table.items() if n not in progressive and i.classification == ItemClassification.useful]
        self.random.shuffle(useful)

        for name in progressive:
            if len(item_pool) >= total_locations:
                raise Exception("Not enough locations for progressive items.")
            data = item_table[name]
            quantity = data.max_quantity
            items = [self.create_item(name) for _ in range(0, quantity)]
            for item in items:
                item.classification = ItemClassification.progression
            item_pool += items
            progressive_items_left_to_be_added = progressive_items_left_to_be_added - quantity

        for name in useful:
            if len(item_pool) >= total_locations:
                break
            data = item_table[name]
            quantity = data.max_quantity
            items = [self.create_item(name) for _ in range(0, quantity)]
            item_pool += items

        # Fill any empty locations with filler items.
        while len(item_pool) < total_locations:
            item_name = self.get_filler_item_name()
            item_pool.append(self.create_item(item_name))

        # print(f"World contains {len(item_pool)} items. {len(progressive)} progression items, {len(useful)} useful items, and {total_locations} locations.")
        self.multiworld.itempool += item_pool

    def get_filler_item_name(self) -> str:
        fillers = {}
        disclude = []
        fillers.update(get_items_by_category("Item", disclude))
        weights = [data.weight for data in fillers.values()]
        return self.multiworld.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]

    def create_item(self, name: str) -> FFXIITMItem:
        data = item_table[name]
        return FFXIITMItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> FFXIITMItem:
        data = event_item_table[name]
        return FFXIITMItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self, self.player, self.options.trial_victory.value)

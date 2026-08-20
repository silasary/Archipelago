from typing import Any, Iterable, List
import typing

import settings
from BaseClasses import ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import FFXIITMItem, FFXIITMItemData, event_item_table, get_items_by_category, item_table, weapons_by_tier, armors_by_tier, hats_by_tier, espers, flattened_weapons_by_tier, flattened_armors_by_tier, flattened_hats_by_tier
from .Locations import FFXIITMLocation, location_table, get_locations_by_category
from .Options import FF12TMOptions
from .Regions import create_regions
from .Rules import set_rules
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
import random


class FFXIITMSettings(settings.Group):
    class InstallScript(settings.Bool):
        """
        Automatically install/update the lua script when you launch the client.
        If false, you will need to manually install the script from data/lua.

        Note: This setting only works if the game is installed in the default location.
        """

    install_script: typing.Union[InstallScript, bool] = True

def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="FFXIITM Client")


components.append(Component("Final Fantasy XII Trial Mode Client",  func=launch_client, component_type=Type.CLIENT))

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

    ut_can_gen_without_yaml = True


    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    item_name_groups = {
        "Item": {name for name, data in item_table.items() if data.category == "Item"},
        "Equipment": {name for name, data in item_table.items() if data.category == "Equipment"},
        "Magick": {name for name, data in item_table.items() if data.category == "Magick"},
        "Technick": {name for name, data in item_table.items() if data.category == "Technick"},
        "Mist": {name for name, data in item_table.items() if data.category == "Mist"},
    }
    for tier, weapons in flattened_weapons_by_tier.items():
        item_name_groups[f'T{tier} weapons'] = weapons
    for tier, armors in flattened_armors_by_tier.items():
        item_name_groups[f'T{tier} armors'] = armors
    for tier, hats in flattened_hats_by_tier.items():
        item_name_groups[f'T{tier} hats'] = hats

    item_name_groups['Accessories'] = [name for name,data in item_table.items() if data.subcategory == 'Accessory']
    item_name_groups['Shields'] = [name for name,data in item_table.items() if data.subcategory == 'Shield']



    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # returns slot data to be used in UT regen
        return slot_data

    def generate_early(self):
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                self.passthrough = self.multiworld.re_gen_passthrough[self.game]

                for key, value in self.passthrough.items():
                    if hasattr(self.options, key):
                        opt = getattr(self.options, key)
                        opt.value = opt.from_any(value).value

    def fill_slot_data(self) -> dict:
        return {
            "trial_victory": self.options.trial_victory.value,
        }

    def create_items(self):
        goal_floor = self.options.trial_victory.value
        # print(goal_floor)
        if goal_floor == 98: goal_floor = 97 #there are no AP locations on floor 98
        victory_location_name = random.sample(list(get_locations_by_category("Trial " + str(goal_floor).rjust(3, "0")).keys()),1)[0]
        self.multiworld.get_location(victory_location_name, self.player).place_locked_item(self.create_item("Victory"))
        item_pool: List[FFXIITMItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        inventory = set(self.options.start_inventory.keys())

        def remove_starting_inventory(items: Iterable[str]) -> List[str]:
            return list(filter(lambda x: x not in inventory, items))

        def extract_items(item_list, name_list, count=1):
            # note: this will mutate item_list
            matched_indeces = []
            for i, item in enumerate(item_list):
                if item in name_list:
                    matched_indeces.append(i)
                    if len(matched_indeces) >= count: break
            # matched_indeces should be in ascending order so it should be safe to pop them in reverse order
            output = []
            for i in matched_indeces[::-1]:
                output.append(item_list.pop(i))
            return output

        # equipment = remove_starting_inventory(self.item_name_groups["Equipment"])
        # magick = remove_starting_inventory(self.item_name_groups["Magick"])
        # technick = remove_starting_inventory(self.item_name_groups["Technick"])
        # mist = remove_starting_inventory(self.item_name_groups["Mist"])

        all_items = remove_starting_inventory({name for name, data in item_table.items() if data.category in ["Mist", "Magick", "Equipment", "Technick"]}) #excludes filler
        progressives = []
        extract_items(all_items, ["Steal", "Poach"],count=2) #remove steal and poach from the item pool
        self.random.shuffle(all_items)

        secret_equipment = extract_items(all_items, ["Seitengrat", "Great Trango","Gendarme", "Wyrmhero Blade"], count=4) #remove secret weapons from pool
        if self.options.secret_equipment and goal_floor >= 5: progressives += secret_equipment #add them to pool

        if goal_floor >= 10:
            progressives += extract_items(all_items, ["Second Job"])
            progressives += extract_items(all_items, espers,count=3+goal_floor//10)
        if (goal_floor >= 5) and (goal_floor < 10): #for small worlds, guarantee at least 3 weapons
            weapon_types = list(weapons_by_tier[3].keys()).copy()
            self.random.shuffle(weapon_types)
            for i in range(3):
                progressives += extract_items(all_items, weapons_by_tier[3][weapon_types[i]], count=1)
        if goal_floor >= 9:
            for type, equipment_list in weapons_by_tier[3].items():
                progressives += extract_items(all_items, equipment_list, count=1)
            for type, equipment_list in armors_by_tier[3].items():
                progressives += extract_items(all_items, equipment_list, count=2)
            for type, equipment_list in hats_by_tier[3].items():
                progressives += extract_items(all_items, equipment_list, count=2)
        if goal_floor >= 15:
            for type, equipment_list in weapons_by_tier[3].items():
                progressives += extract_items(all_items, equipment_list, count=1)
        if goal_floor >= 20:
            progressives += extract_items(all_items, ["Fira", "Thundara", "Blizzara", "Darkra", "Bio", "Aeroga"], count=100)
        if goal_floor >= 30:
            for type, equipment_list in weapons_by_tier[4].items():
                progressives += extract_items(all_items, equipment_list, count=1)
            progressives += extract_items(all_items, ["Cura", "Curaga", "Esuna", "Esunaga", "Raise", "Telekinesis", "Embroidered Tippet", "Golden Amulet", "Rose Corsage"], count=100)
        if goal_floor >= 50:
            for type, equipment_list in weapons_by_tier[4].items():
                progressives += extract_items(all_items, equipment_list, count=1)
            for type, equipment_list in armors_by_tier[4].items():
                progressives += extract_items(all_items, equipment_list, count=2)
            for type, equipment_list in hats_by_tier[4].items():
                progressives += extract_items(all_items, equipment_list, count=2)
            progressives += extract_items(all_items, ["Berserk", "Cat-ear Hood", "Dispel", "Dispelga", "Berserk", "Berserk Bracers", "Protect", "Protectga", "Shell", "Shellga", "Curaja"], count=100)
            progressives += extract_items(all_items, ["Ardor", "Scathe", "Firaga", "Thundaga", "Blizzaga", "Darkga", "Scourge", "Flare",  "Toxify"], count = 100)
            progressives += extract_items(all_items, ["Reverse", "Arise", "Renew", "Reflect", "Reflega", "Hastega", "Bravery", "Faith", "Syphon", "Bubble", "Nihopalaoa", "Genji Gloves", "Opal Ring", "Ribbon", "Embroidered Tippet", "Golden Amulet", "Demon Shield", "Zodiac Escutcheon"], count=100)
        if goal_floor >= 60:
            for type, equipment_list in weapons_by_tier[5].items():
                progressives += extract_items(all_items, equipment_list, count=1)
            for type, equipment_list in armors_by_tier[5].items():
                progressives += extract_items(all_items, equipment_list, count=2)
            for type, equipment_list in hats_by_tier[5].items():
                progressives += extract_items(all_items, equipment_list, count=2)

        if goal_floor >= 80:
            for type, equipment_list in weapons_by_tier[5].items():
                progressives += extract_items(all_items, equipment_list, count=2)
            for type, equipment_list in armors_by_tier[5].items():
                progressives += extract_items(all_items, equipment_list, count=1)
            for type, equipment_list in hats_by_tier[5].items():
                progressives += extract_items(all_items, equipment_list, count=1)
            progressives += extract_items(all_items, ["Wither", "Addle", "Expose", "Shear", "Cleanse", "Zodiark", "Yagyu Darkblade"], count=100)


        progressive_items_left_to_be_added = len(progressives)
        # useful = [n for n, i in item_table.items() if n not in progressive and i.classification == ItemClassification.useful and n not in inventory]
        # self.random.shuffle(useful)

        for name in progressives:
            if len(item_pool) >= total_locations:
                raise Exception("Not enough locations for progressive items.")
            data = item_table[name]
            quantity = data.max_quantity
            items = [self.create_item(name) for _ in range(0, quantity)]
            for item in items:
                item.classification = ItemClassification.progression
            item_pool += items
            progressive_items_left_to_be_added = progressive_items_left_to_be_added - quantity

        for name in all_items:
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

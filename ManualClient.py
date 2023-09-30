from __future__ import annotations
from worlds.AutoWorld import AutoWorldRegister
from collections import Counter
import json
from typing import Optional
from worlds._manual.Rules import infix_to_postfix, evaluate_postfix

import asyncio, re

import ModuleUpdate
ModuleUpdate.update()
from worlds.AutoWorld import World

import Utils

if __name__ == "__main__":
    Utils.init_logging("ManualClient", exception_logger="Client")

from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop
from BaseClasses import Item, ItemClassification, Location, Region, CollectionState, MultiWorld

class ManualClientCommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True

class ManualCollectionState:
    def __init__(self, slot: int, world: World):
        self.prog_items = Counter()
        self.reachable_regions = {player: set() for player in [slot]}
        self.blocked_connections = {player: set() for player in [slot]}
        self.stale = {player: True for player in [slot]}
        self.locations_checked = set()
        self.world = world

    def collect(self, item: Item, event: bool = False, location: Optional[Location] = None) -> bool:
        if location:
            self.locations_checked.add(location)

        changed = False

        if item.advancement or event:
            self.prog_items[item.name, item.player] += 1
            changed = True

        self.stale[item.player] = True

        # if changed and not event:
        #     self.sweep_for_events()

        return changed

    def can_reach(self, requires: str, location_name: str) -> bool:
        if not requires:
            return True
        if not isinstance(requires, str):
            pass
        requires_list = requires

        # parse user written statement into list of each item
        for item in re.findall(r'\|[^|]+\|', requires):
            require_type = 'item'

            if '|@' in item:
                require_type = 'category'

            item_base = item
            item = item.replace('|', '').replace('@', '')

            item_parts = item.split(":")
            item_name = item
            item_count = 1

            if len(item_parts) > 1:
                item_name = item_parts[0]
                item_count = int(item_parts[1])

            total = 0

            if require_type == 'category':
                # todo: implement this
                pass
                # category_items = [item["name"] for item in base.item_name_to_item.values() if "category" in item and item_name in item["category"]]

                # for category_item in category_items:
                #     total += state.item_count(category_item, player)

                #     if total >= item_count:
                #         requires_list = requires_list.replace(item_base, "1")
            elif require_type == 'item':
                total = self.prog_items[item_name]

                if total >= item_count:
                    requires_list = requires_list.replace(item_base, "1")

            if total <= item_count:
                requires_list = requires_list.replace(item_base, "0")

        requires_list = re.sub(r'\s?\bAND\b\s?', '&', requires_list, 0, re.IGNORECASE)
        requires_list = re.sub(r'\s?\bOR\b\s?', '|', requires_list, 0, re.IGNORECASE)

        requires_string = infix_to_postfix("".join(requires_list), location_name)
        return (evaluate_postfix(requires_string, location_name))
        return False

class ManualContext(CommonContext):
    command_processor: int = ManualClientCommandProcessor
    game = "not set" # this is changed in server_auth below based on user input
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password, game, player_name) -> None:
        super(ManualContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.game = game
        self.username = player_name

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ManualContext, self).server_auth(password_requested)

        if "Manual_" not in self.ui.game_bar_text.text:
            raise Exception("The Manual client can only be used for Manual games.")
        
        self.game = self.ui.game_bar_text.text

        self.location_names_to_id = dict([(value, key) for key, value in self.location_names.items()])

        # if the item name has a number after it, remove it
        for item_id, name in enumerate(self.item_names):
            if not isinstance(name, str):
                continue

            name_parts = name.split(":")

            if len(name_parts) > 1:
                self.item_names.pop(name)
                self.item_names[name_parts[0]] = item_id

        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(ManualContext, self).connection_closed()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(ManualContext, self).shutdown()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.ui.build_tracker_and_locations_table()
        elif cmd in {"ReceivedItems"}:
            self.ui.update_tracker_and_locations_table(update_highlights=True)
        elif cmd in {"RoomUpdate"}:
            self.ui.update_tracker_and_locations_table(update_highlights=False)

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager
        
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.layout import Layout
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.textinput import TextInput
        from kivy.uix.tabbedpanel import TabbedPanelItem
        from kivy.uix.treeview import TreeView, TreeViewNode, TreeViewLabel
        from kivy.clock import Clock
        from kivy.core.window import Window

        class TrackerAndLocationsLayout(GridLayout):
            pass
    
        class TrackerLayoutScrollable(ScrollView):
            pass

        class LocationsLayoutScrollable(ScrollView):
            pass

        class TreeViewButton(Button, TreeViewNode):
            pass

        class TreeViewScrollView(ScrollView, TreeViewNode):
            pass

        class ManualManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("Manual", "Manual"),
            ]
            base_title = "Archipelago Manual Client"
            listed_items = {"(no category)": []}
            item_categories = ["(no category)"]
            listed_locations = {"(no category)": []}
            location_categories = ["(no category)"]

            active_item_accordion = 0
            active_location_accordion = 0

            ctx: ManualContext

            def __init__(self, ctx):
                super().__init__(ctx)

            def build(self) -> Layout: 
                super(ManualManager, self).build()

                self.manual_game_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=30)

                game_bar_label = Label(text="Manual Game ID", size=(150, 30), size_hint_y=None, size_hint_x=None)
                self.manual_game_layout.add_widget(game_bar_label)
                self.game_bar_text = TextInput(text=self.ctx.game or "Manual_{\"game\" from game.json}_{\"player\" from game.json}",
                                                size_hint_y=None, height=30, multiline=False, write_tab=False)          
                self.manual_game_layout.add_widget(self.game_bar_text)

                self.grid.add_widget(self.manual_game_layout, 3)

                panel = TabbedPanelItem(text="Tracker and Locations", size_hint_y = 1)
                self.tracker_and_locations_panel = panel.content = TrackerAndLocationsLayout(cols = 2)

                self.tabs.add_widget(panel)

                self.build_tracker_and_locations_table()

                return self.container
            
            def clear_lists(self):
                self.listed_items = {"(no category)": []}
                self.item_categories = ["(no category)"]
                self.listed_locations = {"(no category)": []}
                self.location_categories = ["(no category)"]
                
            def set_active_item_accordion(self, instance):
                index = 0

                for widget in self.children:
                    if widget == instance:
                        self.active_item_accordion = index
                        return
                    
                    index += 1
                
            def set_active_location_accordion(self, instance):
                index = 0

                for widget in self.children:
                    if widget == instance:
                        self.active_item_accordion = index
                        return
                    
                    index += 1

            def build_tracker_and_locations_table(self):
                self.tracker_and_locations_panel.clear_widgets()

                if not self.ctx.server or not self.ctx.auth:
                    self.tracker_and_locations_panel.add_widget(
                                Label(text="Waiting for connection...", size_hint_y=None, height=50, outline_width=1))
                    return

                self.clear_lists()

                # seed all category names to start
                for item in AutoWorldRegister.world_types[self.ctx.game].item_name_to_item.values():
                    if "category" in item and len(item["category"]) > 0:
                        for category in item["category"]:
                            if category not in self.item_categories:
                                self.item_categories.append(category)

                            if category not in self.listed_items:
                                self.listed_items[category] = []


                # Items are not received on connect, so don't bother attempting to work with received items here
                
                if not hasattr(AutoWorldRegister.world_types[self.ctx.game], 'location_name_to_location'):
                    raise Exception("The apworld for %s is too outdated for this client. Please update it." % (self.ctx.game))
                
                for location_id in self.ctx.missing_locations:
                    # holy nesting, wow
                    location_name = self.ctx.location_names[location_id]
                    location = AutoWorldRegister.world_types[self.ctx.game].location_name_to_location[location_name]

                    if not location:
                        continue
                
                    if "category" in location and len(location["category"]) > 0:
                        for category in location["category"]:
                            if category not in self.location_categories:
                                self.location_categories.append(category)

                            if category not in self.listed_locations:
                                self.listed_locations[category] = []

                            self.listed_locations[category].append(location_id)
                    else: # leave it in the generic category
                        self.listed_locations["(no category)"].append(location_id)

                victory_location = AutoWorldRegister.world_types[self.ctx.game].location_name_to_location["__Manual Game Complete__"]

                if "category" in victory_location and len(victory_location["category"]) > 0:
                    for category in victory_location["category"]:
                        if category not in self.location_categories:
                            self.location_categories.append(category)

                        if category not in self.listed_locations:
                            self.listed_locations[category] = []

                items_length = len(self.ctx.items_received)
                tracker_panel_scrollable = TrackerLayoutScrollable()
                tracker_panel = TreeView(root_options=dict(text="Items Received (%d)" % (items_length)))
                
                # Since items_received is not available on connect, don't bother building item labels here
                for item_category in sorted(self.listed_items.keys()):
                    category_tree = tracker_panel.add_node(
                        TreeViewLabel(text = "%s (%s)" % (item_category, len(self.listed_items[item_category])))
                    )

                    category_scroll = tracker_panel.add_node(TreeViewScrollView(size_hint=(1, None), size=(Window.width / 2, 250)), category_tree)
                    category_layout = GridLayout(cols=1, size_hint_y=None)
                    category_layout.bind(minimum_height = category_layout.setter('height'))
                    category_scroll.add_widget(category_layout)

                locations_length = len(self.ctx.missing_locations)
                locations_panel_scrollable = LocationsLayoutScrollable()
                locations_panel = TreeView(root_options=dict(text="Remaining Locations (%d)" % (locations_length + 1)))
                
                if not hasattr(AutoWorldRegister.world_types[self.ctx.game], 'location_name_to_location'):
                    raise Exception("The apworld for %s is too outdated for this client. Please update it." % (self.ctx.game))

                for location_category in sorted(self.listed_locations.keys()):
                    victory_location_data = AutoWorldRegister.world_types[self.ctx.game].location_name_to_location["__Manual Game Complete__"]
                    locations_in_category = len(self.listed_locations[location_category])

                    if ("category" in victory_location_data and location_category in victory_location_data["category"]) or \
                        ("category" not in victory_location_data and location_category == "(no category)"):
                        locations_in_category += 1

                    category_tree = locations_panel.add_node(
                        TreeViewLabel(text = "%s (%s)" % (location_category, locations_in_category))
                    )

                    category_scroll = locations_panel.add_node(TreeViewScrollView(size_hint=(1, None), size=(Window.width / 2, 250)), category_tree)
                    category_layout = GridLayout(cols=1, size_hint_y=None)
                    category_layout.bind(minimum_height = category_layout.setter('height'))
                    category_scroll.add_widget(category_layout)

                    for location_id in self.listed_locations[location_category]:
                        location_button = TreeViewButton(text=self.ctx.location_names[location_id], size_hint=(None, None), height=30, width=400)
                        location_button.bind(on_press=lambda *args, loc_id=location_id: self.location_button_callback(loc_id, *args))
                        category_layout.add_widget(location_button)

                    # if this is the category that Victory is in, display the Victory button
                    # if ("category" in victory_location_data and location_category in victory_location_data["category"]) or \
                    #     ("category" not in victory_location_data and location_category == "(no category)"):
                    if (location_category == "(no category)"):

                        # Add the Victory location to be marked at any point, which is why locations length has 1 added to it above
                        location_button = TreeViewButton(text="VICTORY! (seed finished)", size_hint=(None, None), height=30, width=400)
                        location_button.bind(on_press=self.victory_button_callback)
                        category_layout.add_widget(location_button)
                    
                tracker_panel_scrollable.add_widget(tracker_panel)
                locations_panel_scrollable.add_widget(locations_panel)
                self.tracker_and_locations_panel.add_widget(tracker_panel_scrollable)
                self.tracker_and_locations_panel.add_widget(locations_panel_scrollable)

            def update_tracker_and_locations_table(self, update_highlights=False):
                items_length = len(self.ctx.items_received)
                locations_length = len(self.ctx.missing_locations)

                # This doesn't work, but was an attempt at getting the current logic state
                # to be able to mark location buttons as reachable or not.
                # Continued below in the location-specific area (also commented out).
                #
                #
                # multiworld = MultiWorld(10000)
                # multiworld.add_group("Player" + str(self.ctx.slot), self.ctx.game, [self.ctx.slot])

                collection_state = ManualCollectionState(self.ctx.slot, AutoWorldRegister.world_types[self.ctx.game])

                for network_item in self.ctx.items_received:
                    item_name = self.ctx.item_names[network_item.item]
                    item = AutoWorldRegister.world_types[self.ctx.game].item_name_to_item[item_name]

                    item_classification = ItemClassification.filler

                    if "trap" in item and item["trap"]:
                        item_classification = ItemClassification.trap

                    if "useful" in item and item["useful"]:
                        item_classification = ItemClassification.useful

                    if "progression" in item and item["progression"]:
                        item_classification = ItemClassification.progression

                    item_object = Item(item["name"], item_classification, item["id"], self.ctx.slot)
                    collection_state.collect(item_object)

                for _, child in enumerate(self.tracker_and_locations_panel.children):
                    #
                    # Structure of items:
                    # TrackerLayoutScrollable -> TreeView -> TreeViewLabel, TreeViewScrollView -> GridLayout -> Label
                    #        item tracker     -> category -> category label, category scroll   -> label col  -> item
                    #
                    if type(child) is TrackerLayoutScrollable:
                        treeview = child.children[0] # TreeView
                        treeview_nodes = treeview.iterate_all_nodes()

                        items_received_label = next(treeview_nodes) # always the first node
                        items_received_label.text = "Items Received (%s)" % (items_length)

                        # loop for each category in listed items and get the label + scrollview
                        for x in range(0, len(self.item_categories)):
                            category_label = next(treeview_nodes) # TreeViewLabel for category
                            category_scrollview = next(treeview_nodes) # TreeViewScrollView for housing category's grid layout

                            old_category_text = category_label.text

                            if type(category_label) is TreeViewLabel and type(category_scrollview) is TreeViewScrollView:
                                category_grid = category_scrollview.children[0] # GridLayout

                                category_name = re.sub("\s\(\d+\)$", "", category_label.text)
                                category_count = 0
                                category_unique_name_count = 0

                                # Label (for existing item listings)
                                for item in category_grid.children:
                                     if type(item) is Label:
                                        # Get the item name from the item Label, minus quantity, then do a lookup for count
                                        old_item_text = item.text
                                        item_name = re.sub("\s\(\d+\)$", "", item.text)
                                        item_data = AutoWorldRegister.world_types[self.ctx.game].item_name_to_item[item_name]
                                        item_count = len(list(i for i in self.ctx.items_received if i.item == item_data["id"]))

                                        # Update the label quantity
                                        item.text="%s (%s)" % (item_name, item_count)

                                        if update_highlights:
                                            item.bold = True if old_item_text != item.text else False

                                        if item_count > 0:
                                            category_count += item_count
                                            category_unique_name_count += 1

                                # Label (for new item listings)
                                for network_item in self.ctx.items_received:
                                    item_name = self.ctx.item_names[network_item.item]
                                    item_data = AutoWorldRegister.world_types[self.ctx.game].item_name_to_item[item_name]

                                    if "category" not in item_data or not item_data["category"]:
                                        item_data["category"] = ["(no category)"]

                                    if category_name in item_data["category"] and network_item.item not in self.listed_items[category_name]:
                                        item_name_parts = self.ctx.item_names[network_item.item].split(":")
                                        item_count = len(list(i for i in self.ctx.items_received if i.item == network_item.item))
                                        item_text = Label(text="%s (%s)" % (item_name_parts[0], item_count),
                                                    size_hint=(None, None), height=30, width=400, bold=True)

                                        category_grid.add_widget(item_text)
                                        self.listed_items[category_name].append(network_item.item)

                                        category_count += item_count
                                        category_unique_name_count += 1

                            scrollview_height = 30 * category_unique_name_count

                            if scrollview_height > 250:
                                scrollview_height = 250

                            if scrollview_height < 10:
                                scrollview_height = 50

                            category_name = re.sub("\s\(\d+\)$", "", category_label.text)
                            category_label.text = "%s (%s)" % (category_name, category_count)

                            if update_highlights:
                                category_label.bold = True if old_category_text != category_label.text else False

                            category_scrollview.size=(Window.width / 2, scrollview_height)

                    #
                    # Structure of locations:
                    # LocationsLayoutScrollable -> TreeView -> TreeViewLabel, TreeViewScrollView -> GridLayout -> Button
                    #      location tracker     -> category -> category label, category scroll   -> label col  -> location
                    #
                    if type(child) is LocationsLayoutScrollable:
                        treeview = child.children[0] # TreeView
                        treeview_nodes = treeview.iterate_all_nodes()

                        locations_remaining_label = next(treeview_nodes) # always the first node
                        locations_remaining_label.text = "Remaining Locations (%d)" % (locations_length)

                        # loop for each category in listed items and get the label + scrollview
                        for x in range(0, len(self.location_categories)):
                            category_label = next(treeview_nodes) # TreeViewLabel for category
                            category_scrollview = next(treeview_nodes) # TreeViewScrollView for housing category's grid layout

                            if type(category_label) is TreeViewLabel and type(category_scrollview) is TreeViewScrollView:
                                category_grid = category_scrollview.children[0] # GridLayout

                                category_name = re.sub("\s\(\d+\)$", "", category_label.text)
                                category_count = 0

                                buttons_to_remove = []

                                # Label (for existing item listings)
                                for location_button in category_grid.children:
                                    if type(location_button) is TreeViewButton:
                                        # should only be true for the victory location button, which has different text
                                        if location_button.text not in AutoWorldRegister.world_types[self.ctx.game].location_name_to_location:
                                            category_count += 1

                                            continue

                                        location = AutoWorldRegister.world_types[self.ctx.game].location_name_to_location[location_button.text]

                                        # This is part of an attempt to check a logic state to see if location buttons should be highlighted or not.
                                        # The rest of the logic is about 100 lines above (commented out), but it doesn't work.
                                        #
                                        #
                                        # region_object = None

                                        # if location["region"]:
                                        #     region_object = Region(location["region"], self.ctx.slot, None)

                                        # location_object = Location(self.ctx.slot, location["name"], location["id"], region_object)

                                        try:
                                            if collection_state.can_reach(location['requires'], location_button.text):
                                                # logger.info("Location %s can be reached currently." % (location["name"]))
                                                location_button.background_color = (1, 2, 1, 1)
                                            else:
                                                # logger.info("Location %s can **NOT** be reached currently!" % (location["name"]))
                                                location_button.background_color = (2, 1, 1, 1)
                                        except KeyError as e:
                                            logger.error("Couldn't process requires", exc_info=e)
                                            location_button.background_color = (1, 1, 1, 1)

                                        # if ("victory" not in location or not location["victory"]) and location["id"] not in self.ctx.missing_locations:
                                        #     import logging

                                        #     logging.info("location button being removed: " + location_button.text)
                                        #     buttons_to_remove.append(location_button)
                                        #     continue

                                        category_count += 1

                                scrollview_height = 30 * category_count

                                if scrollview_height > 250:
                                    scrollview_height = 250

                                if scrollview_height < 10:
                                    scrollview_height = 50

                                category_name = re.sub("\s\(\d+\)$", "", category_label.text)
                                category_label.text = "%s (%s)" % (category_name, category_count)
                                checks = [location_button.background_color == (1, 2, 1, 1) for location_button in category_grid.children if type(location_button) is TreeViewButton]
                                if all(checks):
                                    category_label.outline_color = (1, 2, 1, 1)
                                elif all([not check for check in checks]):
                                    category_label.outline_color = (2, 1, 1, 1)
                                else:
                                    category_label.outline_color = (1, 1, 1, 1)
                                category_scrollview.size=(Window.width / 2, scrollview_height)
            def location_button_callback(self, location_id, button):
                if button.text not in self.ctx.location_names_to_id:
                    raise Exception("Locations were not loaded correctly. Please reconnect your client.")

                # location_id = self.ctx.location_names_to_id[button.text]
                
                if location_id:
                    self.ctx.locations_checked.append(location_id)
                    self.ctx.syncing = True
                    button.parent.remove_widget(button)
                    
                    # message = [{"cmd": 'LocationChecks', "locations": [location_id]}]
                    # self.ctx.send_msgs(message)

            def victory_button_callback(self, button):
                self.ctx.items_received.append("__Victory__")
                self.ctx.syncing = True

        self.ui = ManualManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

async def game_watcher(ctx: ManualContext):
    while not ctx.exit_event.is_set():
        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        sending = []
        victory = ("__Victory__" in ctx.items_received)
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def read_apmanual_file(apmanual_file):
    from base64 import b64decode

    with open(apmanual_file, 'r') as f:
        return json.loads(b64decode(f.read()))


if __name__ == '__main__':
    async def main(args):
        config_file = {}
        if args.apmanual_file:
            config_file = read_apmanual_file(args.apmanual_file)
        ctx = ManualContext(args.connect, args.password, config_file.get("game"), config_file.get("player_name"))
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="ManualProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Manual Client, for operating a Manual game in Archipelago.")
    parser.add_argument('apmanual_file', default="", type=str, nargs="?",
                        help='Path to an APMANUAL file')

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()

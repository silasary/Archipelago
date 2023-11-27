import asyncio
import logging
import traceback
import typing
from CommonClient import CommonContext, gui_enabled, get_base_parser, server_loop,ClientCommandProcessor
import os
import time
from typing import Dict, Optional
from BaseClasses import Region,Location

from BaseClasses import CollectionState,MultiWorld
from Options import StartInventoryPool
from settings import get_settings
from Utils import __version__, output_path
from worlds import AutoWorld
from worlds.tracker import TrackerWorld

from Generate import main as GMain

#webserver imports
import urllib.parse

logger = logging.getLogger("Client")

DEBUG = False
ITEMS_HANDLING = 0b111




class TrackerCommandProcessor(ClientCommandProcessor):

    def _cmd_update(self):
        """Print the Updated Accessable Location set"""
        #self.ctx.tracker_page.content.data = new_data = []
        updateTracker(self.ctx)


class TrackerGameContext(CommonContext):
    from kvui import GameManager
    game = ""
    httpServer_task: typing.Optional["asyncio.Task[None]"] = None
    tags = CommonContext.tags|{"Tracker"}
    command_processor = TrackerCommandProcessor
    tracker_page = None
    watcher_task = None

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.items_handling = ITEMS_HANDLING
        self.locations_checked = []
        self.datapackage = []
        self.multiworld:MultiWorld = None
        self.player_id = None

    def build_gui(self,manager : GameManager):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.tabbedpanel import TabbedPanelItem
        from kivy.uix.recycleview import RecycleView


        class TrackerLayout(BoxLayout):
            pass

        class TrackerView(RecycleView):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.data = []
                self.data.append({"text":"Tracker Initializing"})
            
            def resetData(self):
                self.data.clear()

            def addLine(self, line:str):
                self.data.append({"text":line})

        tracker_page = TabbedPanelItem(text="Tracker Page")
        
        try:
            tracker = TrackerLayout(orientation="horizontal")
            tracker_view = TrackerView()
            tracker.add_widget(tracker_view)
            self.tracker_page = tracker_view
            tracker_page.content = tracker
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
        manager.tabs.add_widget(tracker_page)
        

    def run_gui(self):
        from kvui import GameManager

        class TrackerManager(GameManager):
            logging_pairs = [
                ("Client","Archipelago")
            ]
            base_title = "Archipelago Tracker Client"


            def build(self):
                container = super().build()
                self.tabs.do_default_tab = True
                self.tabs.current_tab.height = 40
                self.tabs.tab_height = 40
                self.ctx.build_gui(self)
                
                return container


        self.ui = TrackerManager(self)
        self.load_kv()
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
        return self

    def load_kv(self):
        from kivy.lang import Builder
        import pkgutil

        data = pkgutil.get_data(TrackerWorld.__module__, "Tracker.kv").decode()
        Builder.load_string(data)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TrackerGameContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            player_ids = [i for i,n in self.multiworld.player_name.items() if n==self.username]
            if len(player_ids) < 1:
                print("Player's Yaml not in tracker's list")
                return
            self.player_id = player_ids[0] #should only really ever be one match
            updateTracker(self)
            self.watcher_task = asyncio.create_task(game_watcher(self), name="GameWatcher")
        elif cmd == 'RoomUpdate':
            updateTracker(self)
    
    def run_generator(self):
        try:
            GMain(None, self.TMain)
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(tb)

    def TMain(self, args, seed=None, baked_server_options: Optional[Dict[str, object]] = None):
        
        if not baked_server_options:
            baked_server_options = get_settings().server_options.as_dict()
        assert isinstance(baked_server_options, dict)
        if args.outputpath:
            os.makedirs(args.outputpath, exist_ok=True)
            output_path.cached_path = args.outputpath

        start = time.perf_counter()
        # initialize the multiworld
        multiworld = MultiWorld(args.multi)

        logger = logging.getLogger()
        multiworld.set_seed(seed, args.race, str(args.outputname) if args.outputname else None)
        multiworld.plando_options = args.plando_options

        multiworld.shuffle = args.shuffle.copy()
        multiworld.logic = args.logic.copy()
        multiworld.mode = args.mode.copy()
        multiworld.difficulty = args.difficulty.copy()
        multiworld.item_functionality = args.item_functionality.copy()
        multiworld.timer = args.timer.copy()
        multiworld.goal = args.goal.copy()
        multiworld.boss_shuffle = args.shufflebosses.copy()
        multiworld.enemy_health = args.enemy_health.copy()
        multiworld.enemy_damage = args.enemy_damage.copy()
        multiworld.beemizer_total_chance = args.beemizer_total_chance.copy()
        multiworld.beemizer_trap_chance = args.beemizer_trap_chance.copy()
        multiworld.countdown_start_time = args.countdown_start_time.copy()
        multiworld.red_clock_time = args.red_clock_time.copy()
        multiworld.blue_clock_time = args.blue_clock_time.copy()
        multiworld.green_clock_time = args.green_clock_time.copy()
        multiworld.dungeon_counters = args.dungeon_counters.copy()
        multiworld.triforce_pieces_available = args.triforce_pieces_available.copy()
        multiworld.triforce_pieces_required = args.triforce_pieces_required.copy()
        multiworld.shop_shuffle = args.shop_shuffle.copy()
        multiworld.shuffle_prizes = args.shuffle_prizes.copy()
        multiworld.sprite_pool = args.sprite_pool.copy()
        multiworld.dark_room_logic = args.dark_room_logic.copy()
        multiworld.plando_items = args.plando_items.copy()
        multiworld.plando_texts = args.plando_texts.copy()
        multiworld.plando_connections = args.plando_connections.copy()
        multiworld.required_medallions = args.required_medallions.copy()
        multiworld.game = args.game.copy()
        multiworld.player_name = args.name.copy()
        multiworld.sprite = args.sprite.copy()
        multiworld.glitch_triforce = args.glitch_triforce  # This is enabled/disabled globally, no per player option.

        multiworld.set_options(args)
        multiworld.set_item_links()
        multiworld.state = CollectionState(multiworld)
        logger.info('Archipelago Version %s  -  Seed: %s\n', __version__, multiworld.seed)

        logger.info(f"Found {len(AutoWorld.AutoWorldRegister.world_types)} World Types:")
        longest_name = max(len(text) for text in AutoWorld.AutoWorldRegister.world_types)

        max_item = 0
        max_location = 0
        for cls in AutoWorld.AutoWorldRegister.world_types.values():
            if cls.item_id_to_name:
                max_item = max(max_item, max(cls.item_id_to_name))
                max_location = max(max_location, max(cls.location_id_to_name))

        item_digits = len(str(max_item))
        location_digits = len(str(max_location))
        item_count = len(str(max(len(cls.item_names) for cls in AutoWorld.AutoWorldRegister.world_types.values())))
        location_count = len(str(max(len(cls.location_names) for cls in AutoWorld.AutoWorldRegister.world_types.values())))
        del max_item, max_location

        for name, cls in AutoWorld.AutoWorldRegister.world_types.items():
            if not cls.hidden and len(cls.item_names) > 0:
                logger.info(f" {name:{longest_name}}: {len(cls.item_names):{item_count}} "
                            f"Items (IDs: {min(cls.item_id_to_name):{item_digits}} - "
                            f"{max(cls.item_id_to_name):{item_digits}}) | "
                            f"{len(cls.location_names):{location_count}} "
                            f"Locations (IDs: {min(cls.location_id_to_name):{location_digits}} - "
                            f"{max(cls.location_id_to_name):{location_digits}})")

        del item_digits, location_digits, item_count, location_count

        AutoWorld.call_stage(multiworld, "assert_generate")

        AutoWorld.call_all(multiworld, "generate_early")

        logger.info('')

        for player in multiworld.player_ids:
            for item_name, count in multiworld.worlds[player].options.start_inventory.value.items():
                for _ in range(count):
                    multiworld.push_precollected(multiworld.create_item(item_name, player))

            for item_name, count in multiworld.start_inventory_from_pool.setdefault(player, StartInventoryPool({})).value.items():
                for _ in range(count):
                    multiworld.push_precollected(multiworld.create_item(item_name, player))

        logger.info('Creating World.')
        AutoWorld.call_all(multiworld, "create_regions")

        logger.info('Creating Items.')
        AutoWorld.call_all(multiworld, "create_items")

        logger.info('Calculating Access Rules.')

        for player in multiworld.player_ids:
            # items can't be both local and non-local, prefer local
            multiworld.worlds[player].options.non_local_items.value -= multiworld.worlds[player].options.local_items.value
            multiworld.worlds[player].options.non_local_items.value -= set(multiworld.local_early_items[player])

        AutoWorld.call_all(multiworld, "set_rules")


        self.multiworld = multiworld
        return

def updateTracker(ctx: TrackerGameContext):
    if ctx.player_id == None:
        logger.error("Player YAML not installed")
        ctx.tracker_page.resetData()
        ctx.tracker_page.addLine("Player YAML not installed")
        return

    state = CollectionState(ctx.multiworld)
    state.sweep_for_events(location for location in ctx.multiworld.get_locations() if not location.address)

    for item in ctx.items_received:
        state.collect(ctx.multiworld.create_item(ctx.multiworld.worlds[ctx.player_id].item_id_to_name[item[0]],ctx.player_id))

    state.sweep_for_events(location for location in ctx.multiworld.get_locations() if not location.address)
    
    ctx.tracker_page.resetData()
    for temp_loc in ctx.multiworld.get_reachable_locations(state,ctx.player_id):
        if temp_loc.address == None:
            continue
        if (temp_loc.address in ctx.missing_locations):
            #logger.info("YES rechable (" + temp_loc.name + ")")
            ctx.tracker_page.addLine( temp_loc.name )
    ctx.tracker_page.refresh_from_data()

async def game_watcher(ctx: TrackerGameContext) -> None:
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
        except asyncio.TimeoutError:
            continue
        ctx.watcher_event.clear()
        try:
            updateTracker(ctx)
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)


async def main(args):
 
    ctx = TrackerGameContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    ctx.run_generator()

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():

    parser = get_base_parser(description="Gameless Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args()

    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)


    asyncio.run(main(args))
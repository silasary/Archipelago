from __future__ import annotations

import asyncio
import json
import os

import Utils
from CommonClient import ClientCommandProcessor, gui_enabled, get_base_parser, CommonContext, server_loop, logger, ClientStatus
from MultiServer import mark_raw

# Gets the sims 4 mods folder
if Utils.is_windows:
    # https://stackoverflow.com/questions/6227590/finding-the-users-my-documents-path/30924555#
    import ctypes.wintypes

    CSIDL_PERSONAL = 5  # My Documents
    SHGFP_TYPE_CURRENT = 0  # Get current, not default value

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    Path = os.path.expanduser(rf'{buf.value}\Electronic Arts\The Sims 4\Mods\mod_data\s4ap')
else:
    Path = os.path.expanduser(r'~\Documents\Electronic Arts\The Sims 4\Mods\mod_data\s4ap')


# reads and prints json files
import os
import json


def print_json(obj: object, name: str, ctx: SimsContext):
    full_path = os.path.join(Path, name)
    if not os.path.exists(Path):
        ctx.gui_error(title="Sims 4 files not found.",
                      text=f"Could not find sims 4 mod files, make sure you installed the mod correctly and have ran sims 4.")
    else:
        with open(full_path, 'w') as f:
            json.dump(obj, f)

mtime = None


def load_json(name):
    global mtime
    full_path = os.path.join(Path, name)
    if os.path.isfile(full_path):
        next_mtime = os.path.getmtime(full_path)
        if mtime != next_mtime:
            mtime = next_mtime
            try:
                with open(full_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return None
        else:
            return None
    else:
        return None


class SimsCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    @mark_raw
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True
        print_json(False, 'sync.json')

    @mark_raw
    def _cmd_set_path(self, sims_4_mods_path: str = ''):
        """Set the file path to the Sims 4 mods folder manually (if automatic detection fails)"""
        p = sims_4_mods_path
        global Path
        if p == '':
            self.output('no path inputed')
        elif os.path.exists(os.path.join(p, 'mod_data', 's4ap')):
            self.output('Sims 4 mods folder found')
            Path = p
        else:
            self.ctx.gui_error(title='Sims 4 mods folder not found',
                               text=f'Make sure the file path you inputed is correct.')
            self.output(
                f'Could not find mod_data folder\nif the path you inputed is correct make sure you have enabled script mods in the sims 4 and run the game \nPath: {p}')


class SimsContext(CommonContext):
    game = 'The Sims 4'
    command_processor = SimsCommandProcessor
    items_handling = 0b111
    want_slot_data = True

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.syncing = False
        self.goal = None

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class S4Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago The Sims 4 Client"

        self.ui = S4Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.goal = args["slot_data"]["goal"]
            payload = {
                'cmd': "Connected",
                'host': self.server_address.split(':')[1].replace('//', ''),
                'port': self.server_address.split(':')[2],
                'name': self.slot_info[self.slot].name,
                'seed_name': self.seed_name,
            }
            print_json(payload, 'connection_status.json', self)


        elif cmd == "RoomInfo":
            self.seed_name = args['seed_name']

        elif cmd == "ReceivedItems":
            payload = {
                'cmd': 'ReceivedItems',
                'items': [self.item_names.lookup_in_game(item.item) for item in args['items']],
                'item_ids': [item.item for item in args["items"]],
                'locations': [self.location_names.lookup_in_game(location.location) for location in args['items']],
                'players': [self.player_names[player.player] for player in args["items"]],
                'index': args["index"]
            }
            print_json(payload, 'items.json', ctx=self)

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()


async def game_watcher(ctx: SimsContext):
    while not ctx.exit_event.is_set():
        if ctx.syncing:
            sync_msg = [{'cmd': 'Sync'}]
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        if (ctx.server and ctx.slot) is not None:
            json_data = load_json('locations_cached.json')
            if json_data is not None:
                if "Locations" in json_data and json_data["Locations"] is not None and json_data["Seed"] == ctx.seed_name:
                    locations_to_remove = []
                    for data in json_data["Locations"]:
                        for location_id in ctx.missing_locations:
                            location_current_name = ctx.location_names.lookup_in_game(location_id)
                            if location_current_name == data:
                                if ctx.goal == data.split("(", 1)[0].strip().replace(" ", "_").lower() and not ctx.finished_game:
                                    await SimsContext.send_msgs(ctx, [
                                        {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                                    ctx.finished_game = True
                                await SimsContext.send_msgs(ctx,
                                                            [{"cmd": "LocationChecks", "locations": [location_id]}])
                                locations_to_remove.append(data)
                                break
                    for loc in locations_to_remove:
                        json_data["Locations"].remove(loc)
                        print_json(json_data, 'locations_cached.json', ctx)
            json_data = load_json('sync.json')
            if json_data is not None:
                if json_data:
                    ctx.syncing = True
                    print_json(False, 'sync.json', ctx)
        await asyncio.sleep(0.5)


def main():
    async def _main():
        parser = get_base_parser(description="The Sims 4 Client, for text interfacing.")
        args, rest = parser.parse_known_args()

        ctx = SimsContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await watcher_task
        await ctx.shutdown()

    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    main()

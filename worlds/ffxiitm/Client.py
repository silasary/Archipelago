from __future__ import annotations
import hashlib
import logging
import os
import pkgutil
import sys
import asyncio
import shutil

import ModuleUpdate
ModuleUpdate.update()

import Utils

check_num = 0

if __name__ == "__main__":
    Utils.init_logging("FFXIITMClient", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop


def check_stdin() -> None:
    if Utils.is_windows and sys.stdin:
        print("WARNING: Console input is not routed reliably on Windows, use the GUI instead.")

class FFXIITMClientCommandProcessor(ClientCommandProcessor):
    def _cmd_test(self):
        """Test"""
        self.output(f"Test")


class FFXIITMContext(CommonContext):
    command_processor: int = FFXIITMClientCommandProcessor
    game = "Final Fantasy XII Trial Mode"
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password):
        super(FFXIITMContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        if "localappdata" in os.environ:
            self.game_communication_path = os.path.expandvars(r"%localappdata%/FFXIITM")
        else:
            self.game_communication_path = os.path.expandvars(r"$HOME/FFXIITM")
        if not os.path.exists(self.game_communication_path):
            os.makedirs(self.game_communication_path)
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root+"/"+file)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(FFXIITMContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(FFXIITMContext, self).connection_closed()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root + "/" + file)

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(FFXIITMContext, self).shutdown()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root+"/"+file)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            for ss in self.checked_locations:
                filename = f"send{ss}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.close()
        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                for item in args['items']:
                    net_item = NetworkItem(*item)
                    check_num = 0
                    for filename in os.listdir(self.game_communication_path):
                        if filename.startswith("AP"):
                            if int(filename.split("_")[-1].split(".")[0]) > check_num:
                                check_num = int(filename.split("_")[-1].split(".")[0])
                    item_id = ""
                    location_id = ""
                    player = ""
                    found = False
                    for filename in os.listdir(self.game_communication_path):
                        if filename.startswith("AP"):
                            with open(os.path.join(self.game_communication_path, filename), 'r') as f:
                                item_id = str(f.readline()).replace("\n", "")
                                location_id = str(f.readline()).replace("\n", "")
                                player = str(f.readline()).replace("\n", "")
                                if str(item_id) == str(net_item.item) and str(location_id) == str(net_item.location) and str(player) == str(net_item.player):
                                    found = True
                    if not found:
                        filename = f"AP_{str(check_num+1)}.item"
                        with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                            f.write(str(net_item.item) + "\n" + str(net_item.location) + "\n" + str(net_item.player))
                            f.close()

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.close()

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class FFXIITMManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago FFXIITM Client"

        self.ui = FFXIITMManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def game_watcher(ctx: FFXIITMContext):
    while not ctx.exit_event.is_set():
        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        sending = []
        victory = False
        for root, dirs, files in os.walk(ctx.game_communication_path):
            for file in files:
                if file.find("send") > -1:
                    st = file.split("send", -1)[1]
                    if st != "nil":
                        sending = sending+[(int(st))]
                if file.find("victory") > -1:
                    victory = True
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def launch():
    async def main(args):
        ctx = FFXIITMContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="FFXIITMProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="FFXIITM Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()

def copy_data() -> None:
    try:
        script_name = "ffxii_tm_ap.lua"
        script_paths = [os.path.join(Utils.user_path("data", "lua"), script_name)]
        if Utils.is_windows and os.path.exists("C:\\Program Files (x86)\\Steam\\steamapps\\common\\FINAL FANTASY XII THE ZODIAC AGE\\x64"):
            script_paths.append(os.path.join("C:\\Program Files (x86)\\Steam\\steamapps\\common\\FINAL FANTASY XII THE ZODIAC AGE\\x64\\scripts", script_name))

        for script_path in script_paths:
            if not os.path.exists(script_path):
                with open(script_path, "wb") as script_file:
                    script_file.write(pkgutil.get_data(__name__, "data/" + script_name))
            else:
                with open(script_path, "rb+") as script_file:
                    expected_script = pkgutil.get_data(__name__, "data/" + script_name)

                    expected_hash = hashlib.md5(expected_script).digest()
                    existing_hash = hashlib.md5(script_file.read()).digest()

                    if existing_hash != expected_hash:
                        script_file.seek(0)
                        script_file.truncate()
                        script_file.write(expected_script)
    except IOError:
        logging.warning("Unable to copy ffxii_tm_ap.lua to /data/lua in your Archipelago install.")

copy_data()

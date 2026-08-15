from __future__ import annotations
import hashlib
import logging
import os
import pkgutil
import sys
import asyncio
import shutil
import time
from typing import TYPE_CHECKING

import ModuleUpdate
ModuleUpdate.update()

import Utils

# tracker_loaded = False
# try:
#     from worlds.tracker.TrackerClient import TrackerGameContext as CommonContext
#     tracker_loaded = True
# except ModuleNotFoundError:
#     from CommonClient import CommonContext as CommonContext
from CommonClient import CommonContext as CommonContext

check_num = 0

if __name__ == "__main__":
    Utils.init_logging("FFXIITMClient", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, server_loop


def check_stdin() -> None:
    if Utils.is_windows and sys.stdin:
        print("WARNING: Console input is not routed reliably on Windows, use the GUI instead.")

def clear_AP_files(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if 'obtain' in file or 'current_map' in file: continue
            os.remove(root+"/"+file)

def get_trial_from_location_id(location_id):
    trial = ((location_id//10 -1) % 1000)+1 # 451001 -> 100
    if location_id % 10 == 0: trial -= 1 #specifically for trial 31 because it has 5 chests
    return trial


class FFXIITMClientCommandProcessor(ClientCommandProcessor):

    def _cmd_send_previous_chests(self):
        '''sends missed chests from all trials before the most recently collect chest'''
        check = self.ctx.most_recent_check
        if check > 0:
            current_trial = get_trial_from_location_id(check)
            # self.output(f'you are in Trial {current_trial}')
            locations_to_send = [l for l in self.ctx.missing_locations if get_trial_from_location_id(l) < current_trial]

            for ss in locations_to_send:
                filename = f"send{ss}"
                with open(os.path.join(self.ctx.game_communication_path, filename), 'w') as f:
                    f.close()
        else:
            self.output('No found chests detected in this session.')

    def _cmd_toggle_always_send_previous_chests(self):
        '''toggle whether to always send previous trials chests upon chest pickup'''
        self.ctx.always_send_previous_chests = not self.ctx.always_send_previous_chests
        self.output(f'Current state: {self.ctx.always_send_previous_chests}')

class FFXIITMContext(CommonContext):
    command_processor = FFXIITMClientCommandProcessor
    game = "Final Fantasy XII Trial Mode"
    items_handling = 0b111  # full remote
    tags = {"AP"}


    def __init__(self, server_address, password):
        super(FFXIITMContext, self).__init__(server_address, password)
        self.local_command_processor = self.command_processor(self)
        self.most_recent_check = 0
        self.always_send_previous_chests = False
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        if "localappdata" in os.environ:
            self.game_communication_path = os.path.expandvars(r"%localappdata%/FFXIITM")
        else:
            self.game_communication_path = os.path.expandvars(r"$HOME/FFXIITM")
        os.makedirs(self.game_communication_path, exist_ok=True)
        clear_AP_files(self.game_communication_path)



    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(FFXIITMContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(FFXIITMContext, self).connection_closed()
        clear_AP_files(self.game_communication_path)

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(FFXIITMContext, self).shutdown()
        clear_AP_files(self.game_communication_path)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            os.makedirs(self.game_communication_path,exist_ok=True)
            # for ss in self.checked_locations:
                # filename = f"send{ss}"
                # with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    # f.close()
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
                            # time.sleep(0.1)

        # Collected items do not need to be communicated to the mod
        # if cmd in {"RoomUpdate"}:
            # if "checked_locations" in args:
                # logger.info(f'collect detected. There should now be {len(self.checked_locations)} locations checked')
                # for ss in self.checked_locations:
                    # self.checked_locations
                    # filename = f"send{ss}"
                    # if not os.path.exists(os.path.join(self.game_communication_path, filename)):
                        # with open(os.path.join(self.game_communication_path, f"collected{ss}"), 'w') as f:
                            # f.close()
                        # if ss not in self.locations_checked: self.locations_checked.append(ss)
        super().on_package(cmd, args)

    def make_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        ui = super().make_gui()

        class FFXIITMManager(ui):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago FFXIITM Client"

        return FFXIITMManager


async def game_watcher(ctx: FFXIITMContext):
    new_locations = []
    while not ctx.exit_event.is_set():
        if ctx.syncing:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                # sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
                sync_msg.append({"cmd": "LocationChecks", "locations": new_locations})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        location_roundup = []
        victory = False
        for root, dirs, files in os.walk(ctx.game_communication_path):
            for file in files:
                if 'send' in file:
                    st = file.split("send", -1)[1]
                    if st != "nil":
                        location_roundup.append(int(st))
                if "victory" in file:
                    victory = True
        if len(location_roundup) > len(ctx.locations_checked):
            # logger.info(f"checks: {len(ctx.locations_checked)} -> {len(location_roundup)}")
            ctx.syncing = True
            new_locations = [l for l in location_roundup if l not in ctx.locations_checked]
            ctx.most_recent_check = max(ctx.most_recent_check, new_locations[-1])

            if ctx.always_send_previous_chests: ctx.local_command_processor._cmd_send_previous_chests()
        ctx.locations_checked = location_roundup

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
        script_paths = []
        install = Utils.get_settings().get("ffxiitm", {}).get("install_script", True)
        if Utils.is_windows and os.path.exists("C:\\Program Files (x86)\\Steam\\steamapps\\common\\FINAL FANTASY XII THE ZODIAC AGE\\x64") and install:
            script_paths.append(os.path.join("C:\\Program Files (x86)\\Steam\\steamapps\\common\\FINAL FANTASY XII THE ZODIAC AGE\\x64\\scripts", script_name))
        else:
            script_paths.append(os.path.join(Utils.user_path("data", "lua"), script_name))

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
                        print(f'Updating {script_path}')
                        script_file.seek(0)
                        script_file.truncate()
                        script_file.write(expected_script)
    except IOError:
        logging.warning("Unable to copy ffxii_tm_ap.lua to /data/lua in your Archipelago install.")

# copy_data()

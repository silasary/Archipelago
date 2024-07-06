import time
from typing import List

import ModuleUpdate
from BaseClasses import ItemClassification

ModuleUpdate.update()

import asyncio
from pymem import pymem

from NetUtils import ClientStatus, NetworkItem
from CommonClient import gui_enabled, logger, get_base_parser, CommonContext, server_loop, ClientCommandProcessor

from .Items import FF12OW_BASE_ID, item_data_table, inv_item_table
from .Locations import location_data_table, FF12OpenWorldLocationData

sort_start_addresses = [
    0x204FD4C,  # Items
    0x204FDCC,  # Weapons
    0x204FF5C,  # Armor
    0x2050074,  # Accessories
    0x20500D4,  # Ammo
    0x2050364,  # Technicks
    0x2050394,  # Magicks
    0x2050436,  # Key Items
    0x2050836,  # Loot
]

sort_count_addresses = [
    0x2050C38,  # Items
    0x2050C3C,  # Weapons
    0x2050C40,  # Armor
    0x2050C44,  # Accessories
    0x2050C48,  # Ammo
    0x2050C58,  # Technicks
    0x2050C5C,  # Magicks
    0x2050C60,  # Key Items
    0x2050C64,  # Loot
]


class FF12OpenWorldCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_list_processes(self):
        """List all processes found by pymem."""
        for process in pymem.process.list_processes():
            self.output(f"{process.szExeFile}: {process.th32ProcessID}")

    def _cmd_set_process_by_id(self, process_id: str):
        """Set the process by ID (int)."""
        int_id = int(process_id)
        try:
            self.ctx.ff12 = pymem.Pymem().open_process_from_id(int_id)
            logger.info("You are now auto-tracking")
            self.ctx.ff12connected = True
        except Exception as e:
            if self.ctx.ff12connected:
                self.ctx.ff12connected = False
            logger.info("Failed to set process by ID.")
            logger.info(e)

    def _cmd_debug_info(self):
        """Prints debug information."""
        try:
            logger.info("Current Map ID: " + str(self.ctx.get_current_map()))
            logger.info("Current State: " + str(self.ctx.get_current_game_state()))
            logger.info("Party: " + str([c for c in range(6) if self.ctx.is_chara_in_party(c)]))
            logger.info("Items: " + str(
                [item + ": " + str(self.ctx.get_item_count(item)) for item in item_data_table.keys() if
                 self.ctx.has_item_in_game(item)]))
            logger.info("Missing: " + str(
                [item for item in item_data_table.keys() if
                 self.ctx.get_item_count(item) < self.ctx.get_expected_items(item) and
                 item_data_table[item].classification & ItemClassification.progression]))
            pass
        except Exception as e:
            if self.ff12connected:
                self.ff12connected = False
            logger.info(e)

    def _cmd_check_missing_items(self):
        """Check for missing items."""
        try:
            # Create a task for checking missing items
            asyncio.create_task(self.ctx.check_missing_items())
        except Exception as e:
            if self.ff12connected:
                self.ff12connected = False
            logger.info(e)


# Copied from KH2 Client
class FF12OpenWorldContext(CommonContext):
    command_processor = FF12OpenWorldCommandProcessor
    game = "Final Fantasy 12 Open World"
    items_handling = 0b111  # Indicates you get items sent from other worlds.

    def __init__(self, server_address, password):
        super(FF12OpenWorldContext, self).__init__(server_address, password)

        self.last_big_batch_time = None
        self.ff12_items_received: List[NetworkItem] = []
        self.prev_map_and_time = None
        self.sending: List[int] = []
        self.ff12slotdata = None
        self.server_connected = False
        self.ff12connected = False
        # hooked object
        self.ff12 = None
        self.check_loc_task = None
        self.give_items_task = None
        self.item_lock = asyncio.Lock()

    async def get_username(self):
        if not self.auth:
            self.auth = self.username
            if not self.auth:
                logger.info('Enter slot name:')
                self.auth = await self.console_input()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(FF12OpenWorldContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.ff12connected = False
        self.server_connected = False
        self.ff12_items_received.clear()
        await super(FF12OpenWorldContext, self).connection_closed()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.ff12connected = False
        self.server_connected = False
        self.ff12_items_received.clear()
        await super(FF12OpenWorldContext, self).disconnect()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(FF12OpenWorldContext, self).shutdown()

    def ff12_story_address(self):
        return self.ff12.base_address

    def ff12_write_byte(self, address, value,use_base=True):
        if use_base:
            return self.ff12.write_bytes(self.ff12.base_address + address, value.to_bytes(1, "little"), 1)
        else:
            return self.ff12.write_bytes(address, value.to_bytes(1, "little"), 1)

    def ff12_read_byte(self, address, use_base=True):
        if use_base:
            return int.from_bytes(self.ff12.read_bytes(self.ff12.base_address + address, 1), "little")
        else:
            return int.from_bytes(self.ff12.read_bytes(address, 1), "little")

    def ff12_read_bit(self, address, bit, use_base=True) -> bool:
        return (self.ff12_read_byte(address, use_base) >> bit) & 1 == 1

    def ff12_read_short(self, address, use_base=True):
        if use_base:
            return int.from_bytes(self.ff12.read_bytes(self.ff12.base_address + address, 2), "little")
        else:
            return int.from_bytes(self.ff12.read_bytes(address, 2), "little")

    def ff12_write_short(self, address, value, use_base=True):
        if use_base:
            return self.ff12.write_bytes(self.ff12.base_address + address, value.to_bytes(2, "little"), 2)
        else:
            return self.ff12.write_bytes(address, value.to_bytes(2, "little"), 2)

    def ff12_read_int(self, address, use_base=True):
        if use_base:
            return int.from_bytes(self.ff12.read_bytes(self.ff12.base_address + address, 4), "little")
        else:
            return int.from_bytes(self.ff12.read_bytes(address, 4), "little")

    def ff12_write_int(self, address, value, use_base=True):
        if use_base:
            return self.ff12.write_bytes(self.ff12.base_address + address, value.to_bytes(4, "little"), 4)
        else:
            return self.ff12.write_bytes(address, value.to_bytes(4, "little"), 4)

    def on_package(self, cmd: str, args: dict):

        if cmd in {"Connected"}:
            asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["Final Fantasy 12 Open World"]}]))
            self.ff12slotdata = args['slot_data']
            self.locations_checked = set(args["checked_locations"])

        if cmd in {"ReceivedItems"}:
            self.find_game()
            if self.server_connected:
                # Get the items past the start index in args items
                for index, item in enumerate(args["items"], start=args["index"]):
                    if index >= len(self.ff12_items_received):
                        self.ff12_items_received.append(item)
                    else:
                        self.ff12_items_received[index] = item

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                new_locations = set(args["checked_locations"])
                self.locations_checked |= new_locations

        if cmd in {"DataPackage"}:
            self.find_game()
            self.server_connected = True
            asyncio.create_task(self.send_msgs([{'cmd': 'Sync'}]))

    def find_game(self):
        if not self.ff12connected:
            try:
                self.ff12 = pymem.Pymem(process_name="FFXII_TZA")
                logger.info("You are now auto-tracking")
                self.ff12connected = True
            except Exception as e:
                if self.ff12connected:
                    self.ff12connected = False
                logger.info("Game is not open (Try running the client as an admin).")
                logger.info(e)

    def get_current_map(self) -> int:
        return self.ff12_read_short(0x20454C4)

    def is_in_game(self) -> bool:
        # Check if the game has been on this map for more than 0.25 seconds
        self.prev_map_and_time = self.prev_map_and_time or (self.get_current_map(), time.time())

        if (self.prev_map_and_time[0] != self.get_current_map() or
                self.get_current_map() <= 12 or # Main Menus
                self.get_current_map() == 274 or # Initial Nalbina Fortress Map
                self.get_current_game_state() != 0):
            self.prev_map_and_time = (self.get_current_map(), time.time())
            return False
        else:
            return time.time() - self.prev_map_and_time[1] > 0.25

    def get_current_game_state(self) -> int:
        # 0 - Field
        # 1 - Dialog/Cutscene
        # 4 - Menu
        # 5 - Load Screen
        pointer1 = self.ff12_read_int(0x01E5FFE0)
        return self.ff12_read_byte(pointer1 + 0x3A, False)

    def get_party_address(self) -> int:
        return self.ff12_read_int(0x02D9F190) + 0x08

    def get_save_data_address(self) -> int:
        return self.ff12.base_address + 0x02044480

    def get_scenario_flag(self) -> int:
        return self.ff12_read_short(0x02044480)

    def get_item_index(self) -> int:
        return self.ff12_read_int(self.get_save_data_address() + 0x696, use_base=False)

    def set_item_index(self, index):
        self.ff12_write_int(self.get_save_data_address() + 0x696, index, use_base=False)

    def get_item_add_id(self) -> int:
        return self.ff12_read_short(self.get_save_data_address() + 0x69A, use_base=False)

    def get_item_add_count(self) -> int:
        return self.ff12_read_int(self.get_save_data_address() + 0x69C, use_base=False)

    def set_item_add_id(self, item_id: int) -> None:
        if item_id >= FF12OW_BASE_ID + 98304:  # Gil
            self.ff12_write_short(self.get_save_data_address() + 0x69A,
                                  0xFFFE, use_base=False)
        else:
            self.ff12_write_short(self.get_save_data_address() + 0x69A,
                                  item_id - FF12OW_BASE_ID, use_base=False)

    def set_item_add_count(self, count: int) -> None:
        self.ff12_write_int(self.get_save_data_address() + 0x69C, count, use_base=False)

    def is_chara_in_party(self, chara) -> bool:
        return self.ff12_read_bit(self.get_party_address() + chara * 0x1C8, 4, False)

    def get_item_count_received(self, item_name: str) -> int:
        return len([item for item in self.ff12_items_received[:self.get_item_index()] if
                    item.item == item_data_table[item_name].code])

    def has_item_received(self, item_name: str) -> bool:
        return self.get_item_count_received(item_name) > 0

    def get_item_count(self, item_name: str) -> int:
        int_id = item_data_table[item_name].code - FF12OW_BASE_ID
        if int_id < 0x1000:  # Normal items
            return self.ff12_read_short(0x02097054 + int_id * 2)
        elif int_id < 0x2000:  # Equipment
            return self.ff12_read_short(0x020970D4 + (int_id - 0x1000) * 2)
        elif 0x2000 <= int_id < 0x3000:  # Loot items
            return self.ff12_read_short(0x0209741C + (int_id - 0x2000) * 2)
        elif 0x8000 <= int_id < 0x9000:  # Key items
            byte_index = (int_id - 0x8000) // 8
            bit_index = (int_id - 0x8000) % 8
            return 1 if self.ff12_read_bit(0x0209784C + byte_index, bit_index) else 0
        elif 0xC000 <= int_id < 0xD000:  # Espers
            byte_index = (int_id - 0xC000) // 8
            bit_index = (int_id - 0xC000) % 8
            return 1 if self.ff12_read_bit(0x0209788C + byte_index, bit_index) else 0
        elif 0x3000 <= int_id < 0x4000:  # Magicks
            byte_index = (int_id - 0x3000) // 8
            bit_index = (int_id - 0x3000) % 8
            return 1 if self.ff12_read_bit(0x0209781C + byte_index, bit_index) else 0
        elif 0x4000 <= int_id < 0x5000:  # Technicks
            byte_index = (int_id - 0x4000) // 8
            bit_index = (int_id - 0x4000) % 8
            return 1 if self.ff12_read_bit(0x02097828 + byte_index, bit_index) else 0
        else:
            return 0

    def has_item_in_game(self, item_name: str) -> bool:
        return self.get_item_count(item_name) > 0

    def get_leviathan_progress(self) -> int:
        # Check if currently in Leviathan
        if 0x37A <= self.get_scenario_flag() <= 0x44C:
            return self.get_scenario_flag()

        # Otherwise use the stored flag
        lev_flag = self.ff12_read_short(self.get_save_data_address() + 0xDFF7, False)
        if lev_flag > 10000:  # Used the 2nd checkpoint
            return lev_flag - 10000
        elif lev_flag == 0:  # Not yet started
            return 0
        else:  # Used the 1st checkpoint
            return lev_flag

    def get_escape_progress(self) -> int:
        esc_flag = self.ff12_read_short(self.get_save_data_address() + 0xDFF4, False)

        # Check if stored progress is after beating Mimic Queen
        if self.ff12_read_byte(self.get_save_data_address() + 0xA04, False) >= 2:
            return 0x208  # Close to beating mimic queen
        # Check if currently in the escape sequence after beating Firemane
        elif 0x11D < self.get_scenario_flag() < 0x208:
            return self.get_scenario_flag()
        # Check if the stored progress in the escape sequence after beating Firemane
        elif 0x11D < esc_flag < 0x208:
            return esc_flag
        # Check if stored progress is after beating Firemane
        elif self.ff12_read_byte(self.get_save_data_address() + 0xA06, False) >= 2:
            return 0x11D  # Close to beating Firemane
        # Check if currently in the escape sequence before beating Firemane
        elif 6110 < self.get_scenario_flag() <= 6110 + 70:
            return self.get_scenario_flag() - 6110
        # Check if the stored progress in the escape sequence before beating Firemane
        elif 6110 < esc_flag <= 6110 + 70:
            return esc_flag - 6110
        else:
            return 0

    def get_draklor_progress(self) -> int:
        # Check if currently in Leviathan
        if 0xD48 <= self.get_scenario_flag() <= 0x1036:
            return self.get_scenario_flag()

        # Otherwise use the stored flag
        darklor_flag = self.ff12_read_short(self.get_save_data_address() + 0xDFF9, False)
        if darklor_flag == 0:  # Not yet started
            return 0
        else:
            return darklor_flag

    async def check_locations(self):
        last_end_time = time.time()
        while not self.exit_event.is_set() and self.ff12connected and self.server_connected:
            if time.time() - last_end_time < 0.5:
                await asyncio.sleep(0.1)
                continue
            try:
                self.sending.clear()
                index = 0
                for location_name, data in location_data_table.items():
                    index += 1
                    # Do not check in menus
                    if not self.is_in_game():
                        break
                    if data.address in self.locations_checked:
                        continue
                    if data.type == "inventory":
                        if self.is_chara_in_party(int(data.str_id)):
                            self.sending.append(data.address)
                    elif data.type == "reward":
                        if self.is_reward_met(location_name, data):
                            self.sending.append(data.address)
                    elif data.type == "treasure":
                        treasures: list[str] = self.ff12slotdata["treasures"]
                        if location_name not in treasures:
                            continue
                        treasure_index = treasures.index(location_name)
                        byte_index = treasure_index // 8
                        bit_index = treasure_index % 8
                        if self.ff12_read_bit(self.get_save_data_address() + 0x14B4 + byte_index, bit_index, False):
                            self.sending.append(data.address)

                self.locations_checked |= set(self.sending)

                # Victory, Final Boss
                if self.ff12_read_byte(self.get_save_data_address() + 0xA2E, False) >= 2 \
                        and not self.finished_game:
                    await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    self.finished_game = True

                if len(self.sending) > 0:
                    message = [{"cmd": 'LocationChecks', "locations": self.sending}]
                    await self.send_msgs(message)

            except Exception as e:
                if self.ff12connected:
                    self.ff12connected = False
                logger.info(e)
            last_end_time = time.time()

    def is_reward_met(self, location_name: str, location_data: FF12OpenWorldLocationData):
        if location_data.str_id == "9000" or \
                location_data.str_id == "916B" or \
                location_data.str_id == "916C":  # Tomaj Checks
            return self.get_scenario_flag() >= 6110
        elif location_data.str_id == "9002":  # Shadestone check
            return self.ff12_read_bit(self.get_save_data_address() + 0xA42, 0, False)
        elif location_data.str_id == "9001":  # Sunstone check (if received Shadestone but the item is lost)
            return self.has_item_received("Shadestone") and not self.has_item_in_game("Shadestone")
        elif location_data.str_id == "905E":  # Crescent Stone (if received Sunstone but the item is lost)
            return self.has_item_received("Sunstone") and not self.has_item_in_game("Sunstone")
        elif location_data.str_id == "905F":  # Dalan SotO
            return self.ff12_read_bit(self.get_save_data_address() + 0xA42, 1, False)
        elif location_data.str_id == "911E":  # SotO turn in
            return self.has_item_received("Sword of the Order") and not self.has_item_in_game("Sword of the Order")
        elif location_data.str_id == "9060":  # Judges Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA27, False) >= 2
        elif location_data.str_id == "9061":  # Systems Access Key
            return self.ff12_read_bit(self.get_save_data_address() + 0x14D4 + 4, 0, False)
        elif location_data.str_id == "912C":  # Manufacted Nethicite
            return self.get_leviathan_progress() >= 0x3E8
        elif location_data.str_id == "912D":  # Eksir Berries
            return self.ff12_read_bit(self.get_save_data_address() + 0xA42, 2, False)
        elif location_data.str_id == "9190":  # Belias Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA19, False) >= 2
        elif location_data.str_id == "912E":  # Dawn Shard
            return self.ff12_read_bit(self.get_save_data_address() + 0xA42, 3, False)
        elif location_data.str_id == "918E":  # Vossler Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA3B, False) >= 2
        elif location_data.str_id == "912F":  # Goddess's Magicite
            return self.get_escape_progress() >= 15
        elif location_data.str_id == "9130":  # Tube Fuse
            return self.get_escape_progress() >= 0x13F
        elif location_data.str_id == "911F":  # Garif Reward
            return self.ff12_read_bit(self.get_save_data_address() + 0xA42, 4, False)
        elif location_data.str_id == "9131":  # Lente's Tear (Tiamat Boss)
            return self.ff12_read_byte(self.get_save_data_address() + 0xA08, False) >= 2
        elif location_data.str_id == "9191":  # Mateus Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA21, False) >= 2
        elif location_data.str_id == "9132":  # Sword of Kings
            return self.ff12_read_bit(self.get_save_data_address() + 0xA42, 6, False)
        elif location_data.str_id == "9133":  # Start Mandragoras
            # Kid or Dad
            return self.ff12_read_byte(self.get_save_data_address() + 0x684, False) == 1 or \
                self.ff12_read_byte(self.get_save_data_address() + 0x681, False) == 1
        elif location_data.str_id == "9052":  # Turn in Mandragoras
            return self.ff12_read_byte(self.get_save_data_address() + 0x683, False) == 1
        elif location_data.str_id == "918D":  # Cid 1 Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA29, False) >= 2
        elif 0x9134 <= int(location_data.str_id, 16) <= 0x914F:  # Pinewood Chops
            return (self.ff12_read_byte(self.get_save_data_address() + 0xDFF6, False) >
                    int(location_data.str_id, 16) - 0x9134)
        elif location_data.str_id == "9150":  # Sandalwood Chop
            return self.ff12_read_bit(self.get_save_data_address() + 0xA42, 7, False)
        elif location_data.str_id == "9151":  # Lab Access Card
            return self.get_draklor_progress() >= 0xD48
        elif location_data.str_id == "9192":  # Shemhazai Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA20, False) >= 2
        elif location_data.str_id == "9152":  # Treaty Blade
            return self.ff12_read_bit(self.get_save_data_address() + 0xDFFB, 0, False)
        elif 0x9153 <= int(location_data.str_id, 16) <= 0x916A:  # Black Orbs
            return (self.ff12_read_byte(self.get_save_data_address() + 0xDFFC, False) >
                    int(location_data.str_id, 16) - 0x9153)
        elif location_data.str_id == "9193":  # Hashmal Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA1F, False) >= 2
        elif location_data.str_id == "918F":  # Cid 2 Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA2A, False) >= 2
        elif location_data.str_id == "9003":  # Hunt 1
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 0, False) >= 70
        elif location_data.str_id == "9004":  # Hunt 2
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 1, False) >= 70
        elif location_data.str_id == "9005":  # Hunt 3
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 2, False) >= 90
        elif location_data.str_id == "9006":  # Hunt 4
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 3, False) >= 100
        elif location_data.str_id == "9007":  # Hunt 5
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 4, False) >= 90
        elif location_data.str_id == "9008":  # Hunt 6
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 5, False) >= 100
        elif location_data.str_id == "9009":  # Hunt 7
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 6, False) >= 100
        elif location_data.str_id == "900A":  # Hunt 8
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 7, False) >= 100
        elif location_data.str_id == "900B":  # Hunt 9
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 8, False) >= 100
        elif location_data.str_id == "900C":  # Hunt 10
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 9, False) >= 100
        elif location_data.str_id == "900D":  # Hunt 11
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 10, False) >= 100
        elif location_data.str_id == "900E":  # Hunt 12
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 11, False) >= 100
        elif location_data.str_id == "900F":  # Hunt 13
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 12, False) >= 90
        elif location_data.str_id == "9010":  # Hunt 14
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 13, False) >= 100
        elif location_data.str_id == "9011":  # Hunt 15
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 14, False) >= 100
        elif location_data.str_id == "9012":  # Hunt 16
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 15, False) >= 90
        elif location_data.str_id == "9013":  # Hunt 17
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 16, False) >= 50
        elif location_data.str_id == "9014":  # Hunt 18
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 17, False) >= 50
        elif location_data.str_id == "9015":  # Hunt 19
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 18, False) >= 100
        elif location_data.str_id == "9016":  # Hunt 20
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 19, False) >= 150
        elif location_data.str_id == "9017":  # Hunt 21
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 20, False) >= 150
        elif location_data.str_id == "9018":  # Hunt 22
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 21, False) >= 150
        elif location_data.str_id == "9019":  # Hunt 23
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 22, False) >= 150
        elif location_data.str_id == "901A":  # Hunt 24
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 23, False) >= 50
        elif location_data.str_id == "901B":  # Hunt 25
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 24, False) >= 50
        elif location_data.str_id == "901C":  # Hunt 26
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 25, False) >= 90
        elif location_data.str_id == "901D":  # Hunt 27
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 26, False) >= 90
        elif location_data.str_id == "901E":  # Hunt 28
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 27, False) >= 90
        elif location_data.str_id == "901F":  # Hunt 29
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 28, False) >= 100
        elif location_data.str_id == "9020":  # Hunt 30
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 29, False) >= 100
        elif location_data.str_id == "9021":  # Hunt 31
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 30, False) >= 90
        elif location_data.str_id == "9022":  # Hunt 32
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 31, False) >= 150
        elif location_data.str_id == "9023":  # Hunt 33
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 32, False) >= 100
        elif location_data.str_id == "9024":  # Hunt 34
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 33, False) >= 90
        elif location_data.str_id == "9025":  # Hunt 35
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 34, False) >= 100
        elif location_data.str_id == "9026":  # Hunt 36
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 35, False) >= 100
        elif location_data.str_id == "9027":  # Hunt 37
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 36, False) >= 90
        elif location_data.str_id == "9028":  # Hunt 38
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 37, False) >= 110
        elif location_data.str_id == "9029":  # Hunt 39
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 38, False) >= 50
        elif location_data.str_id == "902A":  # Hunt 40
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 39, False) >= 130
        elif location_data.str_id == "902B":  # Hunt 42
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 40, False) >= 100
        elif location_data.str_id == "902C":  # Hunt 43
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 41, False) >= 150
        elif location_data.str_id == "902D":  # Hunt 44
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 42, False) >= 100
        elif location_data.str_id == "902E":  # Hunt 45
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 43, False) >= 100
        elif location_data.str_id == "9122":  # Hunt 41
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 44, False) >= 100
        elif 0x902F <= int(location_data.str_id, 16) <= 0x903A:  # Clan Rank Rewards
            return (self.ff12_read_byte(self.get_save_data_address() + 0x418, False) >
                    int(location_data.str_id, 16) - 0x902F)
        elif location_data.str_id == "903B":  # Clan Boss Flans
            return self.ff12_read_bit(self.get_save_data_address() + 0x419, 0, False)
        elif location_data.str_id == "903C":  # Clan Boss Firemane
            return self.ff12_read_bit(self.get_save_data_address() + 0x419, 1, False)
        elif location_data.str_id == "903D":  # Clan Boss Earth Tyrant
            return self.ff12_read_bit(self.get_save_data_address() + 0x419, 2, False)
        elif location_data.str_id == "903E":  # Clan Boss Mimic Queen
            return self.ff12_read_bit(self.get_save_data_address() + 0x419, 3, False)
        elif location_data.str_id == "903F":  # Clan Boss Demon Wall 1
            return self.ff12_read_bit(self.get_save_data_address() + 0x419, 4, False)
        elif location_data.str_id == "9040":  # Clan Boss Demon Wall 2
            return self.ff12_read_bit(self.get_save_data_address() + 0x419, 5, False)
        elif location_data.str_id == "9041":  # Clan Boss Elder Wyrm
            return self.ff12_read_bit(self.get_save_data_address() + 0x419, 6, False)
        elif location_data.str_id == "9042":  # Clan Boss Tiamat
            return self.ff12_read_bit(self.get_save_data_address() + 0x419, 7, False)
        elif location_data.str_id == "9043":  # Clan Boss Vinuskar
            return self.ff12_read_bit(self.get_save_data_address() + 0x41A, 0, False)
        elif location_data.str_id == "9044":  # Clan Boss King Bomb
            return self.ff12_read_bit(self.get_save_data_address() + 0x41A, 1, False)
        elif location_data.str_id == "9045":  # Clan Boss Mandragoras
            return self.ff12_read_bit(self.get_save_data_address() + 0x41A, 3, False)
        elif location_data.str_id == "9046":  # Clan Boss Ahriman
            return self.ff12_read_bit(self.get_save_data_address() + 0x41A, 2, False)
        elif location_data.str_id == "9047":  # Clan Boss Hell Wyrm
            return self.ff12_read_bit(self.get_save_data_address() + 0x41A, 4, False)
        elif location_data.str_id == "9048":  # Clan Boss Rafflesia
            return self.ff12_read_bit(self.get_save_data_address() + 0x41A, 5, False)
        elif location_data.str_id == "9049":  # Clan Boss Daedalus
            return self.ff12_read_bit(self.get_save_data_address() + 0x41A, 6, False)
        elif location_data.str_id == "904A":  # Clan Boss Tyrant
            return self.ff12_read_bit(self.get_save_data_address() + 0x41A, 7, False)
        elif location_data.str_id == "904B":  # Clan Boss Hydro
            return self.ff12_read_bit(self.get_save_data_address() + 0x41B, 0, False)
        elif location_data.str_id == "904C":  # Clan Boss Humbaba Mistant
            return self.ff12_read_bit(self.get_save_data_address() + 0x41B, 1, False)
        elif location_data.str_id == "904D":  # Clan Boss Fury
            return self.ff12_read_bit(self.get_save_data_address() + 0x41B, 2, False)
        elif location_data.str_id == "905A":  # Clan Boss Omega Mark XII
            return self.ff12_read_bit(self.get_save_data_address() + 0x41B, 3, False)
        elif 0x904E <= int(location_data.str_id, 16) <= 0x9051:  # Clan Espers (1,4,8,13)
            return (self.ff12_read_byte(self.get_save_data_address() + 0x41C, False) >
                    int(location_data.str_id, 16) - 0x904E)
        elif location_data.str_id == "916D":  # Flowering Cactoid Drop
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 130, False) >= 70
        elif location_data.str_id == "916E":  # Barheim Key
            return self.ff12_read_byte(self.get_save_data_address() + 0x68B, False) >= 11
        elif location_data.str_id == "9081":  # Deliver Cactus Flower
            return self.ff12_read_byte(self.get_save_data_address() + 0x68B, False) >= 3
        elif location_data.str_id == "908A":  # Cactus Family
            return self.ff12_read_byte(self.get_save_data_address() + 0x686, False) >= 7
        elif location_data.str_id == "916F":  # Get Stone of the Condemner
            return self.ff12_read_byte(self.get_save_data_address() + 0x680, False) >= 1
        elif location_data.str_id == "9170":  # Get Wind Globe
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 53, False) >= 50
        elif location_data.str_id == "9171":  # Get Windvane
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 53, False) >= 60
        elif location_data.str_id == "9172":  # White Mousse Drop
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 133, False) >= 50
        elif location_data.str_id == "9173":  # Sluice Gate Key
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 133, False) >= 120
        elif location_data.str_id == "9174":  # Enkelados Drop
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 137, False) >= 50
        elif location_data.str_id == "9062":  # Give Errmonea Leaf
            return self.ff12_read_byte(self.get_save_data_address() + 0x4AE, False) >= 1
        elif location_data.str_id == "9175":  # Merchant's Armband
            return self.ff12_read_byte(self.get_save_data_address() + 0x6FD, False) >= 2
        elif location_data.str_id == "9176":  # Get Pilika's Diary
            return self.ff12_read_byte(self.get_save_data_address() + 0x6FD, False) >= 3
        elif location_data.str_id == "908D":  # Give Pilika's Diary
            return self.ff12_read_byte(self.get_save_data_address() + 0x6FD, False) >= 4
        elif location_data.str_id == "9177":  # Vorpal Bunny Drop
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 141, False) >= 50
        elif location_data.str_id == "9178":  # Croakadile Drop
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 138, False) >= 50
        elif location_data.str_id == "9179":  # Lindwyrm Drop
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 149, False) >= 100
        elif location_data.str_id == "917A":  # Get Silent Urn
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 163, False) >= 50
        elif location_data.str_id == "917B":  # Orthros Drop
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 162, False) >= 70
        elif location_data.str_id == "917D":  # Site 3 Key
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 165, False) >= 50
        elif location_data.str_id == "917E":  # Site 11 Key
            return self.ff12_read_bit(self.get_save_data_address() + 0xDFFB, 2, False)
        elif location_data.str_id == "917F":  # Fafnir Drop
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 158, False) >= 70
        elif location_data.str_id == "9180":  # Marilith Drop
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 136, False) >= 70
        elif location_data.str_id == "9181":  # Vyraal Drop
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 148, False) >= 100
        elif location_data.str_id == "9182":  # Dragon Scale
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 148, False) >= 150
        elif location_data.str_id == "9183":  # Ageworn Key check (if received Dragon Scale but the item is lost)
            return self.has_item_received("Dragon Scale") and not self.has_item_in_game("Dragon Scale")
        elif location_data.str_id == "9184":  # Ann's Letter
            return self.ff12_read_byte(self.get_save_data_address() + 0x5A6, False) >= 1
        elif location_data.str_id == "906C":  # Ann's Sisters
            return self.ff12_read_byte(self.get_save_data_address() + 0x5A6, False) >= 7
        elif location_data.str_id == "9185":  # Dusty Letter
            return self.ff12_read_bit(self.get_save_data_address() + 0x423, 2, False)
        elif location_data.str_id == "917C":  # Blackened Fragment
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 162, False) >= 100
        elif location_data.str_id == "9186":  # Dull Fragment
            return self.ff12_read_bit(self.get_save_data_address() + 0x423, 1, False)
        elif location_data.str_id == "9187":  # Grimy Fragment
            return self.ff12_read_byte(self.get_save_data_address() + 0x416, False) >= 7
        elif location_data.str_id == "9188":  # Moonsilver Medallion
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 59, False) >= 20
        elif location_data.str_id == "9189" or \
                location_data.str_id == "918A" or \
                location_data.str_id == "918B":  # Nabreus Medallions
            return self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 57, False) >= 100
        elif location_data.str_id == "918C":  # Medallion of Might (Humbaba Mistant and Fury bosses)
            return self.ff12_read_byte(self.get_save_data_address() + 0xA0F, False) >= 2 and \
                self.ff12_read_byte(self.get_save_data_address() + 0xA10, False) >= 2
        elif location_data.str_id == "9056":  # Viera Rendevous
            return self.ff12_read_byte(self.get_save_data_address() + 0x40E, False) >= 6
        elif location_data.str_id == "9058":  # Ktjn Reward
            return self.ff12_read_bit(self.get_save_data_address() + 0x409, 0, False)
        elif location_data.str_id == "906A":  # Jovy Reward
            return self.ff12_read_byte(self.get_save_data_address() + 0x5B8, False) >= 6
        elif location_data.str_id == "906E":  # Outpost Glint 1
            return self.ff12_read_byte(self.get_save_data_address() + 0x691, False) >= 1
        elif location_data.str_id == "906F":  # Outpost Glint 2
            return self.ff12_read_byte(self.get_save_data_address() + 0x692, False) >= 1
        elif location_data.str_id == "9057":  # Outpost Glint 3
            return self.ff12_read_byte(self.get_save_data_address() + 0x693, False) >= 1
        elif location_data.str_id == "9070":  # Outpost Glint 4
            return self.ff12_read_byte(self.get_save_data_address() + 0x694, False) >= 1
        elif location_data.str_id == "9059":  # Outpost Glint 5
            return self.ff12_read_byte(self.get_save_data_address() + 0x695, False) >= 1
        elif location_data.str_id == "908F":  # Footrace
            return self.ff12_read_byte(self.get_save_data_address() + 0x73D, False) >= 1
        elif location_data.str_id == "9194":  # Adrammelech Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA25, False) >= 2
        elif location_data.str_id == "9195":  # Zalera Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA1D, False) >= 2
        elif location_data.str_id == "9196":  # Cuchulainn Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA1C, False) >= 2
        elif location_data.str_id == "9197":  # Zeromus Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA22, False) >= 2
        elif location_data.str_id == "9198":  # Exodus Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA23, False) >= 2
        elif location_data.str_id == "9199":  # Chaos Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA1A, False) >= 2
        elif location_data.str_id == "919A":  # Ultima Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA24, False) >= 2
        elif location_data.str_id == "919B":  # Zodiark Boss
            return self.ff12_read_byte(self.get_save_data_address() + 0xA1B, False) >= 2
        elif 0x9090 <= int(location_data.str_id, 16) <= 0x90AE:  # Trophy Drops
            trophy_index = int(location_data.str_id, 16) - 0x9090
            return self.ff12_read_byte(self.get_save_data_address() + 0xC90 + trophy_index, False) >= 2
        elif 0x90F9 <= int(location_data.str_id, 16) <= 0x90FE:  # Rare Game Defeats (5,10,15,20,25,30)
            return self.ff12_read_byte(self.get_save_data_address() + 0x725, False) > \
                (int(location_data.str_id, 16) - 0x90F9) + 1
        elif location_data.str_id == "90F3":  # Atak >=16
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 71, False) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return self.ff12_read_byte(self.get_save_data_address() + 0xb14, False) == max_trophies and \
                max_trophies >= 16
        elif location_data.str_id == "90F4":  # Atak <16
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 71, False) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return self.ff12_read_byte(self.get_save_data_address() + 0xb14, False) == max_trophies and \
                max_trophies < 16
        elif location_data.str_id == "90F5":  # Blok >=16
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 71, False) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return self.ff12_read_byte(self.get_save_data_address() + 0xb15, False) == max_trophies and \
                max_trophies >= 16
        elif location_data.str_id == "90F6":  # Blok <16
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 71, False) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return self.ff12_read_byte(self.get_save_data_address() + 0xb15, False) == max_trophies and \
                max_trophies < 16
        elif location_data.str_id == "90F7":  # Stok >=16
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 71, False) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return self.ff12_read_byte(self.get_save_data_address() + 0xb16, False) == max_trophies and \
                max_trophies >= 16
        elif location_data.str_id == "90F8":  # Stok <16
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 71, False) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return self.ff12_read_byte(self.get_save_data_address() + 0xb16, False) == max_trophies and \
                max_trophies < 16
        elif 0x90FF <= int(location_data.str_id, 16) <= 0x911D:  # Hunt Club Outfitters
            outfitter_index = int(location_data.str_id, 16) - 0x90FF
            return self.ff12_read_byte(self.get_save_data_address() + 0xAF2 + outfitter_index, False) >= 1

    def get_max_trophies(self):
        return max(
            self.ff12_read_byte(self.get_save_data_address() + 0xb14, False),
            self.ff12_read_byte(self.get_save_data_address() + 0xb15, False),
            self.ff12_read_byte(self.get_save_data_address() + 0xb16, False))

    def get_expected_items(self, item_name: str) -> int:
        count = len([self.ff12_items_received[i] for i in range(len(self.ff12_items_received)) if
                     self.ff12_items_received[i].item == item_data_table[item_name].code and i < self.get_item_index()])

        # Limit key item types to 1 as they're stored as bits
        item_id = item_data_table[item_name].code
        if 0x8000 <= item_id < 0x9000:
            count = min(count, 1)

        if item_name == "Black Orb":
            if self.ff12_read_bit(self.get_save_data_address() + 0x931, 0, False):
                count -= 1
            if self.ff12_read_bit(self.get_save_data_address() + 0x931, 1, False):
                count -= 1
            if self.ff12_read_bit(self.get_save_data_address() + 0x931, 2, False):
                count -= 1
            for i in range(0, 12):
                count -= self.ff12_read_byte(self.get_save_data_address() + 0x960 + i, False)
        if item_name == "Cactus Flower":
            if self.ff12_read_byte(self.get_save_data_address() + 0x68B, False) >= 3:
                return 0
        if item_name == "Tube Fuse":
            if self.get_escape_progress() >= 0x141:
                return 0
        if item_name == "Ring of the Toad":
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 10, False) >= 100:
                return 0
        if item_name == "Silent Urn":
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 35, False) >= 100:
                return 0
        if item_name == "Medallion of Bravery":
            # If in Nabudis, we can't rely on this check until the boss is beaten
            if (not (0x1A5 <= self.get_current_map() <= 0x1BE) or
                    self.ff12_read_byte(self.get_save_data_address() + 0xA0F, False) >= 2):
                return 0
        if item_name == "Medallion of Love":
            # If in Nabudis, we can't rely on this check until the boss is beaten
            if (not (0x1A5 <= self.get_current_map() <= 0x1BE) or
                    self.ff12_read_byte(self.get_save_data_address() + 0xA10, False) >= 2):
                return 0
        if item_name == "Medallion of Might":
            # If in Nabudis, we can't rely on this check until the boss is beaten
            if (not (0x1A5 <= self.get_current_map() <= 0x1BE) or
                    self.ff12_read_byte(self.get_save_data_address() + 0xA1A, False) >= 2):
                return 0
        if item_name == "Lusterless Medallion":
            if (self.ff12_read_byte(self.get_save_data_address() + 0xA0F, False) >= 2 and
                    self.ff12_read_byte(self.get_save_data_address() + 0xA10, False) >= 2):
                return 0
        if item_name == "Stone of the Condemner":
            # If in Miriam, we can't rely on this check until the boss is beaten
            if (not (0x251 <= self.get_current_map() <= 0x26C) or
                    self.ff12_read_byte(self.get_save_data_address() + 0xA22, False) >= 2):
                return 0
        if item_name == "Errmonea Leaf":
            # We can only rely on this check until the Enkelados hunt is completed
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 9, False) >= 100:
                return 0
        if item_name == "Rabbit's Tail":
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 13, False) >= 100:
                return 0
        if item_name == "Ann's Letter":
            if self.ff12_read_byte(self.get_save_data_address() + 0x5A6, False) >= 7:
                return 0
        if item_name == "Serpentwyne Must":
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 8, False) >= 100:
                return 0
        if item_name == "Dull Fragment":
            if self.ff12_read_bit(self.get_save_data_address() + 0x406, 0, False):
                return 0
        if item_name == "Blackened Fragment":
            if self.ff12_read_bit(self.get_save_data_address() + 0x406, 1, False):
                return 0
        if item_name == "Grimy Fragment":
            if self.ff12_read_bit(self.get_save_data_address() + 0x406, 2, False):
                return 0
        if item_name == "Stolen Articles":
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 34, False) >= 100:
                return 0
        if item_name == "Pilika's Diary":
            if self.ff12_read_byte(self.get_save_data_address() + 0x6FD, False) >= 4:
                return 0
        if item_name == "Ring of the Light":
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 30, False) >= 90:
                return 0
        if item_name == "Viera Rucksack":
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 20, False) >= 150:
                return 0
        if item_name == "Moonsilver Medallion":
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 59, False) >= 30:
                return 0
        if item_name == "Broken Key":
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 128 + 5, False) >= 120:
                return 0
        if item_name == "Wind Globe":
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 53, False) >= 60:
                return 0
        if item_name == "Shelled Trophy":
            if self.ff12_read_byte(self.get_save_data_address() + 0x1064 + 71, False) >= 30:
                return 0
        if (item_name == "Sword of the Order" or
                item_name == "Shadestone" or
                item_name == "Sunstone" or
                item_name == "Dragon Scale"):
            return 0  # Can't rely on checking these for missing items
        if item_data_table["Belias"].code <= item_data_table[item_name].code <= item_data_table["Second Board"].code:
            return 0  # Not checking espers/second board
        return max(count, 0)

    async def give_items(self):
        last_end_time = time.time()
        while not self.exit_event.is_set() and self.ff12connected and self.server_connected:
            if time.time() - last_end_time < 0.5:
                await asyncio.sleep(0.1)
                continue
            try:
                start_index = self.get_item_index()
                stop_index = len(self.ff12_items_received)
                for index in range(start_index, stop_index):
                    if not self.is_in_game():
                        break
                    item = self.ff12_items_received[index]
                    await self.give_item(item.item, item_data_table[inv_item_table[item.item]].amount)
                    self.set_item_index(index + 1)

            except Exception as e:
                if self.ff12connected:
                    self.ff12connected = False
                logger.info(e)
            last_end_time = time.time()

    async def give_item(self, item_id: int, count: int):
        async with self.item_lock:
            # If it's gil, handle it separately
            if item_data_table[inv_item_table[item_id]].code >= item_data_table["1 Gil"].code:
                current_gil = self.ff12_read_int(0x02044288)
                self.ff12_write_int(0x02044288, current_gil + count)
            else:
                int_id = item_id - FF12OW_BASE_ID
                current_count = self.get_item_count(inv_item_table[item_id])
                # Limit to 99
                new_count = min(current_count + count, 99)
                if int_id < 0x1000:  # Normal items
                    self.ff12_write_short(0x02097054 + int_id * 2, new_count)
                elif int_id < 0x2000:  # Equipment
                    self.ff12_write_short(0x020970D4 + (int_id - 0x1000) * 2, new_count)
                elif 0x2000 <= int_id < 0x3000:  # Loot items
                    self.ff12_write_short(0x0209741C + (int_id - 0x2000) * 2, new_count)
                elif 0x8000 <= int_id < 0x9000:  # Key items
                    byte_index = (int_id - 0x8000) // 8
                    bit_index = (int_id - 0x8000) % 8
                    self.ff12_write_bit(0x0209784C + byte_index, bit_index, True)
                elif 0xC000 <= int_id < 0xD000:  # Espers
                    byte_index = (int_id - 0xC000) // 8
                    bit_index = (int_id - 0xC000) % 8
                    self.ff12_write_bit(0x0209788C + byte_index, bit_index, True)
                elif 0x3000 <= int_id < 0x4000:  # Magicks
                    byte_index = (int_id - 0x3000) // 8
                    bit_index = (int_id - 0x3000) % 8
                    self.ff12_write_bit(0x0209781C + byte_index, bit_index, True)
                elif 0x4000 <= int_id < 0x5000:  # Technicks
                    byte_index = (int_id - 0x4000) // 8
                    bit_index = (int_id - 0x4000) % 8
                    self.ff12_write_bit(0x02097828 + byte_index, bit_index, True)
                else:
                    raise Exception("Invalid item ID when giving items: " + str(item_id))
                self.add_to_sort(item_id)

    def add_to_sort(self, item_id: int):
        int_id = item_id - FF12OW_BASE_ID
        if int_id < 0x1000:  # Normal items
            sort_type = 0
        elif int_id <= 0x10C7:  # Weapons
            sort_type = 1
        elif 0x10C8 <= int_id <= 0x1153:  # Armor
            sort_type = 2
        elif 0x1154 <= int_id <= 0x1183:  # Accessories
            sort_type = 3
        elif 0x1184 <= int_id <= 0x11A3:  # Ammo
            sort_type = 4
        elif 0x4000 <= int_id <= 0x4FFF:  # Tecknicks
            sort_type = 5
        elif 0x3000 <= int_id <= 0x3FFF:  # Magicks
            sort_type = 6
        elif 0x8000 <= int_id <= 0x8FFF:  # Key Items
            sort_type = 7
        elif 0x2000 <= int_id <= 0x2FFF:  # Loot
            sort_type = 8
        else:
            return
        sort_list = self.get_sort_list(sort_type)
        if int_id not in sort_list:
            sort_list.append(int_id)
            self.set_sort_list(sort_type, sort_list)

    def get_sort_list(self, type_index: int) -> List[int]:
        sort_list = []
        max_count = self.ff12_read_int(sort_count_addresses[type_index])
        for i in range(0, max_count):
            item_id = self.ff12_read_short(sort_start_addresses[type_index] + i * 2)
            if item_id != 0xFFFF:
                sort_list.append(item_id)
            else:
                break
        return sort_list

    def set_sort_list(self, type_index: int, sort_list: List[int]):
        self.ff12_write_int(sort_count_addresses[type_index], len(sort_list))
        for i in range(0, len(sort_list)):
            self.ff12_write_short(sort_start_addresses[type_index] + i * 2, sort_list[i])

    async def check_missing_items(self):
        try:
            # Cannot check for missing items if not given all expected items
            if self.get_item_index() < len(self.ff12_items_received):
                return

            for item in item_data_table.keys():
                missing_count = self.get_expected_items(item) - self.get_item_count(item)
                if (item_data_table[item].classification & ItemClassification.progression and
                        missing_count > 0):
                    logger.info("Adding missing item: " + str(missing_count) + " " + item)
                    await self.give_item(item_data_table[item].code,
                                         missing_count)
        except Exception as e:
            if self.ff12connected:
                self.ff12connected = False
            logger.info(e)

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class FF12OpenWorldManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago FF12 Open World Client"

        self.ui = FF12OpenWorldManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def ff12_write_bit(self, byte_index: int, bit_index: int, value: bool,use_base=True):
        byte = self.ff12_read_byte(byte_index, use_base)
        if value:
            byte |= 1 << bit_index
        else:
            byte &= ~(1 << bit_index)
        self.ff12_write_byte(byte_index, byte, use_base)


async def ff12_watcher(ctx: FF12OpenWorldContext):
    while not ctx.exit_event.is_set():
        try:
            if ctx.ff12connected and ctx.server_connected:
                if ctx.check_loc_task is None or ctx.check_loc_task.done():
                    ctx.check_loc_task = asyncio.create_task(ctx.check_locations())

                if ctx.give_items_task is None or ctx.give_items_task.done():
                    ctx.give_items_task = asyncio.create_task(ctx.give_items())
            elif not ctx.ff12connected and ctx.server_connected:
                logger.info("Game Connection lost. waiting 15 seconds until trying to reconnect.")
                ctx.ff12 = None
                while not ctx.ff12connected and ctx.server_connected:
                    await asyncio.sleep(15)
                    ctx.find_game()
        except Exception as e:
            if ctx.ff12connected:
                ctx.ff12connected = False
            logger.info(e)
        await asyncio.sleep(0.2)

    if ctx.check_loc_task is not None:
        ctx.check_loc_task.cancel()
        ctx.check_loc_task = None
    if ctx.give_items_task is not None:
        ctx.give_items_task.cancel()
        ctx.give_items_task = None


def launch():
    async def main(args):
        ctx = FF12OpenWorldContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            ff12_watcher(ctx), name="FF12ProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="FF12 Open World Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()

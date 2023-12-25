import logging
import struct
import sys
import time
import typing
from base64 import b64encode
from struct import unpack, pack
from typing import Any, TYPE_CHECKING
# TODO: REMOVE ASAP
# This imports the bizhawk apworld if it's not already imported. This code block should be removed for a PR.
if "worlds._bizhawk" not in sys.modules:
    import importlib.util
    import os
    import zipimport

    bh_apworld_path = os.path.join(os.path.dirname(sys.modules["worlds"].__file__), "_bizhawk.apworld")
    if os.path.isfile(bh_apworld_path):
        importer = zipimport.zipimporter(bh_apworld_path)
        spec = importer.find_spec(os.path.basename(bh_apworld_path).rsplit(".", 1)[0])
        mod = importlib.util.module_from_spec(spec)
        mod.__package__ = f"worlds.{mod.__package__}"
        mod.__name__ = f"worlds.{mod.__name__}"
        sys.modules[mod.__name__] = mod
        importer.exec_module(mod)
    elif not os.path.isdir(os.path.splitext(bh_apworld_path)[0]):
        logging.error("Did not find _bizhawk.apworld required to play Mega Man 2.")

from NetUtils import ClientStatus, color
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = Any

k64_logger = logging.getLogger("K64")

ability_to_bit = {
    0x640001: 0,
    0x640002: 1,
    0x640003: 2,
    0x640004: 3,
    0x640005: 4,
    0x640006: 5,
    0x640007: 6,
    0x640200: 7,
    0x640201: 8,
    0x640202: 9,
    0x640203: 10,
    0x640204: 11,
    0x640205: 12,
    0x640206: 13,
    0x640207: 14,
    0x640208: 15,
    0x640209: 16,
    0x64020A: 17,
    0x64020B: 18,
    0x64020C: 19,
    0x64020D: 20,
    0x64020E: 21,
    0x64020F: 22,
    0x640210: 23,
    0x640211: 24,
    0x640212: 25,
    0x640213: 26,
    0x640214: 27,
    0x640215: 28,
    0x640216: 29,
    0x640217: 30,
    0x640218: 31,
    0x640219: 32,
    0x64021A: 33,
    0x64021B: 34,
}

power_combos = {
    (1, 1): 7,
    (1, 2): 8,
    (1, 3): 9,
    (1, 4): 10,
    (1, 5): 11,
    (1, 6): 12,
    (1, 7): 13,
    (2, 2): 14,
    (2, 3): 15,
    (2, 4): 16,
    (2, 5): 17,
    (2, 6): 18,
    (2, 7): 19,
    (3, 3): 20,
    (3, 4): 21,
    (3, 5): 22,
    (3, 6): 23,
    (3, 7): 24,
    (4, 4): 25,
    (4, 5): 26,
    (4, 6): 27,
    (4, 7): 28,
    (5, 5): 29,
    (5, 6): 30,
    (5, 7): 31,
    (6, 6): 32,
    (6, 7): 33,
    (7, 7): 34,
}

stage_to_byte = {
    1: [0,1,2],
    2: [6,7,8,9],
    3: [12,13,14,15],
    4: [18,19,20,21],
    5: [24,25,26,27],
    6: [30,31,32],
}

K64_IS_DEMO = 0x3387B2
K64_SAVE_ADDRESS = 0xD6B00
K64_BOSS_CRYSTALS = K64_SAVE_ADDRESS + 0xC0
K64_CRYSTAL_ARRAY = K64_SAVE_ADDRESS + 0xC8
K64_STAGE_STATUSES = K64_SAVE_ADDRESS + 0xE0
K64_ENEMY_CARDS = K64_SAVE_ADDRESS + 0x110
K64_COPY_ABILITY = K64_SAVE_ADDRESS + 0x168
K64_CRYSTAL_ADDRESS = K64_SAVE_ADDRESS + 0x170
K64_RECV_INDEX = K64_SAVE_ADDRESS + 0x174
K64_KIRBY_HEALTH_VISUAL = K64_SAVE_ADDRESS + 0x38C

K64_SPLIT_POWER_COMBO = 0x1FFF220
K64_DEATHLINK = 0x1FFF221
K64_LEVEL_ADDRESS = 0x1FFF230


class K64Client(BizHawkClient):
    game = "Kirby 64 - The Crystal Shards"
    system = "N64"
    patch_suffix = ".apk64cs"
    death_link: typing.Optional[bool] = None
    rom: typing.Optional[bytes] = None
    levels: typing.Optional[typing.Dict[int, typing.List[int]]] = None
    split_power_combos: typing.Optional[bool] = None

    def interpret_copy_ability(self, current, new_ability):
        if self.split_power_combos:
            # simple, just allow the new power combo
            xorVal = 1 << ability_to_bit[new_ability]
            output = current | (current ^ xorVal)
        else:
            # complex, we need to figure out what abilities they are allowed to have
            # since we have the currently unlocked abilities,and they can only get abilities related to the newly
            # obtained ability, we can just loop once
            shifter = 1
            copy_abilties = {}
            for i in range(1, 8):
                copy_abilties[i] = shifter & current
                shifter <<= 1
            new = new_ability & 0xFF
            copy_abilties[new] = 1
            output = current | 1 << new - 1
            for i in range(1, 8):
                if copy_abilties[i]:
                    if i < new:
                        output |= (1 << power_combos[i, new])
                    else:
                        output |= (1 << power_combos[new, i])

        return K64_COPY_ABILITY, struct.pack(">Q", output), "RDRAM"

    async def deathlink_kill_player(self, ctx) -> None:
        # what a mess
        # they store his HP as a float...
        # there's 7 possible values...
        # and he only dies after taking a hit at 0 hp
        pass

    async def set_auth(self, ctx: BizHawkClientContext) -> None:
        if self.rom:
            ctx.auth = b64encode(self.rom).decode()

    async def validate_rom(self, ctx) -> bool:
        from worlds._bizhawk import RequestFailedError, read

        try:
            game_name = ((await read(ctx.bizhawk_ctx, [(0x1FFF200, 21, "ROM")]))[0])
            if game_name[:3] != b"K64":
                return False
        except UnicodeDecodeError:
            return False
        except RequestFailedError:
            return False  # Should verify on the next pass
        ctx.game = self.game
        self.rom = game_name
        ctx.items_handling = 0b111
        return True

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        from worlds._bizhawk import read, write

        if ctx.server is None:
            return

        if ctx.slot is None:
            await ctx.send_connect(name=ctx.auth)

        if ctx.slot_data is None:
            return

        if self.levels is None:
            levels = (await read(ctx.bizhawk_ctx, [
                (K64_LEVEL_ADDRESS, 56, "ROM")
            ]))[0]
            self.levels = {}
            level_counter = 0
            for level, stage_num in zip(range(1, 7), (4, 5, 5, 5, 5, 4)):
                self.levels[level] = []
                for i in range(stage_num):
                    self.levels[level].append(struct.unpack(">H", levels[level_counter:level_counter+2])[0])
                    level_counter += 2

        if self.death_link is None:
            deathlink = (await read(ctx.bizhawk_ctx, [
                (K64_DEATHLINK, 1, "ROM")
            ]))[0]

            self.death_link = bool(deathlink[0])

        if self.split_power_combos is None:
            split_power_combos = (await read(ctx.bizhawk_ctx, [
                (K64_SPLIT_POWER_COMBO, 1, "ROM")
            ]))[0]

            self.split_power_combos = bool(split_power_combos[0])

        halken, is_demo, stage_array, boss_crystals, crystal_array,\
        copy_ability, crystals, recv_index, health = await read(ctx.bizhawk_ctx, [
            (K64_SAVE_ADDRESS, 16, "RDRAM"),
            (K64_IS_DEMO, 4, "RDRAM"),
            (K64_STAGE_STATUSES, 42, "RDRAM"),
            (K64_BOSS_CRYSTALS, 8, "RDRAM"),
            (K64_CRYSTAL_ARRAY, 24, "RDRAM"),
            (K64_COPY_ABILITY, 8, "RDRAM"),
            (K64_CRYSTAL_ADDRESS, 4, "RDRAM"),
            (K64_RECV_INDEX, 4, "RDRAM"),
            (K64_KIRBY_HEALTH_VISUAL, 4, "RDRAM")
        ])

        if halken != b'-HALKEN--KIRBY4-':
            return

        if boss_crystals[6] != 0:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        writes = []

        recv_count = struct.unpack(">I",recv_index)[0]
        if recv_count < len(ctx.items_received):
            item = ctx.items_received[recv_count]
            recv_count += 1

            writes.append((K64_RECV_INDEX, struct.pack(">I", recv_count), "RDRAM"))
            if item.item in ability_to_bit:
                writes.append(self.interpret_copy_ability(struct.unpack(">Q", copy_ability)[0], item.item))
            elif item.item & 0x100:
                pass
            elif item.item == 0x640020:
                # crystal shard
                writes.append((K64_CRYSTAL_ADDRESS, struct.pack(">I", struct.unpack(">I", crystals)[0] + 1), "RDRAM"))


        await write(ctx.bizhawk_ctx, writes)
        new_checks = []

        for i, crystal in zip(range(6), boss_crystals):
            # purposely leave out the last two
            loc_id = i + 0x640200
            if loc_id not in ctx.checked_locations and crystal != 0x00:
                new_checks.append(loc_id)

        # check stages
        for level, stage_num in zip(range(1, 7), (3, 4, 4, 4, 4, 3)):
            for stage in range(stage_num):
                loc_id = 0x640000 + self.levels[level][stage]
                if loc_id not in ctx.checked_locations and stage_array[stage_to_byte[level][stage]] == 0x02:
                    new_checks.append(loc_id)

        # check crystals
        current_crystal = 0x640101
        for level, stage_num in zip(range(6), (3, 4, 4, 4, 4, 3)):
            level_crystals = struct.unpack("I", crystal_array[level*4:(level*4)+4])[0]
            for stage in range(stage_num):
                shifter = (stage * 8)
                for i in range(3):
                    if level_crystals & (1 << shifter) and current_crystal not in ctx.checked_locations:
                        new_checks.append(current_crystal)
                    shifter += 1
                    current_crystal += 1

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names[new_check_id]
            k64_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

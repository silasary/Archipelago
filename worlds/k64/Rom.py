import pkgutil
import typing
from pkgutil import get_data
from random import Random

import Utils
from typing import Optional, Dict, List
import hashlib
import os
import struct

import settings
from BaseClasses import MultiWorld
from worlds.Files import APDeltaPatch
import bsdiff4

if typing.TYPE_CHECKING:
    from . import K64World

K64UHASH = "d33e4254336383a17ff4728360562ada"

stage_locations = {
    0x640001: 0x800D01A4,
    0x640002: 0x800D027C,
    0x640003: 0x800D039C,
    0x640004: 0x800D0570,
    0x640005: 0x800D066C,
    0x640006: 0x800D078C,
    0x640007: 0x800D08F4,
    0x640008: 0x800D0AA4,
    0x640009: 0x800D0BC4,
    0x64000A: 0x800D0CE4,
    0x64000B: 0x800D0E28,
    0x64000C: 0x800D0F90,
    0x64000D: 0x800D10B0,
    0x64000E: 0x800D11F4,
    0x64000F: 0x800D12F0,
    0x640010: 0x800D147C,
    0x640011: 0x800D159C,
    0x640012: 0x800D16BC,
    0x640013: 0x800D1824,
    0x640014: 0x800D19B0,
    0x640015: 0x800D1A64,
    0x640016: 0x800D1B84,
    0x640200: 0x800D0528,
    0x640201: 0x800D0A5C,
    0x640202: 0x800D0F48,
    0x640203: 0x800D1434,
    0x640204: 0x800D1968,
    0x640205: 0x800D1EE4,
}

area_world_level = {
    0x640001: [30690096, 30693872, 30689808, 30690384, 30690816, 30701168, 30694016, 30690960, 30701024, 30704348,
               30705448, 30701600, 30701456, 30693728, 30704204, 30689952, 30690672, 30690528, 30700880, 30700736,
               30690240, 30704492, 30701312],
    0x640002: [30712440, 30724988, 30725132, 30728928, 30729072, 30732716, 30732860, 30733004, 30735924, 30737984],
    0x640003: [30748128, 30754076, 30754220, 30758492, 30758636, 30763032, 30763176, 30763320, 30769572, 30769716,
               30770580, 30770724, 30774044, 30774188, 30774332, 30776100, 30776244, 30785984, 30786128, 30789880,
               30790456],
    0x640004: [30805412, 30816272, 30816416, 30816560, 30819808, 30819952, 30820096, 30829908, 30830196, 30830340,
               30837996],
    0x640005: [30849252, 30861572, 30861716, 30869612, 30869756, 30879988, 30880132, 30890532, 30890676, 30904012,
               30904156],
    0x640006: [30920016, 30920160, 30928440, 30928728, 30928872, 30929160, 30929304, 30929592, 30933000, 30933144,
               30939848, 30940136, 30940280, 30940424, 30940712, 30941000, 30941144, 30941288, 30951308, 30952172,
               30959580, 30966588, 30966732, 30974260, 30974404],
    0x640007: [30982036, 30982180, 30985128, 30985272, 30988224, 30988368, 30990624, 30990768, 30990912, 30993164,
               30993308, 30993452, 31000676, 31000820, 31000964, 31001108, 31004292, 31004436, 31008204, 31008348],
    0x640008: [31022088, 31034344, 31034488, 31040956, 31041100, 31050312, 31050456, 31054492, 31054636, 31066796,
               31066940],
    0x640009: [31077576, 31082528, 31082672, 31090520, 31090664, 31106228, 31106516, 31123908, 31139768, 31139912],
    0x64000A: [31150720, 31161348, 31161492, 31167552, 31167696, 31176928, 31177504, 31177648, 31183844, 31183988,
               31187616, 31187760, 31193628, 31193772, 31194204],
    0x64000B: [31203080, 31211428, 31211572, 31230960, 31231104, 31256156, 31256300, 31265032, 31265176, 31273856,
               31274288],
    0x64000C: [31290052, 31298360, 31298504, 31305064, 31305208, 31310780, 31310924, 31315608, 31315752, 31326304,
               31326448],
    0x64000D: [31329828, 31329972, 31372324, 31387928, 31388072, 31400104, 31400248, 31404480, 31404768, 31410396,
               31410540],
    0x64000E: [31426756, 31443220, 31443364, 31447048, 31447192, 31459680, 31459824, 31476972, 31477116],
    0x64000F: [31485080, 31492116, 31492260, 31510172, 31510316, 31533856, 31534000, 31540760, 31540904, 31559008,
               31559152, 31583176, 31583320, 31583464],
    0x640010: [31595652, 31600644, 31600788, 31623348, 31632160, 31642964, 31643108, 31662080, 31662224],
    0x640011: [31669204, 31669348, 31681280, 31686752, 31686896, 31687040, 31701228, 31701372, 31714292, 31714436,
               31714580, 31719120, 31719264],
    0x640012: [31723272, 31730888, 31731032, 31743380, 31748756, 31748900, 31750880, 31751024, 31752848, 31752992,
               31766916, 31767060, 31787144, 31787288],
    0x640013: [31791688, 31791832, 31800648, 31800792, 31800936, 31819588, 31835136, 31842760, 31842904, 31851216,
               31851360, 31859544, 31859688],
    0x640014: [31874072, 31876912, 31877056, 31883920, 31884064],
    0x640015: [31889812, 31889956, 31893380, 31893524, 31893668, 31905416, 31905560, 31924940, 31925084, 31946908,
               31947052, 31950488, 31950632, 31950776],
    0x640016: [31953996, 31956072, 31956216, 31962800, 31962944, 31965120, 31965264, 31971848, 31971992, 31974524,
               31974668, 31981288, 31981432, 31983608, 31983752, 31990336, 31990480, 31992612, 31992756, 31997212,
               31997356],
}


class RomData:
    def __init__(self, file: str, name: typing.Optional[str] = None):
        self.file = bytearray()
        self.read_from_file(file)
        self.name = name

    def read_byte(self, offset: int):
        return self.file[offset]

    def read_bytes(self, offset: int, length: int):
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int):
        self.file[offset] = value

    def write_bytes(self, offset: int, values):
        self.file[offset:offset + len(values)] = values

    def write_to_file(self, file: str):
        with open(file, 'wb') as outfile:
            outfile.write(self.file)

    def read_from_file(self, file: str):
        with open(file, 'rb') as stream:
            self.file = bytearray(stream.read())

    def apply_basepatch(self, patch: bytes):
        self.file = bytearray(bsdiff4.patch(bytes(self.file), patch))


class K64DeltaPatch(APDeltaPatch):
    hash = [K64UHASH]
    game = "Kirby 64 - The Crystal Shards"
    patch_file_ending = ".apk64cs"
    result_file_ending = ".z64"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def patch_rom(world: "K64World", player: int, rom: RomData):
    rom.apply_basepatch(pkgutil.get_data(__name__, os.path.join("data", "k64basepatch.bsdiff4")))

    # now just apply slot data
    # first stage shuffle
    if world.stage_shuffle_enabled:
        for i in range(1, 7):
            stages = [stage_locations[world.player_levels[i][stage]] if stage < len(world.player_levels[i]) else 0
                      for stage in range(5)]
            rom.write_bytes(0x7A1E8 + ((i - 1) * 48), struct.pack(">IIIII", *stages))
            for j, stage in enumerate(world.player_levels[i]):
                target = struct.pack("BB", i - 1, j)
                if stage in area_world_level:
                    for ptr in area_world_level[stage]:
                        rom.write_bytes(ptr, target)

    rom.write_bytes(0x1FFF100, world.boss_requirements)

    from Utils import __version__
    rom.name = bytearray(f'K64{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x1FFF200, rom.name)

    rom.write_byte(0x1FFF220, world.options.split_power_combos.value)
    rom.write_byte(0x1FFF221, world.options.death_link.value)
    level_counter = 0
    for level in world.player_levels:
        for stage in world.player_levels[level]:
            rom.write_bytes(0x1FFF230 + level_counter, struct.pack(">H", stage & 0xFFFF))
            level_counter += 2


def get_base_rom_bytes() -> bytes:
    rom_file: str = get_base_rom_path()
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        base_rom_bytes = bytes(Utils.read_snes_rom(open(rom_file, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {K64UHASH}:
            raise Exception("Supplied Base Rom does not match known MD5 for US or JP release. "
                            "Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = settings.get_settings()
    if not file_name:
        file_name = options["k64_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name

import pkgutil
import typing
from pkgutil import get_data
from random import Random

import Utils
from typing import Optional, Dict, List, Tuple
import hashlib
import os
import struct

import settings
from BaseClasses import MultiWorld
from worlds.Files import APDeltaPatch
import bsdiff4

from .Aesthetics import kirby_target_palettes, get_palette_bytes, get_kirby_palette

if typing.TYPE_CHECKING:
    from . import K64World

K64UHASH = "d33e4254336383a17ff4728360562ada"

stage_locations: Dict[int, Tuple[int, int]] = {
    0x640001: (0, 0),
    0x640002: (0, 1),
    0x640003: (0, 2),
    0x640004: (1, 0),
    0x640005: (1, 1),
    0x640006: (1, 2),
    0x640007: (1, 3),
    0x640008: (2, 0),
    0x640009: (2, 1),
    0x64000A: (2, 2),
    0x64000B: (2, 3),
    0x64000C: (3, 0),
    0x64000D: (3, 1),
    0x64000E: (3, 2),
    0x64000F: (3, 3),
    0x640010: (4, 0),
    0x640011: (4, 1),
    0x640012: (4, 2),
    0x640013: (4, 3),
    0x640014: (5, 0),
    0x640015: (5, 1),
    0x640016: (5, 2),
    0x640200: (0, 3),
    0x640201: (1, 4),
    0x640202: (2, 4),
    0x640203: (3, 4),
    0x640204: (4, 4),
    0x640205: (5, 3),
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
            stages = [stage_locations[world.player_levels[i][stage]] if stage < len(world.player_levels[i]) - 1
                      else (-1, -1) for stage in range(8)]
            rom.write_bytes(0x1FFF300 + ((i - 1) * 48), struct.pack(">iiiiiiii", [stage[0] for stage in stages]))
            rom.write_bytes(0x1FFF450 + ((i - 1) * 48), struct.pack(">iiiiiiii", [stage[1] for stage in stages]))

    rom.write_bytes(0x1FFF100, world.boss_requirements)

    palette = get_palette_bytes(get_kirby_palette(world), [f"{i}" for i in range(1, 16)])
    for target in kirby_target_palettes:
        rom.write_bytes(target, palette)

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

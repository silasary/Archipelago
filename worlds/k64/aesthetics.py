import struct
from .options import KirbyFlavorPreset
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import K64World
    from .rom import K64ProcedurePatch

kirby_flavor_presets = {
    13: {
         "1": "000008",
         "2": "5A4AF6",
         "3": "52416A",
         "4": "F6F6F6",
         "5": "B4A4F6",
         "6": "626AE6",
         "7": "5A0800",
         "8": "A48BEE",
         "9": "733141",
         "10": "D5D5D5",
         "11": "292031",
         "12": "9C948B",
         "13": "D50000",
         "14": "6A628B",
         "15": "8B83BD",
         "16": "4669FF",
         "17": "781CFF",
    },
}

kirby_target_palettes = [
    0x614818,
    0x859A06,
    0xA80832,
    0xB6B674,
    0xB6D8F4,
    0xDC7344,
    0xDD03A4,
    0xED0D14,
]

kirby_24bit_targets = [
    (0x5AF9C4, "5"),
    (0x5AFAD4, "5"),
    (0x5B3AF4, "5"),
    (0x5B3C0C, "5"),
    (0x7E285C, "5"),
    (0x7E29CC, "5"),
    (0x7E2B14, "5"),
    (0x7E2C8C, "5"),
    (0x7E5854, "5"),
    (0x7E5BB4, "5"),
    (0x7E5F94, "5"),
    (0x7E620C, "5"),
    (0x7E634C, "5"),
    (0x7E9C1C, "5"),
    (0x7E9D94, "5"),
    (0x7E9F04, "5"),
    (0x7EA074, "5"),
    (0x7F4E6C, "5"),
    (0x7F6A8C, "5"),
    (0x7F973C, "5"),
    (0x7F9904, "5"),
    (0x80410C, "5"),
    (0x80422C, "5"),
    (0x80AC8C, "5"),
    (0x80B19C, "5"),
    (0x80B2BC, "5"),
    (0x81519C, "5"),
    (0x8152BC, "5"),
    (0x815E2C, "5"),
    (0x8171BC, "5"),
    (0x828ED4, "5"),
    (0x828FF4, "5"),
    (0x848E04, "5"),
    (0x9C9BFC, "5"),
    (0x9CC89C, "5"),
    (0x9CC914, "5"),
    (0xD27A54, "5"),
    (0xD27E2C, "5"),
    (0xD27FEC, "5"),
    (0xD28134, "5"),
    (0x7E5F4C, "16"),
    (0x7E6124, "16"),
    (0x817174, "16"),
    (0xD27DD4, "16"),
    (0x5AEE74, "17"),
    (0x5AEF84, "17"),
    (0x5B34B4, "17"),
    (0x5B35CC, "17"),
    (0x7E1A84, "17"),
    (0x7E1C44, "17"),
    (0x7E1D8C, "17"),
    (0x7E1F4C, "17"),
    (0x7E5374, "17"),
    (0x7E550C, "17"),
    (0x7E8E54, "17"),
    (0x7E9014, "17"),
    (0x7E9144, "17"),
    (0x7E9304, "17"),
    (0x7F520C, "17"),
    (0x7F5414, "17"),
    (0x7F6734, "17"),
    (0x7F68E4, "17"),
    (0x7F9884, "17"),
    (0x80374C, "17"),
    (0x803864, "17"),
    (0x80AA5C, "17"),
    (0x80AB74, "17"),
    (0x80DA9C, "17"),
    (0x8111EC, "17"),
    (0x811394, "17"),
    (0x812B3C, "17"),
    (0x814B34, "17"),
    (0x814C4C, "17"),
    (0x816CB4, "17"),
    (0x8287E4, "17"),
    (0x828984, "17"),
    (0x82AAA4, "17"),
    (0x82AC54, "17"),
    (0x849994, "17"),
    (0x97681C, "17"),
    (0x9769CC, "17"),
    (0x9C959C, "17"),
    (0x9CC6CC, "17"),
    (0x9CC744, "17"),
    (0xBE0B94, "17"),
    (0xBE0F74, "17"),
    (0xBE3DB4, "17"),
    (0xBE3FB4, "17"),
    (0xBE6004, "17"),
    (0xBE6164, "17"),
    (0xBE7A44, "17"),
    (0xBE7B34, "17"),
    (0xD27744, "17"),
    (0xD278CC, "17"),
]


def get_kirby_palette(world):
    palette = world.options.kirby_flavor_preset.value
    if palette == KirbyFlavorPreset.option_custom:
        return world.options.kirby_flavor.value
    return kirby_flavor_presets.get(palette, None)


def rgb888_to_rgba5551(red, green, blue) -> bytes:
    red = red >> 3
    green = green >> 3
    blue = blue >> 3
    outcol = (red << 11) + (green << 6) + (blue << 1) + 1
    return struct.pack(">H", outcol)


def get_palette_bytes(palette, target):
    output_data = bytearray()
    for color in target:
        hexcol = palette[color]
        if hexcol.startswith("#"):
            hexcol = hexcol.replace("#", "")
        colint = int(hexcol, 16)
        col = ((colint & 0xFF0000) >> 16, (colint & 0xFF00) >> 8, colint & 0xFF)
        byte_data = rgb888_to_rgba5551(col[0], col[1], col[2])
        output_data.extend(bytearray(byte_data))
    return output_data


def write_aesthetics(world: "K64World", patch: "K64ProcedurePatch"):
    if world.options.kirby_flavor_preset != world.options.kirby_flavor_preset.default:
        str_pal = get_kirby_palette(world)
        palette = get_palette_bytes(str_pal, [f"{i}" for i in range(1, 16)])
        for target in kirby_target_palettes:
            patch.write_bytes(target, palette)

        for addr, color in kirby_24bit_targets:
            hexcol = str_pal[color]
            if hexcol.startswith("#"):
                hexcol = hexcol.replace("#", "")
            colint = int(hexcol, 16)
            patch.write_bytes(addr, colint.to_bytes(3, "big"))

import struct
from .options import KirbyFlavorPreset
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import K64World
    from .rom import K64ProcedurePatch

kirby_flavor_presets = {
    1: {
        "1": "080000",
        "2": "FE67AC",
        "3": "962656",
        "4": "FCFFFF",
        "5": "FF99C1",
        "6": "DD2638",
        "7": "0A1437",
        "8": "D55E86",
        "9": "530011",
        "10": "D8E6FF",
        "11": "0D111D",
        "12": "F2C6D7",
        "13": "1A44D6",
        "14": "9D4B7C",
        "15": "C66A99",
        "16": "5D0F1C",
        "17": "F12153"
    },
    3: {
        "0": "FFB5B5",
        "1": "000800",
        "2": "FF7384",
        "3": "213A84",
        "4": "F7F7F7",
        "5": "94B5FF",
        "6": "EF6B7B",
        "7": "00085A",
        "8": "7B94DE",
        "9": "294A94",
        "10": "D6D6D6",
        "11": "312129",
        "12": "8C949C",
        "13": "0000D6",
        "14": "6384CE",
        "15": "4A6BCE",
        "16": "D9CDFF",
        "17": "3333B3"
    },
    4: {
        "0": "FFB5B5",
        "1": "000800",
        "2": "FF734A",
        "3": "0945A0",
        "4": "F7F7F7",
        "5": "FFD673",
        "6": "FF6342",
        "7": "00085A",
        "8": "F7AD4A",
        "9": "423173",
        "10": "D6D6D6",
        "11": "312129",
        "12": "8C949C",
        "13": "0000D6",
        "14": "BD7321",
        "15": "DE9C31",
        "16": "FFF4C2",
        "17": "FF8000"
    },
    5: {
        "0": "FFB5B5",
        "1": "000800",
        "2": "FF8473",
        "3": "3A6321",
        "4": "F7F7F7",
        "5": "94D66B",
        "6": "EF7B5A",
        "7": "00085A",
        "8": "84C55A",
        "9": "423173",
        "10": "D6D6D6",
        "11": "312129",
        "12": "8C949C",
        "13": "0000D6",
        "14": "63A53A",
        "15": "5A8C42",
        "16": "B6FCBE",
        "17": "665C33"
    },
    12: {
        "1": "080000",
        "2": "949400",
        "3": "3e6806",
        "4": "F6F6F6",
        "5": "96f11d",
        "6": "b8b800",
        "7": "2d2d2d",
        "8": "86e10e",
        "9": "525252",
        "10": "D5D5D5",
        "11": "1e3203",
        "12": "949494",
        "13": "6b6b6b",
        "14": "599509",
        "15": "77c70c",
        "16": "ffff00",
        "17": "747400",
    },
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
    14: {
        "1": "000008",
        "2": "E6298A",
        "3": "008B8F",
        "4": "C4CED4",
        "5": "75C7C1",
        "6": "E84053",
        "7": "04292B",
        "8": "3AA6A4",
        "9": "430B1D",
        "10": "BEC9D0",
        "11": "121415",
        "12": "2F3436",
        "13": "5DCCD9",
        "14": "00ADC9",
        "15": "2EB8C6",
        "16": "FBDDCD",
        "17": "494E59",
    },
    15: {
        "1": "234331",
        "10": "D3E29A",
        "11": "234331",
        "12": "537A3E",
        "13": "234331",
        "14": "537A3E",
        "15": "537A3E",
        "16": "A7BA4A",
        "17": "234331",
        "2": "537A3E",
        "3": "234331",
        "4": "D3E29A",
        "5": "A7BA4A",
        "6": "537A3E",
        "7": "234331",
        "8": "A7BA4A",
        "9": "234331"
    },
    16: {
        "1": "080000",
        "2": "F64A5A",
        "3": "005B18",
        "4": "F6F6F6",
        "5": "45EF64",
        "6": "E66A62",
        "7": "00085A",
        "8": "45EF64",
        "9": "640A00",
        "10": "D5D5D5",
        "11": "311F29",
        "12": "8B949C",
        "13": "0000D5",
        "14": "8B626A",
        "15": "45EF64",
        "16": "FFAC8F",
        "17": "005B18",
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
    (0x9CC898, "5"),
    (0x9CC910, "5"),
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
    (0x848994, "17"),
    (0x97681C, "17"),
    (0x9769CC, "17"),
    (0x9C959C, "17"),
    (0x9CC6C8, "17"),
    (0x9CC740, "17"),
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

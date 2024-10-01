import struct
from .options import KirbyFlavorPreset

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
    },
}

kirby_target_palettes = [
    0x614816,
    0x859A04,
    0xA80830,
    0xB6B672,
    0xB6D8F2,
    0xDC7342,
    0xDD03A2,
    0xED0D12,
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

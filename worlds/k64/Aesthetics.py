import struct
from .Options import KirbyFlavorPreset

kirby_flavor_presets = {
    13: {
        "1": "7C73B0",
        "2": "CACAE7",
        "3": "7B7BA8",
        "4": "5F5FA7",
        "5": "B57EDC",
        "6": "8585C5",
        "7": "5B5B82",
        "8": "474796",
        "9": "B2B2D8",
        "10": "B790EF",
        "11": "9898C2",
        "12": "6B6BB7",
        "13": "CDADFA",
        "14": "E6E6FA",
        "15": "976FBD",
    },
}

kirby_target_palettes = [
    0x614816,
    0x859A04,
    0xA80830,
    0xB6B672,
    0xB6D8F2,
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

from typing import Any, Dict, Tuple

from ..enums import KeymastersKeepGoals, KeymastersKeepItems, KeymastersKeepLocations, KeymastersKeepRegions


color_to_hex_codes: Dict[str, str] = {
    "aliceblue": "F0F8FF",
    "antiquewhite": "FAEBD7",
    "aqua": "00FFFF",
    "aquamarine": "7FFFD4",
    "azure": "F0FFFF",
    "beige": "F5F5DC",
    "bisque": "FFE4C4",
    "black": "000000",
    "blanchedalmond": "FFEBCD",
    "blue": "0000FF",
    "blueviolet": "8A2BE2",
    "brown": "A52A2A",
    "burlywood": "DEB887",
    "cadetblue": "5F9EA0",
    "chartreuse": "7FFF00",
    "chocolate": "D2691E",
    "coral": "FF7F50",
    "cornflowerblue": "6495ED",
    "cornsilk": "FFF8DC",
    "crimson": "DC143C",
    "cyan": "00FFFF",
    "darkblue": "00008B",
    "darkcyan": "008B8B",
    "darkgoldenrod": "B8860B",
    "darkgray": "A9A9A9",
    "darkgreen": "006400",
    "darkgrey": "A9A9A9",
    "darkkhaki": "BDB76B",
    "darkmagenta": "8B008B",
    "darkolivegreen": "556B2F",
    "darkorange": "FF8C00",
    "darkorchid": "9932CC",
    "darkred": "8B0000",
    "darksalmon": "E9967A",
    "darkseagreen": "8FBC8F",
    "darkslateblue": "483D8B",
    "darkslategray": "2F4F4F",
    "darkslategrey": "2F4F4F",
    "darkturquoise": "00CED1",
    "darkviolet": "9400D3",
    "deeppink": "FF1493",
    "deepskyblue": "00BFFF",
    "dimgray": "696969",
    "dimgrey": "696969",
    "dodgerblue": "1E90FF",
    "firebrick": "B22222",
    "floralwhite": "FFFAF0",
    "forestgreen": "228B22",
    "fuchsia": "FF00FF",
    "gainsboro": "DCDCDC",
    "ghostwhite": "F8F8FF",
    "gold": "FFD700",
    "goldenrod": "DAA520",
    "gray": "808080",
    "green": "008000",
    "greenyellow": "ADFF2F",
    "grey": "808080",
    "honeydew": "F0FFF0",
    "hotpink": "FF69B4",
    "indianred": "CD5C5C",
    "indigo": "4B0082",
    "ivory": "FFFFF0",
    "khaki": "F0E68C",
    "lavender": "E6E6FA",
    "lavenderblush": "FFF0F5",
    "lawngreen": "7CFC00",
    "lemonchiffon": "FFFACD",
    "lightblue": "ADD8E6",
    "lightcoral": "F08080",
    "lightcyan": "E0FFFF",
    "lightgoldenrodyellow": "FAFAD2",
    "lightgray": "D3D3D3",
    "lightgreen": "90EE90",
    "lightgrey": "D3D3D3",
    "lightpink": "FFB6C1",
    "lightsalmon": "FFA07A",
    "lightseagreen": "20B2AA",
    "lightskyblue": "87CEFA",
    "lightslategray": "778899",
    "lightslategrey": "778899",
    "lightsteelblue": "B0C4DE",
    "lightyellow": "FFFFE0",
    "lime": "00FF00",
    "limegreen": "32CD32",
    "linen": "FAF0E6",
    "magenta": "FF00FF",
    "maroon": "800000",
    "mediumaquamarine": "66CDAA",
    "mediumblue": "0000CD",
    "mediumorchid": "BA55D3",
    "mediumpurple": "9370DB",
    "mediumseagreen": "3CB371",
    "mediumslateblue": "7B68EE",
    "mediumspringgreen": "00FA9A",
    "mediumturquoise": "48D1CC",
    "mediumvioletred": "C71585",
    "midnightblue": "191970",
    "mintcream": "F5FFFA",
    "mistyrose": "FFE4E1",
    "moccasin": "FFE4B5",
    "navajowhite": "FFDEAD",
    "navy": "000080",
    "oldlace": "FDF5E6",
    "olive": "808000",
    "olivedrab": "6B8E23",
    "orange": "FFA500",
    "orangered": "FF4500",
    "orchid": "DA70D6",
    "palegoldenrod": "EEE8AA",
    "palegreen": "98FB98",
    "paleturquoise": "AFEEEE",
    "palevioletred": "DB7093",
    "papayawhip": "FFEFD5",
    "peachpuff": "FFDAB9",
    "peru": "CD853F",
    "pink": "FFC0CB",
    "plum": "DDA0DD",
    "powderblue": "B0E0E6",
    "purple": "800080",
    "red": "FF0000",
    "rosybrown": "BC8F8F",
    "royalblue": "4169E1",
    "saddlebrown": "8B4513",
    "salmon": "FA8072",
    "sandybrown": "F4A460",
    "seagreen": "2E8B57",
    "seashell": "FFF5EE",
    "sienna": "A0522D",
    "silver": "C0C0C0",
    "skyblue": "87CEEB",
    "slateblue": "6A5ACD",
    "slategray": "708090",
    "slategrey": "708090",
    "snow": "FFFAFA",
    "springgreen": "00FF7F",
    "steelblue": "4682B4",
    "tan": "D2B48C",
    "teal": "008080",
    "thistle": "D8BFD8",
    "tomato": "FF6347",
    "turquoise": "40E0D0",
    "violet": "EE82EE",
    "wheat": "F5DEB3",
    "white": "FFFFFF",
    "whitesmoke": "F5F5F5",
    "yellow": "FFFF00",
    "yellowgreen": "9ACD32",
}

key_item_to_colors: Dict[KeymastersKeepItems, Tuple[str, str]] = {
    KeymastersKeepItems.KEY_AMBER_INFERNO: ("orange", "darkorange"),
    KeymastersKeepItems.KEY_AMBER_STONE: ("gold", "darkgoldenrod"),
    KeymastersKeepItems.KEY_ASHEN_SPARK: ("gray", "orangered"),
    KeymastersKeepItems.KEY_AURIC_FLASH: ("gold", "goldenrod"),
    KeymastersKeepItems.KEY_AURORA_BEAM: ("powderblue", "darkturquoise"),
    KeymastersKeepItems.KEY_AZURE_TIDE: ("blue", "deepskyblue"),
    KeymastersKeepItems.KEY_BRONZE_ROOT: ("sienna", "peru"),
    KeymastersKeepItems.KEY_CELESTIAL_STAR: ("silver", "dimgray"),
    KeymastersKeepItems.KEY_CERULEAN_RIPPLE: ("royalblue", "cornflowerblue"),
    KeymastersKeepItems.KEY_COBALT_SKY: ("steelblue", "lightskyblue"),
    KeymastersKeepItems.KEY_COPPER_BLOOM: ("chocolate", "saddlebrown"),
    KeymastersKeepItems.KEY_CRIMSON_BLAZE: ("red", "firebrick"),
    KeymastersKeepItems.KEY_CRYSTAL_GLACIER: ("lightcyan", "lightblue"),
    KeymastersKeepItems.KEY_DUSKLIGHT_VEIL: ("darkgray", "tomato"),
    KeymastersKeepItems.KEY_EBONY_OAK: ("black", "darkslategray"),
    KeymastersKeepItems.KEY_ELECTRIC_STORM: ("blue", "aqua"),
    KeymastersKeepItems.KEY_EMERALD_GROVE: ("seagreen", "mediumaquamarine"),
    KeymastersKeepItems.KEY_FROSTBITE: ("azure", "paleturquoise"),
    KeymastersKeepItems.KEY_FROZEN_TWILIGHT: ("thistle", "blueviolet"),
    KeymastersKeepItems.KEY_GLACIAL_SHARD: ("darkturquoise", "mediumturquoise"),
    KeymastersKeepItems.KEY_GOLDEN_BIRCH: ("gold", "khaki"),
    KeymastersKeepItems.KEY_GOLDEN_FLAME: ("gold", "darkorange"),
    KeymastersKeepItems.KEY_GOLDEN_ZEPHYR: ("yellow", "gold"),
    KeymastersKeepItems.KEY_HALO_FLAME: ("darkorange", "tomato"),
    KeymastersKeepItems.KEY_ICY_CASCADE: ("lightskyblue", "powderblue"),
    KeymastersKeepItems.KEY_IRONCLAD: ("darkgray", "slategray"),
    KeymastersKeepItems.KEY_IVORY_DRIFT: ("ivory", "aliceblue"),
    KeymastersKeepItems.KEY_IVORY_SPROUT: ("beige", "mintcream"),
    KeymastersKeepItems.KEY_MAHOGANY_BARK: ("maroon", "saddlebrown"),
    KeymastersKeepItems.KEY_MIDNIGHT_ABYSS: ("midnightblue", "navy"),
    KeymastersKeepItems.KEY_MIDNIGHT_SHADE: ("indigo", "darkslateblue"),
    KeymastersKeepItems.KEY_OBSIDIAN_CORE: ("black", "darkgray"),
    KeymastersKeepItems.KEY_OBSIDIAN_WRAITH: ("darkslategray", "maroon"),
    KeymastersKeepItems.KEY_ONYX_ECLIPSE: ("black", "slategray"),
    KeymastersKeepItems.KEY_PALE_GALE: ("gainsboro", "whitesmoke"),
    KeymastersKeepItems.KEY_PEARLESCENT_GLOW: ("ghostwhite", "honeydew"),
    KeymastersKeepItems.KEY_PLASMA_SURGE: ("blueviolet", "magenta"),
    KeymastersKeepItems.KEY_PLATINUM_FORGE: ("gainsboro", "silver"),
    KeymastersKeepItems.KEY_RADIANT_DAWN: ("orangered", "tomato"),
    KeymastersKeepItems.KEY_RUSTSTONE: ("brown", "darkgoldenrod"),
    KeymastersKeepItems.KEY_SAPPHIRE_SURGE: ("mediumblue", "dodgerblue"),
    KeymastersKeepItems.KEY_SCARLET_EMBER: ("crimson", "darkred"),
    KeymastersKeepItems.KEY_SILVER_BREEZE: ("silver", "lightsteelblue"),
    KeymastersKeepItems.KEY_SILVER_SHIELD: ("gray", "slategray"),
    KeymastersKeepItems.KEY_SNOWDRIFT: ("snow", "aliceblue"),
    KeymastersKeepItems.KEY_STORMCALL: ("slategray", "steelblue"),
    KeymastersKeepItems.KEY_STORMCLOUD: ("darkgray", "indigo"),
    KeymastersKeepItems.KEY_VERDANT_MOSS: ("darkolivegreen", "olivedrab"),
    KeymastersKeepItems.KEY_VERDANT_TIMBER: ("forestgreen", "seagreen"),
    KeymastersKeepItems.KEY_VOID_EMBER: ("black", "orangered"),
}

label_mapping: Dict[Any, str] = {
    False: "Off",
    True: "On",
    KeymastersKeepGoals.KEYMASTERS_CHALLENGE: "Keymaster's Challenge",
    KeymastersKeepGoals.MAGIC_KEY_HEIST: "Magic Key Heist",
}

region_to_trial_locations: Dict[KeymastersKeepRegions, KeymastersKeepLocations] = {
    KeymastersKeepRegions.THE_ARCANE_DOOR: KeymastersKeepLocations.THE_ARCANE_DOOR_TRIAL,
    KeymastersKeepRegions.THE_ARCANE_PASSAGE: KeymastersKeepLocations.THE_ARCANE_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_ARCANE_THRESHOLD: KeymastersKeepLocations.THE_ARCANE_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_CLANDESTINE_PASSAGE: KeymastersKeepLocations.THE_CLANDESTINE_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_CLOAKED_ENTRANCE: KeymastersKeepLocations.THE_CLOAKED_ENTRANCE_TRIAL,
    KeymastersKeepRegions.THE_CLOAKED_THRESHOLD: KeymastersKeepLocations.THE_CLOAKED_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_CLOAKED_VAULT: KeymastersKeepLocations.THE_CLOAKED_VAULT_TRIAL,
    KeymastersKeepRegions.THE_CONCEALED_THRESHOLD: KeymastersKeepLocations.THE_CONCEALED_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_CONCEALED_VAULT: KeymastersKeepLocations.THE_CONCEALED_VAULT_TRIAL,
    KeymastersKeepRegions.THE_CRYPTIC_CHAMBER: KeymastersKeepLocations.THE_CRYPTIC_CHAMBER_TRIAL,
    KeymastersKeepRegions.THE_CRYPTIC_GATEWAY: KeymastersKeepLocations.THE_CRYPTIC_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_CRYPTIC_VAULT: KeymastersKeepLocations.THE_CRYPTIC_VAULT_TRIAL,
    KeymastersKeepRegions.THE_DISGUISED_GATEWAY: KeymastersKeepLocations.THE_DISGUISED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_ECHOING_PASSAGE: KeymastersKeepLocations.THE_ECHOING_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_ELUSIVE_DOOR: KeymastersKeepLocations.THE_ELUSIVE_DOOR_TRIAL,
    KeymastersKeepRegions.THE_ENCHANTED_GATEWAY: KeymastersKeepLocations.THE_ENCHANTED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_ENCHANTED_PASSAGE: KeymastersKeepLocations.THE_ENCHANTED_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_ENIGMATIC_PORTAL: KeymastersKeepLocations.THE_ENIGMATIC_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_ENIGMATIC_THRESHOLD: KeymastersKeepLocations.THE_ENIGMATIC_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_FADED_GATEWAY: KeymastersKeepLocations.THE_FADED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_FAINT_DOORWAY: KeymastersKeepLocations.THE_FAINT_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_FAINT_PATH: KeymastersKeepLocations.THE_FAINT_PATH_TRIAL,
    KeymastersKeepRegions.THE_FAINT_THRESHOLD: KeymastersKeepLocations.THE_FAINT_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_FORBIDDEN_ENTRANCE: KeymastersKeepLocations.THE_FORBIDDEN_ENTRANCE_TRIAL,
    KeymastersKeepRegions.THE_FORGOTTEN_DOOR: KeymastersKeepLocations.THE_FORGOTTEN_DOOR_TRIAL,
    KeymastersKeepRegions.THE_FORGOTTEN_GATEWAY: KeymastersKeepLocations.THE_FORGOTTEN_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_FORGOTTEN_PORTAL: KeymastersKeepLocations.THE_FORGOTTEN_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_FORGOTTEN_THRESHOLD: KeymastersKeepLocations.THE_FORGOTTEN_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_GHOSTED_PASSAGEWAY: KeymastersKeepLocations.THE_GHOSTED_PASSAGEWAY_TRIAL,
    KeymastersKeepRegions.THE_GHOSTLY_PASSAGE: KeymastersKeepLocations.THE_GHOSTLY_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_ARCHWAY: KeymastersKeepLocations.THE_HIDDEN_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_CHAMBER: KeymastersKeepLocations.THE_HIDDEN_CHAMBER_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_DOORWAY: KeymastersKeepLocations.THE_HIDDEN_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_ENTRANCE: KeymastersKeepLocations.THE_HIDDEN_ENTRANCE_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_KEYHOLE: KeymastersKeepLocations.THE_HIDDEN_KEYHOLE_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_PASSAGEWAY: KeymastersKeepLocations.THE_HIDDEN_PASSAGEWAY_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_PATH: KeymastersKeepLocations.THE_HIDDEN_PATH_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_REACH: KeymastersKeepLocations.THE_HIDDEN_REACH_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_VAULT: KeymastersKeepLocations.THE_HIDDEN_VAULT_TRIAL,
    KeymastersKeepRegions.THE_INCONSPICUOUS_DOOR: KeymastersKeepLocations.THE_INCONSPICUOUS_DOOR_TRIAL,
    KeymastersKeepRegions.THE_INVISIBLE_DOORWAY: KeymastersKeepLocations.THE_INVISIBLE_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_LOCKED_DOORWAY: KeymastersKeepLocations.THE_LOCKED_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_LOCKED_GATEWAY: KeymastersKeepLocations.THE_LOCKED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_LOST_ARCHWAY: KeymastersKeepLocations.THE_LOST_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_LOST_PORTAL: KeymastersKeepLocations.THE_LOST_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_LOST_THRESHOLD: KeymastersKeepLocations.THE_LOST_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_MYSTERIOUS_ARCH: KeymastersKeepLocations.THE_MYSTERIOUS_ARCH_TRIAL,
    KeymastersKeepRegions.THE_MYSTERIOUS_DOORWAY: KeymastersKeepLocations.THE_MYSTERIOUS_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_MYSTERIOUS_PASSAGE: KeymastersKeepLocations.THE_MYSTERIOUS_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_MYSTERIOUS_VAULT: KeymastersKeepLocations.THE_MYSTERIOUS_VAULT_TRIAL,
    KeymastersKeepRegions.THE_MYSTICAL_PASSAGE: KeymastersKeepLocations.THE_MYSTICAL_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_OBSCURED_ARCH: KeymastersKeepLocations.THE_OBSCURED_ARCH_TRIAL,
    KeymastersKeepRegions.THE_OBSCURED_DOORWAY: KeymastersKeepLocations.THE_OBSCURED_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_OBSCURED_PORTAL: KeymastersKeepLocations.THE_OBSCURED_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_OBSCURED_VAULT: KeymastersKeepLocations.THE_OBSCURED_VAULT_TRIAL,
    KeymastersKeepRegions.THE_OBSCURE_PASSAGE: KeymastersKeepLocations.THE_OBSCURE_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_PHANTOM_PASSAGE: KeymastersKeepLocations.THE_PHANTOM_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_PHANTOM_VAULT: KeymastersKeepLocations.THE_PHANTOM_VAULT_TRIAL,
    KeymastersKeepRegions.THE_QUIET_ARCHWAY: KeymastersKeepLocations.THE_QUIET_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_QUIET_THRESHOLD: KeymastersKeepLocations.THE_QUIET_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_SEALED_CHAMBER: KeymastersKeepLocations.THE_SEALED_CHAMBER_TRIAL,
    KeymastersKeepRegions.THE_SEALED_GATEWAY: KeymastersKeepLocations.THE_SEALED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_SEALED_THRESHOLD: KeymastersKeepLocations.THE_SEALED_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_SECRETED_DOOR: KeymastersKeepLocations.THE_SECRETED_DOOR_TRIAL,
    KeymastersKeepRegions.THE_SECRETIVE_DOOR: KeymastersKeepLocations.THE_SECRETIVE_DOOR_TRIAL,
    KeymastersKeepRegions.THE_SECRET_ARCHWAY: KeymastersKeepLocations.THE_SECRET_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_SECRET_PASSAGEWAY: KeymastersKeepLocations.THE_SECRET_PASSAGEWAY_TRIAL,
    KeymastersKeepRegions.THE_SECRET_THRESHOLD: KeymastersKeepLocations.THE_SECRET_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_SECRET_VAULT: KeymastersKeepLocations.THE_SECRET_VAULT_TRIAL,
    KeymastersKeepRegions.THE_SHADOWED_PORTAL: KeymastersKeepLocations.THE_SHADOWED_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_SHADOWED_THRESHOLD: KeymastersKeepLocations.THE_SHADOWED_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_SHADOWY_PASSAGE: KeymastersKeepLocations.THE_SHADOWY_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_SHIMMERING_PASSAGE: KeymastersKeepLocations.THE_SHIMMERING_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_SHROUDED_GATEWAY: KeymastersKeepLocations.THE_SHROUDED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_SHROUDED_PORTAL: KeymastersKeepLocations.THE_SHROUDED_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_SILENT_ARCHWAY: KeymastersKeepLocations.THE_SILENT_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_SILENT_PASSAGE: KeymastersKeepLocations.THE_SILENT_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_SILENT_THRESHOLD: KeymastersKeepLocations.THE_SILENT_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_SILENT_VAULT: KeymastersKeepLocations.THE_SILENT_VAULT_TRIAL,
    KeymastersKeepRegions.THE_UNFATHOMABLE_DOOR: KeymastersKeepLocations.THE_UNFATHOMABLE_DOOR_TRIAL,
    KeymastersKeepRegions.THE_UNKNOWN_ARCH: KeymastersKeepLocations.THE_UNKNOWN_ARCH_TRIAL,
    KeymastersKeepRegions.THE_UNKNOWN_GATEWAY: KeymastersKeepLocations.THE_UNKNOWN_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_UNMARKED_PASSAGE: KeymastersKeepLocations.THE_UNMARKED_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_UNMARKED_VAULT: KeymastersKeepLocations.THE_UNMARKED_VAULT_TRIAL,
    KeymastersKeepRegions.THE_UNRAVELED_DOOR: KeymastersKeepLocations.THE_UNRAVELED_DOOR_TRIAL,
    KeymastersKeepRegions.THE_UNSEEN_ARCHWAY: KeymastersKeepLocations.THE_UNSEEN_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_UNSEEN_DOOR: KeymastersKeepLocations.THE_UNSEEN_DOOR_TRIAL,
    KeymastersKeepRegions.THE_UNSEEN_PASSAGE: KeymastersKeepLocations.THE_UNSEEN_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_UNSEEN_PORTAL: KeymastersKeepLocations.THE_UNSEEN_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_UNSPOKEN_GATE: KeymastersKeepLocations.THE_UNSPOKEN_GATE_TRIAL,
    KeymastersKeepRegions.THE_UNTOLD_GATEWAY: KeymastersKeepLocations.THE_UNTOLD_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_UNTRACEABLE_PATH: KeymastersKeepLocations.THE_UNTRACEABLE_PATH_TRIAL,
    KeymastersKeepRegions.THE_VANISHING_ARCHWAY: KeymastersKeepLocations.THE_VANISHING_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_VANISHING_DOOR: KeymastersKeepLocations.THE_VANISHING_DOOR_TRIAL,
    KeymastersKeepRegions.THE_VAULT_OF_WHISPERS: KeymastersKeepLocations.THE_VAULT_OF_WHISPERS_TRIAL,
    KeymastersKeepRegions.THE_VEILED_PASSAGE: KeymastersKeepLocations.THE_VEILED_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_VEILED_PATH: KeymastersKeepLocations.THE_VEILED_PATH_TRIAL,
    KeymastersKeepRegions.THE_WHISPERED_PORTAL: KeymastersKeepLocations.THE_WHISPERED_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_WHISPERED_THRESHOLD: KeymastersKeepLocations.THE_WHISPERED_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_WHISPERING_DOOR: KeymastersKeepLocations.THE_WHISPERING_DOOR_TRIAL,
}

region_to_unlock_location_and_item: Dict[KeymastersKeepRegions, Tuple[KeymastersKeepLocations, KeymastersKeepItems]] = {
    KeymastersKeepRegions.THE_ARCANE_DOOR: (
        KeymastersKeepLocations.THE_ARCANE_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ARCANE_DOOR
    ),
    KeymastersKeepRegions.THE_ARCANE_PASSAGE: (
        KeymastersKeepLocations.THE_ARCANE_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ARCANE_PASSAGE
    ),
    KeymastersKeepRegions.THE_ARCANE_THRESHOLD: (
        KeymastersKeepLocations.THE_ARCANE_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ARCANE_THRESHOLD
    ),
    KeymastersKeepRegions.THE_CLANDESTINE_PASSAGE: (
        KeymastersKeepLocations.THE_CLANDESTINE_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CLANDESTINE_PASSAGE
    ),
    KeymastersKeepRegions.THE_CLOAKED_ENTRANCE: (
        KeymastersKeepLocations.THE_CLOAKED_ENTRANCE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CLOAKED_ENTRANCE
    ),
    KeymastersKeepRegions.THE_CLOAKED_THRESHOLD: (
        KeymastersKeepLocations.THE_CLOAKED_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CLOAKED_THRESHOLD
    ),
    KeymastersKeepRegions.THE_CLOAKED_VAULT: (
        KeymastersKeepLocations.THE_CLOAKED_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CLOAKED_VAULT
    ),
    KeymastersKeepRegions.THE_CONCEALED_THRESHOLD: (
        KeymastersKeepLocations.THE_CONCEALED_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CONCEALED_THRESHOLD
    ),
    KeymastersKeepRegions.THE_CONCEALED_VAULT: (
        KeymastersKeepLocations.THE_CONCEALED_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CONCEALED_VAULT
    ),
    KeymastersKeepRegions.THE_CRYPTIC_CHAMBER: (
        KeymastersKeepLocations.THE_CRYPTIC_CHAMBER_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CRYPTIC_CHAMBER
    ),
    KeymastersKeepRegions.THE_CRYPTIC_GATEWAY: (
        KeymastersKeepLocations.THE_CRYPTIC_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CRYPTIC_GATEWAY
    ),
    KeymastersKeepRegions.THE_CRYPTIC_VAULT: (
        KeymastersKeepLocations.THE_CRYPTIC_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CRYPTIC_VAULT
    ),
    KeymastersKeepRegions.THE_DISGUISED_GATEWAY: (
        KeymastersKeepLocations.THE_DISGUISED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_DISGUISED_GATEWAY
    ),
    KeymastersKeepRegions.THE_ECHOING_PASSAGE: (
        KeymastersKeepLocations.THE_ECHOING_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ECHOING_PASSAGE
    ),
    KeymastersKeepRegions.THE_ELUSIVE_DOOR: (
        KeymastersKeepLocations.THE_ELUSIVE_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ELUSIVE_DOOR
    ),
    KeymastersKeepRegions.THE_ENCHANTED_GATEWAY: (
        KeymastersKeepLocations.THE_ENCHANTED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ENCHANTED_GATEWAY
    ),
    KeymastersKeepRegions.THE_ENCHANTED_PASSAGE: (
        KeymastersKeepLocations.THE_ENCHANTED_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ENCHANTED_PASSAGE
    ),
    KeymastersKeepRegions.THE_ENIGMATIC_PORTAL: (
        KeymastersKeepLocations.THE_ENIGMATIC_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ENIGMATIC_PORTAL
    ),
    KeymastersKeepRegions.THE_ENIGMATIC_THRESHOLD: (
        KeymastersKeepLocations.THE_ENIGMATIC_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ENIGMATIC_THRESHOLD
    ),
    KeymastersKeepRegions.THE_FADED_GATEWAY: (
        KeymastersKeepLocations.THE_FADED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FADED_GATEWAY
    ),
    KeymastersKeepRegions.THE_FAINT_DOORWAY: (
        KeymastersKeepLocations.THE_FAINT_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FAINT_DOORWAY
    ),
    KeymastersKeepRegions.THE_FAINT_PATH: (
        KeymastersKeepLocations.THE_FAINT_PATH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FAINT_PATH
    ),
    KeymastersKeepRegions.THE_FAINT_THRESHOLD: (
        KeymastersKeepLocations.THE_FAINT_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FAINT_THRESHOLD
    ),
    KeymastersKeepRegions.THE_FORBIDDEN_ENTRANCE: (
        KeymastersKeepLocations.THE_FORBIDDEN_ENTRANCE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FORBIDDEN_ENTRANCE
    ),
    KeymastersKeepRegions.THE_FORGOTTEN_DOOR: (
        KeymastersKeepLocations.THE_FORGOTTEN_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_DOOR
    ),
    KeymastersKeepRegions.THE_FORGOTTEN_GATEWAY: (
        KeymastersKeepLocations.THE_FORGOTTEN_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_GATEWAY
    ),
    KeymastersKeepRegions.THE_FORGOTTEN_PORTAL: (
        KeymastersKeepLocations.THE_FORGOTTEN_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_PORTAL
    ),
    KeymastersKeepRegions.THE_FORGOTTEN_THRESHOLD: (
        KeymastersKeepLocations.THE_FORGOTTEN_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_THRESHOLD
    ),
    KeymastersKeepRegions.THE_GHOSTED_PASSAGEWAY: (
        KeymastersKeepLocations.THE_GHOSTED_PASSAGEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_GHOSTED_PASSAGEWAY
    ),
    KeymastersKeepRegions.THE_GHOSTLY_PASSAGE: (
        KeymastersKeepLocations.THE_GHOSTLY_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_GHOSTLY_PASSAGE
    ),
    KeymastersKeepRegions.THE_HIDDEN_ARCHWAY: (
        KeymastersKeepLocations.THE_HIDDEN_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_ARCHWAY
    ),
    KeymastersKeepRegions.THE_HIDDEN_CHAMBER: (
        KeymastersKeepLocations.THE_HIDDEN_CHAMBER_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_CHAMBER
    ),
    KeymastersKeepRegions.THE_HIDDEN_DOORWAY: (
        KeymastersKeepLocations.THE_HIDDEN_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_DOORWAY
    ),
    KeymastersKeepRegions.THE_HIDDEN_ENTRANCE: (
        KeymastersKeepLocations.THE_HIDDEN_ENTRANCE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_ENTRANCE
    ),
    KeymastersKeepRegions.THE_HIDDEN_KEYHOLE: (
        KeymastersKeepLocations.THE_HIDDEN_KEYHOLE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_KEYHOLE
    ),
    KeymastersKeepRegions.THE_HIDDEN_PASSAGEWAY: (
        KeymastersKeepLocations.THE_HIDDEN_PASSAGEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_PASSAGEWAY
    ),
    KeymastersKeepRegions.THE_HIDDEN_PATH: (
        KeymastersKeepLocations.THE_HIDDEN_PATH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_PATH
    ),
    KeymastersKeepRegions.THE_HIDDEN_REACH: (
        KeymastersKeepLocations.THE_HIDDEN_REACH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_REACH
    ),
    KeymastersKeepRegions.THE_HIDDEN_VAULT: (
        KeymastersKeepLocations.THE_HIDDEN_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_VAULT
    ),
    KeymastersKeepRegions.THE_INCONSPICUOUS_DOOR: (
        KeymastersKeepLocations.THE_INCONSPICUOUS_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_INCONSPICUOUS_DOOR
    ),
    KeymastersKeepRegions.THE_INVISIBLE_DOORWAY: (
        KeymastersKeepLocations.THE_INVISIBLE_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_INVISIBLE_DOORWAY
    ),
    KeymastersKeepRegions.THE_LOCKED_DOORWAY: (
        KeymastersKeepLocations.THE_LOCKED_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_LOCKED_DOORWAY
    ),
    KeymastersKeepRegions.THE_LOCKED_GATEWAY: (
        KeymastersKeepLocations.THE_LOCKED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_LOCKED_GATEWAY
    ),
    KeymastersKeepRegions.THE_LOST_ARCHWAY: (
        KeymastersKeepLocations.THE_LOST_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_LOST_ARCHWAY
    ),
    KeymastersKeepRegions.THE_LOST_PORTAL: (
        KeymastersKeepLocations.THE_LOST_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_LOST_PORTAL
    ),
    KeymastersKeepRegions.THE_LOST_THRESHOLD: (
        KeymastersKeepLocations.THE_LOST_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_LOST_THRESHOLD
    ),
    KeymastersKeepRegions.THE_MYSTERIOUS_ARCH: (
        KeymastersKeepLocations.THE_MYSTERIOUS_ARCH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_ARCH
    ),
    KeymastersKeepRegions.THE_MYSTERIOUS_DOORWAY: (
        KeymastersKeepLocations.THE_MYSTERIOUS_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_DOORWAY
    ),
    KeymastersKeepRegions.THE_MYSTERIOUS_PASSAGE: (
        KeymastersKeepLocations.THE_MYSTERIOUS_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_PASSAGE
    ),
    KeymastersKeepRegions.THE_MYSTERIOUS_VAULT: (
        KeymastersKeepLocations.THE_MYSTERIOUS_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_VAULT
    ),
    KeymastersKeepRegions.THE_MYSTICAL_PASSAGE: (
        KeymastersKeepLocations.THE_MYSTICAL_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_MYSTICAL_PASSAGE
    ),
    KeymastersKeepRegions.THE_OBSCURED_ARCH: (
        KeymastersKeepLocations.THE_OBSCURED_ARCH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_OBSCURED_ARCH
    ),
    KeymastersKeepRegions.THE_OBSCURED_DOORWAY: (
        KeymastersKeepLocations.THE_OBSCURED_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_OBSCURED_DOORWAY
    ),
    KeymastersKeepRegions.THE_OBSCURED_PORTAL: (
        KeymastersKeepLocations.THE_OBSCURED_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_OBSCURED_PORTAL
    ),
    KeymastersKeepRegions.THE_OBSCURED_VAULT: (
        KeymastersKeepLocations.THE_OBSCURED_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_OBSCURED_VAULT
    ),
    KeymastersKeepRegions.THE_OBSCURE_PASSAGE: (
        KeymastersKeepLocations.THE_OBSCURE_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_OBSCURE_PASSAGE
    ),
    KeymastersKeepRegions.THE_PHANTOM_PASSAGE: (
        KeymastersKeepLocations.THE_PHANTOM_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_PHANTOM_PASSAGE
    ),
    KeymastersKeepRegions.THE_PHANTOM_VAULT: (
        KeymastersKeepLocations.THE_PHANTOM_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_PHANTOM_VAULT
    ),
    KeymastersKeepRegions.THE_QUIET_ARCHWAY: (
        KeymastersKeepLocations.THE_QUIET_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_QUIET_ARCHWAY
    ),
    KeymastersKeepRegions.THE_QUIET_THRESHOLD: (
        KeymastersKeepLocations.THE_QUIET_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_QUIET_THRESHOLD
    ),
    KeymastersKeepRegions.THE_SEALED_CHAMBER: (
        KeymastersKeepLocations.THE_SEALED_CHAMBER_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SEALED_CHAMBER
    ),
    KeymastersKeepRegions.THE_SEALED_GATEWAY: (
        KeymastersKeepLocations.THE_SEALED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SEALED_GATEWAY
    ),
    KeymastersKeepRegions.THE_SEALED_THRESHOLD: (
        KeymastersKeepLocations.THE_SEALED_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SEALED_THRESHOLD
    ),
    KeymastersKeepRegions.THE_SECRETED_DOOR: (
        KeymastersKeepLocations.THE_SECRETED_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRETED_DOOR
    ),
    KeymastersKeepRegions.THE_SECRETIVE_DOOR: (
        KeymastersKeepLocations.THE_SECRETIVE_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRETIVE_DOOR
    ),
    KeymastersKeepRegions.THE_SECRET_ARCHWAY: (
        KeymastersKeepLocations.THE_SECRET_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRET_ARCHWAY
    ),
    KeymastersKeepRegions.THE_SECRET_PASSAGEWAY: (
        KeymastersKeepLocations.THE_SECRET_PASSAGEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRET_PASSAGEWAY
    ),
    KeymastersKeepRegions.THE_SECRET_THRESHOLD: (
        KeymastersKeepLocations.THE_SECRET_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRET_THRESHOLD
    ),
    KeymastersKeepRegions.THE_SECRET_VAULT: (
        KeymastersKeepLocations.THE_SECRET_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRET_VAULT
    ),
    KeymastersKeepRegions.THE_SHADOWED_PORTAL: (
        KeymastersKeepLocations.THE_SHADOWED_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHADOWED_PORTAL
    ),
    KeymastersKeepRegions.THE_SHADOWED_THRESHOLD: (
        KeymastersKeepLocations.THE_SHADOWED_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHADOWED_THRESHOLD
    ),
    KeymastersKeepRegions.THE_SHADOWY_PASSAGE: (
        KeymastersKeepLocations.THE_SHADOWY_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHADOWY_PASSAGE
    ),
    KeymastersKeepRegions.THE_SHIMMERING_PASSAGE: (
        KeymastersKeepLocations.THE_SHIMMERING_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHIMMERING_PASSAGE
    ),
    KeymastersKeepRegions.THE_SHROUDED_GATEWAY: (
        KeymastersKeepLocations.THE_SHROUDED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHROUDED_GATEWAY
    ),
    KeymastersKeepRegions.THE_SHROUDED_PORTAL: (
        KeymastersKeepLocations.THE_SHROUDED_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHROUDED_PORTAL
    ),
    KeymastersKeepRegions.THE_SILENT_ARCHWAY: (
        KeymastersKeepLocations.THE_SILENT_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SILENT_ARCHWAY
    ),
    KeymastersKeepRegions.THE_SILENT_PASSAGE: (
        KeymastersKeepLocations.THE_SILENT_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SILENT_PASSAGE
    ),
    KeymastersKeepRegions.THE_SILENT_THRESHOLD: (
        KeymastersKeepLocations.THE_SILENT_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SILENT_THRESHOLD
    ),
    KeymastersKeepRegions.THE_SILENT_VAULT: (
        KeymastersKeepLocations.THE_SILENT_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SILENT_VAULT
    ),
    KeymastersKeepRegions.THE_UNFATHOMABLE_DOOR: (
        KeymastersKeepLocations.THE_UNFATHOMABLE_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNFATHOMABLE_DOOR
    ),
    KeymastersKeepRegions.THE_UNKNOWN_ARCH: (
        KeymastersKeepLocations.THE_UNKNOWN_ARCH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNKNOWN_ARCH
    ),
    KeymastersKeepRegions.THE_UNKNOWN_GATEWAY: (
        KeymastersKeepLocations.THE_UNKNOWN_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNKNOWN_GATEWAY
    ),
    KeymastersKeepRegions.THE_UNMARKED_PASSAGE: (
        KeymastersKeepLocations.THE_UNMARKED_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNMARKED_PASSAGE
    ),
    KeymastersKeepRegions.THE_UNMARKED_VAULT: (
        KeymastersKeepLocations.THE_UNMARKED_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNMARKED_VAULT
    ),
    KeymastersKeepRegions.THE_UNRAVELED_DOOR: (
        KeymastersKeepLocations.THE_UNRAVELED_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNRAVELED_DOOR
    ),
    KeymastersKeepRegions.THE_UNSEEN_ARCHWAY: (
        KeymastersKeepLocations.THE_UNSEEN_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNSEEN_ARCHWAY
    ),
    KeymastersKeepRegions.THE_UNSEEN_DOOR: (
        KeymastersKeepLocations.THE_UNSEEN_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNSEEN_DOOR
    ),
    KeymastersKeepRegions.THE_UNSEEN_PASSAGE: (
        KeymastersKeepLocations.THE_UNSEEN_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNSEEN_PASSAGE
    ),
    KeymastersKeepRegions.THE_UNSEEN_PORTAL: (
        KeymastersKeepLocations.THE_UNSEEN_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNSEEN_PORTAL
    ),
    KeymastersKeepRegions.THE_UNSPOKEN_GATE: (
        KeymastersKeepLocations.THE_UNSPOKEN_GATE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNSPOKEN_GATE
    ),
    KeymastersKeepRegions.THE_UNTOLD_GATEWAY: (
        KeymastersKeepLocations.THE_UNTOLD_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNTOLD_GATEWAY
    ),
    KeymastersKeepRegions.THE_UNTRACEABLE_PATH: (
        KeymastersKeepLocations.THE_UNTRACEABLE_PATH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNTRACEABLE_PATH
    ),
    KeymastersKeepRegions.THE_VANISHING_ARCHWAY: (
        KeymastersKeepLocations.THE_VANISHING_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_VANISHING_ARCHWAY
    ),
    KeymastersKeepRegions.THE_VANISHING_DOOR: (
        KeymastersKeepLocations.THE_VANISHING_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_VANISHING_DOOR
    ),
    KeymastersKeepRegions.THE_VAULT_OF_WHISPERS: (
        KeymastersKeepLocations.THE_VAULT_OF_WHISPERS_UNLOCK, KeymastersKeepItems.UNLOCK_THE_VAULT_OF_WHISPERS
    ),
    KeymastersKeepRegions.THE_VEILED_PASSAGE: (
        KeymastersKeepLocations.THE_VEILED_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_VEILED_PASSAGE
    ),
    KeymastersKeepRegions.THE_VEILED_PATH: (
        KeymastersKeepLocations.THE_VEILED_PATH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_VEILED_PATH
    ),
    KeymastersKeepRegions.THE_WHISPERED_PORTAL: (
        KeymastersKeepLocations.THE_WHISPERED_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_WHISPERED_PORTAL
    ),
    KeymastersKeepRegions.THE_WHISPERED_THRESHOLD: (
        KeymastersKeepLocations.THE_WHISPERED_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_WHISPERED_THRESHOLD
    ),
    KeymastersKeepRegions.THE_WHISPERING_DOOR: (
        KeymastersKeepLocations.THE_WHISPERING_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_WHISPERING_DOOR
    ),
}

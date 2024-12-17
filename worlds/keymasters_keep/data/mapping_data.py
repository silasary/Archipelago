from typing import Dict, Tuple

from ..enums import KeymastersKeepItems, KeymastersKeepLocations, KeymastersKeepRegions


key_item_to_colors: Dict[KeymastersKeepItems, Tuple[str, str]] = {
    KeymastersKeepItems.KEY_AMBER_INFERNO: ("#FF7F00", "#FFB84D"),
    KeymastersKeepItems.KEY_AMBER_STONE: ("#FFBF00", "#FF9F00"),
    KeymastersKeepItems.KEY_ASHEN_SPARK: ("#B8B8B8", "#FF4500"),
    KeymastersKeepItems.KEY_AURIC_FLASH: ("#FFD700", "#FFCC00"),
    KeymastersKeepItems.KEY_AURORA_BEAM: ("#B0E0E6", "#00CED1"),
    KeymastersKeepItems.KEY_AZURE_TIDE: ("#0066CC", "#3399FF"),
    KeymastersKeepItems.KEY_BRONZE_ROOT: ("#CD7F32", "#B4654B"),
    KeymastersKeepItems.KEY_CELESTIAL_STAR: ("#C0C0C0", "#A9A9A9"),
    KeymastersKeepItems.KEY_CERULEAN_RIPPLE: ("#4A90E2", "#5B8DF4"),
    KeymastersKeepItems.KEY_COBALT_SKY: ("#0047AB", "#0066CC"),
    KeymastersKeepItems.KEY_COPPER_BLOOM: ("#B87333", "#D66C2F"),
    KeymastersKeepItems.KEY_CRIMSON_BLAZE: ("#FF3333", "#FF6666"),
    KeymastersKeepItems.KEY_CRYSTAL_GLACIER: ("#E0FFFF", "#ADD8E6"),
    KeymastersKeepItems.KEY_DUSKLIGHT_VEIL: ("#A9A9A9", "#FF6347"),
    KeymastersKeepItems.KEY_EBONY_OAK: ("#3B3C36", "#5B5F57"),
    KeymastersKeepItems.KEY_ELECTRIC_STORM: ("#0000FF", "#00FFFF"),
    KeymastersKeepItems.KEY_EMERALD_GROVE: ("#2E8B57", "#66CDAA"),
    KeymastersKeepItems.KEY_FROSTBITE: ("#E0FFFF", "#AFEEEE"),
    KeymastersKeepItems.KEY_FROZEN_TWILIGHT: ("#D8BFD8", "#8A2BE2"),
    KeymastersKeepItems.KEY_GLACIAL_SHARD: ("#00CED1", "#48D1CC"),
    KeymastersKeepItems.KEY_GOLDEN_BIRCH: ("#FFD700", "#F0E68C"),
    KeymastersKeepItems.KEY_GOLDEN_FLAME: ("#FFD700", "#FFAA33"),
    KeymastersKeepItems.KEY_GOLDEN_ZEPHYR: ("#FFCC00", "#FFDF00"),
    KeymastersKeepItems.KEY_HALO_FLAME: ("#FF8C00", "#FF6347"),
    KeymastersKeepItems.KEY_ICY_CASCADE: ("#ADD8E6", "#B0E0E6"),
    KeymastersKeepItems.KEY_IRONCLAD: ("#4B4B4B", "#A9A9A9"),
    KeymastersKeepItems.KEY_IVORY_DRIFT: ("#FFFFF0", "#F0F8FF"),
    KeymastersKeepItems.KEY_IVORY_SPROUT: ("#FFFFF0", "#F0F8FF"),
    KeymastersKeepItems.KEY_MAHOGANY_BARK: ("#3E2A47", "#5B3F39"),
    KeymastersKeepItems.KEY_MIDNIGHT_ABYSS: ("#000080", "#00008B"),
    KeymastersKeepItems.KEY_MIDNIGHT_SHADE: ("#191970", "#2F4F4F"),
    KeymastersKeepItems.KEY_OBSIDIAN_CORE: ("#000000", "#1C1C1C"),
    KeymastersKeepItems.KEY_OBSIDIAN_WRAITH: ("#1C1C1C", "#800000"),
    KeymastersKeepItems.KEY_ONYX_ECLIPSE: ("#1C1C1C", "#000000"),
    KeymastersKeepItems.KEY_PALE_GALE: ("#D3D3D3", "#F5F5F5"),
    KeymastersKeepItems.KEY_PEARLESCENT_GLOW: ("#F8F8FF", "#E0FFFF"),
    KeymastersKeepItems.KEY_PLASMA_SURGE: ("#8A2BE2", "#FF00FF"),
    KeymastersKeepItems.KEY_PLATINUM_FORGE: ("#E5E4E2", "#C0C0C0"),
    KeymastersKeepItems.KEY_RADIANT_DAWN: ("#FF6347", "#FF4500"),
    KeymastersKeepItems.KEY_RUSTSTONE: ("#B7410E", "#7C4700"),
    KeymastersKeepItems.KEY_SAPPHIRE_SURGE: ("#0066CC", "#1E90FF"),
    KeymastersKeepItems.KEY_SCARLET_EMBER: ("#D40000", "#FF2A00"),
    KeymastersKeepItems.KEY_SILVER_BREEZE: ("#C0C0C0", "#B0E0E6"),
    KeymastersKeepItems.KEY_SILVER_SHIELD: ("#C0C0C0", "#A9A9A9"),
    KeymastersKeepItems.KEY_SNOWDRIFT: ("#FFFAFA", "#F0F8FF"),
    KeymastersKeepItems.KEY_STORMCALL: ("#3C3C3C", "#0066CC"),
    KeymastersKeepItems.KEY_STORMCLOUD: ("#808080", "#4B0082"),
    KeymastersKeepItems.KEY_VERDANT_MOSS: ("#556B2F", "#6B8E23"),
    KeymastersKeepItems.KEY_VERDANT_TIMBER: ("#228B22", "#2E8B57"),
    KeymastersKeepItems.KEY_VOID_EMBER: ("#000000", "#FF4500"),
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

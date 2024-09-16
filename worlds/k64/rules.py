from worlds.generic.Rules import set_rule
from .names import LocationName, ItemName
import typing

if typing.TYPE_CHECKING:
    from . import K64World
    from BaseClasses import CollectionState


def has_any_bomb(state: "CollectionState", player: int):
    return state.has_any({ItemName.bomb, ItemName.bomb_bomb, ItemName.bomb_spark, ItemName.bomb_cutter,
                          ItemName.burn_bomb, ItemName.ice_bomb, ItemName.stone_bomb, ItemName.needle_bomb}, player)


def has_any_stone(state: "CollectionState", player: int):
    return state.has_any({ItemName.stone, ItemName.stone_stone, ItemName.stone_spark, ItemName.stone_cutter,
                          ItemName.burn_stone, ItemName.stone_ice, ItemName.stone_bomb, ItemName.stone_needle}, player)


def has_any_needle(state: "CollectionState", player: int):
    return state.has_any({ItemName.needle, ItemName.needle_needle, ItemName.needle_spark, ItemName.needle_cutter,
                          ItemName.burn_needle, ItemName.ice_needle, ItemName.needle_bomb, ItemName.stone_needle},
                         player)


def has_any_ice(state: "CollectionState", player: int):
    return state.has_any({ItemName.ice, ItemName.ice_ice, ItemName.ice_spark, ItemName.ice_cutter,
                          ItemName.burn_ice, ItemName.ice_needle, ItemName.ice_bomb, ItemName.stone_ice}, player)


def has_any_burn(state: "CollectionState", player: int):
    return state.has_any({ItemName.burn, ItemName.burn_burn, ItemName.burn_spark, ItemName.burn_cutter,
                          ItemName.burn_ice, ItemName.burn_needle, ItemName.burn_bomb, ItemName.burn_stone}, player)


def has_any_spark(state: "CollectionState", player: int):
    return state.has_any({ItemName.spark, ItemName.spark_spark, ItemName.burn_spark, ItemName.spark_cutter,
                          ItemName.ice_spark, ItemName.needle_spark, ItemName.bomb_spark, ItemName.stone_spark}, player)


def has_any_cutter(state: "CollectionState", player: int):
    return state.has_any({ItemName.cutter, ItemName.cutter_cutter, ItemName.spark_cutter, ItemName.burn_cutter,
                          ItemName.ice_cutter, ItemName.needle_cutter, ItemName.bomb_cutter, ItemName.stone_cutter},
                         player)


def has_great_cutter(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.cutter_cutter, player)
    else:
        return state.has(ItemName.cutter, player)


def has_geokinesis(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.stone_spark, player)
    else:
        return state.has_all({ItemName.stone, ItemName.spark}, player)


def has_lightbulb(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.bomb_spark, player)
    else:
        return state.has_all({ItemName.bomb, ItemName.spark}, player)


def has_exploding_snowman(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.ice_bomb, player)
    else:
        return state.has_all({ItemName.ice, ItemName.bomb}, player)


def has_volcano(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.burn_stone, player)
    else:
        return state.has_all({ItemName.stone, ItemName.burn}, player)


def has_shurikens(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.bomb_cutter, player)
    else:
        return state.has_all({ItemName.bomb, ItemName.cutter}, player)


def has_stone_friends(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.stone_cutter, player)
    else:
        return state.has_all({ItemName.stone, ItemName.cutter}, player)


def has_dynamite(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.stone_bomb, player)
    else:
        return state.has_all({ItemName.stone, ItemName.bomb}, player)


def has_lightning_rod(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.needle_spark, player)
    else:
        return state.has_all({ItemName.needle, ItemName.spark}, player)


def has_drill(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.stone_needle, player)
    else:
        return state.has_all({ItemName.needle, ItemName.stone}, player)


def has_lightsaber(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.spark_cutter, player)
    else:
        return state.has_all({ItemName.cutter, ItemName.spark}, player)


def has_exploding_gordo(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.needle_bomb, player)
    else:
        return state.has_all({ItemName.needle, ItemName.bomb}, player)


def has_fire_arrows(state: "CollectionState", player: int, specific_ability: int):
    if specific_ability:
        return state.has(ItemName.burn_needle, player)
    else:
        return state.has_all({ItemName.needle, ItemName.burn}, player)


def has_waddle_dee(state: "CollectionState", player: int):
    return state.has(ItemName.waddle_dee, player)


def has_adeleine(state: "CollectionState", player: int):
    return state.has(ItemName.adeleine, player)


def has_king_dedede(state: "CollectionState", player: int):
    return state.has(ItemName.king_dedede, player)


def set_rules(world: "K64World") -> None:
    # Level 1
    set_rule(world.multiworld.get_location(LocationName.pop_star_1_s2, world.player),
             lambda state: has_any_bomb(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.pop_star_3_s1, world.player),
             lambda state: has_great_cutter(state, world.player, world.options.split_power_combos.value))
    # Level 2
    set_rule(world.multiworld.get_location(LocationName.rock_star_1_s3, world.player),
             lambda state: has_geokinesis(state, world.player, world.options.split_power_combos.value))
    set_rule(world.multiworld.get_location(LocationName.rock_star_2_s3, world.player),
             lambda state: has_king_dedede(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.rock_star_3_s1, world.player),
             lambda state: has_any_stone(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.rock_star_4_s2, world.player),
             lambda state: has_lightbulb(state, world.player, world.options.split_power_combos.value)
             and has_adeleine(state, world.player))
    # Level 3
    set_rule(world.multiworld.get_location(LocationName.aqua_star_1_s3, world.player),
             lambda state: has_exploding_snowman(state, world.player, world.options.split_power_combos.value))
    set_rule(world.multiworld.get_location(LocationName.aqua_star_2_s1, world.player),
             lambda state: has_volcano(state, world.player, world.options.split_power_combos.value))
    set_rule(world.multiworld.get_location(LocationName.aqua_star_2_s2, world.player),
             lambda state: has_waddle_dee(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.aqua_star_3_s1, world.player),
             lambda state: has_shurikens(state, world.player, world.options.split_power_combos.value))
    set_rule(world.multiworld.get_location(LocationName.aqua_star_3_s3, world.player),
             lambda state: has_stone_friends(state, world.player, world.options.split_power_combos.value))
    # Level 4
    set_rule(world.multiworld.get_location(LocationName.neo_star_2_s2, world.player),
             lambda state: has_waddle_dee(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.neo_star_2_s3, world.player),
             lambda state: has_dynamite(state, world.player, world.options.split_power_combos.value))
    set_rule(world.multiworld.get_location(LocationName.neo_star_3_s1, world.player),
             lambda state: has_any_needle(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.neo_star_3_s2, world.player),
             lambda state: has_adeleine(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.neo_star_4_s1, world.player),
             lambda state: has_king_dedede(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.neo_star_4_s2, world.player),
             lambda state: has_any_ice(state, world.player))
    # Level 5
    set_rule(world.multiworld.get_location(LocationName.shiver_star_1_s1, world.player),
             lambda state: has_waddle_dee(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.shiver_star_1_s2, world.player),
             lambda state: has_any_burn(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.shiver_star_2_s3, world.player),
             lambda state: has_lightning_rod(state, world.player, world.options.split_power_combos.value))
    set_rule(world.multiworld.get_location(LocationName.shiver_star_3_s3, world.player),
             lambda state: has_adeleine(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.shiver_star_4_s1, world.player),
             lambda state: has_drill(state, world.player, world.options.split_power_combos.value))
    set_rule(world.multiworld.get_location(LocationName.shiver_star_4_s2, world.player),
             lambda state: has_lightsaber(state, world.player, world.options.split_power_combos.value))
    # Level 6
    set_rule(world.multiworld.get_location(LocationName.ripple_star_1_s3, world.player),
             lambda state: has_exploding_gordo(state, world.player, world.options.split_power_combos.value)
             and state.has_any([ItemName.bomb, ItemName.needle], world.player))  # by default cannot carry enemy across
    set_rule(world.multiworld.get_location(LocationName.ripple_star_2_s1, world.player),
             lambda state: has_any_spark(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.ripple_star_2_s3, world.player),
             lambda state: has_any_cutter(state, world.player))
    set_rule(world.multiworld.get_location(LocationName.ripple_star_3_s2, world.player),
             lambda state: has_fire_arrows(state, world.player, world.options.split_power_combos.value))

    # Crystal Requirements
    for i, level in zip(range(1, 7), world.boss_requirements):
        set_rule(world.multiworld.get_entrance(f"To Level {i+1}", world.player),
                 lambda state, j=level: state.has(ItemName.crystal_shard, world.player, j))
        set_rule(world.multiworld.get_location(f"{LocationName.level_names[i]} - Boss Defeated", world.player),
                 lambda state, j=level: state.has(ItemName.crystal_shard, world.player, j))

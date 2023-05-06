"""
Classes and functions related to creating a ROM patch
"""
from typing import List
import os

import bsdiff4

from BaseClasses import MultiWorld
from Options import Toggle
from Patch import APDeltaPatch
import Utils

from .data import PokemonEmeraldData, TrainerPokemonDataTypeEnum, data
from .items import reverse_offset_item_value
from .options import (RandomizeWildPokemon, RandomizeTrainerParties, TmCompatibility,
    HmCompatibility, EliteFourRequirement, NormanRequirement, get_option_value)
from .pokemon import get_random_species, get_random_move


class PokemonEmeraldDeltaPatch(APDeltaPatch):
    game = "Pokemon Emerald"
    hash = "605b89b67018abcea91e693a4dd25be3"
    patch_file_ending = ".apemerald"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def generate_output(modified_data: PokemonEmeraldData, multiworld: MultiWorld, player: int, output_directory: str) -> None:
    base_rom = get_base_rom_as_bytes()
    with open(os.path.join(os.path.dirname(__file__), "data/base_patch.bsdiff4"), "rb") as stream:
        base_patch = bytes(stream.read())
        patched_rom = bytearray(bsdiff4.patch(base_rom, base_patch))

    # Set item values
    for location in multiworld.get_locations(player):
        if location.is_event:
            continue

        if location.item and location.item.player == player:
            _set_bytes_little_endian(patched_rom, location.rom_address, 2, reverse_offset_item_value(location.item.code))
        else:
            _set_bytes_little_endian(patched_rom, location.rom_address, 2, data.constants["ITEM_ARCHIPELAGO_PROGRESSION"])

    # Set start inventory
    start_inventory = multiworld.start_inventory[player].value.copy()

    starting_badges = 0
    if start_inventory.pop("Stone Badge", 0) > 0:
        starting_badges |= (1 << 0)
    if start_inventory.pop("Knuckle Badge", 0) > 0:
        starting_badges |= (1 << 1)
    if start_inventory.pop("Dynamo Badge", 0) > 0:
        starting_badges |= (1 << 2)
    if start_inventory.pop("Heat Badge", 0) > 0:
        starting_badges |= (1 << 3)
    if start_inventory.pop("Balance Badge", 0) > 0:
        starting_badges |= (1 << 4)
    if start_inventory.pop("Feather Badge", 0) > 0:
        starting_badges |= (1 << 5)
    if start_inventory.pop("Mind Badge", 0) > 0:
        starting_badges |= (1 << 6)
    if start_inventory.pop("Rain Badge", 0) > 0:
        starting_badges |= (1 << 7)

    for i, item_name in enumerate(start_inventory):
        if i >= 20:
            break

        address = data.rom_addresses["sNewGamePCItems"] + (i * 4)
        item = reverse_offset_item_value(multiworld.worlds[player].item_name_to_id[item_name])
        quantity = min(start_inventory[item_name], 99)
        _set_bytes_little_endian(patched_rom, address + 0, 2, item)
        _set_bytes_little_endian(patched_rom, address + 2, 2, quantity)

    # Set species data
    _set_species_info(modified_data, patched_rom)

    # Randomize TM moves
    if get_option_value(multiworld, player, "tm_moves") == Toggle.option_true:
        _randomize_tm_moves(multiworld, player, patched_rom)

    # Set encounter tables
    if get_option_value(multiworld, player, "wild_pokemon") != RandomizeWildPokemon.option_vanilla:
        _set_encounter_tables(modified_data, patched_rom)

    # Set opponent data
    if get_option_value(multiworld, player, "trainer_parties") != RandomizeTrainerParties.option_vanilla:
        _set_opponents(modified_data, patched_rom)

    # Randomize opponent double or single
    _randomize_opponent_battle_type(multiworld, player, patched_rom)

    # Set starters
    _set_starters(modified_data, patched_rom)

    # Modify TM/HM compatibility
    _modify_tmhm_compatibility(multiworld, player, patched_rom)

    # Options
    # struct ArchipelagoOptions
    # {
    #     /* 0x00 */ bool8 advanceTextWithHoldA;
    #     /* 0x01 */ bool8 isFerryEnabled;
    #     /* 0x02 */ bool8 areTrainersBlind;
    #     /* 0x03 */ bool8 canFlyWithoutBadge;
    #     /* 0x04 */ u16 expMultiplierNumerator;
    #     /* 0x06 */ u16 expMultiplierDenominator;
    #     /* 0x08 */ u16 birchPokemon;
    #     /* 0x0A */ bool8 guaranteedCatch;
    #     /* 0x0B */ bool8 betterShopsEnabled;
    #     /* 0x0C */ bool8 eliteFourRequiresGyms;
    #     /* 0x0D */ u8 eliteFourRequiredCount;
    #     /* 0x0E */ bool8 normanRequiresGyms;
    #     /* 0x0F */ u8 normanRequiredCount;
    #     /* 0x10 */ u8 startingBadges;
    #     /* 0x11 */ u8 receivedItemMessageFilter; // 0 = Show All; 1 = Show Progression Only; 2 = Show None
    #     /* 0x12 */ bool8 reusableTms;
    # };
    options_address = data.rom_addresses["gArchipelagoOptions"]

    # Set hold A to advance text
    turbo_a = 1 if get_option_value(multiworld, player, "turbo_a") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x00, 1, turbo_a)

    # Set ferry enabled
    enable_ferry = 1 if get_option_value(multiworld, player, "enable_ferry") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x01, 1, enable_ferry)

    # Set blind trainers
    blind_trainers = 1 if get_option_value(multiworld, player, "blind_trainers") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x02, 1, blind_trainers)

    # Set fly without badge
    fly_without_badge = 1 if get_option_value(multiworld, player, "fly_without_badge") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x03, 1, fly_without_badge)

    # Set exp modifier
    numerator = min(max(get_option_value(multiworld, player, "exp_modifier"), 0), 2**16 - 1)
    _set_bytes_little_endian(patched_rom, options_address + 0x04, 2, numerator)
    _set_bytes_little_endian(patched_rom, options_address + 0x06, 2, 100)

    # Set Birch pokemon
    _set_bytes_little_endian(patched_rom, options_address + 0x08, 2, get_random_species(multiworld.per_slot_randoms[player], data.species).species_id)

    # Set guaranteed catch
    guaranteed_catch = 1 if get_option_value(multiworld, player, "guaranteed_catch") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0A, 1, guaranteed_catch)

    # Set better shops
    better_shops = 1 if get_option_value(multiworld, player, "better_shops") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0B, 1, better_shops)

    # Set elite four requirement
    elite_four_requires_gyms = 1 if get_option_value(multiworld, player, "elite_four_requirement") == EliteFourRequirement.option_gyms else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0C, 1, elite_four_requires_gyms)

    # Set elite four count
    elite_four_count = min(max(get_option_value(multiworld, player, "elite_four_count"), 0), 8)
    _set_bytes_little_endian(patched_rom, options_address + 0x0D, 1, elite_four_count)

    # Set norman requirement
    norman_requires_gyms = 1 if get_option_value(multiworld, player, "norman_requirement") == NormanRequirement.option_gyms else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0E, 1, norman_requires_gyms)

    # Set norman count
    norman_count = min(max(get_option_value(multiworld, player, "norman_count"), 0), 8)
    _set_bytes_little_endian(patched_rom, options_address + 0x0F, 1, norman_count)

    # Set starting badges
    _set_bytes_little_endian(patched_rom, options_address + 0x10, 1, starting_badges)

    # Set receive item messages type
    receive_item_messages_type = get_option_value(multiworld, player, "receive_item_messages")
    _set_bytes_little_endian(patched_rom, options_address + 0x11, 1, receive_item_messages_type)

    # Set better shops
    reusable_tms = 1 if get_option_value(multiworld, player, "reusable_tms") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x12, 1, reusable_tms)

    # Write Output
    outfile_player_name = f"_P{player}"
    outfile_player_name += f"_{multiworld.get_file_safe_player_name(player).replace(' ', '_')}" \
        if multiworld.player_name[player] != f"Player{player}" else ""

    output_path = os.path.join(output_directory, f"AP_{multiworld.seed_name}{outfile_player_name}.gba")
    with open(output_path, "wb") as outfile:
        outfile.write(patched_rom)
    patch = PokemonEmeraldDeltaPatch(os.path.splitext(output_path)[0] + ".apemerald", player=player,
                                     player_name=multiworld.player_name[player], patched_path=output_path)

    patch.write()
    os.unlink(output_path)


def get_base_rom_as_bytes() -> bytes:
    with open(get_base_rom_path(), "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes


def get_base_rom_path() -> str:
    options = Utils.get_options()
    file_name = options["pokemon_emerald_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name


def _set_bytes_little_endian(byte_array, address, size, value) -> None:
    offset = 0
    while size > 0:
        byte_array[address + offset] = value & 0xFF
        value = value >> 8
        offset += 1
        size -= 1


def _set_encounter_tables(modified_data: PokemonEmeraldData, rom: bytearray) -> None:
    """
    Encounter tables are lists of
    struct {
        min_level:  0x01 bytes,
        max_level:  0x01 bytes,
        species_id: 0x02 bytes
    }
    """

    for map_data in modified_data.maps:
        tables = [map_data.land_encounters, map_data.water_encounters, map_data.fishing_encounters]
        for table in tables:
            if table is not None:
                for i, species_id in enumerate(table.slots):
                    address = table.rom_address + 2 + (4 * i)
                    _set_bytes_little_endian(rom, address, 2, species_id)


def _set_species_info(modified_data: PokemonEmeraldData, rom: bytearray) -> None:
    for species in modified_data.species:
        _set_bytes_little_endian(rom, species.rom_address + 8, 1, species.catch_rate)
        _set_bytes_little_endian(rom, species.rom_address + 22, 1, species.abilities[0])
        _set_bytes_little_endian(rom, species.rom_address + 23, 1, species.abilities[1])

        for i, learnset_move in enumerate(species.learnset):
            level_move = learnset_move.level << 9 | learnset_move.move_id
            _set_bytes_little_endian(rom, species.learnset_rom_address + (i * 2), 2, level_move)


def _set_opponents(modified_data: PokemonEmeraldData, rom: bytearray) -> None:
    for trainer in modified_data.trainers:
        party_address = trainer.party.rom_address

        pokemon_data_size: int
        if (
            trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES or
            trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES
        ):
            pokemon_data_size = 8
        else: # Custom Moves
            pokemon_data_size = 16

        for i, pokemon in enumerate(trainer.party.pokemon):
            pokemon_address = party_address + (i * pokemon_data_size)

            # Replace species
            _set_bytes_little_endian(rom, pokemon_address + 0x04, 2, pokemon.species_id)

            # Replace custom moves if applicable
            if trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES:
                _set_bytes_little_endian(rom, pokemon_address + 0x06, 2, pokemon.moves[0])
                _set_bytes_little_endian(rom, pokemon_address + 0x08, 2, pokemon.moves[1])
                _set_bytes_little_endian(rom, pokemon_address + 0x0A, 2, pokemon.moves[2])
                _set_bytes_little_endian(rom, pokemon_address + 0x0C, 2, pokemon.moves[3])
            elif trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES:
                _set_bytes_little_endian(rom, pokemon_address + 0x08, 2, pokemon.moves[0])
                _set_bytes_little_endian(rom, pokemon_address + 0x0A, 2, pokemon.moves[1])
                _set_bytes_little_endian(rom, pokemon_address + 0x0C, 2, pokemon.moves[2])
                _set_bytes_little_endian(rom, pokemon_address + 0x0E, 2, pokemon.moves[3])


def _randomize_opponent_battle_type(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    probability = get_option_value(multiworld, player, "double_battle_chance") / 100

    battle_type_map = {
        0: 4,
        1: 8,
        2: 6,
        3: 13,
    }

    for trainer_data in data.trainers:
        if trainer_data.battle_script_rom_address != 0 and len(trainer_data.party.pokemon) > 1:
            if multiworld.per_slot_randoms[player].random() < probability:
                # Set the trainer to be a double battle
                _set_bytes_little_endian(rom, trainer_data.rom_address + 0x18, 1, 1)

                # Swap the battle type in the script for the purpose of loading the right text
                # and setting data to the right places
                original_battle_type = rom[trainer_data.battle_script_rom_address + 1]
                if original_battle_type in battle_type_map:
                    _set_bytes_little_endian(rom, trainer_data.battle_script_rom_address + 1, 1, battle_type_map[original_battle_type])


def _set_starters(modified_data: PokemonEmeraldData, rom: bytearray) -> None:
    address = data.rom_addresses["sStarterMon"]
    (starter_1, starter_2, starter_3) = modified_data.starters

    _set_bytes_little_endian(rom, address + 0, 2, starter_1)
    _set_bytes_little_endian(rom, address + 2, 2, starter_2)
    _set_bytes_little_endian(rom, address + 4, 2, starter_3)


def _randomize_tm_moves(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    random = multiworld.per_slot_randoms[player]
    tm_list_address = data.rom_addresses["sTMHMMoves"]

    for i in range(50):
        new_move = get_random_move(random)
        _set_bytes_little_endian(rom, tm_list_address + (i * 2), 2, new_move)


def _modify_tmhm_compatibility(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    random = multiworld.per_slot_randoms[player]

    learnsets_address = data.rom_addresses["gTMHMLearnsets"]
    size_of_learnset = 8

    tm_compatibility = get_option_value(multiworld, player, "tm_compatibility")
    hm_compatibility = get_option_value(multiworld, player, "hm_compatibility")

    for species in data.species:
        compatibility_array = [False if bit == "0" else True for bit in list(species.tm_hm_compatibility)]

        tm_compatibility_array = compatibility_array[0:50]
        if tm_compatibility == TmCompatibility.option_fully_compatible:
            tm_compatibility_array = [True for i in tm_compatibility_array]
        elif tm_compatibility == TmCompatibility.option_completely_random:
            tm_compatibility_array = [random.choice([True, False]) for i in tm_compatibility_array]

        hm_compatibility_array = compatibility_array[50:58]
        if hm_compatibility == HmCompatibility.option_fully_compatible:
            hm_compatibility_array = [True for i in hm_compatibility_array]
        elif hm_compatibility == HmCompatibility.option_completely_random:
            hm_compatibility_array = [random.choice([True, False]) for i in hm_compatibility_array]

        compatibility_array = [] + tm_compatibility_array + hm_compatibility_array + [False, False, False, False, False, False]
        compatibility_bytes = _tmhm_compatibility_array_to_bytearray(compatibility_array)

        for i, byte in enumerate(compatibility_bytes):
            address = learnsets_address + (species.species_id * size_of_learnset) + i
            _set_bytes_little_endian(rom, address, 1, byte)


# TODO: Read compatibility from ROM during extraction
def _tmhm_compatibility_array_to_bytearray(compatibility: List[bool]) -> bytearray:
    bits = [1 if bit else 0 for bit in compatibility]
    bits.reverse()

    bytes = []
    while len(bits) > 0:
        byte = 0
        for i in range(8):
            byte += bits.pop() << i

        bytes.append(byte)

    return bytearray(bytes)

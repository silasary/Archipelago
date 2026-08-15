from typing import TYPE_CHECKING

from BaseClasses import CollectionState, LocationProgressType, MultiWorld
from worlds.generic.Rules import add_rule, set_rule
from rule_builder.rules import Has, HasAny, HasAll, HasGroup, Rule, HasFromList

from .Locations import get_locations_by_category
from .Items import flattened_weapons_by_tier, flattened_armors_by_tier, flattened_hats_by_tier

if TYPE_CHECKING:
    from worlds.ffxiitm import FFXIITMWorld

def has_item(state: CollectionState, player: int, item) -> bool:
    return state.has(item, player)

def set_rules(world: "FFXIITMWorld", player: int):
    # Win condition.
    world.multiworld.completion_condition[player] = lambda state: state.has_all({"Victory"}, player)
    max_floor = world.options.trial_victory.value

    # def get_entrance(entrance: str):
        # return world.multiworld.get_entrance(entrance, world.player)
    # get_entrance = world.get_entrance
    def get_floor_entrance(floor: int):
        return world.get_entrance(f"Trial {floor:03}")


    T2_magick = ["Fira", "Thundara", "Blizzara", "Darkra", "Bio", "Aeroga"]
    T3_magick = ["Firaga", "Thundaga", "Blizzaga", "Darkga", "Scourge","Scathe"]
    for floor in range(1, max_floor+1):
        floor_entrance = get_floor_entrance(floor)



        if floor + 1 % 10 == 0: #add esper requirements on floors 10n+1 to avoid rule conflicts on the same entrance
            world.set_rule(floor_entrance,HasGroup("Mist", (floor+1)//10))

        if floor == 10:
            world.set_rule(floor_entrance,Has("Second Job"))

        if floor == 5:
            world.set_rule(floor_entrance, HasFromList(*flattened_weapons_by_tier[3], count=1))
        if floor == 9:
            world.set_rule(floor_entrance,
            HasFromList(*flattened_armors_by_tier[3], count=1) &
            HasFromList(*flattened_hats_by_tier[3], count=1))
        if floor == 15:
            world.set_rule(floor_entrance,
            HasFromList(*flattened_armors_by_tier[3], count=3) &
            HasFromList(*flattened_hats_by_tier[3], count=2) &
            HasFromList(*flattened_weapons_by_tier[3], count=4))
        if floor == 20:
            world.set_rule(floor_entrance,
            HasFromList(*(T2_magick + T3_magick), count=1))
        if floor == 30:
            world.set_rule(floor_entrance,
            Has("Cura") &
            HasFromList(*(T2_magick + T3_magick), count=3) &
            HasFromList(*flattened_weapons_by_tier[4], count=2) &
            HasFromList(*(flattened_hats_by_tier[3]+flattened_hats_by_tier[4]), count=4) &
            HasFromList(*(flattened_armors_by_tier[3]+flattened_armors_by_tier[4]), count=4))

        if floor == 40:
            world.set_rule(floor_entrance,
            HasAny("Esuna","Esunaga") &
            HasFromList(*flattened_weapons_by_tier[4], count=3))

        if floor == 50:
            world.set_rule(floor_entrance,
            HasFromList(*T3_magick, count=1) &
            HasAny("Raise","Arise") &
            HasFromList(*flattened_weapons_by_tier[4], count=4) &
            HasFromList(*flattened_armors_by_tier[4], count=2) &
            HasFromList(*flattened_hats_by_tier[4], count=2))
        if floor == 60:
            world.set_rule(floor_entrance,
            HasFromList(*flattened_weapons_by_tier[5], count=1) &
            HasFromList(*flattened_armors_by_tier[5], count=1) &
            HasFromList(*flattened_hats_by_tier[5], count=1))
        if floor == 63:
            world.set_rule(floor_entrance,HasAny("Berserk","Zodiark")) #for Vorpal Bunny
        if floor == 70:
            world.set_rule(floor_entrance,
            HasFromList(*T3_magick, count=2) &
            Has("Cat-ear Hood") &
            HasAny("Dispel", "Dispelga") &
            HasAny("Curaga", "Renew") &
            HasFromList(*flattened_weapons_by_tier[5], count=2) &
            HasFromList(*flattened_armors_by_tier[5], count=2) &
            HasFromList(*flattened_hats_by_tier[5], count=2))

        if floor == 80:
            world.set_rule(floor_entrance,
            HasAny("Berserk","Berserk Bracers") &
            HasFromList(*flattened_weapons_by_tier[5], count=3) &
            HasFromList(*flattened_armors_by_tier[5], count=3) &
            HasFromList(*flattened_hats_by_tier[5], count=3))
        if floor == 84:
            world.set_rule(floor_entrance, HasAny("Scourge","Flare", "Scathe", "Bio","Toxify","Telekinesis")) #can't use attacks against Chaos
        if floor == 85:
            world.set_rule(floor_entrance,Has("Zodiark"))
        if floor == 90:
            world.set_rule(floor_entrance,
            HasAny("Reflega", "Reflect") &
            HasAll("Opal Ring", "Nihopalaoa", "Reverse") &
            HasFromList(*flattened_weapons_by_tier[5], count=5) &
            HasFromList(*flattened_armors_by_tier[5], count=5) &
            HasFromList(*flattened_hats_by_tier[5], count=5) &
            HasFromList("Wither", "Addle", "Expose", "Shear", count=2))
        if floor == 98:
            world.set_rule(floor_entrance,
            Has("Yagyu Darkblade") &
            HasAny("Darkra", "Darkga"))

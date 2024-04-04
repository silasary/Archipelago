import random
from dataclasses import dataclass

from Options import DeathLink, Choice, Toggle, OptionDict, Range, PlandoBosses, DefaultOnToggle, \
    PerGameCommonOptions
import typing


class GoalSpeed(Choice):
    """
    Normal: the goal is unlocked after defeating the 6 bosses
    Fast: the goal is unlocked after acquiring the target number of Crystal Shards
    """
    display_name = "Goal Speed"
    option_normal = 0
    option_fast = 1


class SplitPowerCombos(Toggle):
    """
    If enabled, Power Combos are added to the pool as separate items, and must be unlocked separate from
    its base abilities.
    """
    display_name = "Split Power Combos"


class TotalCrystalShards(Range):
    """
    Maximum number of heart stars to include in the pool of items.
    """
    display_name = "Max Crystal Shards"
    range_start = 5  # set to 5 so strict bosses does not degrade
    range_end = 72  # 72 default locations, let's not push our luck
    default = 30


class CrystalShardsRequired(Range):
    """
    Percentage of heart stars required to purify the five bosses and reach Zero.
    Each boss will require a differing amount of heart stars to purify.
    """
    display_name = "Required Crystal Shards"
    range_start = 1
    range_end = 100
    default = 50


class LevelShuffle(Choice):
    """
    None: No stage shuffling.
    Same World: shuffles stages around their world.
    Shuffled: shuffles stages across all worlds.
    """
    display_name = "Stage Shuffle"
    option_none = 0
    option_same_world = 1
    option_shuffled = 2
    default = 0


class BossRequirementRandom(Toggle):
    """
    If enabled, unlocking a boss will require a random amount of Crystal Shards, up to a certain amount per level.
    """
    display_name = "Randomize Boss Unlock Requirement"


class FillerPercentage(Range):
    """
        Percentage of non-required Crystal Shards to be converted to filler items (1-Ups, Maxim Tomatoes, Invincibility Candy).
        """
    display_name = "Filler Percentage"
    range_start = 0
    range_end = 100
    default = 50


class KirbyFlavorPreset(Choice):
    """
    The color of Kirby, from a list of presets.
    """
    display_name = "Kirby Flavor"
    option_default = 0
    #option_bubblegum = 1
    #option_cherry = 2
    #option_blueberry = 3
    #option_lemon = 4
    #option_kiwi = 5
    #option_grape = 6
    #option_chocolate = 7
    #option_marshmallow = 8
    #option_licorice = 9
    #option_watermelon = 10
    #option_orange = 11
    #option_lime = 12
    option_lavender = 13
    option_custom = 14
    default = 0

    @classmethod
    def from_text(cls, text: str) -> Choice:
        text = text.lower()
        if text == "random":
            choice_list = list(cls.name_lookup)
            choice_list.remove(14)
            return cls(random.choice(choice_list))
        return super().from_text(text)


class KirbyFlavor(OptionDict):
    """
    A custom color for Kirby. To use a custom color, set the preset to Custom and then define a dict of keys from "1" to
    "15", with their values being an HTML hex color.
    """
    default = {
      "1": "080000",
      "2": "F64A5A",
      "3": "6A4152",
      "4": "F6F6F6",
      "5": "F6A4B4",
      "6": "E66A62",
      "7": "00085A",
      "8": "EE8BA4",
      "9": "413173",
      "10": "D5D5D5",
      "11": "312029",
      "12": "8B949C",
      "13": "0000D5",
      "14": "8B626A",
      "15": "BD838B",
    }


@dataclass
class K64Options(PerGameCommonOptions):
    death_link: DeathLink
    goal_speed: GoalSpeed
    split_power_combos: SplitPowerCombos
    stage_shuffle: LevelShuffle
    boss_requirement_random: BossRequirementRandom
    total_crystals: TotalCrystalShards
    required_crystals: CrystalShardsRequired
    filler_percentage: FillerPercentage
    kirby_flavor_preset: KirbyFlavorPreset
    kirby_flavor: KirbyFlavor

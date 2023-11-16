import random
from dataclasses import dataclass

from Options import Option, DeathLink, Choice, Toggle, OptionDict, Range, PlandoBosses, DefaultOnToggle, \
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

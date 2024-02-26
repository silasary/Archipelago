from dataclasses import dataclass
from typing import Dict

from Options import Choice, PerGameCommonOptions, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class TrialVictory(Range):
    """
    Which Trial holds the victory items
    """
    default = 20
    range_start = 10
    range_end = 100
    display_name = "Victory Trial"

@dataclass
class FF12TMOptions(PerGameCommonOptions):
    trial_victory: TrialVictory

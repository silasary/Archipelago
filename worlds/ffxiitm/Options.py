from dataclasses import dataclass
from typing import Dict

from Options import Choice, PerGameCommonOptions, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class TrialVictory(Range):
    """
    Which Trial holds the victory items
    """
    default = 20
    range_start = 1
    range_end = 100
    display_name = "Victory Trial"

class SecretEquipment(Toggle):
    """
    Adds the Seitengrat, Great Trango, Wyrmhero Blade, and Gendarme to the item pool
    """
    display_name = "Include Secret Equipment"

@dataclass
class FF12TMOptions(PerGameCommonOptions):
    trial_victory: TrialVictory
    secret_equipment: SecretEquipment

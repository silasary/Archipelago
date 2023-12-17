from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

ffxiitm_options: Dict[str, type(Option)] = {
}
class TrialVictory(Range):
    """
    Which Trial holds the victory items
    """
    default = 20
    range_start = 10
    range_end = 100
    display_name = "Victory Trial"

ffxiitm_options: Dict[str, type(Option)] = {
    "trial_victory": TrialVictory,
}
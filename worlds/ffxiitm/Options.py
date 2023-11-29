from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

ffxiitm_options: Dict[str, type(Option)] = {
}
class TrialMinVictory(Range):
    """
    What is the lowest Trial that can hold the Victory item?
    """
    default = 50
    range_start = 1
    range_end = 100
    display_name = "Minimum Victory Trial"
    
class TrialRange(Range):
    """
    How many Trials above the minimum can hold the Victory item?  If the range would put the trial above 100, it is flattened to 100.
    """
    default = 50
    range_start = 0
    range_end = 99
    display_name = "Trial Range"

ffxiitm_options: Dict[str, type(Option)] = {
    "trial_minimum_victory": TrialMinVictory,
    "trial_range": TrialRange,
}
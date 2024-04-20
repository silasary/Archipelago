from typing import Dict
from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions


class AllowSeitengrat(Toggle):
    """Allow Seitengrat to appear in the item pool and bazaars."""
    display_name = "Allow Seitengrat"
    default = 0


class ShuffleMainParty(Toggle):
    """Shuffle the 6 main party members around."""
    display_name = "Shuffle Main Party"
    default = 1

class CharacterProgressionScaling(Toggle):
    """In addition to the progression scaling, also scale the progression based on the number of party members
       and if the second license board has been unlocked."""
    display_name = "Character Progression Scaling"
    default = 1

class BahamutUnlock(Choice):
    """Determines where the Writ of Transit is placed to unlock travel to the Bahamut to beat the game."""
    display_name = "Bahamut Unlock Goal"
    option_defeat_cid_2 = 0
    option_collect_pinewood_chops = 1
    option_random_location = 2
    default = 0


@dataclass
class FF12OpenWorldGameOptions(PerGameCommonOptions):
    shuffle_main_party: ShuffleMainParty
    character_progression_scaling: CharacterProgressionScaling
    allow_seitengrat: AllowSeitengrat
    bahamut_unlock: BahamutUnlock

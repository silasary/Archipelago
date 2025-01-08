from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions


class AspirationGoal(Choice):
    """The Aspiration Needed to win the game"""
    display_name = "goal"
    default = 1
    option_bodybuilder = 0
    option_painter_extraordinaire = 1
    option_bestselling_author = 2
    option_musical_genius = 3
    option_public_enemy = 4
    option_chief_of_mischief = 5
    option_readily_a_parent = 6
    option_successful_lineage = 7
    option_big_happy_family = 8
    option_master_chef = 9
    option_master_mixologist = 10
    option_fabulously_wealthy = 11
    option_mansion_baron = 12
    option_renaissance_sim = 13
    option_nerd_brain = 14
    option_computer_whiz = 15
    option_serial_romantic = 16
    option_soulmate = 17
    option_freelance_botanist = 18
    option_the_curator = 19
    option_angling_ace = 20
    option_joke_star = 21
    option_party_animal = 22
    option_friend_of_the_world = 23
    option_neighborly_advisor = 24

class ExpansionPacks(OptionSet):



@dataclass
class Sims4Options(PerGameCommonOptions):
    goal: AspirationGoal

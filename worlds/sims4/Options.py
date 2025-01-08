from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, OptionSet
from .Names.DLC import ExpansionNames, GamePackNames, StuffNames

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
    """List of Expansion Packs that will be included in the shuffling."""
    display_name = "expansion_packs"
    valid_keys = {ExpansionNames.get_to_work, ExpansionNames.get_together, ExpansionNames.city_living,
                  ExpansionNames.cats_and_dogs, ExpansionNames.seasons, ExpansionNames.get_famous,
                  ExpansionNames.island_living, ExpansionNames.discover_university, ExpansionNames.eco_lifestyle,
                  ExpansionNames.snowy_escape, ExpansionNames.high_school_years, ExpansionNames.growing_together,
                  ExpansionNames.horse_ranch, ExpansionNames.for_rent, ExpansionNames.lovestruck,
                  ExpansionNames.life_and_death}

class GamePacks(OptionSet):
    """List of Game Packs that will be included in the shuffling."""
    display_name = "game_packs"
    valid_keys = {GamePackNames.outdoor_retreat, GamePackNames.spa_day, GamePackNames.dine_out,
                  GamePackNames.vampires, GamePackNames.parenthood, GamePackNames.jungle_adventure,
                  GamePackNames.stranger_ville, GamePackNames.realm_of_magic, GamePackNames.dream_home_decorator,
                  GamePackNames.my_wedding_stories, GamePackNames.werewolves}

class StuffPacks(OptionSet):
    """List of Stuff Packs that will be included in the shuffling."""
    display_name = "stuff_packs"
    valid_keys = {StuffNames.luxury_party, StuffNames.perfect_patio, StuffNames.cool_kitchen,
                  StuffNames.spooky, StuffNames.movie_hangout, StuffNames.romantic_garden,
                  StuffNames.kids_room, StuffNames.backyard, StuffNames.vintage_glamour,
                  StuffNames.bowling_night, StuffNames.fitness, StuffNames.toddler,
                  StuffNames.laundry_day, StuffNames.my_first_pet, StuffNames.moshino,
                  StuffNames.tiny_living, StuffNames.nifty_knitting, StuffNames.paranormal,
                  StuffNames.home_chef_hustle, StuffNames.crystal_creations}

@dataclass
class Sims4Options(PerGameCommonOptions):
    goal: AspirationGoal
    expansion_packs: ExpansionPacks
    game_packs: GamePacks
    stuff_packs: StuffPacks

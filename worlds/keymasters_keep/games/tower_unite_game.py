from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet 

from ..game import Game 
from ..game_objective_template import GameObjectiveTemplate 

from ..enums import KeymastersKeepGamePlatforms 


@dataclass
class TowerUniteArchipelagoOptions:
    tower_unite_multiplayer: TowerUniteMultiplayer
    plaza_activities: PlazaActivities
    game_worlds: GameWorlds

class TowerUniteGame(Game):
    name = "TowerUnite"
    #version = 0.18.5.1 as of the time of writing this
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = True
    #Tower Unite doesn't have an official rating as the game is working towards a 1.0 release/leaving Early Access

    options_cls = TowerUniteArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()
    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = list()

    if "Casino" in self.activities:
        templates.append(
              GameObjectiveTemplate(
                label="In the Casino, win a game of GAME.",
                data={
                    "GAME": (self.casino, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
                )
            )
        
        templates.append(
              GameObjectiveTemplate(
                label="In the Casino, cash out with a streak of at least 3 at Double or Nothing.",
                data={
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
                )
            )
        
        templates.append(
              GameObjectiveTemplate(
                label="In the Casino, get at least 4 hits in KENO.",
                data={
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
                )
            )
        
        templates.append(
              GameObjectiveTemplate(
                label="In the Casino, defeat the dragon in Grand Quest.",
                data={
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
                )
            )
        
        templates.append(
              GameObjectiveTemplate(
                label="In the Casino, get any combination of 3 at Triple Diamonds.",
                data={
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
                )
            )
        
        templates.append(
              GameObjectiveTemplate(
                label="In the Casino, spin the wheel 5 times in Wheel of Money.",
                data={
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
                )
            )
        if "PAEnabled" in self.multiplayer:
            templates.append(
                GameObjectiveTemplate(
                    label="In the Casino, win a game of GAME.",
                    data={
                        "GAME": (self.casino_multi, 1),              
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                    )
                )
    if "Arcade" in self.activities:
        templates.append(
            GameObjectiveTemplate(
                label="In the Arcade, play a round of GAME.",
                    data={
                        "GAME": (self.arcade, 1),              
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )
        
    if "Trivia" in self.activities:
        templates.append(
            GameObjectiveTemplate(
                label="Get a score of 3 or higher in Trivia.",
                    data={         
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            ) 

    if "Bowling" in self.activities:
        templates.append(
            GameObjectiveTemplate(
                label="Get a score of 150 or higher in Bowling.",
                    data={         
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )

    if "Laser Tag" in self.activities:
        if "PAEnabled" in self.multiplayer:
            templates.append(
                GameObjectiveTemplate(
                    label="Play a round of Laser Tag.",
                        data={          
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=3,
                    )
                )

    if "Dark Voyage" in self.activities:
        templates.append(
            GameObjectiveTemplate(
                label="Get a solo score higher than RANGE at Dark Voyage.",
                    data={
                        "RANGE": (self.dark_voyage_range, 1),           
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )
        if "PAEnabled" in self.multiplayer:
            templates.append(
                GameObjectiveTemplate(
                    label="Get a team score higher than RANGE at Dark Voyage.",
                        data={
                            "RANGE": (self.dark_voyage_multi_range, 1),              
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

    if "Minigames Arena" in self.activities:
        templates.append(
            GameObjectiveTemplate(
                label="Play any of the following minigames: Balloon Burst, Fruit Frenzy, Target Practice or any holiday exclusive minigame.",
                    data={         
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )
        if "PAEnabled" in self.multiplayer:
            templates.append(
            GameObjectiveTemplate(
                label="Play any of the following minigames: Chainsaw Deathmatch, Plane Wars, Snowball Battle or any holiday exclusive minigame.",
                    data={         
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )

    if "Billiards" in self.activities:
        templates.append(
            GameObjectiveTemplate(
                label="Play a game of Billiards/Pool at the Nightclub or the Arcade.",
                    data={         
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

    if "Boardwalk" in self.activities:
        templates.append(
            GameObjectiveTemplate(
                label="At the Boardwalk, play a round of GAME.",
                    data={
                        "GAME": (self.boardwalk, 1),         
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )

        templates.append(
            GameObjectiveTemplate(
                label="At the Boardwalk, ride the ATTRACTION attraction.",
                    data={
                        "ATTRACTION": (self.boardwalk_rides, 1),         
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )

        if "PAEnabled" in self.multiplayer:
            templates.append(
                GameObjectiveTemplate(
                    label="At the Boardwalk, play a round of Bumper Cars.",
                        data={       
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=2,
                    )
                )
    if "Fishing" in self.activities:
        templates.append(
            GameObjectiveTemplate(
                label="Fish up RANGE fish, marine life, treasures or trash using the bait: BAIT.",
                    data={
                        "RANGE": (self.fishing_range, 1),
                        "BAIT": (self.fishing_baits, 1),    
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )

    if "Minigolf" in self.worlds:
        templates.append(
            GameObjectiveTemplate(
                label="Complete a game of Minigolf on STAGE.",
                    data={
                        "STAGE": (self.minigolf_maps, 1),   
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )
        
        templates.append(
            GameObjectiveTemplate(
                label="Complete a game of Minigolf on a Custom Level.",
                    data={
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )

        templates.append(
            GameObjectiveTemplate(
                label="Get a hole in one on any map in Minigolf.",
                    data={
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        templates.append(
            GameObjectiveTemplate(
                label="Get par or under on STAGE in Minigolf.",
                    data={
                        "STAGE": (self.minigolf_maps, 1),   
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                )
            )

    if "Ball Race" in self.worlds:
        templates.append(
            GameObjectiveTemplate(
                label="Complete a game of Ball Race on STAGE.",
                    data={
                        "STAGE": (self.ball_race_maps, 1),   
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )
        
        templates.append(
            GameObjectiveTemplate(
                label="Complete a game of Ball Race on a Custom Level.",
                    data={
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )
        
        templates.append(
            GameObjectiveTemplate(
                label="Get at least 30 collectibles on any bonus stage in Ball Race.",
                    data={
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        templates.append(
            GameObjectiveTemplate(
                label="Complete a game of Ball Race on STAGE without dying once.",
                    data={
                        "STAGE": (self.ball_race_maps, 1),   
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                )
            )

    if "SDNL" in self.worlds:
        if "GWEnabled" in self.multiplayer:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete a game of SDNL on STAGE.",
                        data={
                            "STAGE": (self.sdnl_maps, 1),   
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=3,
                    )
                )
            
            templates.append(
                GameObjectiveTemplate(
                    label="Complete a game of SDNL on a Custom Level.",
                        data={
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )
            
            templates.append(
                GameObjectiveTemplate(
                    label="In SDNL, either place 1st or win with your team.",
                        data={
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    )
                )
            
            templates.append(
                GameObjectiveTemplate(
                    label="In SDNL, get 5 kills in total before the end of the match.",
                        data={
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=2,
                    )
                )
    
    if "Virus" in self.worlds:
        if "GWEnabled" in self.multiplayer:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete a game of Virus on STAGE.",
                        data={
                            "STAGE": (self.virus_maps, 1),   
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=3,
                    )
                )

            templates.append(
                GameObjectiveTemplate(
                    label="Complete a game of Virus on a Custom Level.",
                        data={
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )
            
            templates.append(
                GameObjectiveTemplate(
                    label="In Virus, survive a round without getting infected.",
                        data={
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    )
                )
            
            templates.append(
                GameObjectiveTemplate(
                    label="In Virus, infect 3 survivors in total before the end of the match.",
                        data={
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=2,
                    )
                )
        
    if "Little Crusaders" in self.worlds:
        if "GWEnabled" in self.multiplayer:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete a game of Little Crusaders on STAGE.",
                        data={
                            "STAGE": (self.little_crusaders_maps, 1),   
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=3,
                    )
                )
            
            templates.append(
                GameObjectiveTemplate(
                    label="Complete a game of Little Crusaders on a Custom Level.",
                        data={
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )
            
            templates.append(
                GameObjectiveTemplate(
                    label="In Little Crusaders, be promoted to the rank of Count.",
                        data={
                            "STAGE": (self.little_crusaders_maps, 1),   
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    )
                )
            
            templates.append(
                GameObjectiveTemplate(
                    label="In Little Crusaders, eat all the Knights in a single round.",
                        data={
                            "STAGE": (self.little_crusaders_maps, 1),   
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=2,
                    )
                )
    
    if "Zombie Massacre" in self.worlds:
        templates.append(
            GameObjectiveTemplate(
                label="Complete a game of Zombie Massacre on STAGE.",
                    data={
                        "STAGE": (self.zombie_massacre_maps, 1),   
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )
        
        templates.append(
            GameObjectiveTemplate(
                label="Complete a game of Zombie Massacre on a Custom Level.",
                    data={
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )
        
        templates.append(
            GameObjectiveTemplate(
                label="Complete a game of Zombie Massacre on STAGE as the ROLE.",
                    data={
                        "STAGE": (self.zombie_massacre_maps, 1),
                        "ROLE": (self.zombie_massacre_roles, 1),   
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        templates.append(
            GameObjectiveTemplate(
                label="Complete a game of Zombie Massacre on STAGE without dying once.",
                    data={
                        "STAGE": (self.zombie_massacre_maps, 1),   
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                )
            )

    if "Accelerate" in self.worlds:
        templates.append(
            GameObjectiveTemplate(
                label="Complete a game of Accelerate on STAGE.",
                    data={
                        "STAGE": (self.accelerate_maps, 1),   
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )
        if "GWEnabled" in self.multiplayer:
            templates.append(
            GameObjectiveTemplate(
                label="In Accelerate, place 1st with at least 2 other players in the match.",
                    data={
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                )
            )

            templates.append(
            GameObjectiveTemplate(
                label="In Accelerate, attack a player or defend against an attack.",
                    data={
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

    @property
    def multiplayer(self):
        return sorted(self.archipelago_options.tower_unite_multiplayer.value)

    @property
    def activities(self):
        return sorted(self.archipelago_options.plaza_activities.value)

    @property
    def worlds(self):
        return sorted(self.archipelago_options.game_worlds.value)
    
    @staticmethod
    def casino() -> List[str]:
        return [
            "Roulette",
            "Blackjack",
            "Silver Saddles",
            #"Double or Nothing",
            "Spin to Win",
            #"KENO",
            #"Grand Quest",
            #"Triple Diamonds",
            #"Wheel of Money",
            "Planet Bingo",
            "Video Poker",
            "Video Blackjack",
        ]

    @staticmethod
    def casino_multi() -> List[str]:
        return [
            "Five Card Draw",
            "Texas Hold'em",
        ]

    @staticmethod
    def arcade() -> List[str]:
        return [
            "Pluck-a-Pal",
            "Mind Tester",
            "Starfield Lanes",
            "Prismatic",
            "Sunlight Roller",
            "Wheel of Fire",
            "Ultimate Cow Wheel",
            "The Ice Cave",
            "Salmon Says",
            "Little Birde Feeders",
            "Mas Fuerte 2K",
            "Dizzy",
            "Avalanche",
            "The Offering",
            "Ring God",
            "Coloracle 2: Whose Hue",
            "Bug Bytes",
            "Whack-A-Mole",
            "Super Hoopers",
            "Planetary Piano",
            "Dragon's Treasure",
            "Lonely Gun 30XX",
            "Tornado",
            "Candy Slam",
            "Coin River",
            "Gears of Coin",
            "Whirl-a-Fish",
            "Newton's Apples",
            "Meteoroid Mania!",
            "Stack 'Em",
        ]
    
    @staticmethod
    def dark_voyage_range() -> List[str]:
        return (100 * range(40, 60))

    @staticmethod
    def dark_voyage_multi_range() -> List[str]:
        return (100 * range(80, 120))

    @staticmethod
    def boardwalk() -> List[str]:
        return [
            "Balloon Pop",
            "Milk Jug Toss",
            "Super Hoopers",
            "Splash Blasterz",
            "Roll and Race",
            "Typing Derby",
        ]

    @staticmethod
    def boardwalk_rides() -> List[str]:
        return [
            "Poseidon",
            "Ferris Wheel",
        ]

    @staticmethod
    def fishing_baits() -> List[str]:
        return [
            "Clump",
            "Curly Grub",
            "Gummy Worm",
            "Lure",
            "Maggot",
            "Magnet",
            "Meatball",
            "Mighty Ball",
            "Minnow",
            "Worm",
        ]

    @staticmethod
    def fishing_range() -> List[str]:
        return range(5, 20)
    
    @staticmethod
    def minigolf_maps() -> List[str]:
        return [
            "Haven",
            "Treasure Cove",
            "Waterhole",
            "Island",
            "Forest",
            "Garden",
            "Emission",
            "Mushroom Wood",
            "Nostalgia",
            "Dino Drive",
            "Altitude",
            "Alpine",
            "Sweet Tooth",
            "Kingdom",
        ]
    
    @staticmethod
    def ball_race_maps() -> List[str]:
        return [
            "Summit",
            "Woodlands",
            "GLXY",
            "Heavenscape",
            "Paradise",
            "Event Horizon",
            "Nimbus",
            "Khromidro",
            "Oasis",
            "Memories",
            "Eruption",
            "Prism",
            "Midori",
        ]

    @staticmethod
    def sdnl_maps() -> List[str]:
        return [
            "Hinderance",
            "Container Ship",
            "Decommision",
            "Frostbite",
            "Meadows",
        ]

    @staticmethod
    def virus_maps() -> List[str]:
        return [
            "Desertion",
            "Hospital",
            "Overtime",
            "Corrosion",
            "Solar",
            "Subway",
            "Catzek Temple",
        ]

    @staticmethod
    def little_crusaders_maps() -> List[str]:
        return [
            "Cardboard Castle",
            "Mystic Grove",
            "Knightsend-by-sea",
            "Market",
            "Throne Room",
            "Toy Room",
            "Amphitheatre",
        ]

    @staticmethod
    def zombie_massacre_maps() -> List[str]:
        return [
            "Trainyard",
            "Gasoline",
            "Compound",
            "Nightyard",
            "Village",
            "Acrophobia",
        ]

    @staticmethod
    def zombie_massacre_roles() -> List[str]:
        return [
            "Doctor",
            "Electrician",
            "Journalist",
            "Mercenary",
            "Survivor",
            "Scientist",
        ]

    @staticmethod
    def accelerate_maps() -> List[str]:
        return [
            "Holly Jolly Highway",
            "Wishy Washy Waterfall",
            "Pine Valley",
            "Sunrise Isles",
            "Riptide Retreat",
            "Criss-Cross Rapids",
            "Hallway Raceway",
            "Bedzoom",
        ]

# Archipelago Options
class TowerUniteMultiplayer(OptionSet):
    """
    Indicates if the player wants to include multiplayer content when generating objectives.
    """

    display_name = "Tower Unite Multiplayer"
    valid_keys = [
        "PAEnabled",
        "GWEnabled",
    ]

    default = valid_keys

class PlazaActivities(OptionSet):
    """
    Indicates which Plaza activities the player wants to include when generating objectives.
    """

    display_name = "Plaza Activities"
    valid_keys = [
        "Casino",
        "Arcade",
        "Trivia",
        "Bowling",
        "Laser Tag",
        "Dark Voyage",
        "Minigames Arena",
        "Billiards",
        "Boardwalk",
        "Fishing",
    ]

    default = valid_keys

class GameWorlds(OptionSet):
    """
    Indicates which Game Worlds the player wants to include when generating objectives.
    """

    display_name = "Game Worlds"
    valid_keys = [
        "Minigolf",
        "Ball Race",
        "SDNL",
        "Virus",
        "Little Crusaders",
        "Zombie Massacre",
        "Accelerate",
    ]

    default = valid_keys

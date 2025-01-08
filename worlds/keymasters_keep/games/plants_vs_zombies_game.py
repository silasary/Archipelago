from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PlantsVSZombiesArchipelagoOptions:
    pass


class PlantsVSZombiesGame(Game):
    name = "Plants vs. Zombies"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.NDS,
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.VITA,
        KeymastersKeepGamePlatforms.X360,
    ]

    is_adult_only_or_unrated = False

    options_cls = PlantsVSZombiesArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Cannot use the following plants: PLANTS",
                data={
                    "PLANTS": (self.plants, 5),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete the following Minigame: MINIGAME",
                data={
                    "MINIGAME": (self.minigames, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete ADVENTURE in Adventure Mode",
                data={
                    "ADVENTURE": (self.adventure, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete the following Vasebreaker level: VASEBREAKER",
                data={
                    "VASEBREAKER": (self.vasebreaker, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete the following I, Zombie level: I_ZOMBIE",
                data={
                    "I_ZOMBIE": (self.i_zombie, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain the following achievement: ACHIEVEMENT",
                data={
                    "ACHIEVEMENT": (self.achievements, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach Wave WAVE in ENDLESS",
                data={
                    "WAVE": (self.endless_range, 1),
                    "ENDLESS": (self.endless, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def minigames() -> List[str]:
        return [
            "Beghouled Twist",
            "Beghouled",
            "Big Trouble Little Zombie",
            "Bobsled Bonanza",
            "Column Like You See Em",
            "Dr. Zomboss's Revenge",
            "Invisi-ghoul",
            "It's Raining Seeds",
            "Last Stand",
            "Pogo Party",
            "Portal Combat",
            "Seeing Stars",
            "Slot Machine",
            "Wall-nut Bowling 2",
            "Wall-nut Bowling",
            "Whack a Zombie",
            "ZomBotany 2",
            "Zombie Nimble Zombie Quick",
            "Zombiquarium",
            "Zombotany",
        ]

    @staticmethod
    def vasebreaker() -> List[str]:
        return [
            "Vasebreaker",
            "To the Left",
            "Third Vase",
            "Chain Reaction",
            "M is for Metal",
            "Scary Potter",
            "Hokey Pokey",
            "Another Chain Reaction",
            "Ace of Vase",
        ]

    @staticmethod
    def i_zombie() -> List[str]:
        return [
            "I, Zombie",
            "I, Zombie Too",
            "Can You Dig It?",
            "Totally Nuts",
            "Dead Zeppelin",
            "Me Smash!",
            "ZomBoogie",
            "Three Hit Wonder",
            "All your brainz r belong to us",
        ]

    @staticmethod
    def survival() -> List[str]:
        return [
            "Survival: Day",
            "Survival: Night",
            "Survival: Pool",
            "Survival: Fog",
            "Survival: Roof",
            "Survival: Day (Hard)",
            "Survival: Night (Hard)",
            "Survival: Pool (Hard)",
            "Survival: Fog (Hard)",
            "Survival: Roof (Hard)",
            "Survival: Roof (Hard)",
        ]

    @staticmethod
    def adventure() -> List[str]:
        return [
            "Day 1",
            "Day 2",
            "Day 3",
            "Day 4",
            "Day 5",
            "Day 6",
            "Day 7",
            "Day 8",
            "Day 9",
            "Day 10",
            "Night 1",
            "Night 2",
            "Night 3",
            "Night 4",
            "Night 5",
            "Night 6",
            "Night 7",
            "Night 8",
            "Night 9",
            "Night 10",
            "Pool 1",
            "Pool 2",
            "Pool 3",
            "Pool 4",
            "Pool 5",
            "Pool 6",
            "Pool 7",
            "Pool 8",
            "Pool 9",
            "Pool 10",
            "Fog 1",
            "Fog 2",
            "Fog 3",
            "Fog 4",
            "Fog 5",
            "Fog 6",
            "Fog 7",
            "Fog 8",
            "Fog 9",
            "Fog 10",
            "Roof 1",
            "Roof 2",
            "Roof 3",
            "Roof 4",
            "Roof 5",
            "Roof 6",
            "Roof 7",
            "Roof 8",
            "Roof 9",
            "Roof 10",
        ]

    @staticmethod
    def achievements() -> List[str]:
        return [
            "Ask Me About Mustache Mode",
            "Better Off Dead",
            "Beyond the Grave",
            "China Shop",
            "Cryptozombologist",
            "Disco is Undead",
            "Don't Pea in the Pool",
            "Explodonator",
            "Good Morning",
            "Grounded",
            "Home Lawn Security",
            "Immortal",
            "Morticulturalist",
            "No Fungus Among Us",
            "Nobel Peas Prize",
            "Penny Pincher",
            "Popcorn Party",
            "Roll Some Heads",
            "SPUDOW!",
            "Sunny Days",
            "Towering Wisdom",
        ]

    @staticmethod
    def endless_range() -> range:
        return range(1, 31)

    @staticmethod
    def endless() -> List[str]:
        return [
            "I, Zombie Endless",
            "Vasebreaker Endless",
            "Survival Endless",
        ]

    @staticmethod
    def plants() -> List[str]:
        return [
            "Peashooter",
            "Sunflower",
            "Cherry Bomb",
            "Wall-nut",
            "Potato Mine",
            "Snow Pea",
            "Chomper",
            "Repeater",
            "Puff-Shroom",
            "Sun-Shroom",
            "Fume-Shroom",
            "Grave Buster",
            "Hypno-Shroom",
            "Scaredy-Shroom",
            "Ice-Shroom",
            "Doom-Shroom",
            "Lily Pad",
            "Squash",
            "Threepeater",
            "Tangle Kelp",
            "Jalapeno",
            "Spikeweed",
            "Torchwood",
            "Tall-nut",
            "Sea-Shroom",
            "Plantern",
            "Cactus",
            "Blover",
            "Split Pea",
            "Starfruit",
            "Pumpkin",
            "Magnet-Shroom",
            "Cabbage-pult",
            "Flower Pot",
            "Kernel-pult",
            "Coffee Bean",
            "Garlic",
            "Umbrella Leaf",
            "Marigold",
            "Melon-pult",
            "Gatling Pea",
            "Twin Sunflower",
            "Gloom-shroom",
            "Cattail",
            "Winter Melon",
            "Gold Magnet",
            "Spikerock",
            "Cob Cannon",
            "Imitater",
        ]

# Archipelago Options
# ...

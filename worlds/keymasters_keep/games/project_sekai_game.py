from __future__ import annotations

from typing import List
from math import ceil

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import Choice, OptionSet


@dataclass
class ProjectSekaiArchipelagoOptions:
    project_sekai_include_songs: ProjectSekaiIncludeSongs
    project_sekai_min_difficulty: ProjectSekaiMinDifficulty
    project_sekai_max_difficulty: ProjectSekaiMaxDifficulty


# Pair setup

virtual_singers = [
    "Hatsune Miku",
    "Kagamine Rin",
    "Kagamine Len",
    "Megurine Luka",
    "MEIKO",
    "KAITO"
]

leo_need = [
    "Ichika Hoshino",
    "Saki Tenma",
    "Shiho Hinomori",
    "Honami Mochizuki"
]

more_more_jump = [
    "Minori Hanasato",
    "Haruka Kiritani",
    "Airi Momoi",
    "Shizuku Hinomori"
]

vivid_bad_squad = [
    "Kohane Azusawa",
    "An Shiraishi",
    "Akito Shinonome",
    "Toya Aoyagi"
]

wonderlands_x_showtime = [
    "Tsukasa Tenma",
    "Emu Otori",
    "Rui Kamishiro",
    "Nene Kusanagi"
]

nightcord_at_2500 = [
    "Kanade Yoisaki",
    "Mafuyu Asahina",
    "Ena Shinonome",
    "Mizuki Akiyama"
]

pairs = [
    # intra-group pairs
    "Shiho Hinomori and Shizuku Hinomori",
    "Saki Tenma and Tsukasa Tenma",
    "Akito Shinonome and Ena Shinonome",
    # cross-leader pairs
    "Ichika Hoshino and Minori Hanasato",
    "Ichika Hoshino and Kohane Azusawa",
    "Ichika Hoshino and Tsukasa Tenma",
    "Ichika Hoshino and Kanade Yoisaki",
    "Minori Hanasato and Kohane Azusawa",
    "Minori Hanasato and Tsukasa Tenma",
    "Minori Hanasato and Kanade Yoisaki",
    "Kohane Azusawa and Tsukasa Tenma",
    "Kohane Azusawa and Kanade Yoisaki",
    "Tsukasa Tenma and Kanade Yoisaki",
    # one singular song, not including April Fools for now
    "Robo-Nene and Mikudayo"
]
for group in [leo_need, more_more_jump, vivid_bad_squad, wonderlands_x_showtime, nightcord_at_2500, virtual_singers]:
    for member in group:
        for secondary in sorted({*group, *virtual_singers}):
            if member == secondary:
                pairs.append(member)
            else:
                pairs.append(f"{member} and {secondary}")


class ProjectSekaiGame(Game):
    name = "Project Sekai: Colorful Stage"
    platform = KeymastersKeepGamePlatforms.AND

    platforms_other = [KeymastersKeepGamePlatforms.IOS]

    is_adult_only_or_unrated = False

    options_cls = ProjectSekaiArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives = [
            GameObjectiveTemplate(
                label="Complete a show featuring PAIR",
                data={"PAIR": (self.characters, 1)},
                weight=10
            ),
            GameObjectiveTemplate(
                label="Complete a show featuring PAIR with 7 or less GOOD/BAD/MISS",
                data={"PAIR": (self.characters, 1)},
                weight=4
            ),
            GameObjectiveTemplate(
                label="Complete a show featuring PAIR on DIFF difficulty (or higher)",
                data={"PAIR": (self.characters, 1), "DIFF": (self.difficulties, 1)},
                weight=6
            ),
            GameObjectiveTemplate(
                label="Complete a show featuring PAIR on DIFF difficulty (or higher) with 7 or less GOOD/BAD/MISS",
                data={"PAIR": (self.characters, 1), "DIFF": (self.difficulties, 1)},
                is_difficult=True,  # arguable but it is asking a bit more out of you
                weight=2
            ),
            GameObjectiveTemplate(
                label="Complete 5 shows with 3DMVs",
                data={},
                weight=2
            ),
            GameObjectiveTemplate(
                label="Complete 5 shows with 2DMVs/Original MVs",
                data={},
                weight=2
            ),
            GameObjectiveTemplate(
                label="Complete 5 Co-op/Cheerful Shows",
                data={},
                weight=4
            ),
            GameObjectiveTemplate(
                label="Complete 5 shows featuring songs from the following groups: GROUP",
                data={"GROUP": (self.groups, range(1, 4))},
                weight=6
            )
        ]
        if self.archipelago_options.include_difficult_objectives and \
                self.archipelago_options.project_sekai_max_difficulty in ("expert", "master"):
            objectives.extend([
                GameObjectiveTemplate(
                    label="Complete a show on APPEND difficulty",
                    data={},
                    is_difficult=True,
                    weight=4
                ),
                GameObjectiveTemplate(
                    label="Complete a show on APPEND difficulty with 7 or less GOOD/BAD/MISS",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=2
                ),
            ])
        else:
            objectives.append(GameObjectiveTemplate(
                label="Attempt a show on APPEND difficulty",
                data={},
                weight=2
            ))
        if self.archipelago_options.project_sekai_include_songs:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Play SONG on DIFF difficulty (or higher)",
                    data={"SONG": (self.songs, 1), "DIFF": (self.difficulties, 1)},
                    weight=max(1, ceil(len(self.songs()) / 4))
                ),
                GameObjectiveTemplate(
                    label="Play SONG on DIFF difficulty (or higher) with 7 or less GOOD/BAD/MISS",
                    data={"SONG": (self.songs, 1), "DIFF": (self.difficulties, 1)},
                    weight=max(1, ceil(len(self.songs()) / 4) - 2)
                ),
            ])
        return objectives

    @staticmethod
    def characters():
        return pairs

    def difficulties(self):
        difficulties = [
            "Easy",
            "Normal",
            "Hard",
            "Expert",
            "Master"
        ]
        return difficulties[self.archipelago_options.project_sekai_min_difficulty.value:
                            self.archipelago_options.project_sekai_max_difficulty.value + 1]

    def songs(self):
        return sorted(self.archipelago_options.project_sekai_include_songs.value)

    @staticmethod
    def groups():
        return [
            "VIRTUAL SINGERs",
            "Leo/need",
            "MORE MORE JUMP!",
            "Vivid BAD Squad",
            "Wonderlands X Showtime",
            "Nightcord at 25:00"
        ]


class ProjectSekaiIncludeSongs(OptionSet):
    """Additional songs that can be rolled as objectives in Project Sekai"""
    display_name = "Project Sekai Include Songs"


class ProjectSekaiMinDifficulty(Choice):
    """The minimum difficulty that should be rolled for objectives in Project Sekai"""
    display_name = "Project Sekai Min Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3
    option_master = 4
    default = 1


class ProjectSekaiMaxDifficulty(Choice):
    """The minimum difficulty that should be rolled for objectives in Project Sekai (excluding APPEND)"""
    display_name = "Project Sekai Max Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3
    option_master = 4
    default = 2

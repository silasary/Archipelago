from __future__ import annotations

from typing import Any, List, Tuple, Type

from dataclasses import dataclass
from random import Random

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GameMedleyArchipelagoOptions:
    pass


class GameMedleyGame(Game):
    name = "Game Medley"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_metagame = True
    is_adult_only_or_unrated = False

    should_autoregister = False

    options_cls = GameMedleyArchipelagoOptions

    game_selection: List[Type[Game]]

    def __init__(
        self,
        random: Random = None,
        include_time_consuming_objectives: bool = False,
        include_difficult_objectives: bool = False,
        archipelago_options: Any = None,
        game_selection: List[Type[Game]] = None
    ) -> None:
        super().__init__(
            random=random,
            include_time_consuming_objectives=include_time_consuming_objectives,
            include_difficult_objectives=include_difficult_objectives,
            archipelago_options=archipelago_options
        )

        self.game_selection = game_selection

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def generate_objectives(
        self,
        count: int = 1,
        include_difficult: bool = False,
        include_time_consuming: bool = False,
    ) -> Tuple[List[str], List[str]]:
        optional_constraints: List[str] = list()
        objectives: List[str] = list()

        for _ in range(count):
            game: Type[Game] = self.random.choice(self.game_selection)
            game_instance: Game = game(random=self.random, archipelago_options=self.archipelago_options)

            templates: List[GameObjectiveTemplate] = game_instance.filter_game_objective_templates(
                include_difficult=include_difficult,
                include_time_consuming=include_time_consuming,
            )

            if not len(templates):
                templates = game_instance.game_objective_templates()

            weights: List[int] = [template.weight for template in templates]

            objective_template: GameObjectiveTemplate = self.random.choices(templates, weights=weights)[0]

            objective: str = objective_template.generate_game_objective(self.random)
            objective = f"{game.name} -> {objective}"

            objectives.append(objective)

        return optional_constraints, objectives

# Archipelago Options
# ...

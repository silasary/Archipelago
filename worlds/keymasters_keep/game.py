from __future__ import annotations

import abc

from collections import Counter
from random import Random
from typing import Any, Dict, List, Optional, Tuple, Type

from .enums import KeymastersKeepGamePlatforms

from .game_objective_template import GameObjectiveTemplate


class AutoGameRegister(type):
    games: Dict[str, Type[Game]] = dict()

    def __new__(mcs, name: str, bases: Tuple[type, ...], dict_: Dict[str, Any]) -> AutoGameRegister:
        new_class: Type[Game] = super().__new__(mcs, name, bases, dict_)

        if name != "Game" and new_class.should_autoregister:
            game_name: str = new_class.game_name_with_platforms()
            mcs.games[game_name] = new_class

        return new_class


class Game(metaclass=AutoGameRegister):
    name: str  # Official name of the game. Use a resource like IGDB to get the correct name
    platform: KeymastersKeepGamePlatforms  # Platform that the game integration was developed with and tested on

    # Other available platforms the game integration might work with
    platforms_other: Optional[List[KeymastersKeepGamePlatforms]] = None

    is_adult_only_or_unrated: bool = True  # ESRB AO / PEGI 18 / USK 18 / Unrated? Used for filtering

    should_autoregister: bool = True  # Development flag. Used to prevent AutoGameRegister from registering the game

    include_time_consuming_objectives: bool = False  # Set automatically based on player options
    include_difficult_objectives: bool = False  # Set automatically based on player options

    archipelago_options: Any  # Archipelago options dataclass (for access)

    random: Random  # Random instance

    options_cls: Type = None  # Archipelago options type

    def __init__(
        self,
        random: Random = None,
        include_time_consuming_objectives: bool = False,
        include_difficult_objectives: bool = False,
        archipelago_options: Any = None,
    ) -> None:
        self.random = random or Random()
        self.include_time_consuming_objectives = include_time_consuming_objectives
        self.include_difficult_objectives = include_difficult_objectives
        self.archipelago_options = archipelago_options

    @property
    def only_has_difficult_objectives(self) -> bool:
        template: GameObjectiveTemplate
        for template in self.game_objective_templates():
            if not template.is_difficult:
                return False

        return True

    @property
    def only_has_time_consuming_objectives(self) -> bool:
        template: GameObjectiveTemplate
        for template in self.game_objective_templates():
            if not template.is_time_consuming:
                return False

        return True

    @property
    def has_objectives(self) -> bool:
        return bool(self.game_objective_templates())

    @abc.abstractmethod
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    @abc.abstractmethod
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        ...

    def filter_game_objective_templates(
        self,
        include_difficult: bool = False,
        include_time_consuming: bool = False,
    ) -> List[GameObjectiveTemplate]:
        filtered_objectives: List[GameObjectiveTemplate] = list()

        template: GameObjectiveTemplate
        for template in self.game_objective_templates():
            if not include_difficult and template.is_difficult:
                continue

            if not include_time_consuming and template.is_time_consuming:
                continue

            filtered_objectives.append(template)

        return filtered_objectives

    def generate_objectives(
        self,
        count: int = 1,
        include_difficult: bool = False,
        include_time_consuming: bool = False,
        objectives_in_use: Counter[str] | None = None,
        objective_bag_size: int = 1,
        **kwargs: Any,
    ) -> tuple[list[str], list[str], Counter[str]]:
        objectives_in_use = objectives_in_use or Counter()

        optional_constraints: list[str] = []
        optional_constraint_templates: list[GameObjectiveTemplate] = self.optional_game_constraint_templates()

        if len(optional_constraint_templates):
            template: GameObjectiveTemplate = self.random.choice(self.optional_game_constraint_templates())
            optional_constraints.append(template.generate_game_objective(self.random))

        filtered_templates: list[GameObjectiveTemplate] = self.filter_game_objective_templates(
            include_difficult=include_difficult,
            include_time_consuming=include_time_consuming,
        )

        weights: list[int] = [template.weight for template in filtered_templates]
        objectives: list[str] = []

        passes_templates: int = 0

        while len(objectives) < count:
            passes_templates += 1

            template: GameObjectiveTemplate = self.random.choices(filtered_templates, weights=weights, k=1)[0]

            passes: int = 0

            while True:
                passes += 1
                objective: str = template.generate_game_objective(self.random)

                if objective_bag_size == 0 or objectives_in_use[objective] < objective_bag_size:
                    objectives.append(objective)
                    objectives_in_use[objective] += 1

                    break

                if passes_templates > 50:
                    objectives.append(objective)
                    objectives_in_use[objective] += 1
                    break

                if passes > 10:
                    break

        return optional_constraints, objectives, objectives_in_use

    @classmethod
    def game_name_with_platforms(cls) -> str:
        game_name = f"{cls.name} ({cls.platform.value}"

        if cls.platforms_other:
            game_name += " + "
            game_name += f"{', '.join(platform.value for platform in cls.platforms_other)}"

        game_name += ")"

        return game_name

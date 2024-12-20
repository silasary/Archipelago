from random import Random
from typing import Any, Dict, List, Tuple, Type

from .game import Game
from .games import games, metagames


GameObjectiveGeneratorData = List[Tuple[Type[Game], List[str], List[str]]]


class GameObjectiveGenerator:
    games: List[Type[Game]]
    archipelago_options: Any

    def __init__(
        self,
        allowable_games: List[str] = None,
        include_adult_only_or_unrated_games: bool = False,
        archipelago_options: Any = None,
    ) -> None:
        self.games = self._filter_games(allowable_games, include_adult_only_or_unrated_games)
        self.archipelago_options = archipelago_options

    def generate_from_plan(
        self,
        plan: List[int] = None,
        random: Random = None,
        include_difficult: bool = False,
        include_time_consuming: bool = False,
    ) -> GameObjectiveGeneratorData:
        if plan is None or not len(plan):
            return list()

        plan_length: int = len(plan)
        random = random or Random()

        game_selection: List[Type[Game]] = list()

        if plan_length <= len(self.games):
            game_selection = random.sample(self.games, plan_length)
        else:
            for _ in range(plan_length):
                game_selection.append(random.choice(self.games))

        data: GameObjectiveGeneratorData = list()

        i: int
        count: int
        for i, count in enumerate(plan):
            game: Type[Game] = game_selection[i](random=random, archipelago_options=self.archipelago_options)

            optional_constraints: List[str]
            objectives: List[str]
            optional_constraints, objectives = game.generate_objectives(
                count=count,
                include_difficult=include_difficult,
                include_time_consuming=include_time_consuming,
            )

            data.append((game, optional_constraints, objectives))

        return data

    @staticmethod
    def _filter_games(allowable_games: List[str], include_adult_only_or_unrated_games: bool) -> Dict[str, Type[Game]]:
        filtered_games = list()

        game_name: str
        for game_name in allowable_games:
            if game_name not in games and game_name not in metagames:
                continue

            game: Type[Game] = games.get(game_name, metagames.get(game_name))

            if not include_adult_only_or_unrated_games and game.is_adult_only_or_unrated:
                continue

            filtered_games.append(game)

        return filtered_games

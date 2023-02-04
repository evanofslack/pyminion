import copy
import logging
from typing import List, Union

from pyminion.bots.bot import Bot
from pyminion.game import Game
from pyminion.players import Human, Player
from pyminion.result import GameResult, SimulatorResult, SimulatorStats

logger = logging.getLogger()


def get_percent(occurrence: int, total: int) -> float:
    """
    helper function to compute percent

    """
    return round(((occurrence / total) * 100), 3)


class Simulator:
    """
    Simulate multiple games of dominion and compute statistics

    Attributes:
        game: pyminion game instance.
        iterations: number of times the game will be simulated.

    """

    def __init__(self, game: Game, iterations: int = 100):
        self.game = game
        self.iterations = iterations
        self.results: List[GameResult]

    def run(self) -> SimulatorStats:
        logger.info(f"Simulating {self.iterations} games...")
        for _ in range(self.iterations):
            game = copy.copy((self.game))
            result = game.play()
            self.results.append(result)

        return self.summerize_simulation()

        # self.get_stats()

    def summerize_simulation(self) -> SimulatorResult:
        result = SimulatorResult(iterations=self.iterations, game_results=self.results)
        return result

    # def get_stats(self) -> None:
    #     logger.info(f"\nSimulation of {self.iterations} games")
    #     for player in self.game.players:
    #         logger.info(
    #             f"{player.player_id} wins: {get_percent(self.winners.count(player), self.iterations)}% ({self.winners.count(player)})"
    #         )
    #
    #     logger.info(
    #         f"Ties: {get_percent(self.winners.count('tie'), self.iterations)}% ({self.winners.count('tie')})\n"
    #     )

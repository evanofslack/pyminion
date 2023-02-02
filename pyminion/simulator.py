import copy
import logging
from typing import List, Union

from pyminion.bots.bot import Bot
from pyminion.game import Game
from pyminion.players import Human, Player

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
        self.winners: List[Union[Player, Human, Bot]]

    def run(self) -> None:
        logger.info(f"Simulating {self.iterations} games...")
        winners = []
        for i in range(self.iterations):
            game = copy.copy((self.game))
            game.play()
            winner = game.get_winner()
            winners.append(winner if winner else "tie")
        self.winners = winners
        self.get_stats()

    def get_stats(self) -> None:
        logger.info(f"\nSimulation of {self.iterations} games")
        for player in self.game.players:
            logger.info(
                f"{player.player_id} wins: {get_percent(self.winners.count(player), self.iterations)}% ({self.winners.count(player)})"
            )

        logger.info(
            f"Ties: {get_percent(self.winners.count('tie'), self.iterations)}% ({self.winners.count('tie')})\n"
        )

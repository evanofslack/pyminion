import copy
import logging
from typing import List, Union

from pyminion.game import Game
from pyminion.players import Bot, Human, Player

logger = logging.getLogger()


class Simulator:
    def __init__(self, game: Game, iterations: int = 100):
        self.game = game
        self.iterations = iterations
        self.winners: List[Union[Player, Human, Bot]] = None

    def run(self) -> List[str]:
        logger.info(f"Simulating {self.iterations} games...")
        winners = []
        for i in range(self.iterations):
            game = copy.copy((self.game))
            game.play()
            winner = game.get_winner()
            game.get_stats()
            winners.append(winner if winner else "tie")
        self.winners = winners
        return winners

    def get_stats(self):
        logger.info(f"\n\nSimulation of {self.iterations} games")
        for player in self.game.players:
            logger.info(f"{player.player_id} wins: {self.winners.count(player)}")
        logger.info(f"Ties: {self.winners.count('tie')}")

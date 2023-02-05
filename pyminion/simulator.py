import copy
import logging
from typing import Dict, List

from pyminion.game import Game
from pyminion.players import Player
from pyminion.result import GameResult, PlayerSimulatorResult, SimulatorResult

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
        self.results: List[GameResult] = []

    def run(self) -> SimulatorResult:
        logger.info(f"Simulating {self.iterations} games...")
        for _ in range(self.iterations):
            game = copy.copy((self.game))
            result = game.play()
            self.results.append(result)

        return self.get_sim_result()

    def get_sim_result(self) -> SimulatorResult:

        # make temp hashmap to store player sim results
        player_results: Dict[Player, PlayerSimulatorResult] = {}

        # initialize each player result with default values
        for player in self.game.players:
            player_results[player] = PlayerSimulatorResult(
                player=player, wins=0, losses=0, ties=0
            )

        # iterate through each simulated game to determine win record
        for result in self.results:

            # single player wins
            if len(result.winners) == 1:
                player_results[result.winners[0]].wins += 1

            # multiple players tie
            else:
                for player in result.winners:
                    player_results[player].ties += 1

            # rest of players are losers
            for player in self.game.players:
                if player not in result.winners:
                    player_results[player].losses += 1

        player_results_final: List[PlayerSimulatorResult] = list(
            player_results.values()
        )

        sim_result = SimulatorResult(
            iterations=self.iterations,
            game_results=self.results,
            player_results=player_results_final,
        )
        return sim_result

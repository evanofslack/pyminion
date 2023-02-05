from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from pyminion.core import DeckCounter
    from pyminion.game import Game
    from pyminion.players import Player


class GameOutcome(Enum):
    """
    player can either lose, tie, or win the game

    """

    loss = -1
    tie = 0
    win = 1


@dataclass
class PlayerSummary:
    """
    holds summary of a player from a complete game

    """

    player: "Player"
    result: GameOutcome
    score: int
    turns: int
    shuffles: int
    turn_order: int
    deck: "DeckCounter"

    def __repr__(self):

        order_format = "None"
        if self.turn_order == 1:
            order_format = "1st"

        elif self.turn_order == 2:
            order_format = "2nd"

        elif self.turn_order == 3:
            order_format = "3rd"

        elif self.turn_order == 4:
            order_format = "4th"

        player = f"Player: {self.player.player_id}"
        result = f"Result: {self.result.name}"
        score = f"Score: {self.score}"
        turns = f"Turns: {self.turns}"
        shuffles = f"Shuffles: {self.shuffles}"
        order = f"Turn Order: {order_format}"
        deck = f"Deck: {self.deck}"

        return f"{player}\n{result}\n{score}\n{turns}\n{shuffles}\n{order}\n{deck}"


@dataclass
class GameResult:
    """
    holds summary of a complete game

    """

    game: "Game"
    winners: List["Player"]
    turns: int
    player_summaries: List[PlayerSummary]

    def __repr__(self):
        if len(self.winners) == 1:
            result = f"{self.winners[0]} won in {self.turns} turns"
        else:
            result = f"{[w for w in self.winners]} tied after {self.turns} turns"

        format_summaries = ""
        for s in self.player_summaries:
            format_summaries += f"\n{s}"

        return f"Game Result: {result}{format_summaries}"


@dataclass
class PlayerSimulatorResult:
    player: "Player"
    wins: int
    losses: int
    ties: int


@dataclass
class SimulatorResult:
    """
    holds summary of game outcomes over a simulation

    """

    iterations: int
    game_results: List[GameResult]
    player_results: List[PlayerSimulatorResult]

    def __repr__(self):
        title = f"ran {self.iterations} games"

        format_results = ""
        for result in self.player_results:
            format_results += f"\n{result.player.player_id} won {result.wins}, lost {result.losses}, tied {result.ties}"

        return f"Simulation Result: {title}{format_results}"

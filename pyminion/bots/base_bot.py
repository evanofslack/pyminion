import logging
from typing import TYPE_CHECKING, List, Optional

from pyminion.bots import AbstractBot
from pyminion.core import Card
from pyminion.players import Player

if TYPE_CHECKING:
    from pyminion.game import Game

logger = logging.getLogger()


class Bot(AbstractBot):
    """
    Barebones implementation of Bot class.
    Implements default responses as to not crash the game.
    Not optimized in the slightest.

    """

    def __init__(
        self,
        player_id: str = "bot",
    ):
        super().__init__(player_id=player_id)

    def binary_resp(
        self, card: Card, relevant_cards: Optional[List[Card]] = None
    ) -> bool:
        return True

    def discard_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def multiple_discard_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_discard: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:
        if required:
            return valid_cards[:num_discard]
        else:
            return None

    def gain_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def multiple_gain_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_gain: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:
        if required:
            return valid_cards[:num_gain]
        else:
            return None

    def trash_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Card:
        if required:
            return valid_cards[0]
        else:
            return None

    def multiple_trash_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_trash: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:
        if required:
            return valid_cards[:num_trash]
        else:
            return None

    def topdeck_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def double_play_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        return True

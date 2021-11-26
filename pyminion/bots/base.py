import logging
from typing import List, Optional

from pyminion.bots import AbstractBot
from pyminion.core import Card
from pyminion.players import Player

logger = logging.getLogger()


class Bot(AbstractBot):
    """
    Barebones implementation of Bot class.
    Implement default responses to not crash the game with an error.
    Not optimized in the slightest.

    """

    def __init__(
        self,
        player_id: str = "bot",
    ):
        super().__init__(player_id=player_id)

    def binary_resp(self, card: Card) -> bool:
        return True

    def discard_resp(
        self, card: Card, valid_cards: List[Card], required: bool = True
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def multiple_discard_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        num_discard: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:
        if required:
            return valid_cards[:num_discard]
        else:
            return None

    def gain_resp(
        self, card: Card, valid_cards: List[Card], required: bool = True
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def multiple_gain_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        num_gain: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:
        if required:
            return valid_cards[:num_gain]
        else:
            return None

    def trash_resp(
        self, card: Card, valid_cards: List[Card], required: bool = True
    ) -> Card:
        if required:
            return valid_cards[0]
        else:
            return None

    def multiple_trash_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        num_trash: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:
        if required:
            return valid_cards[:num_trash]
        else:
            return None

    def topdeck_resp(
        self, card: Card, valid_cards: List[Card], required: bool = True
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        # for card in self.hand.cards:
        #     if card.name == "Moat":
        #         return False
        return True

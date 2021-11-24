import logging
from typing import Iterator

from pyminion.bots import Bot
from pyminion.expansions.base import gold, province, silver
from pyminion.game import Game
from pyminion.models.core import Card, Deck

logger = logging.getLogger()


class BigMoney(Bot):
    """
    Only buys money and provinces

    """

    def __init__(
        self,
        deck: Deck = None,
        player_id: str = "big_money",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def buy_priority(self, game: Game) -> Iterator[Card]:

        money = self.state.money

        if money >= 8:
            yield province
        if money >= 6:
            yield gold
        if money >= 3:
            yield silver

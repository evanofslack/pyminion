import logging
from typing import Iterator

from pyminion.bots import Bot
from pyminion.expansions.base import gold, province, silver, smithy
from pyminion.game import Game
from pyminion.models.core import Card

logger = logging.getLogger()


class BigMoney(Bot):
    """
    Only buys money and provinces

    """

    def __init__(
        self,
        player_id: str = "big_money",
    ):
        super().__init__(player_id=player_id)

    def action_priority(self, game: Game) -> Iterator[Card]:
        yield smithy

    def buy_priority(self, game: Game) -> Iterator[Card]:
        money = self.state.money
        if money >= 8:
            yield province
        if money >= 6:
            yield gold
        if money >= 4:
            yield smithy
        if money >= 3:
            yield silver

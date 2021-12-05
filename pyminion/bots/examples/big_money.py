import logging
from typing import Iterator

from pyminion.bots.bot import Bot
from pyminion.core import Card
from pyminion.expansions.base import gold, province, silver
from pyminion.game import Game

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

    def buy_priority(self, game: Game) -> Iterator[Card]:
        money = self.state.money
        if money >= 8:
            yield province
        if money >= 6:
            yield gold
        if money >= 3:
            yield silver

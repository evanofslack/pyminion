import logging

from pyminion.bots.bot import Bot
from pyminion.expansions.base import gold, province, silver, smithy
from pyminion.game import Game

logger = logging.getLogger()


class BigMoneySmithy(Bot):
    """
    Big money + smithy

    """

    def __init__(
        self,
        player_id: str = "big_money_smithy",
    ):
        super().__init__(player_id=player_id)

    def action_priority(self, game: Game):
        yield smithy

    def buy_priority(self, game: Game):
        money = self.state.money
        if money >= 8:
            yield province
        if money >= 6:
            yield gold
        if money == 4:
            yield smithy
        if money >= 3:
            yield silver

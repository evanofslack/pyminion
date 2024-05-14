import logging
from typing import Iterator

from pyminion.bots.bot import Bot, BotDecider
from pyminion.core import Card
from pyminion.expansions.base import gold, province, silver
from pyminion.player import Player
from pyminion.game import Game

logger = logging.getLogger()


class BigMoneyDecider(BotDecider):
    """
    Only buys money and provinces

    """

    def action_priority(self, player: Player, game: Game) -> Iterator[Card]:
        return iter([])

    def buy_priority(self, player: Player, game: Game) -> Iterator[Card]:
        money = player.state.money
        if money >= 8:
            yield province
        if money >= 6:
            yield gold
        if money >= 3:
            yield silver


class BigMoney(Bot):
    def __init__(
        self,
        player_id: str = "big_money",
    ):
        super().__init__(decider=BigMoneyDecider(), player_id=player_id)

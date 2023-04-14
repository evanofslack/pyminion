from pyminion.bots.bot import Bot, BotDecider
from pyminion.expansions.base import gold, province, silver, smithy
from pyminion.player import Player
from pyminion.game import Game


class BigMoneySmithyDecider(BotDecider):
    """
    Big money + smithy

    """

    def action_priority(self, player: Player, game: Game):
        yield smithy

    def buy_priority(self, player: Player, game: Game):
        money = player.state.money
        if money >= 8:
            yield province
        if money >= 6:
            yield gold
        if money == 4:
            yield smithy
        if money >= 3:
            yield silver


class BigMoneySmithy(Bot):
    def __init__(
        self,
        player_id: str = "big_money_smithy",
    ):
        super().__init__(decider=BigMoneySmithyDecider(), player_id=player_id)

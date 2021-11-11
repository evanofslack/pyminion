import logging

from pyminion.expansions.base import gold, province, silver
from pyminion.game import Game
from pyminion.models.core import Deck
from pyminion.players import Bot

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

    def start_action_phase(self, game: Game):
        viable_actions = [card for card in self.hand.cards if "Action" in card.type]
        logger.info(f"{self.player_id}'s hand: {self.hand}")
        while viable_actions and self.state.actions:

            # Add logic for playing action cards here

            return

    def start_buy_phase(self, game: Game):
        while self.state.buys and self.state.money:
            if self.state.money >= 8:
                buy_card = province
            elif self.state.money >= 6:
                buy_card = gold
            elif self.state.money >= 3:
                buy_card = silver
            else:
                return
            self.buy(buy_card, supply=game.supply)
            logger.info(f"{self.player_id} buys {buy_card}")

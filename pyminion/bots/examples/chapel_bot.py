import logging
from typing import Iterator

from pyminion.bots.optimized_bot import OptimizedBot
from pyminion.core import Card
from pyminion.expansions.base import chapel, duchy, estate, gold, province, silver
from pyminion.game import Game

logger = logging.getLogger()


class ChapelBot(OptimizedBot):
    """
    Attempt the following buys in order:

    Buy Chapel if #Chapel < 1
    Buy Province if total money in deck is > 15
    Buy Duchy if remaining Provinces < 5
    Buy Estate if remaining Provinces < 3
    Buy Gold
    Buy Duchy if remaining Provinces < 7
    Buy Silver

    """

    def __init__(
        self,
        player_id: str = "chapel_bot",
    ):
        super().__init__(player_id=player_id)

    def action_priority(self, game: Game) -> Iterator[Card]:
        yield chapel

    def buy_priority(self, game: Game) -> Iterator[Card]:

        money = self.state.money
        deck_money = self.get_deck_money()
        num_province = game.supply.pile_length(pile_name="Province")
        num_chapel = self.get_card_count(card=chapel)

        if num_chapel < 1 and money >= 2:
            yield chapel
        if deck_money > 15 and money >= 8:
            yield province
        if num_province < 5 and money >= 5:
            yield duchy
        if num_province < 3 and money >= 2:
            yield estate
        if money >= 6:
            yield gold
        if num_province < 7 and money >= 5:
            yield duchy
        if money >= 3:
            yield silver

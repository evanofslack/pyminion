import logging
from typing import Iterator

from pyminion.bots.bot import Bot
from pyminion.core import Card
from pyminion.expansions.base import duchy, estate, gold, province, silver, smithy
from pyminion.game import Game

logger = logging.getLogger()


class BigMoneyUltimate(Bot):
    """
    Attempt the following buys in order:

    Buy Province if total money in deck is > 15
    Buy Duchy if remaining Provinces < 5
    Buy Estate if remaining Provinces < 3
    Buy Gold
    Buy Duchy if remaining Provinces < 7
    Buy Smithy if #Smithies < (#Treasures / 11)
    Buy Silver

    """

    def __init__(
        self,
        player_id: str = "big_money_ultimate",
    ):
        super().__init__(player_id=player_id)

    def action_priority(self, game: Game) -> Iterator[Card]:
        yield smithy

    def buy_priority(self, game: Game) -> Iterator[Card]:

        money = self.state.money
        deck_money = self.get_deck_money()
        num_province = game.supply.pile_length(pile_name="Province")
        num_smithy = self.get_card_count(card=smithy)
        num_treasure = len(
            [card for card in self.get_all_cards() if "Treasure" in card.type]
        )

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
        if num_smithy < num_treasure / 11 and money >= 4:
            yield smithy
        if money >= 3:
            yield silver

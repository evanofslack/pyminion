import logging
from typing import List

from pyminion.bots import Bot
from pyminion.exceptions import EmptyPile
from pyminion.expansions.base import duchy, estate, gold, province, silver, smithy
from pyminion.game import Game
from pyminion.models.core import Card, Deck

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
        deck: Deck = None,
        player_id: str = "big_money",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def start_action_phase(self, game: Game):
        viable_actions: List[Card] = [
            card for card in self.hand.cards if "Action" in card.type
        ]
        logger.info(f"{self.player_id}'s hand: {self.hand}")

        while viable_actions and self.state.actions:

            if viable_actions:
                print(viable_actions)

                self.play(target_card=smithy, game=game)

            return

    def start_buy_phase(self, game: Game):

        money = self.state.money
        num_province = game.supply.pile_length(pile_name="Province")
        num_smithy = self.get_card_count(card=smithy)
        num_treasure = len(
            [card for card in self.get_all_cards() if "Treasure" in card.type]
        )

        while self.state.buys and self.state.money:
            if self.get_deck_money() > 15 and num_province > 1 and money >= 8:
                try:
                    self.buy(card=province, supply=game.supply)
                    return
                except EmptyPile:
                    pass
            if num_province < 5 and money >= 5:
                try:
                    self.buy(card=duchy, supply=game.supply)
                    return
                except EmptyPile:
                    pass
            if num_province < 3 and money >= 2:
                try:
                    self.buy(card=estate, supply=game.supply)
                    return
                except EmptyPile:
                    pass
            if money >= 6:
                try:
                    self.buy(card=gold, supply=game.supply)
                    return
                except EmptyPile:
                    pass
            if num_province < 7 and money >= 5:
                try:
                    self.buy(card=duchy, supply=game.supply)
                    return
                except EmptyPile:
                    pass
            if num_smithy < num_treasure / 11 and money >= 4:
                try:
                    self.buy(card=smithy, supply=game.supply)
                    return
                except EmptyPile:
                    pass
            if money >= 3:
                try:
                    self.buy(card=silver, supply=game.supply)
                    return
                except EmptyPile:
                    pass
            else:
                logger.info(f"{self} buys nothing")
                return

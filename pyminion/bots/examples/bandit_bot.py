from typing import Iterator

from pyminion.bots.optimized_bot import OptimizedBot, OptimizedBotDecider
from pyminion.core import CardType, Card
from pyminion.expansions.base import (
    bandit,
    duchy,
    estate,
    gold,
    province,
    silver,
    smithy,
)
from pyminion.player import Player
from pyminion.game import Game


class BanditBotDecider(OptimizedBotDecider):
    """
    Attempt the following buys in order:

    Buy Province if total money in deck is > 15
    Buy Duchy if remaining Provinces < 5
    Buy Estate if remaining Provinces < 3
    Buy Gold
    Buy Duchy if remaining Provinces < 7
    Buy Bandit if #Bandits < 1
    Buy Smithy if #Smithies < (#Treasures / 11)
    Buy Silver

    """

    def action_priority(self, player: Player, game: Game) -> Iterator[Card]:
        yield bandit
        yield smithy

    def buy_priority(self, player: Player, game: Game) -> Iterator[Card]:

        money = player.state.money
        deck_money = player.get_deck_money()
        num_province = game.supply.pile_length(pile_name="Province")
        num_smithy = player.get_card_count(card=smithy)
        num_bandit = player.get_card_count(card=bandit)
        num_treasure = len(
            [card for card in player.get_all_cards() if CardType.Treasure in card.type]
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
        if num_bandit < 1 and money >= 5:
            yield bandit
        if num_smithy < num_treasure / 11 and money >= 4:
            yield smithy
        if money >= 3:
            yield silver


class BanditBot(OptimizedBot):
    def __init__(
        self,
        player_id: str = "bandit_bot",
    ):
        super().__init__(decider=BanditBotDecider(), player_id=player_id)

import logging
from typing import TYPE_CHECKING, List, Tuple

from pyminion.core import AbstractDeck, CardType, Action, Card, ScoreCard, Treasure, Victory
from pyminion.effects import AttackEffect, EffectAction, FuncPlayerCardGameEffect, FuncPlayerGameEffect, PlayerCardGameEffect
from pyminion.exceptions import EmptyPile
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class Bazaar(Action):
    """
    +1 Card
    +2 Actions
    +$1

    """

    def __init__(self):
        super().__init__(name="Bazaar", cost=5, type=(CardType.Action,), draw=1, actions=2, money=1)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw()
        player.state.actions += 2
        player.state.money += 1


bazaar = Bazaar()


seaside_set: List[Card] = [
    bazaar,
]

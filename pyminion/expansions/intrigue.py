import logging
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from pyminion.bots.bot import Bot
from pyminion.core import AbstractDeck, Action, Card, Treasure, Victory
from pyminion.players import Human, Player

if TYPE_CHECKING:
    from pyminion.game import Game

logger = logging.getLogger()

class Courtyard(Action):
    """
    +3 Cards

    Put a card from your hand onto your deck.
    """

    def __init__(
        self,
        name: str = "Courtyard",
        cost: int = 2,
        type: Tuple[str] = ("Action",),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")
        if generic_play:
            super().generic_play(player)

        player.draw(3)

        if isinstance(player, Human):
            topdeck_card = player.single_card_decision(
                prompt="Enter the card you would like to topdeck: ",
                valid_cards=player.hand.cards,
            )

        elif isinstance(player, Bot):
            topdeck_card = player.topdeck_resp(
                card=self,
                valid_cards=player.hand.cards,
                game=game,
                required=True,
            )

        player.hand.remove(topdeck_card)
        player.deck.add(topdeck_card)

courtyard = Courtyard()

intrigue_set = [
    courtyard,
]

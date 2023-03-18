import logging
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from pyminion.bots.bot import Bot
from pyminion.core import AbstractDeck, Action, Card, Treasure, Victory
from pyminion.exceptions import (EmptyPile, InvalidBotImplementation,
                                 InvalidMultiCardInput, InvalidSingleCardInput)
from pyminion.players import Human, Player

if TYPE_CHECKING:
    from pyminion.game import Game

logger = logging.getLogger()

class Courtyard(Action):
    """
    +3 Cards

    Put a card from your hand onto your deck.

    """

    def __init__(self):
        super().__init__(name="Courtyard", cost=2, type=("Action",))

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

class Lurker(Action):
    """
    +1 Action

    Choose one: Trash an Action card from the Supply, or gain an Action card from the trash.

    """

    def __init__(self):
        super().__init__(name="Lurker", cost=2, type=("Action",))

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")
        if generic_play:
            super().generic_play(player)

        player.state.actions += 1

        supply_action_cards = [
            c for c in game.supply.avaliable_cards() if "Action" in c.type
        ]
        trash_action_cards = [
            c for c in game.trash.cards if "Action" in c.type
        ]

        if len(supply_action_cards) > 0 or len(trash_action_cards) > 0:
            if len(supply_action_cards) == 0:
                option = 1
            elif len(trash_action_cards) == 0:
                option = 0
            else:
                if isinstance(player, Human):
                    option = player.multiple_option_decision([
                        "Trash an Action card from the Supply",
                        "Gain an Action card from the trash",
                    ])
                elif isinstance(player, Bot):
                    # TODO
                    option = 0

            if isinstance(player, Human):
                if option == 0:
                    # TODO: wrap in function
                    trash_card = player.single_card_decision(
                        "Choose a card from the Supply to trash",
                        supply_action_cards,
                    )
                    if trash_card is None or isinstance(trash_card, str):
                        raise InvalidSingleCardInput("You must trash a card")
                    game.supply.trash_card(trash_card, game.trash)
                else:
                    # TODO: wrap in function
                    gain_card = player.single_card_decision(
                        "Choose a card to gain from the trash",
                        trash_action_cards,
                    )
                    if gain_card is None or isinstance(gain_card, str):
                        raise InvalidSingleCardInput("You must gain a card")
                    game.trash.remove(gain_card)
                    player.discard_pile.add(gain_card)
            elif isinstance(player, Bot):
                if option == 0:
                    trash_card = player.trash_resp(
                        card=self,
                        valid_cards=supply_action_cards,
                        game=game,
                        required=True,
                    )
                    if not trash_card:
                        raise InvalidBotImplementation(
                            "Card was not trashed when playing Lurker"
                        )
                    game.supply.trash_card(trash_card, game.trash)
                else:
                    gain_card = player.gain_resp(
                        card=self,
                        valid_cards=trash_action_cards,
                        game=game,
                        required=True,
                    )
                    if not gain_card:
                        raise InvalidBotImplementation(
                            "Card was not gained when playing Lurker"
                        )
                    game.trash.remove(gain_card)
                    player.discard_pile.add(gain_card)

courtyard = Courtyard()
lurker = Lurker()

intrigue_set: List[Card] = [
    courtyard,
    lurker,
]

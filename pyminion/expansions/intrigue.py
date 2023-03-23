import logging
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from pyminion.bots.bot import Bot
from pyminion.core import AbstractDeck, Action, Card, CardType, Treasure, Victory
from pyminion.decisions import validate_input
from pyminion.exceptions import (EmptyPile, InvalidBotImplementation,
                                 InvalidMultiCardInput, InvalidSingleCardInput)
from pyminion.players import Human, Player
from pyminion.expansions.base import duchy, estate

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class Baron(Action):
    """
    +1 Buy

    You may discard an Estate for +4 money. If you don't, gain an Estate.

    """

    def __init__(self):
        super().__init__(name="Baron", cost=4, type=(CardType.Action,))

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")
        if generic_play:
            super().generic_play(player)

        player.state.buys += 1

        discard_estate = False
        if estate in player.hand.cards:
            options = [
                "Discard estate for +4 money",
                "Gain an estate",
            ]
            if isinstance(player, Human):
                response = player.multiple_option_decision(options)
            elif isinstance(player, Bot):
                response = player.multiple_option_decision(self, options, game)

            discard_estate = response == 0

        if discard_estate:
            player.discard(estate)
            player.state.money += 4
        elif game.supply.pile_length(estate.name) > 0:
            player.gain(estate, game.supply)


class Courtyard(Action):
    """
    +3 Cards

    Put a card from your hand onto your deck.

    """

    def __init__(self):
        super().__init__(name="Courtyard", cost=2, type=(CardType.Action,))

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


class Duke(Victory):
    """
    Worth 1VP per Duchy you have.

    """

    def __init__(self):
        super().__init__("Duke", 5, (CardType.Victory,))

    def score(self, player: Player) -> int:
        vp = 0
        for card in player.get_all_cards():
            if card.name == duchy.name:
                vp += 1
        return vp


class Lurker(Action):
    """
    +1 Action

    Choose one: Trash an Action card from the Supply, or gain an Action card from the trash.

    """

    def __init__(self):
        super().__init__(name="Lurker", cost=2, type=(CardType.Action,), actions=1)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")
        if generic_play:
            super().generic_play(player)

        player.state.actions += 1

        supply_action_cards = [
            c for c in game.supply.avaliable_cards() if CardType.Action in c.type
        ]
        trash_action_cards = [
            c for c in game.trash.cards if CardType.Action in c.type
        ]

        if len(supply_action_cards) > 0 or len(trash_action_cards) > 0:
            if len(supply_action_cards) == 0:
                option = 1
            elif len(trash_action_cards) == 0:
                option = 0
            else:
                options = [
                    "Trash an Action card from the Supply",
                    "Gain an Action card from the trash",
                ]
                if isinstance(player, Human):
                    option = player.multiple_option_decision(options)
                elif isinstance(player, Bot):
                    option = player.multiple_option_decision(
                        self,
                        options,
                        game,
                    )

            @validate_input(exceptions=InvalidSingleCardInput)
            def get_trash_card() -> Card:
                trash_card = player.single_card_decision(
                    "Choose a card from the Supply to trash",
                    supply_action_cards,
                )

                if trash_card is None or isinstance(trash_card, str):
                    raise InvalidSingleCardInput("You must trash a card")

                return trash_card

            @validate_input(exceptions=InvalidSingleCardInput)
            def get_gain_card() -> Card:
                gain_card = player.single_card_decision(
                    "Choose a card to gain from the trash",
                    trash_action_cards,
                )

                if gain_card is None or isinstance(gain_card, str):
                    raise InvalidSingleCardInput("You must gain a card")

                return gain_card

            if isinstance(player, Human):
                if option == 0:
                    trash_card = get_trash_card()
                else:
                    gain_card = get_gain_card()
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

            if option == 0:
                game.supply.trash_card(trash_card, game.trash)
            else:
                game.trash.remove(gain_card)
                player.discard_pile.add(gain_card)


class Nobles(Action, Victory):
    """
    Choose one: +3 Cards; or +2 Actions.

    """

    def __init__(self):
        Action.__init__(self, "Nobles", 6, (CardType.Action, CardType.Victory))

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        options = [
            "+3 Cards",
            "+2 Actions",
        ]
        if isinstance(player, Human):
            option = player.multiple_option_decision(options)
        elif isinstance(player, Bot):
            option = player.multiple_option_decision(
                self,
                options,
                game,
            )

        if option == 0:
            player.draw(3)
        else:
            player.state.actions += 2

    def score(self, player: Player) -> int:
        vp = 2
        return vp


class ShantyTown(Action):
    """
    +2 Actions

    Reveal your hand.
    If you have no Action cards in hand, +2 Cards.

    """

    def __init__(self):
        super().__init__(name="Shanty Town", cost=3, type=(CardType.Action,), actions=2)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 2

        if not any(CardType.Action in c.type for c in player.hand.cards):
            player.draw(2)


class Steward(Action):
    """
    Choose one: +2 Cards; or +2 money; or trash 2 cards from your hand.

    """

    def __init__(self):
        super().__init__(name="Steward", cost=3, type=(CardType.Action,))

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        options = [
            "+2 Cards",
            "+2 Money",
            "Trash 2 cards from your hand",
        ]
        if isinstance(player, Human):
            option = player.multiple_option_decision(options)
        elif isinstance(player, Bot):
            option = player.multiple_option_decision(self, options, game)

        if option == 0:
            player.draw(2)
        elif option == 1:
            player.state.money += 2
        else:
            trash_cards = self._get_trash_cards(player, game)
            for card in trash_cards:
                player.trash(card, game.trash)

    def _get_trash_cards(self, player: Union[Human, Bot], game: "Game") -> List[Card]:

        if len(player.hand) <= 2:
            return player.hand.cards[:]

        @validate_input(exceptions=InvalidMultiCardInput)
        def get_trash_cards() -> List[Card]:
            trash_cards = player.multiple_card_decision(
                prompt="Enter 2 cards you would like to trash from your hand: ",
                valid_cards=player.hand.cards,
            )
            if trash_cards is None or len(trash_cards) != 2:
                raise InvalidMultiCardInput(
                    "You must trash 2 cards with steward"
                )
            return trash_cards

        trash_cards: List[Card] = []
        if isinstance(player, Human):
            trash_cards = get_trash_cards()

        elif isinstance(player, Bot):
            resp = player.multiple_trash_resp(
                card=self,
                valid_cards=player.hand.cards,
                game=game,
                required=True,
            )
            if resp is None or len(resp) != 2:
                raise InvalidMultiCardInput(
                    "You must trash 2 cards with steward"
                )
            trash_cards = resp

        return trash_cards

baron = Baron()
courtyard = Courtyard()
duke = Duke()
lurker = Lurker()
nobles = Nobles()
shanty_town = ShantyTown()
steward = Steward()


intrigue_set: List[Card] = [
    baron,
    courtyard,
    duke,
    lurker,
    nobles,
    shanty_town,
    steward,
]

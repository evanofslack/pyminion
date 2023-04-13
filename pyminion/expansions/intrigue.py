from enum import IntEnum, unique
import logging
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from pyminion.bots.bot import Bot
from pyminion.core import AbstractDeck, Action, Card, CardType, Treasure, Victory
from pyminion.decisions import validate_input
from pyminion.exceptions import (EmptyPile, InvalidBotImplementation,
                                 InvalidMultiCardInput, InvalidSingleCardInput)
from pyminion.players import Human, Player
from pyminion.expansions.base import duchy, estate, gold

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class Baron(Action):
    """
    +1 Buy

    You may discard an Estate for +4 money. If you don't, gain an Estate.

    """

    @unique
    class Choice(IntEnum):
        DiscardEstate = 0
        GainEstate = 1

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
                response = player.multiple_option_decision(options)[0]
            elif isinstance(player, Bot):
                response = player.multiple_option_decision(self, options, game)[0]

            discard_estate = (response == Baron.Choice.DiscardEstate)

        if discard_estate:
            player.discard(estate)
            player.state.money += 4
        elif game.supply.pile_length(estate.name) > 0:
            player.gain(estate, game.supply)


class Conspirator(Action):
    """
    +2 Money

    If you've played 3 or more Actions this turn (counting this), +1 Card and +1 Action.

    """

    def __init__(self):
        super().__init__(name="Conspirator", cost=4, type=(CardType.Action,), money=2)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")
        if generic_play:
            super().generic_play(player)

        player.state.money += 2

        if player.actions_played_this_turn >= 3:
            player.draw(1)
            player.state.actions += 1


class Courtier(Action):
    """
    Reveal a card from your hand. For each type it has (Action, Attack, etc.),
    choose one: +1 Action; or +1 Buy; or +3 Money; or gain a Gold. The choices
    must be different.

    """

    @unique
    class Choice(IntEnum):
        Action = 0
        Buy = 1
        Money = 2
        GainGold = 3

    def __init__(self):
        super().__init__(name="Courtier", cost=5, type=(CardType.Action,))

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")
        if generic_play:
            super().generic_play(player)

        hand_len = len(player.hand)

        if hand_len == 0:
            return

        @validate_input(exceptions=InvalidSingleCardInput)
        def get_reveal_card() -> Card:

            reveal_card = player.single_card_decision(
                prompt="Reveal a card from your hand: ",
                valid_cards=player.hand.cards,
            )

            if reveal_card is None or isinstance(reveal_card, str):
                raise InvalidSingleCardInput("Invalid card to reveal")

            return reveal_card

        if hand_len == 1:
            reveal_card = player.hand.cards[0]
        elif isinstance(player, Human):
            reveal_card = get_reveal_card()
        elif isinstance(player, Bot):
            reveal_card = player.reveal_resp(
                card=self,
                valid_cards=player.hand.cards,
                game=game,
            )
            if reveal_card is None:
                raise InvalidBotImplementation(
                    "Card must be revealed when playing courtier"
                )

        logger.info(f"{player} reveals {reveal_card}")

        num_choices = min(len(reveal_card.type), 4)

        if num_choices == 4:
            choices = [c.value for c in Courtier.Choice]
        else:
            options = [
                "+1 Action",
                "+1 Buy",
                "+3 Money",
                "Gain a Gold",
            ]
            if isinstance(player, Human):
                choices = player.multiple_option_decision(
                    options,
                    num_choices=num_choices,
                    unique=True,
                )
            elif isinstance(player, Bot):
                choices = player.multiple_option_decision(
                    self,
                    options,
                    game,
                    num_choices=num_choices,
                    unique=True,
                )

        for choice in choices:
            if choice == Courtier.Choice.Action:
                player.state.actions += 1
            elif choice == Courtier.Choice.Buy:
                player.state.buys += 1
            elif choice == Courtier.Choice.Money:
                player.state.money += 3
            elif choice == Courtier.Choice.GainGold:
                player.gain(gold, game.supply)
            else:
                raise ValueError(f"Unknown courtier choice '{choice}'")


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


class Harem(Treasure, Victory):
    def __init__(self):
        Treasure.__init__(
            self,
            name="Harem",
            cost=6,
            type=(CardType.Treasure, CardType.Victory),
            money=2,
        )

    def play(self, player: Player, game: "Game") -> None:
        player.playmat.add(self)
        player.hand.remove(self)
        player.state.money += self.money

    def score(self, player: Player) -> int:
        vp = 2
        return vp


class Lurker(Action):
    """
    +1 Action

    Choose one: Trash an Action card from the Supply, or gain an Action card from the trash.

    """

    @unique
    class Choice(IntEnum):
        TrashAction = 0
        GainAction = 1

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
                choice = Lurker.Choice.GainAction
            elif len(trash_action_cards) == 0:
                choice = Lurker.Choice.TrashAction
            else:
                options = [
                    "Trash an Action card from the Supply",
                    "Gain an Action card from the trash",
                ]
                if isinstance(player, Human):
                    choice = player.multiple_option_decision(options)[0]
                elif isinstance(player, Bot):
                    choice = player.multiple_option_decision(
                        self,
                        options,
                        game,
                    )[0]

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
                if choice == Lurker.Choice.TrashAction:
                    trash_card = get_trash_card()
                elif choice == Lurker.Choice.GainAction:
                    gain_card = get_gain_card()
                else:
                    raise ValueError(f"Unknown lurker choice '{choice}'")
            elif isinstance(player, Bot):
                if choice == Lurker.Choice.TrashAction:
                    trash_card = player.trash_resp(
                        card=self,
                        valid_cards=supply_action_cards,
                        game=game,
                        required=True,
                    )
                    if not trash_card:
                        raise InvalidBotImplementation(
                            "Card was not trashed when playing lurker"
                        )
                elif choice == Lurker.Choice.GainAction:
                    gain_card = player.gain_resp(
                        card=self,
                        valid_cards=trash_action_cards,
                        game=game,
                        required=True,
                    )
                    if not gain_card:
                        raise InvalidBotImplementation(
                            "Card was not gained when playing lurker"
                        )
                else:
                    raise ValueError(f"Unknown lurker choice '{choice}'")

            if choice == Lurker.Choice.TrashAction:
                game.supply.trash_card(trash_card, game.trash)
            elif choice == Lurker.Choice.GainAction:
                game.trash.remove(gain_card)
                player.discard_pile.add(gain_card)
            else:
                raise ValueError(f"Unknown lurker choice '{choice}'")


class Masquerade(Action):
    """
    +2 Cards

    Each player with any cards in hand passes one to the next such player to
    their left, at once. Then you may trash a card from your hand.

    """

    def __init__(self):
        super().__init__(name="Masquerade", cost=3, type=(CardType.Action,), draw=2)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(2)

        @validate_input(exceptions=InvalidSingleCardInput)
        def get_pass_card(p: Human) -> Card:
            pass_card = p.single_card_decision(
                "Pick a card to pass to the player on your left: ",
                p.hand.cards,
            )

            if pass_card is None or isinstance(pass_card, str):
                raise InvalidSingleCardInput("Invalid card to pass")

            return pass_card

        @validate_input(exceptions=InvalidSingleCardInput)
        def get_trash_card() -> Card:
            trash_card = player.single_card_decision(
                "Choose a card from your hand to trash",
                player.hand.cards,
            )

            if trash_card is None or isinstance(trash_card, str):
                raise InvalidSingleCardInput("You must trash a card")

            return trash_card

        # get players who have at least 1 card in their hand
        valid_players = [p for p in game.players if len(p.hand) > 0]

        # prompt each player to choose a card to pass
        passed_cards: List[Card] = []
        for p in valid_players:
            if isinstance(p, Human):
                pass_card = get_pass_card(p)
            elif isinstance(p, Bot):
                pass_card = p.pass_resp(
                    card=self,
                    valid_cards=p.hand.cards,
                    game=game,
                )
                if pass_card is None:
                    raise InvalidBotImplementation(
                        "Card must be passed in response to masquerade"
                    )

            passed_cards.append(pass_card)

        # pass the cards
        for idx, p in enumerate(valid_players):
            c = passed_cards[idx]
            p.hand.remove(c)
            next_idx = (idx + 1) % len(valid_players)
            next_player = valid_players[next_idx]
            next_player.hand.add(c)
            logger.info(f"{p} passes {c} to {next_player}")

        if isinstance(player, Human):
            trash = player.binary_decision(
                prompt="Would you like to trash a card from your hand?"
            )
        elif isinstance(player, Bot):
            trash = player.binary_resp(game=game, card=self)

        if trash:
            if isinstance(player, Human):
                trash_card = get_trash_card()
            elif isinstance(player, Bot):
                trash_card = player.trash_resp(
                    card=self,
                    valid_cards=player.hand.cards,
                    game=game,
                )
                if trash_card is None:
                    raise InvalidBotImplementation("Card must be trashed")

            player.trash(trash_card, game.trash)


class Nobles(Action, Victory):
    """
    Choose one: +3 Cards; or +2 Actions.

    """

    @unique
    class Choice(IntEnum):
        Cards = 0
        Actions = 1

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
            choice = player.multiple_option_decision(options)[0]
        elif isinstance(player, Bot):
            choice = player.multiple_option_decision(
                self,
                options,
                game,
            )[0]

        if choice == Nobles.Choice.Cards:
            player.draw(3)
        elif choice == Nobles.Choice.Actions:
            player.state.actions += 2
        else:
            raise ValueError(f"Unknown nobles choice '{choice}'")

    def score(self, player: Player) -> int:
        vp = 2
        return vp


class Pawn(Action):
    """
    Choose two: +1 Card; +1 Action; +1 Buy; +1 Money.
    The choices must be different.

    """

    @unique
    class Choice(IntEnum):
        Card = 0
        Action = 1
        Buy = 2
        Money = 3

    def __init__(self):
        super().__init__(name="Pawn", cost=2, type=(CardType.Action,))

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        options = [
            "+1 Card",
            "+1 Action",
            "+1 Buy",
            "+1 Money",
        ]
        if isinstance(player, Human):
            choices = player.multiple_option_decision(
                options,
                num_choices=2,
                unique=True,
            )
        elif isinstance(player, Bot):
            choices = player.multiple_option_decision(
                self,
                options,
                game,
                num_choices=2,
                unique=True,
            )

        for choice in choices:
            if choice == Pawn.Choice.Card:
                player.draw(1)
            elif choice == Pawn.Choice.Action:
                player.state.actions += 1
            elif choice == Pawn.Choice.Buy:
                player.state.buys += 1
            elif choice == Pawn.Choice.Money:
                player.state.money += 1
            else:
                raise ValueError(f"Unknown pawn choice '{choice}'")


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

    @unique
    class Choice(IntEnum):
        Cards = 0
        Money = 1
        Trash = 2

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
            choice = player.multiple_option_decision(options)[0]
        elif isinstance(player, Bot):
            choice = player.multiple_option_decision(self, options, game)[0]

        if choice == Steward.Choice.Cards:
            player.draw(2)
        elif choice == Steward.Choice.Money:
            player.state.money += 2
        elif choice == Steward.Choice.Trash:
            trash_cards = self._get_trash_cards(player, game)
            for card in trash_cards:
                player.trash(card, game.trash)
        else:
            raise ValueError(f"Unknown steward choice '{choice}'")

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
conspirator = Conspirator()
courtier = Courtier()
courtyard = Courtyard()
duke = Duke()
harem = Harem()
lurker = Lurker()
masquerade = Masquerade()
nobles = Nobles()
pawn = Pawn()
shanty_town = ShantyTown()
steward = Steward()


intrigue_set: List[Card] = [
    baron,
    conspirator,
    courtier,
    courtyard,
    duke,
    harem,
    lurker,
    masquerade,
    nobles,
    pawn,
    shanty_town,
    steward,
]

import logging
import math
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from pyminion.bots.bot import Bot
from pyminion.core import AbstractDeck, Action, Card, Treasure, Victory
from pyminion.decisions import validate_input
from pyminion.exceptions import (EmptyPile, InvalidBotImplementation,
                                 InvalidMultiCardInput, InvalidSingleCardInput)
from pyminion.players import Human, Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class Copper(Treasure):
    def __init__(
        self,
        name: str = "Copper",
        cost: int = 0,
        type: Tuple[str] = ("Treasure",),
        money: int = 1,
    ):
        super().__init__(name, cost, type, money)

    def play(self, player: Player, game: "Game"):
        player.playmat.add(self)
        player.hand.remove(self)
        player.state.money += self.money


class Silver(Treasure):
    def __init__(
        self,
        name: str = "Silver",
        cost: int = 3,
        type: Tuple[str] = ("Treasure",),
        money: int = 2,
    ):
        super().__init__(name, cost, type, money)

    def play(self, player: Player, game: "Game"):

        # check if this is the first silver played and if there are any merchants in play
        if self not in player.playmat.cards:
            if num_merchants := len(
                [card for card in player.playmat.cards if card.name == "Merchant"]
            ):
                player.state.money += num_merchants

        player.playmat.add(self)
        player.hand.remove(self)
        player.state.money += self.money


class Gold(Treasure):
    def __init__(
        self,
        name: str = "Gold",
        cost: int = 6,
        type: Tuple[str] = ("Treasure",),
        money: int = 3,
    ):
        super().__init__(name, cost, type, money)

    def play(self, player: Player, game: "Game"):
        player.playmat.add(self)
        player.hand.remove(self)
        player.state.money += self.money


class Estate(Victory):
    def __init__(
        self,
        name: str = "Estate",
        cost: int = 2,
        type: Tuple[str] = ("Victory",),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        vp = 1
        return vp


class Duchy(Victory):
    def __init__(
        self,
        name: str = "Duchy",
        cost: int = 5,
        type: Tuple[str] = ("Victory",),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        vp = 3
        return vp


class Province(Victory):
    def __init__(
        self,
        name: str = "Province",
        cost: int = 8,
        type: Tuple[str] = ("Victory",),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        vp = 6
        return vp


class Curse(Victory):
    def __init__(
        self,
        name: str = "Curse",
        cost: int = 0,
        type: Tuple[str] = ("Curse",),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        vp = -1
        return vp


class Gardens(Victory):
    """
    Worth 1VP for every 10 cards you have (round down)

    """

    def __init__(
        self,
        name: str = "Gardens",
        cost: int = 4,
        type: Tuple[str] = ("Victory",),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        total_count = len(player.get_all_cards())
        vp = math.floor(total_count / 10)
        return vp


class Smithy(Action):
    """
    + 3 cards

    """

    def __init__(
        self,
        name: str = "Smithy",
        cost: int = 4,
        type: Tuple[str] = ("Action",),
        draw: int = 3,
    ):
        super().__init__(name, cost, type, draw=draw)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(3)


class Village(Action):
    """
    + 1 card, + 2 actions

    """

    def __init__(
        self,
        name: str = "Village",
        cost: int = 3,
        type: Tuple[str] = ("Action",),
        actions: int = 2,
        draw: int = 1,
    ):
        super().__init__(name, cost, type, actions=actions, draw=draw)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 2
        player.draw()


class Laboratory(Action):
    """
    +2 cards, +1 action

    """

    def __init__(
        self,
        name: str = "Laboratory",
        cost: int = 5,
        type: Tuple[str] = ("Action",),
        actions: int = 1,
        draw: int = 2,
    ):
        super().__init__(name, cost, type, actions=actions, draw=draw)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.draw(2)


class Market(Action):
    """
    +1 card, +1 action, +1 money, +1 buy

    """

    def __init__(
        self,
        name: str = "Market",
        cost: int = 5,
        type: Tuple[str] = ("Action",),
        actions: int = 1,
        draw: int = 1,
        money: int = 1,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.draw()
        player.state.money += 1
        player.state.buys += 1


class Moneylender(Action):
    """
    You may trash a copper from your hand for + 3 money

    """

    def __init__(
        self,
        name: str = "Moneylender",
        cost: int = 4,
        type: Tuple[str] = ("Action",),
    ):
        super().__init__(name, cost, type)

    def play(
        self,
        player: Union[Human, Bot],
        game: "Game",
        generic_play: bool = True,
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        if copper not in player.hand.cards:
            return

        if isinstance(player, Human):
            response = player.binary_decision(
                prompt="Do you want to trash a copper from your hand for +3 money? y/n: ",
            )

        elif isinstance(player, Bot):
            response = player.binary_resp(game=game, card=self)

        if response:
            player.trash(target_card=copper, trash=game.trash)
            player.state.money += 3


class Cellar(Action):
    """
    +1 Action

    Discard any number of cards, then draw that many

    """

    def __init__(
        self,
        name: str = "Cellar",
        cost: int = 2,
        type: Tuple[str] = ("Action",),
        actions: int = 1,
    ):
        super().__init__(name, cost, type, actions=actions)

    def play(
        self,
        player: Union[Human, Bot],
        game: "Game",
        generic_play: bool = True,
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 1

        if not player.hand.cards:
            return

        if isinstance(player, Human):
            discard_cards = player.multiple_card_decision(
                prompt="Enter the cards you would like to discard seperated by commas: ",
                valid_cards=player.hand.cards,
            )

        elif isinstance(player, Bot):
            discard_cards = player.multiple_discard_resp(
                card=self,
                valid_cards=player.hand.cards,
                game=game,
                required=False,
            )

        if discard_cards:
            for card in discard_cards:
                player.discard(card)
            player.draw(len(discard_cards))


class Chapel(Action):
    """
    Trash up to 4 cards from your hand

    """

    def __init__(
        self,
        name: str = "Chapel",
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

        if not player.hand.cards:
            return

        @validate_input(exceptions=InvalidMultiCardInput)
        def get_trash_cards() -> Optional[List[Card]]:

            trash_cards = player.multiple_card_decision(
                prompt="Enter up to 4 cards you would like to trash from your hand: ",
                valid_cards=player.hand.cards,
            )

            if trash_cards and len(trash_cards) > 4:
                raise InvalidMultiCardInput(
                    "You cannot trash more than 4 cards with chapel"
                )

            return trash_cards

        if isinstance(player, Human):
            trash_cards = get_trash_cards()

        elif isinstance(player, Bot):
            trash_cards = player.multiple_trash_resp(
                card=self,
                valid_cards=player.hand.cards,
                game=game,
                required=False,
            )
            if trash_cards and len(trash_cards) > 4:
                raise InvalidMultiCardInput(
                    "Attempted to trash more than 4 cards with chapel"
                )
        if not trash_cards:
            return
        for card in trash_cards:
            player.trash(card, game.trash)


class Workshop(Action):
    """
    Gain a card costing up to 4 money

    """

    def __init__(
        self,
        name: str = "Workshop",
        cost: int = 3,
        type: Tuple[str] = ("Action",),
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        @validate_input(exceptions=InvalidSingleCardInput)
        def get_gain_card() -> Card:

            gain_card = player.single_card_decision(
                prompt="Gain a card costing up to 4 money: ",
                valid_cards=game.supply.avaliable_cards(),
            )

            if not gain_card:
                raise InvalidSingleCardInput("You must gain a card")
            if gain_card.cost > 4:
                raise InvalidSingleCardInput("Card must cost less than 4 money")

            return gain_card

        if isinstance(player, Human):
            gain_card = get_gain_card()

        elif isinstance(player, Bot):
            gain_card = player.gain_resp(
                card=self,
                valid_cards=[
                    card for card in game.supply.avaliable_cards() if card.cost <= 4
                ],
                game=game,
                required=True,
            )
            if not gain_card:
                raise InvalidSingleCardInput("You must gain a card")
            if gain_card.cost > 4:
                raise InvalidSingleCardInput("Card must cost less than 4 money")

        player.gain(gain_card, game.supply)


class Festival(Action):
    """
    + 2 actions, + 1 buy, + 2 money

    """

    def __init__(
        self,
        name: str = "Festival",
        cost: int = 5,
        type: Tuple[str] = ("Action",),
        actions: int = 2,
        money: int = 2,
    ):
        super().__init__(name, cost, type, actions=actions, money=money)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 2
        player.state.money += 2
        player.state.buys += 1


class Harbinger(Action):
    """
    +1 card, +1 action

    Look through your discard pile. You may put a card from it onto your deck

    """

    def __init__(
        self,
        name: str = "Harbinger",
        cost: int = 3,
        type: Tuple[str] = ("Action",),
        actions: int = 1,
        draw: int = 1,
    ):
        super().__init__(name, cost, type, actions=actions, draw=draw)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.draw()

        if not player.discard_pile:
            return

        if isinstance(player, Human):
            topdeck_card = player.single_card_decision(
                prompt="You may select a card from your discard pile to put onto your deck: ",
                valid_cards=player.discard_pile.cards,
            )

        elif isinstance(player, Bot):
            topdeck_card = player.topdeck_resp(
                card=self,
                valid_cards=player.discard_pile.cards,
                game=game,
                required=False,
            )

        if not topdeck_card or isinstance(topdeck_card, str):
            return

        player.deck.add(player.discard_pile.remove(topdeck_card))


class Vassal(Action):
    """
    +2 money

    Discard the top card of your deck. If it's an action card you may play it.

    """

    def __init__(
        self,
        name: str = "Vassal",
        cost: int = 3,
        type: Tuple[str] = ("Action",),
        money: int = 2,
    ):
        super().__init__(name, cost, type, money=money)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.money += 2
        player.draw(destination=player.discard_pile, silent=True)

        if not player.discard_pile:
            return

        discard_card = player.discard_pile.cards[-1]

        logger.info(f"{player} discards {discard_card}")

        if "Action" not in discard_card.type:
            return

        if isinstance(player, Human):
            decision = player.binary_decision(
                prompt=f"You discarded {discard_card.name}, would you like to play it? (y/n):  "
            )
        elif isinstance(player, Bot):
            decision = player.binary_resp(game=game, card=self)

        if not decision:
            return

        played_card = player.discard_pile.cards.pop()
        player.playmat.add(played_card)
        player.exact_play(card=player.playmat.cards[-1], game=game, generic_play=False)
        return


class Artisan(Action):
    """
    Gain a card to your hand costing up to 5 money.

    Put a card from your hand onto your deck

    """

    def __init__(
        self,
        name: str = "Artisan",
        cost: int = 6,
        type: Tuple[str] = ("Action",),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        @validate_input(exceptions=InvalidSingleCardInput)
        def get_gain_card() -> Card:
            gain_card = player.single_card_decision(
                prompt="Gain a card costing up to 5 money: ",
                valid_cards=game.supply.avaliable_cards(),
            )
            if not gain_card or isinstance(gain_card, str):
                raise InvalidSingleCardInput("You must gain a card")
            if gain_card.cost > 4:
                raise InvalidSingleCardInput("Card must cost at most 5 money")
            return gain_card

        @validate_input(exceptions=InvalidSingleCardInput)
        def get_topdeck_card() -> Card:
            topdeck_card = player.single_card_decision(
                prompt="Put a card from your hand onto your deck: ",
                valid_cards=player.hand.cards,
            )
            if not topdeck_card or isinstance(topdeck_card, str):
                raise InvalidSingleCardInput("You must topdeck a card")
            return topdeck_card

        if isinstance(player, Human):
            gain_card = get_gain_card()
            player.gain(card=gain_card, supply=game.supply, destination=player.hand)
            topdeck_card = get_topdeck_card()

        elif isinstance(player, Bot):
            gain_card = player.gain_resp(
                card=self,
                valid_cards=[
                    card for card in game.supply.avaliable_cards() if card.cost <= 5
                ],
                game=game,
                required=True,
            )

            if not gain_card:
                raise InvalidSingleCardInput("Must gain a card with Artisan")
            if gain_card.cost > 5:
                raise InvalidSingleCardInput("Card must cost at most 5 money")

            player.gain(card=gain_card, supply=game.supply, destination=player.hand)

            topdeck_card = player.topdeck_resp(
                card=self,
                valid_cards=player.hand.cards,
                game=game,
                required=True,
            )

        for card in player.hand.cards:
            if card == topdeck_card:
                player.deck.add(player.hand.remove(card))
                return


class Poacher(Action):
    """
    +1 card, +1 action, + 1 money

    Discard a card per empty Supply pile

    """

    def __init__(
        self,
        name: str = "Poacher",
        cost: int = 4,
        type: Tuple[str] = ("Action",),
        actions: int = 1,
        draw: int = 1,
        money: int = 1,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw()
        player.state.actions += 1
        player.state.money += 1

        empty_piles = game.supply.num_empty_piles()

        if empty_piles == 0:
            return

        discard_num = min(empty_piles, len(player.hand))

        if isinstance(player, Human):

            @validate_input(exceptions=InvalidMultiCardInput)
            def get_discard_cards() -> List[Card]:
                discard_cards = player.multiple_card_decision(
                    prompt=f"Discard {discard_num} card(s) from your hand: ",
                    valid_cards=player.hand.cards,
                )
                if not discard_cards or len(discard_cards) != discard_num:
                    raise InvalidMultiCardInput(
                        f"You must discard {discard_num} card(s)"
                    )

                return discard_cards

            discard_cards = get_discard_cards()

        elif isinstance(player, Bot):
            discard_cards = player.multiple_discard_resp(
                card=self,
                valid_cards=player.hand.cards,
                game=game,
                num_discard=discard_num,
                required=True,
            )
            if not discard_cards or len(discard_cards) != discard_num:
                raise InvalidMultiCardInput(f"You must discard {discard_num} card(s)")

        for discard_card in discard_cards:
            player.discard(discard_card)


class CouncilRoom(Action):
    """
    +4 cards, +1 buy

    Each other player draws a card

    """

    def __init__(
        self,
        name: str = "Council Room",
        cost: int = 5,
        type: Tuple[str] = ("Action",),
        draw: int = 4,
    ):
        super().__init__(name, cost, type, draw=draw)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(4)
        player.state.buys += 1

        for p in game.players:
            if p is not player:
                p.draw()


class Witch(Action):
    """
    +2 cards

    Each other player gains a curse

    """

    def __init__(
        self,
        name: str = "Witch",
        cost: int = 5,
        type: Tuple[str] = ("Action", "Attack"),
        draw: int = 2,
    ):
        super().__init__(name, cost, type, draw=draw)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(2)

        for opponent in game.players:
            if opponent is not player:
                if opponent.is_attacked(player=player, attack_card=self):

                    # attempt to gain a curse. if curse pile is empty, proceed
                    try:
                        opponent.gain(
                            card=curse,
                            supply=game.supply,
                        )
                    except EmptyPile:
                        pass


class Moat(Action):
    """
    +2 cards

    When another player plays an attack card, you may first
    reveal this from your hand, to be unaffected by it

    """

    def __init__(
        self,
        name: str = "Moat",
        cost: int = 2,
        type: Tuple[str] = ("Action", "Reaction"),
        draw: int = 2,
    ):
        super().__init__(name, cost, type, draw=draw)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(2)


class Merchant(Action):
    """
    +1 card, +1 action

    The first time you play a Silver this turn, +1 money

    """

    def __init__(
        self,
        name: str = "Merchant",
        cost: int = 3,
        type: Tuple[str] = ("Action",),
        actions: int = 1,
        draw: int = 1,
    ):
        super().__init__(name, cost, type, actions=actions, draw=draw)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(1)
        player.state.actions += 1


class Bandit(Action):
    """
    Gain a Gold. Each other player reveals the top 2 cards of their deck,
    trashes a revealed treasure other than Copper, and discards the rest

    """

    def __init__(
        self,
        name: str = "Bandit",
        cost: int = 5,
        type: Tuple[str] = ("Action", "Attack"),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        # attempt to gain a gold. if gold pile is empty, proceed
        try:
            player.gain(card=gold, supply=game.supply)
        except EmptyPile:
            pass

        for opponent in game.players:
            if opponent is not player:
                if opponent.is_attacked(player=player, attack_card=self):

                    revealed_cards = AbstractDeck()
                    opponent.draw(num_cards=2, destination=revealed_cards, silent=True)

                    logger.info(f"{opponent} reveals {revealed_cards}")

                    trash_card = None
                    for card in revealed_cards.cards:
                        if card.name == "Silver":
                            trash_card = card
                        elif card.name == "Gold" and not trash_card:
                            trash_card = card
                        elif (
                            "Treasure" in card.type
                            and card.name != "Copper"
                            and not trash_card
                        ):
                            trash_card = card

                    if trash_card:
                        game.trash.add(revealed_cards.remove(trash_card))

                    revealed_cards.move_to(opponent.discard_pile)
                    del revealed_cards


class Bureaucrat(Action):
    """
    Gain a Silver onto your deck. Each other player reveals a victory card from
    their hand and puts it onto their deck (or reveals a hand with no victory cards)

    """

    def __init__(
        self,
        name: str = "Bureaucrat",
        cost: int = 4,
        type: Tuple[str] = ("Action", "Attack"),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        # attempt to gain a silver. if silver pile is empty, proceed
        try:
            player.gain(card=silver, supply=game.supply, destination=player.deck)
        except EmptyPile:
            pass

        for opponent in game.players:
            if opponent is not player and opponent.is_attacked(
                player=player, attack_card=self
            ):

                victory_cards = []
                for card in opponent.hand.cards:
                    if "Victory" in card.type:
                        victory_cards.append(card)

                if not victory_cards:
                    # Log opponent revealed hand
                    return

                @validate_input(exceptions=InvalidSingleCardInput)
                def get_topdeck_card(opponent: Human) -> Card:
                    topdeck_card = opponent.single_card_decision(
                        prompt="You must topdeck a Victory card from your hand: ",
                        valid_cards=victory_cards,
                    )
                    if not topdeck_card or isinstance(topdeck_card, str):
                        raise InvalidSingleCardInput("You must topdeck a Victory card")

                    return topdeck_card

                if isinstance(opponent, Human):
                    topdeck_card = get_topdeck_card(opponent)

                elif isinstance(opponent, Bot):
                    topdeck_card = opponent.topdeck_resp(
                        card=self,
                        valid_cards=victory_cards,
                        game=game,
                        required=True,
                    )
                    if not topdeck_card:
                        raise InvalidSingleCardInput("You must topdeck a Victory card")

                opponent.deck.add(opponent.hand.remove(topdeck_card))


class ThroneRoom(Action):
    """
    You may play an Action card from your hand twice

    """

    def __init__(
        self,
        name: str = "Throne Room",
        cost: int = 4,
        type: Tuple[str] = ("Action",),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        action_cards = [card for card in player.hand.cards if "Action" in card.type]

        if not action_cards:
            return

        if isinstance(player, Human):
            dp_card = player.single_card_decision(
                prompt="You may play an action card from your hand twice: ",
                valid_cards=action_cards,
            )

        elif isinstance(player, Bot):
            dp_card = player.double_play_resp(
                card=self,
                valid_cards=action_cards,
                game=game,
                required=True,
            )

        if not dp_card or isinstance(dp_card, str):
            return

        for card in player.hand.cards:
            if card.name == dp_card.name:
                player.playmat.add(player.hand.remove(card))
                for i in range(2):
                    player.exact_play(card=card, game=game, generic_play=False)
                return


class Remodel(Action):
    """
    Trash a card from your hand. Gain a card costing up to $2 more than it

    """

    def __init__(
        self,
        name: str = "Remodel",
        cost: int = 4,
        type: Tuple[str] = ("Action",),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        if isinstance(player, Human):

            @validate_input(exceptions=InvalidSingleCardInput)
            def get_trash_card() -> Card:

                trash_card = player.single_card_decision(
                    prompt="Trash a card form your hand: ",
                    valid_cards=player.hand.cards,
                )

                if not trash_card or isinstance(trash_card, str):
                    raise InvalidSingleCardInput("You must trash a card")
                return trash_card

            @validate_input(exceptions=InvalidSingleCardInput)
            def get_gain_card(trash_card: Card) -> Card:

                gain_card = player.single_card_decision(
                    prompt=f"Gain a card costing up to {trash_card.cost + 2} money: ",
                    valid_cards=game.supply.avaliable_cards(),
                )

                if not gain_card or isinstance(gain_card, str):
                    raise InvalidSingleCardInput("You must gain a card")
                if gain_card.cost > trash_card.cost + 2:
                    raise InvalidSingleCardInput(
                        f"Card must cost less than {trash_card.cost + 2} money"
                    )
                return gain_card

            trash_card = get_trash_card()
            gain_card = get_gain_card(trash_card)

        elif isinstance(player, Bot):
            trash_card = player.trash_resp(
                card=self,
                valid_cards=player.hand.cards,
                game=game,
                required=True,
            )
            if not trash_card:
                raise InvalidBotImplementation(
                    "Card must be trashed when playing remodel"
                )
            gain_card = player.gain_resp(
                card=self,
                valid_cards=[
                    card
                    for card in game.supply.avaliable_cards()
                    if card.cost <= trash_card.cost + 2
                ],
                game=game,
                required=True,
            )
            if not gain_card:
                raise InvalidBotImplementation(
                    "Card must be gained when playing remodel"
                )

        player.trash(trash_card, trash=game.trash)
        player.gain(gain_card, game.supply)


class Mine(Action):
    """
    You may trash a Treasure from your hand. Gain a Treasure to your hand costing up to $3 more than it

    """

    def __init__(
        self,
        name: str = "Mine",
        cost: int = 5,
        type: Tuple[str] = ("Action",),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        treasures = [card for card in player.hand.cards if "Treasure" in card.type]

        if not treasures:
            return

        if isinstance(player, Human):

            @validate_input(exceptions=InvalidSingleCardInput)
            def get_trash_card() -> Optional[Card]:

                trash_card = player.single_card_decision(
                    prompt="You may trash a Treasure from your hand: ",
                    valid_cards=treasures,
                )
                if isinstance(trash_card, str):
                    raise InvalidSingleCardInput(f"You can not trash {trash_card}")

                return trash_card

            @validate_input(exceptions=InvalidSingleCardInput)
            def get_gain_card(trash_card: Card) -> Card:

                gain_card = player.single_card_decision(
                    prompt=f"Gain a Treasure card costing up to {trash_card.cost + 3} money to your hand: ",
                    valid_cards=game.supply.avaliable_cards(),
                )

                if not gain_card or isinstance(gain_card, str):
                    raise InvalidSingleCardInput("You must gain a card")
                if "Treasure" not in trash_card.type:
                    raise InvalidSingleCardInput("Card must be a Treasure")
                if gain_card.cost > trash_card.cost + 3:
                    raise InvalidSingleCardInput(
                        f"Card must cost less than {trash_card.cost + 3} money"
                    )
                return gain_card

            trash_card = get_trash_card()
            if not trash_card:
                return
            gain_card = get_gain_card(trash_card)

        elif isinstance(player, Bot):
            trash_card = player.trash_resp(
                card=self,
                valid_cards=treasures,
                game=game,
                required=False,
            )
            if not trash_card:
                return

            gain_card = player.gain_resp(
                card=self,
                valid_cards=[
                    card
                    for card in game.supply.avaliable_cards()
                    if "Treasure" in card.type and card.cost <= trash_card.cost + 3
                ],
                game=game,
                required=True,
            )
            if not gain_card:
                raise InvalidBotImplementation("Card must be gained when playing mine")

        player.trash(trash_card, trash=game.trash)
        player.gain(gain_card, game.supply, destination=player.hand)


class Militia(Action):
    """
    +2 Money

    Each other player discards down to 3 cards in hand

    """

    def __init__(
        self,
        name: str = "Militia",
        cost: int = 4,
        type: Tuple[str] = ("Action", "Attack"),
        money: int = 2,
    ):
        super().__init__(name, cost, type, money=money)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.money += 2

        for opponent in game.players:
            if opponent is not player and opponent.is_attacked(
                player=player, attack_card=self
            ):

                num_discard = len(opponent.hand) - 3
                if num_discard <= 0:
                    return

                @validate_input(exceptions=InvalidMultiCardInput)
                def get_discard_cards() -> List[Card]:
                    cards = opponent.multiple_card_decision(
                        prompt=f"You must discard {num_discard} cards from your hand: ",
                        valid_cards=opponent.hand.cards,
                    )
                    if len(cards) != num_discard:
                        raise InvalidMultiCardInput(
                            f"You must discard {num_discard} cards, you selected {len(cards)}"
                        )
                    return cards

                if isinstance(opponent, Human):
                    discard_cards = get_discard_cards()

                elif isinstance(opponent, Bot):
                    discard_cards = opponent.multiple_discard_resp(
                        card=self,
                        valid_cards=opponent.hand.cards,
                        game=game,
                        num_discard=num_discard,
                        required=True,
                    )
                    if not discard_cards:
                        return

                for card in discard_cards:
                    opponent.discard(target_card=card)


class Sentry(Action):
    """
    +1 card, +1 action

    Look at the top 2 cards of your deck. Trash and/or discard any number of them. Put the rest back on top in any order

    """

    def __init__(
        self,
        name: str = "Sentry",
        cost: int = 5,
        type: Tuple[str] = ("Action",),
        actions: int = 1,
        draw: int = 1,
    ):
        super().__init__(name, cost, type, actions=actions, draw=draw)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw()
        player.state.actions += 1

        revealed = AbstractDeck()
        player.draw(num_cards=2, destination=revealed, silent=True)
        logger.info(f"{player} looks at {revealed}")

        if isinstance(player, Human):

            def get_trash_cards() -> Optional[List[Card]]:
                trash_cards = player.multiple_card_decision(
                    prompt="Enter the cards you would like to trash: ",
                    valid_cards=revealed.cards,
                )
                return trash_cards

            def get_discard_cards(
                revealed: AbstractDeck,
            ) -> Optional[List[Card]]:
                if not revealed.cards:
                    return None

                discard_cards = player.multiple_card_decision(
                    prompt="Enter the cards you would like to discard: ",
                    valid_cards=revealed.cards,
                )
                return discard_cards

            trash_cards = get_trash_cards()
            if trash_cards:
                for card in trash_cards:
                    revealed.remove(card)
            discard_cards = get_discard_cards(revealed=revealed)
            if discard_cards:
                for card in discard_cards:
                    revealed.remove(card)
            reorder = False
            if len(revealed.cards) == 2:
                logger.info(
                    f"Current order: {revealed.cards[0]} (Top), {revealed.cards[1]} (Bottom)"
                )
                reorder = player.binary_decision(
                    prompt="Would you like to switch the order of the cards?"
                )

        elif isinstance(player, Bot):
            trash_cards = player.multiple_trash_resp(
                card=self,
                valid_cards=revealed.cards,
                game=game,
                required=False,
            )
            if trash_cards:
                for card in trash_cards:
                    revealed.remove(card)
            discard_cards = player.multiple_discard_resp(
                card=self,
                valid_cards=revealed.cards,
                game=game,
                required=False,
            )
            if discard_cards:
                for card in discard_cards:
                    revealed.remove(card)
            reorder = False
            if len(revealed.cards) == 2:
                reorder = player.binary_resp(game=game, card=self)

        if trash_cards:
            for card in trash_cards:
                game.trash.add(card)
                logger.info(f"{player} trashes {card}")
        if discard_cards:
            for card in discard_cards:
                player.discard_pile.add(card)
                logger.info(f"{player} discards {card}")
        if revealed.cards:
            if reorder:
                for card in revealed.cards:
                    player.deck.add(card)
            else:
                for card in reversed(revealed.cards):
                    player.deck.add(card)
            logger.info(f"{player} topdecks {len(revealed.cards)} cards")


class Library(Action):
    """
    Draw until you have 7 cards in hand, skipping any Action cards you choose to; set those aside, discarding them afterwards

    """

    def __init__(
        self,
        name: str = "Library",
        cost: int = 5,
        type: Tuple[str] = ("Action",),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Union[Human, Bot], game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        set_aside = AbstractDeck()
        while len(player.hand) < 7:

            if len(player.deck) == 0 and len(player.discard_pile) == 0:
                return

            player.draw(num_cards=1, destination=set_aside)
            drawn_card = set_aside.cards[-1]

            if "Action" in drawn_card.type:
                if isinstance(player, Human):
                    if player.binary_decision(
                        prompt=f"You drew {drawn_card}, would you like to skip it? y/n: "
                    ):
                        pass
                    else:
                        player.hand.add(set_aside.remove(drawn_card))

                    pass
                if isinstance(player, Bot):
                    if player.binary_resp(
                        game=game, card=self, relevant_cards=[drawn_card]
                    ):
                        pass
                    else:
                        player.hand.add(set_aside.remove(drawn_card))

            else:
                player.hand.add(set_aside.remove(drawn_card))

        if set_aside.cards:
            logger.info(f"{player} discards {set_aside}")
            set_aside.move_to(destination=player.discard_pile)


copper = Copper()
silver = Silver()
gold = Gold()
estate = Estate()
duchy = Duchy()
province = Province()
curse = Curse()

artisan = Artisan()
bandit = Bandit()
bureaucrat = Bureaucrat()
cellar = Cellar()
chapel = Chapel()
council_room = CouncilRoom()
festival = Festival()
gardens = Gardens()
harbinger = Harbinger()
laboratory = Laboratory()
library = Library()
market = Market()
merchant = Merchant()
militia = Militia()
mine = Mine()
moat = Moat()
moneylender = Moneylender()
poacher = Poacher()
remodel = Remodel()
sentry = Sentry()
smithy = Smithy()
throne_room = ThroneRoom()
vassal = Vassal()
village = Village()
witch = Witch()
workshop = Workshop()


base_set = [
    artisan,
    bandit,
    bureaucrat,
    cellar,
    chapel,
    council_room,
    festival,
    gardens,
    harbinger,
    laboratory,
    library,
    market,
    merchant,
    militia,
    mine,
    moat,
    moneylender,
    poacher,
    remodel,
    sentry,
    smithy,
    throne_room,
    vassal,
    village,
    witch,
    workshop,
]

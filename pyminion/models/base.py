import logging
import math
from typing import List, Optional, Tuple, Union

from pyminion.decisions import validate_input
from pyminion.exceptions import InvalidMultiCardInput, InvalidSingleCardInput
from pyminion.game import Game
from pyminion.models.cards import Action, Treasure, Victory
from pyminion.models.core import AbstractDeck, Card, Player
from pyminion.players import Bot, Human

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

    def play(self, player: Player, game: Game) -> int:
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

    def play(self, player: Player, game: Game) -> int:

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

    def play(self, player: Player, game: Game) -> int:
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
        VICTORY_POINTS = 1
        return VICTORY_POINTS


class Duchy(Victory):
    def __init__(
        self,
        name: str = "Duchy",
        cost: int = 5,
        type: Tuple[str] = ("Victory",),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        VICTORY_POINTS = 3
        return VICTORY_POINTS


class Province(Victory):
    def __init__(
        self,
        name: str = "Province",
        cost: int = 8,
        type: Tuple[str] = ("Victory",),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        VICTORY_POINTS = 6
        return VICTORY_POINTS


class Curse(Victory):
    def __init__(
        self,
        name: str = "Curse",
        cost: int = 0,
        type: Tuple[str] = ("Curse",),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        VICTORY_POINTS = -1
        return VICTORY_POINTS


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
        return math.floor(total_count / 10)


class Smithy(Action):
    """
    + 3 cards

    """

    def __init__(
        self,
        name: str = "Smithy",
        cost: int = 4,
        type: Tuple[str] = ("Action",),
        actions: int = 0,
        draw: int = 3,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self,
        player: Union[Human, Bot],
        game: Game,
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

        if isinstance(player, Bot):
            response = player.binary_decision(card=self)

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
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self,
        player: Union[Human, Bot],
        game: Game,
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

        if isinstance(player, Bot):
            discard_cards = player.multiple_card_decision(
                card=self, valid_cards=player.hand.cards
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
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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

            if len(trash_cards) > 4:
                raise InvalidMultiCardInput("You cannot trash more than 4 cards")

            return trash_cards

        if isinstance(player, Human):
            trash_cards = get_trash_cards()

        if isinstance(player, Bot):
            trash_cards = player.multiple_card_decision(
                card=self, valid_cards=player.hand.cards
            )
            if len(trash_cards) > 4:
                raise InvalidMultiCardInput("You cannot trash more than 4 cards")

        trash_cards = get_trash_cards()
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
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:

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

        if isinstance(player, Bot):
            gain_card = player.single_card_decision(
                card=self, valid_cards=game.supply.avaliable_cards()
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
        draw: int = 0,
        money: int = 2,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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

        if isinstance(player, Bot):
            topdeck_card = player.single_card_decision(
                card=self, valid_cards=player.discard_pile.cards
            )

        if not topdeck_card:
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
        actions: int = 0,
        draw: int = 0,
        money: int = 2,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.money += 2
        player.draw(destination=player.discard_pile)

        if not player.discard_pile:
            return

        discard_card = player.discard_pile.cards[-1]

        if "Action" not in discard_card.type:
            return

        if isinstance(player, Human):
            decision = player.binary_decision(
                prompt=f"You discarded {discard_card.name}, would you like to play it? (y/n):  "
            )
        if isinstance(player, Bot):
            decision = player.binary_decision(card=self)

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
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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
            if not gain_card:
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
            if not topdeck_card:
                raise InvalidSingleCardInput("You must topdeck a card")
            return topdeck_card

        if isinstance(player, Human):
            gain_card = get_gain_card()

            player.gain(card=gain_card, supply=game.supply, destination=player.hand)

            topdeck_card = get_topdeck_card()

        if isinstance(player, Bot):
            gain_card = player.single_card_decision(
                card=self, valid_cards=game.supply.avaliable_cards()
            )
            if not gain_card:
                raise InvalidSingleCardInput("You must gain a card")
            if gain_card.cost > 4:
                raise InvalidSingleCardInput("Card must cost at most 5 money")

            player.gain(card=gain_card, supply=game.supply, destination=player.hand)

            topdeck_card = player.single_card_decision(
                card=self, valid_cards=player.hand.cards
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
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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

        @validate_input(exceptions=InvalidMultiCardInput)
        def get_discard_cards() -> List[Card]:
            discard_cards = player.multiple_card_decision(
                prompt=f"Discard {discard_num} card(s) from your hand: ",
                valid_cards=player.hand.cards,
            )
            if len(discard_cards) != discard_num:
                raise InvalidMultiCardInput(f"You must discard {discard_num} card(s)")

            return discard_cards

        if isinstance(player, Human):
            discard_cards = get_discard_cards()

        if isinstance(player, Bot):
            discard_cards = player.multi_card_decision(
                card=self, valid_cards=player.hand.cards
            )
            if len(discard_cards) != discard_num:
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
        actions: int = 0,
        draw: int = 4,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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
        actions: int = 0,
        draw: int = 2,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(2)

        for opponent in game.players:
            if opponent is not player:
                if opponent.is_attacked(player=player, attack_card=self):
                    opponent.gain(
                        card=curse,
                        supply=game.supply,
                    )


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
        actions: int = 0,
        draw: int = 2,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
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
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.gain(card=gold, supply=game.supply)

        for opponent in game.players:
            if opponent is not player:
                if opponent.is_attacked(player=player, attack_card=self):

                    revealed_cards = AbstractDeck()
                    opponent.draw(num_cards=2, destination=revealed_cards)

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
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.gain(card=silver, supply=game.supply, destination=player.deck)

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
                    if not topdeck_card:
                        raise InvalidSingleCardInput(f"You must topdeck a Victory card")

                    return topdeck_card

                if isinstance(opponent, Human):
                    topdeck_card = get_topdeck_card(opponent)

                if isinstance(opponent, Bot):
                    topdeck_card = opponent.single_card_decision(
                        card=self,
                        valid_cards=victory_cards,
                    )
                    if not topdeck_card:
                        raise InvalidSingleCardInput("You must topdeck a Victory card")

                opponent.deck.add(opponent.hand.remove(topdeck_card))


class ThroneRoom(Action):
    """
    +2 money

    Discard the top card of your deck. If it's an action card you may play it.

    """

    def __init__(
        self,
        name: str = "Throne Room",
        cost: int = 4,
        type: Tuple[str] = ("Action",),
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        action_cards: List[Card] = []
        for card in player.hand.cards:
            if "Action" in card.type:
                action_cards.append(card)

        if not action_cards:
            return

        if isinstance(player, Human):
            dp_card = player.single_card_decision(
                prompt="You may play an action card from your hand twice: ",
                valid_cards=action_cards,
            )

        if isinstance(player, Bot):
            dp_card = player.single_card_decision(
                card=self,
                valid_cards=action_cards,
            )

        if not dp_card:
            return

        for card in player.hand.cards:
            if card.name == dp_card.name:
                player.playmat.add(player.hand.remove(card))
                for i in range(2):
                    player.exact_play(card=card, game=game, generic_play=False)
                return


copper = Copper()
silver = Silver()
gold = Gold()

estate = Estate()
duchy = Duchy()
province = Province()
curse = Curse()
gardens = Gardens()

smithy = Smithy()
village = Village()
laboratory = Laboratory()
market = Market()
moneylender = Moneylender()
cellar = Cellar()
chapel = Chapel()
workshop = Workshop()
festival = Festival()
harbinger = Harbinger()
vassal = Vassal()
artisan = Artisan()
poacher = Poacher()
council_room = CouncilRoom()
witch = Witch()
moat = Moat()
merchant = Merchant()
bandit = Bandit()
bureaucrat = Bureaucrat()
throne_room = ThroneRoom()

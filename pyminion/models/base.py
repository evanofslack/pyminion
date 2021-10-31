from pyminion.models.cards import Action, Treasure, Victory
from pyminion.models.core import Player, Trash, Game
from pyminion.decisions import (
    binary_decision,
    multiple_card_decision,
    single_card_decision,
    validate_input,
)
from pyminion.exceptions import (
    InvalidBinaryInput,
    InvalidMultiCardInput,
    InvalidSingleCardInput,
)
import math


class Copper(Treasure):
    def __init__(
        self,
        name: str = "Copper",
        cost: int = 0,
        type: str = "Treasure",
        money: int = 1,
    ):
        super().__init__(name, cost, type, money)


class Silver(Treasure):
    def __init__(
        self,
        name: str = "Silver",
        cost: int = 3,
        type: str = "Treasure",
        money: int = 2,
    ):
        super().__init__(name, cost, type, money)


class Gold(Treasure):
    def __init__(
        self,
        name: str = "Gold",
        cost: int = 6,
        type: str = "Treasure",
        money: int = 3,
    ):
        super().__init__(name, cost, type, money)


class Estate(Victory):
    def __init__(
        self,
        name: str = "Estate",
        cost: int = 2,
        type: str = "Victory",
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
        type: str = "Victory",
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
        type: str = "Victory",
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
        type: str = "Curse",
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        VICTORY_POINTS = -1
        return VICTORY_POINTS


class Gardens(Victory):
    def __init__(
        self,
        name: str = "Gardens",
        cost: int = 4,
        type: str = "Victory",
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        """
        Worth 1VP for every 10 cards you have (round down)

        """
        total_count = len(player.get_all_cards())
        return math.floor(total_count / 10)


class Smithy(Action):
    def __init__(
        self,
        name: str = "Smithy",
        cost: int = 4,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        +3 cards

        """
        if generic_play:
            super().generic_play(player)

        player.draw(3)


class Village(Action):
    def __init__(
        self,
        name: str = "Village",
        cost: int = 3,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        +1 card, +2 actions

        """
        if generic_play:
            super().generic_play(player)

        player.state.actions += 2
        player.draw()


class Laboratory(Action):
    def __init__(
        self,
        name: str = "Laboratory",
        cost: int = 5,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        +2 cards, +1 action

        """
        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.draw(2)


class Market(Action):
    def __init__(
        self,
        name: str = "Market",
        cost: int = 5,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        +1 card, +1 action, +1 money, +1 buy

        """
        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.draw()
        player.state.money += 1
        player.state.buys += 1


class Moneylender(Action):
    def __init__(
        self,
        name: str = "Moneylender",
        cost: int = 4,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        You may trash a copper from your hand for + 3 money

        """
        if generic_play:
            super().generic_play(player)

        if copper in player.hand.cards:

            @validate_input(exceptions=InvalidBinaryInput)
            def trash_decision() -> None:
                if binary_decision(
                    prompt="Do you want to trash a copper from your hand? y/n?"
                ):
                    player.trash(target_card=copper, trash=game.trash)
                    player.state.money += 3
                return

            return trash_decision()


class Cellar(Action):
    def __init__(
        self,
        name: str = "Cellar",
        cost: int = 2,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        +1 Action

        Discard any number of cards, then draw that many

        """
        if generic_play:
            super().generic_play(player)

        player.state.actions += 1

        if not player.hand.cards:
            return

        @validate_input(exceptions=InvalidMultiCardInput)
        def discard_decision() -> None:

            if discard_cards := multiple_card_decision(
                prompt="Enter the cards you would like to discard seperated by commas: ",
                valid_cards=player.hand.cards,
            ):
                for card in discard_cards:
                    player.discard(card)
                player.draw(len(discard_cards))
            return

        return discard_decision()


class Chapel(Action):
    def __init__(
        self,
        name: str = "Chapel",
        cost: int = 2,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        Trash up to 4 cards from your hand

        """
        if generic_play:
            super().generic_play(player)

        if not player.hand.cards:
            return

        @validate_input(exceptions=InvalidMultiCardInput)
        def trash_decisions() -> None:
            if discard_cards := multiple_card_decision(
                prompt="Enter up to 4 cards you would like to trash from your hand: ",
                valid_cards=player.hand.cards,
            ):
                if len(discard_cards) > 4:
                    raise InvalidMultiCardInput("You cannot trash more than 4 cards")
                for card in discard_cards:
                    player.trash(card, game.trash)
            return

        return trash_decisions()


class Workshop(Action):
    def __init__(
        self,
        name: str = "Workshop",
        cost: int = 3,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        Gain a card costing up to 4 money

        """
        if generic_play:
            super().generic_play(player)

        @validate_input(exceptions=InvalidSingleCardInput)
        def gain_decision() -> None:
            gain_card = single_card_decision(
                prompt="Gain a card costing up to 4 money: ",
                valid_cards=game.supply.avaliable_cards(),
            )
            if not gain_card:
                raise InvalidSingleCardInput("You must gain a card")
            if gain_card.cost > 4:
                raise InvalidSingleCardInput("Card must cost less than 4 money")
            player.gain(gain_card, game.supply)
            return

        return gain_decision()


class Festival(Action):
    def __init__(
        self,
        name: str = "Festival",
        cost: int = 5,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        + 2 actions, + 1 buy, + 2 money

        """
        if generic_play:
            super().generic_play(player)

        player.state.actions += 2
        player.state.money += 2
        player.state.buys += 1


class Harbinger(Action):
    def __init__(
        self,
        name: str = "Harbinger",
        cost: int = 3,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        Look through your discard pile. You may put a card from it onto your deck

        """
        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.draw()

        @validate_input(exceptions=InvalidSingleCardInput)
        def topdeck() -> None:
            if not player.discard_pile:
                return
            print(player.discard_pile)
            topdeck = single_card_decision(
                prompt="You may select a card from your discard pile to put onto your deck: ",
                valid_cards=player.discard_pile.cards,
            )
            if not topdeck:
                return
            player.deck.add(player.discard_pile.remove(topdeck))
            return

        return topdeck()


class Vassal(Action):
    def __init__(
        self,
        name: str = "Vassal",
        cost: int = 3,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        +2 money

        Discard the top card of your deck. If it's an action card you may play it.

        """
        if generic_play:
            super().generic_play(player)

        player.state.money += 2
        player.draw(destination=player.discard_pile)

        if not player.discard_pile:
            return

        print("player discarded ", player.discard_pile.cards[-1])

        if player.discard_pile.cards[-1].type != "Action":
            return

        @validate_input(
            exceptions=(InvalidBinaryInput, Exception)
        )  # Stuck in loop if discard pile is empty
        def play() -> None:
            card = player.discard_pile.cards[-1]
            decision = binary_decision(
                prompt=f"You discarded {card.name}, would you like to play it? (y/n):  ",
            )
            if not decision:
                return
            played_card = player.discard_pile.cards.pop()
            player.playmat.add(played_card)
            player.exact_play(
                card=player.playmat.cards[-1], game=game, generic_play=False
            )

            return

        play()


class Artisan(Action):
    def __init__(
        self,
        name: str = "Artisan",
        cost: int = 6,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        Gain a card to your hand costing up to 5 money.

        Put a card from your hand onto your deck

        """
        if generic_play:
            super().generic_play(player)

        @validate_input(exceptions=InvalidSingleCardInput)
        def gain_decision() -> None:
            gain_card = single_card_decision(
                prompt="Gain a card costing up to 5 money: ",
                valid_cards=game.supply.avaliable_cards(),
            )
            if not gain_card:
                raise InvalidSingleCardInput("You must gain a card")
            if gain_card.cost > 5:
                raise InvalidSingleCardInput("Card must cost less than 5 money")
            player.gain(card=gain_card, supply=game.supply, destination=player.hand)
            return

        gain_decision()

        @validate_input(exceptions=InvalidSingleCardInput)
        def topdeck_decision() -> None:
            topdeck_card = single_card_decision(
                prompt="Put a card from your hand onto your deck: ",
                valid_cards=player.hand.cards,
            )
            if not topdeck_card:
                raise InvalidSingleCardInput("You must put a card onto your deck")
            for card in player.hand.cards:
                if card == topdeck_card:
                    player.deck.add(player.hand.remove(card))
                    return

        return topdeck_decision()


class Poacher(Action):
    def __init__(
        self,
        name: str = "Poacher",
        cost: int = 4,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:
        """
        +1 card, +1 action, + 1 money

        Discard a card per empty Supply pile

        """
        if generic_play:
            super().generic_play(player)

        player.draw()
        player.state.actions += 1
        player.state.money += 1

        if game.supply.num_empty_piles == 0:
            return

        @validate_input(exceptions=InvalidSingleCardInput)
        def discard() -> None:
            discard_card = single_card_decision(
                prompt=" Discard a card from your hand: ", valid_cards=player.hand.cards
            )
            if not discard_card:
                raise InvalidSingleCardInput("You must discard a card")
            player.discard(discard_card)
            return

        for i in range(game.supply.num_empty_piles()):
            discard()


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

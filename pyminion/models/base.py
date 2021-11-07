from pyminion.models.cards import Action, Treasure, Victory
from pyminion.models.core import Player, Card
from pyminion.bots import Bot
from pyminion.players import Human
from pyminion.game import Game
from pyminion.decisions import (
    binary_decision,
    multiple_card_decision,
    single_card_decision,
    validate_input,
)
from pyminion.validations import single_card_validation, multiple_card_validation
from pyminion.exceptions import (
    InvalidBinaryInput,
    InvalidMultiCardInput,
    InvalidSingleCardInput,
)

import math
from typing import Optional, List, Union


class Copper(Treasure):
    def __init__(
        self,
        name: str = "Copper",
        cost: int = 0,
        type: str = "Treasure",
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
        type: str = "Treasure",
        money: int = 2,
    ):
        super().__init__(name, cost, type, money)

    def play(self, player: Player, game: Game) -> int:
        player.playmat.add(self)
        player.hand.remove(self)
        player.state.money += self.money


class Gold(Treasure):
    def __init__(
        self,
        name: str = "Gold",
        cost: int = 6,
        type: str = "Treasure",
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
    """
    Worth 1VP for every 10 cards you have (round down)

    """

    def __init__(
        self,
        name: str = "Gardens",
        cost: int = 4,
        type: str = "Victory",
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
        type: str = "Action",
        actions: int = 0,
        draw: int = 3,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:

        if generic_play:
            super().generic_play(player)

        player.draw(3)

    def bot_play(self, bot: Bot, game: Game, generic_play: bool = True) -> None:
        self.play(bot, game, generic_play)


class Village(Action):
    """
    + 1 card, + 2 actions

    """

    def __init__(
        self,
        name: str = "Village",
        cost: int = 3,
        type: str = "Action",
        actions: int = 2,
        draw: int = 1,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:

        if generic_play:
            super().generic_play(player)

        player.state.actions += 2
        player.draw()

    def bot_play(self, bot: Bot, game: Game, generic_play: bool = True) -> None:
        self.play(bot, game, generic_play)


class Laboratory(Action):
    """
    +2 cards, +1 action

    """

    def __init__(
        self,
        name: str = "Laboratory",
        cost: int = 5,
        type: str = "Action",
        actions: int = 1,
        draw: int = 2,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:

        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.draw(2)

    def bot_play(self, bot: Bot, game: Game, generic_play: bool = True) -> None:
        self.play(bot, game, generic_play)


class Market(Action):
    """
    +1 card, +1 action, +1 money, +1 buy

    """

    def __init__(
        self,
        name: str = "Market",
        cost: int = 5,
        type: str = "Action",
        actions: int = 1,
        draw: int = 1,
        money: int = 1,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:

        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.draw()
        player.state.money += 1
        player.state.buys += 1

    def bot_play(self, bot: Bot, game: Game, generic_play: bool = True) -> None:
        self.play(bot, game, generic_play)


class Moneylender(Action):
    """
    You may trash a copper from your hand for + 3 money

    """

    def __init__(
        self,
        name: str = "Moneylender",
        cost: int = 4,
        type: str = "Action",
        actions: int = 0,
        draw: int = 0,
        money: int = 3,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self,
        player: Union[Human, Bot],
        game: Game,
        generic_play: bool = True,
    ) -> None:

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
        type: str = "Action",
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
        type: str = "Action",
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Union[Human, Bot], game: Game, generic_play: bool = True
    ) -> None:

        if generic_play:
            super().generic_play(player)

        if not player.hand.cards:
            return

        if isinstance(player, Human):
            trash_cards = player.multiple_card_decision(
                prompt="Enter up to 4 cards you would like to trash from your hand: ",
                valid_cards=player.hand.cards,
            )

        if isinstance(player, Bot):
            trash_cards = player.multiple_card_decision(
                card=self, valid_cards=player.hand.cards
            )

        if not trash_cards:
            return

        if len(trash_cards) > 4:
            raise InvalidMultiCardInput("You cannot trash more than 4 cards")

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
        type: str = "Action",
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:

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

    def bot_play(
        self,
        bot: Bot,
        game: Game,
        gain_card: Card = None,
        generic_play: bool = True,
    ) -> None:
        if generic_play:
            super().generic_play(bot)

        if not gain_card:
            raise InvalidSingleCardInput("You must gain a card")
        if gain_card.cost > 4:
            raise InvalidSingleCardInput("Card must cost less than 4 money")

        if single_card_validation(gain_card, valid_cards=game.supply.avaliable_cards()):
            bot.gain(gain_card, game.supply)


class Festival(Action):
    """
    + 2 actions, + 1 buy, + 2 money

    """

    def __init__(
        self,
        name: str = "Festival",
        cost: int = 5,
        type: str = "Action",
        actions: int = 2,
        draw: int = 0,
        money: int = 2,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:

        if generic_play:
            super().generic_play(player)

        player.state.actions += 2
        player.state.money += 2
        player.state.buys += 1

    def bot_play(self, bot: Bot, game: Game, generic_play: bool = True) -> None:
        self.play(bot, game, generic_play)


class Harbinger(Action):
    """
    +1 card, +1 action

    Look through your discard pile. You may put a card from it onto your deck

    """

    def __init__(
        self,
        name: str = "Harbinger",
        cost: int = 3,
        type: str = "Action",
        actions: int = 1,
        draw: int = 1,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:

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

    def bot_play(
        self,
        bot: Bot,
        game: Game,
        topdeck: Optional[Card] = None,
        generic_play: bool = True,
    ) -> None:

        if generic_play:
            super().generic_play(bot)

        bot.state.actions += 1
        bot.draw()

        if not bot.discard_pile or not topdeck:
            return

        if single_card_validation(topdeck, valid_cards=bot.discard_pile.cards):
            bot.deck.add(bot.discard_pile.remove(topdeck))


class Vassal(Action):
    """
    +2 money

    Discard the top card of your deck. If it's an action card you may play it.

    """

    def __init__(
        self,
        name: str = "Vassal",
        cost: int = 3,
        type: str = "Action",
        actions: int = 0,
        draw: int = 0,
        money: int = 2,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:

        if generic_play:
            super().generic_play(player)

        player.state.money += 2
        player.draw(destination=player.discard_pile)

        if not player.discard_pile:
            return

        print("player discarded ", player.discard_pile.cards[-1])

        if player.discard_pile.cards[-1].type != "Action":
            return

        @validate_input(exceptions=(InvalidBinaryInput, Exception))
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

    def bot_play(
        self,
        bot: Bot,
        game: Game,
        decision: bool = True,
        generic_play: bool = True,
    ) -> None:

        if generic_play:
            super().generic_play(bot)

        bot.state.money += 2
        bot.draw(destination=bot.discard_pile)

        if not bot.discard_pile:
            return

        if bot.discard_pile.cards[-1].type != "Action":
            return

        if not decision:
            return

        played_card = bot.discard_pile.cards.pop()
        bot.playmat.add(played_card)
        bot.exact_play(card=bot.playmat.cards[-1], game=game, generic_play=False)


class Artisan(Action):
    """
    Gain a card to your hand costing up to 5 money.

    Put a card from your hand onto your deck

    """

    def __init__(
        self,
        name: str = "Artisan",
        cost: int = 6,
        type: str = "Action",
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:

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

    def bot_play(
        bot: Bot,
        game: Game,
        gain_card: Card = None,
        topdeck_card: Card = None,
        generic_play: bool = True,
    ) -> None:

        if generic_play:
            super().generic_play(bot)

        gain_card = silver if not gain_card else gain_card

        if gain_card.cost > 5:
            raise InvalidSingleCardInput("Card must cost less than 5 money")

        if single_card_validation(
            target_card=gain_card, valid_cards=game.supply.avaliable_cards()
        ):
            bot.gain(card=gain_card, supply=game.supply, destination=bot.hand)

        topdeck_card = gain_card if not topdeck_card else topdeck_card

        for card in bot.hand.cards:
            if card == topdeck_card:
                bot.deck.add(bot.hand.remove(card))


class Poacher(Action):
    """
    +1 card, +1 action, + 1 money

    Discard a card per empty Supply pile

    """

    def __init__(
        self,
        name: str = "Poacher",
        cost: int = 4,
        type: str = "Action",
        actions: int = 1,
        draw: int = 1,
        money: int = 1,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(self, player: Player, game: Game, generic_play: bool = True) -> None:

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
            if not player.hand:
                return
            discard()

    def bot_play(
        bot: Bot, game: Game, discard_cards: List[Card], generic_play: bool = False
    ) -> None:

        if generic_play:
            super().generic_play(bot)

        bot.draw()
        bot.state.actions += 1
        bot.state.money += 1

        if game.supply.num_empty_piles() == 0:
            return

        if multiple_card_validation(
            target_cards=discard_cards, valid_cards=bot.hand.cards
        ):
            for i in range(game.supply.num_empty_piles()):
                if not bot.hand:
                    return
                try:
                    bot.discard(discard_cards[i])
                except:
                    bot.discard(
                        bot.hand.cards[-1]
                    )  # default to discarding the last card in hand


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

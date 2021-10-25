from pyminion.models.cards import Action, Treasure, Victory
from pyminion.models.core import Turn, Player, Trash, Game
from pyminion.decisions import binary_decision, multiple_card_decision
from pyminion.exceptions import InvalidBinaryInput, InvalidMultiCardInput

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

    def play(self, turn: Turn, player: Player, game: Game):
        """
        +3 cards

        """
        super().common_play(turn, player)

        player.draw(3)


class Village(Action):
    def __init__(
        self,
        name: str = "Village",
        cost: int = 3,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, turn: Turn, player: Player, game: Game):
        """
        +1 card, +2 actions

        """
        super().common_play(turn, player)
        turn.actions += 2
        player.draw()


class Laboratory(Action):
    def __init__(
        self,
        name: str = "Laboratory",
        cost: int = 5,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, turn: Turn, player: Player, game: Game):
        """
        +2 cards, +1 action

        """
        super().common_play(turn, player)
        turn.actions += 1
        player.draw()
        player.draw()


class Market(Action):
    def __init__(
        self,
        name: str = "Market",
        cost: int = 5,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, turn: Turn, player: Player, game: Game):
        """
        +1 card, +1 action, +1 money, +1 buy

        """
        super().common_play(turn, player)
        turn.actions += 1
        player.draw()
        turn.money += 1
        turn.buys += 1


class Moneylender(Action):
    def __init__(
        self,
        name: str = "Moneylender",
        cost: int = 4,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, turn: Turn, player: Player, game: Game):
        """
        You may trash a copper from your hand for + 3 money

        """
        super().common_play(turn, player)
        if copper in player.hand.cards:
            while True:
                try:
                    if binary_decision(
                        prompt="Do you want to trash a copper from your hand? y/n?"
                    ):
                        player.trash(target_card=copper, trash=game.trash)
                        turn.money += 3
                    return
                except InvalidBinaryInput as e:
                    print(e)


class Cellar(Action):
    def __init__(
        self,
        name: str = "Cellar",
        cost: int = 2,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, turn: Turn, player: Player, game: Game):
        """
        +1 Action

        Discard any number of cards, then draw that many

        """
        super().common_play(turn, player)
        turn.actions += 1

        if not player.hand.cards:
            return

        while True:
            try:
                if discard_cards := multiple_card_decision(
                    prompt="Enter the cards you would like to discard seperated by commas: ",
                    valid_cards=player.hand.cards,
                ):
                    for card in discard_cards:
                        player.discard(card)
                    player.draw(len(discard_cards))
                return
            except InvalidMultiCardInput as e:
                print(e)


class Chapel(Action):
    def __init__(
        self,
        name: str = "Chapel",
        cost: int = 2,
        type: str = "Action",
    ):
        super().__init__(name, cost, type)

    def play(self, turn: Turn, player: Player, game: Game):
        """
        Trash up to 4 cards from your hand

        """
        super().common_play(turn, player)

        if not player.hand.cards:
            return

        while True:
            try:
                if discard_cards := multiple_card_decision(
                    prompt="Enter up to 4 cards you would like to trash from your hand: ",
                    valid_cards=player.hand.cards,
                ):
                    if len(discard_cards) > 4:
                        raise InvalidMultiCardInput(
                            "You cannot trash more than 4 cards"
                        )
                    for card in discard_cards:
                        player.trash(card, game.trash)
                return
            except InvalidMultiCardInput as e:
                print(e)


copper = Copper()
silver = Silver()
gold = Gold()

estate = Estate()
duchy = Duchy()
province = Province()
gardens = Gardens()

smithy = Smithy()
village = Village()
laboratory = Laboratory()
market = Market()
moneylender = Moneylender()
cellar = Cellar()
chapel = Chapel()

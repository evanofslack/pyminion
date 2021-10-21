from pyminion.models.cards import Action, Treasure, Victory
from pyminion.models.core import Turn, Player, Trash
from pyminion.util import binary_decision, multiple_card_decision


class Copper(Treasure):
    def __init__(self, name: str = "Copper", cost: int = 0, money: int = 1):
        super().__init__(name, cost, money)


class Silver(Treasure):
    def __init__(self, name: str = "Silver", cost: int = 3, money: int = 2):
        super().__init__(name, cost, money)


class Gold(Treasure):
    def __init__(self, name: str = "Gold", cost: int = 6, money: int = 3):
        super().__init__(name, cost, money)


class Estate(Victory):
    def __init__(self, name: str = "Estate", cost: int = 2, victory_points: int = 1):
        super().__init__(name, cost, victory_points)


class Duchy(Victory):
    def __init__(self, name: str = "Duchy", cost: int = 5, victory_points: int = 3):
        super().__init__(name, cost, victory_points)


class Province(Victory):
    def __init__(self, name: str = "Province", cost: int = 8, victory_points: int = 6):
        super().__init__(name, cost, victory_points)


class Smithy(Action):
    def __init__(self, name: str = "Smithy", cost: int = 4):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player):
        """
        +3 cards

        """
        super().common_play(turn, player)

        for i in range(3):
            player.draw()


class Village(Action):
    def __init__(self, name: str = "Village", cost: int = 3):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player):
        """
        +1 card, +1 action

        """
        super().common_play(turn, player)
        turn.actions += 2
        player.draw()


class Laboratory(Action):
    def __init__(self, name: str = "Laboratory", cost: int = 5):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player):
        """
        +2 cards, +1 action

        """
        super().common_play(turn, player)
        turn.actions += 1
        player.draw()
        player.draw()


class Laboratory(Action):
    def __init__(self, name: str = "Laboratory", cost: int = 5):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player):
        """
        +2 cards, +1 action

        """
        super().common_play(turn, player)
        turn.actions += 1
        player.draw()
        player.draw()


class Market(Action):
    def __init__(self, name: str = "Market", cost: int = 5):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player):
        """
        +1 card, +1 action, +1 money, +1 buy

        """
        super().common_play(turn, player)
        turn.actions += 1
        player.draw()
        turn.money += 1
        turn.buys += 1


class Moneylender(Action):
    def __init__(self, name: str = "Moneylender", cost: int = 4):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player, trash: Trash):
        """
        You may trash a copper from your hand for + 3 money

        """
        super().common_play(turn, player)
        if copper in player.hand.cards:
            if binary_decision(
                prompt="Do you want to trash a copper from your hand? y/n?"
            ):
                player.trash(target_card=copper, trash=trash)
                turn.money += 3


class Cellar(Action):
    def __init__(self, name: str = "Cellar", cost: int = 4):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player):
        """
        +1 Action

        Discard any number of cards, then draw that many

        """
        super().common_play(turn, player)
        turn.actions += 1

        discard_cards = multiple_card_decision(
            prompt="Enter the cards you would like to discard seperated by commas: ",
            valid_cards=player.hand.cards,
        )
        for card in discard_cards:
            player.discard(card)
        player.draw(len(discard_cards))


copper = Copper()
silver = Silver()
gold = Gold()
estate = Estate()
duchy = Duchy()
province = Province()

smithy = Smithy()
village = Village()
laboratory = Laboratory()
market = Market()
moneylender = Moneylender()
cellar = Cellar()

from typing import List


class Card:
    def __init__(self, name: str, cost: int):
        self.name = name
        self.cost = cost


class Treasure(Card):
    def __init__(self, name: str, cost: int, money: int):
        super().__init__(name, cost)
        self.money = money


class Victory(Card):
    def __init__(self, name: str, cost: int, victory_points: int):
        super().__init__(name, cost)
        self.victory_points = victory_points


class Action(Card):
    def __init__(self, name: str, cost: int):
        super().__init__(name, cost)

    def play():
        pass


class Deck:
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def draw(self, num_cards: int = 1):
        drawn_cards = [self.cards.pop(-i) for i in range(len(self.cards))]
        return drawn_cards


class Discard:
    pass


class Hand:
    pass


class Pile:
    def __init__(self, cards: List[Card]):
        self.cards = cards

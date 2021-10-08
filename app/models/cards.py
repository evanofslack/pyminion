from typing import List
import random


class Card:
    def __init__(self, name: str, cost: int):
        self.name = name
        self.cost = cost

    def __repr__(self):
        return f"{self.name} ({type(self).__name__})"


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


class AbstractDeck:
    def __init__(self, cards: List[Card] = None):
        if cards: 
            self.cards = cards
        else: 
            self.cards = []
        
    def __len__(self):
        return len(self.cards)

    def add(self, card: Card):
        self.cards.append(card)


class Deck(AbstractDeck):
    def __init__(self, cards: List[Card]):
        super().__init__(cards)

    def draw(self, num_cards: int = 1): #TODO make this return just one card potentially
        drawn_cards = [self.cards.pop() for i in range(num_cards)]
        return drawn_cards

    def shuffle(self):
        random.shuffle(self.cards)

    def combine(self, cards: List[Card]):
        self.cards += cards


class DiscardPile(AbstractDeck):
    def __init__(self, cards: List[Card] = None):
        super().__init__(cards)


class Hand(AbstractDeck):
    def __init__(self, cards: List[Card] = None):
        super().__init__(cards)
    

class Pile(AbstractDeck):
    def __init__(self, cards: List[Card] = None):
        super().__init__(cards)


class Playmat(AbstractDeck):
    def __init__(self, cards: List[Card] = None):
        super().__init__(cards)



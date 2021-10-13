from typing import List
import random

from pyminion.exceptions import InsufficientActions, InsufficientMoney, InsufficientBuys


class Card:
    def __init__(self, name: str, cost: int):
        self.name = name
        self.cost = cost

    def __repr__(self):
        return f"{self.name} ({type(self).__name__})"


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

    def remove(self, card: Card):
        self.cards.remove(card)


class Deck(AbstractDeck):
    def __init__(self, cards: List[Card]):
        super().__init__(cards)

    def draw(self):
        drawn_card = self.cards.pop()
        return drawn_card

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


class Trash(AbstractDeck):
    def __init__(self, cards: List[Card] = None):
        super().__init__(cards)


class Player:
    def __init__(
        self,
        deck: Deck,
        discard: DiscardPile,
        hand: Hand,
        playmat: Playmat,
        name: str = "TestPlayer",
    ):
        self.deck = deck
        self.discard = discard
        self.hand = hand
        self.playmat = playmat
        self.name = name


class Turn:
    def __init__(self, player: Player, actions: int = 1, money: int = 0, buys: int = 1):
        self.player = player
        self.actions = actions
        self.money = money
        self.buys = buys

    def buy(self, card: Card):
        if card.cost > self.money:
            raise InsufficientMoney(
                f"{self.player.name}: Not enough money to buy {card.name}"
            )
        if self.buys < 1:
            raise InsufficientBuys(
                f"{self.player.name}: Not enough buys to buy {card.name}"
            )
        self.money -= card.cost
        self.buys -= 1
        self.player.discard.add(card)
        # game.pile[card].draw

    def clean_up(self):
        pass

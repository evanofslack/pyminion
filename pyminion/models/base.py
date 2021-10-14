from typing import List
import random

from pyminion.exceptions import InsufficientMoney, InsufficientBuys


class Card:
    """
    Base class representing a dominion card

    """

    def __init__(self, name: str, cost: int):
        self.name = name
        self.cost = cost

    def __repr__(self):
        return f"{self.name} ({type(self).__name__})"


class AbstractDeck:
    """
    Base class representing a generic list of dominion cards

    """

    def __init__(self, cards: List[Card] = None):
        if cards:
            self.cards = cards
        else:
            self.cards = []

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"{type(self).__name__} {[card.name for card in self.cards]}"

    def add(self, card: Card) -> Card:
        self.cards.append(card)

    def remove(self, card: Card) -> Card:
        self.cards.remove(card)
        return card


class Deck(AbstractDeck):
    def __init__(self, cards: List[Card]):
        super().__init__(cards)

    def draw(self) -> Card:
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
        if cards and len(set(cards)) == 1:
            self.name = cards[0].name
        elif cards:
            self.name = "Mixed"
        else:
            self.name == None


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
        player_id: str = None,
    ):
        self.deck = deck
        self.discard = discard
        self.hand = hand
        self.playmat = playmat
        self.player_id = player_id


class Turn:
    def __init__(self, player: Player, actions: int = 1, money: int = 0, buys: int = 1):
        self.player = player
        self.actions = actions
        self.money = money
        self.buys = buys

    def draw_five(self):
        for i in range(5):  # draw 5 cards from deck and add to hand
            self.player.hand.add(self.player.deck.draw())

    def buy(self, card: Card):
        if card.cost > self.money:
            raise InsufficientMoney(
                f"{self.player.player_id}: Not enough money to buy {card.name}"
            )
        if self.buys < 1:
            raise InsufficientBuys(
                f"{self.player.player_id}: Not enough buys to buy {card.name}"
            )
        self.money -= card.cost
        self.buys -= 1
        self.player.discard.add(card)
        # game.pile[card].draw

    def clean_up(self):
        pass


class Supply:
    def __init__(self, piles: List[Pile] = None):
        if piles:
            self.piles = piles
        else:
            self.piles = []

    def __len__(self):
        return len(self.piles)

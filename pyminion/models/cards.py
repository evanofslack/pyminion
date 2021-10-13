from typing import List
import random

from app.exceptions import InsufficientActions, InsufficientMoney, InsufficientBuys


class Card:
    def __init__(self, name: str, cost: int):
        self.name = name
        self.cost = cost

    def __repr__(self):
        return f"{self.name} ({type(self).__name__})"


class Victory(Card):
    def __init__(self, name: str, cost: int, victory_points: int):
        super().__init__(name, cost)
        self.victory_points = victory_points


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


class Treasure(Card):
    def __init__(self, name: str, cost: int, money: int):
        super().__init__(name, cost)
        self.money = money

    def play(self, turn: Turn):
        turn.money += self.money
        turn.player.playmat.add(self)
        turn.player.hand.remove(self)


class Action(Card):
    def __init__(self, name: str, cost: int):
        super().__init__(name, cost)

    def play(self):
        """
        Specific play method unique to each action card

        """
        raise NotImplementedError(f"Play method must be implemented for {self.name}")

    def common_play(self, turn: Turn):
        """
        Common play method that gets executes for all action cards

        """
        if turn.actions < 1:
            raise InsufficientActions(
                f"{turn.player.name}: Not enough actions to play {self.name}"
            )

        turn.player.playmat.add(self)
        turn.player.hand.remove(self)
        turn.actions -= 1


class Smithy(Action):
    def __init__(self, name: str = "Smithy", cost: int = 4):
        super().__init__(name, cost)

    def play(self, turn: Turn):
        super().common_play(turn)

        for i in range(3):  # draw 3 cards from deck and add to hand
            turn.player.hand.add(turn.player.deck.draw())

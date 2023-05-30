import logging
import random
from collections import Counter
from typing import TYPE_CHECKING, Any, Iterable, Iterator, List, Optional, Tuple

if TYPE_CHECKING:
    from pyminion.game import Game
    from pyminion.player import Player

from enum import Enum
from pyminion.exceptions import EmptyPile, InsufficientActions, PileNotFound

logger = logging.getLogger()



class CardType(Enum):
    """
    Enum class for all card types that are currently used in the implemented expansions

    """
    Treasure = 1
    Victory = 2
    Curse = 3
    Action = 4
    Attack = 5
    Reaction = 6

class Card:

    """
    Base class representing a dominion card

    """

    def __init__(self, name: str, cost: int, type: Tuple[CardType]):
        self.name = name
        self._cost = cost
        self.type = type

    def __repr__(self):
        return f"{self.name}"

    def get_cost(self, player: "Player", game: "Game") -> int:
        cost = max(0, self._cost - game.card_cost_reduction)
        return cost


class Victory(Card):
    def __init__(self, name: str, cost: int, type: Tuple[CardType]):
        super().__init__(name, cost, type)

    def score(self, player: "Player") -> int:
        """
        Specific score method unique to each victory card

        """
        raise NotImplementedError(f"Score method must be implemented for {self.name}")


class Treasure(Card):
    def __init__(self, name: str, cost: int, type: Tuple[CardType], money: int):
        super().__init__(name, cost, type)
        self.money = money

    def play(self, player: "Player"):
        """
        Specific play method unique to each treasure card

        """
        raise NotImplementedError(f"Play method must be implemented for {self.name}")


class Action(Card):
    def __init__(
        self,
        name: str,
        cost: int,
        type: Tuple[CardType],
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
    ):
        super().__init__(name, cost, type)
        self.actions = actions
        self.draw = draw
        self.money = money

    def play(self, player: "Player", game: "Game", generic_play: bool = True) -> None:
        """
        Specific play method unique to each action card

        """
        raise NotImplementedError(f"play method must be implemented for {self.name}")

    def generic_play(self, player: "Player") -> None:
        """
        Generic play method that gets executes for all action cards

        """
        if player.state.actions < 1:
            raise InsufficientActions(
                f"{player.player_id}: Not enough actions to play {self.name}"
            )

        player.playmat.add(self)
        player.hand.remove(self)
        player.state.actions -= 1

    def multi_play(self, player: "Player", game: "Game", state: Any, generic_play: bool = True) -> Any:
        """
        Called by "Throne Room variants" to play a card multiple times.
        By default this just calls self.play() but can be overridden by derived
        cards to implement different behavior.

        """
        self.play(player, game, generic_play)
        return None


class DeckCounter(Counter):
    def __str__(self):
        return ", ".join(f"{value} {key}" for key, value in (self).items())


class AbstractDeck:

    """
    Base class representing a generic list of dominion cards

    """

    def __init__(self, cards: Optional[List[Card]] = None):
        if cards:
            self.cards = cards
        else:
            self.cards = []

    def __repr__(self):
        return str(DeckCounter(self.cards))

    def __len__(self):
        return len(self.cards)

    def add(self, card: Card) -> None:
        self.cards.append(card)

    def remove(self, card: Card) -> Card:
        self.cards.remove(card)
        return card

    def move_to(self, destination: "AbstractDeck"):
        destination.cards += self.cards
        self.cards = []


class Deck(AbstractDeck):
    def __init__(self, cards: Optional[List[Card]] = None):
        super().__init__(cards)

    def draw(self) -> Card:
        drawn_card = self.cards.pop()
        return drawn_card

    def shuffle(self):
        random.shuffle(self.cards)


class DiscardPile(AbstractDeck):
    def __init__(self, cards: Optional[List[Card]] = None):
        super().__init__(cards)


class Hand(AbstractDeck):
    def __init__(self, cards: Optional[List[Card]] = None):
        super().__init__(cards)


class Pile(AbstractDeck):
    def __init__(self, cards: Optional[List[Card]] = None):
        super().__init__(cards)
        if cards and len(set(cards)) == 1:
            self.name = cards[0].name
        elif cards:
            self.name = "Mixed"
        else:
            self.name = None

    def remove(self, card: Card) -> Card:
        if len(self.cards) < 1:
            raise EmptyPile(f"{self.name} pile is empty, cannot gain card")
        self.cards.remove(card)
        return card


class Playmat(AbstractDeck):
    def __init__(self, cards: Optional[List[Card]] = None):
        super().__init__(cards)


class Trash(AbstractDeck):
    def __init__(self, cards: Optional[List[Card]] = None):
        super().__init__(cards)


class Supply:
    """
    Collection of card piles that make up the game's supply.

    """

    def __init__(self, piles: Optional[List[Pile]] = None):
        if piles:
            self.piles = piles
        else:
            self.piles = []

    def __repr__(self):
        return str(self.avaliable_cards())

    def __len__(self):
        return len(self.piles)

    def get_pile(self, pile_name: str) -> Pile:
        """
        Get a pile by name.

        """
        for pile in self.piles:
            if pile.name == pile_name:
                return pile
        raise PileNotFound(f"{pile_name} pile is not valid")

    def gain_card(self, card: Card) -> Card:
        """
        Gain a card from the supply.

        """
        pile = self.get_pile(card.name)
        try:
            return pile.remove(card)

        except EmptyPile as e:
            raise e

    def return_card(self, card: Card):
        """
        Return a card to the supply.

        """
        pile = self.get_pile(card.name)
        pile.add(card)

    def trash_card(self, card: Card, trash: "Trash") -> None:
        """
        Trash a card from the supply.

        """
        pile = self.get_pile(card.name)
        pile.remove(card)
        trash.add(card)

    def avaliable_cards(self) -> List[Card]:
        """
        Returns a list containing a single card from each non-empty pile in the supply.

        """
        cards = [pile.cards[0] for pile in self.piles if pile]
        return cards

    def num_empty_piles(self) -> int:
        """
        Returns the number of empty piles in the supply.

        """
        empty_piles: int = 0
        for pile in self.piles:
            if len(pile) == 0:
                empty_piles += 1
        return empty_piles

    def pile_length(self, pile_name: str) -> int:
        """
        Get the number of cards in a specified pile in the supply.

        """
        pile = self.get_pile(pile_name)
        return len(pile)


def get_action_cards(cards: Iterable[Card]) -> Iterator[Action]:
    for card in cards:
        if CardType.Action in card.type:
            assert isinstance(card, Action)
            yield card


def get_treasure_cards(cards: Iterable[Card]) -> Iterator[Treasure]:
    for card in cards:
        if CardType.Treasure in card.type:
            assert isinstance(card, Treasure)
            yield card


def get_victory_cards(cards: Iterable[Card]) -> Iterator[Victory]:
    for card in cards:
        if CardType.Victory in card.type:
            assert isinstance(card, Victory)
            yield card

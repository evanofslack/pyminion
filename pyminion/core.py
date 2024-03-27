import logging
import random
from collections import Counter
from typing import TYPE_CHECKING, Any, Callable, Iterable, Iterator, List, Optional, Tuple

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

    def __init__(self, name: str, cost: int, type: Tuple[CardType, ...]):
        self.name = name
        self._cost = cost
        self.type = type

    def __repr__(self):
        return f"{self.name}"

    def get_cost(self, player: "Player", game: "Game") -> int:
        cost = max(0, self._cost - game.card_cost_reduction)
        return cost

    def get_pile_starting_count(self, game: "Game") -> int:
        return 10

    def set_up(self, game: "Game") -> None:
        pass


class ScoreCard(Card):
    def __init__(self, name: str, cost: int, type: Tuple[CardType, ...]):
        super().__init__(name, cost, type)

    def score(self, player: "Player") -> int:
        """
        Specific score method unique to card

        """
        raise NotImplementedError(f"Score method must be implemented for {self.name}")


class Victory(ScoreCard):
    def __init__(self, name: str, cost: int, type: Tuple[CardType, ...]):
        super().__init__(name, cost, type)

    def get_pile_starting_count(self, game: "Game") -> int:
        num_players = len(game.players)
        if num_players == 1:
            return 5
        elif num_players == 2:
            return 8
        else:
            return 12


class Treasure(Card):
    def __init__(self, name: str, cost: int, type: Tuple[CardType, ...], money: int):
        super().__init__(name, cost, type)
        self.money = money

    def play(self, player: "Player", game: "Game") -> None:
        """
        Specific play method unique to each treasure card

        """
        raise NotImplementedError(f"Play method must be implemented for {self.name}")


class Action(Card):
    def __init__(
        self,
        name: str,
        cost: int,
        type: Tuple[CardType, ...],
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
        buys: int = 0,
    ):
        super().__init__(name, cost, type)
        self.actions = actions
        self.draw = draw
        self.money = money
        self.buys = buys

    def play(self, player: "Player", game: "Game", generic_play: bool = True) -> None:
        """
        Specific play method unique to each action card

        """
        logger.info(f"{player} plays {self}")

        if generic_play:
            self.generic_play(player)

        if self.draw > 0:
            player.draw(self.draw)
        player.state.actions += self.actions
        player.state.money += self.money
        player.state.buys += self.buys

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

    def __init__(
            self,
            cards: Optional[List[Card]] = None,
            on_add: Optional[Callable[[Card], None]] = None,
            on_remove: Optional[Callable[[Card], None]] = None,
    ):
        if cards:
            self.cards = cards
        else:
            self.cards = []
        self.on_add = on_add
        self.on_remove = on_remove

    def __repr__(self):
        return str(DeckCounter(self.cards))

    def __len__(self):
        return len(self.cards)

    def add(self, card: Card) -> None:
        self.cards.append(card)
        if self.on_add is not None:
            self.on_add(card)

    def remove(self, card: Card) -> Card:
        self.cards.remove(card)
        if self.on_remove is not None:
            self.on_remove(card)
        return card

    def move_to(self, destination: "AbstractDeck") -> None:
        if destination.on_add is None and self.on_remove is None:
            destination.cards += self.cards
            self.cards = []
        else:
            cards = self.cards[:] # copy cards that are being moved
            destination.cards += self.cards
            self.cards = []

            if destination.on_add is not None:
                for card in cards:
                    destination.on_add(card)

            if self.on_remove is not None:
                for card in cards:
                    self.on_remove(card)


class Deck(AbstractDeck):
    def __init__(
            self,
            cards: Optional[List[Card]] = None,
            on_add: Optional[Callable[[Card], None]] = None,
            on_remove: Optional[Callable[[Card], None]] = None,
            on_shuffle: Optional[Callable[[], None]] = None,
    ):
        super().__init__(cards, on_add, on_remove)
        self.on_shuffle = on_shuffle

    def draw(self) -> Card:
        drawn_card = self.cards.pop()
        if self.on_remove is not None:
            self.on_remove(drawn_card)
        return drawn_card

    def shuffle(self) -> None:
        random.shuffle(self.cards)
        if self.on_shuffle is not None:
            self.on_shuffle()


class DiscardPile(AbstractDeck):
    def __init__(self, cards: Optional[List[Card]] = None):
        super().__init__(cards)


class Hand(AbstractDeck):
    def __init__(
            self,
            cards: Optional[List[Card]] = None,
            on_add: Optional[Callable[[Card], None]] = None,
            on_remove: Optional[Callable[[Card], None]] = None,
    ):
        super().__init__(cards, on_add, on_remove)


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
        super().remove(card)
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
        return str(self.available_cards())

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

    def return_card(self, card: Card) -> None:
        """
        Return a card to the supply.

        """
        pile = self.get_pile(card.name)
        pile.add(card)

    def available_cards(self) -> List[Card]:
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
    """
    Returns an iterator over the action cards in a Card iterable.

    """
    for card in cards:
        if CardType.Action in card.type:
            assert isinstance(card, Action)
            yield card


def get_treasure_cards(cards: Iterable[Card]) -> Iterator[Treasure]:
    """
    Returns an iterator over the treasure cards in a Card iterable.

    """
    for card in cards:
        if CardType.Treasure in card.type:
            assert isinstance(card, Treasure)
            yield card


def get_victory_cards(cards: Iterable[Card]) -> Iterator[Victory]:
    """
    Returns an iterator over the victory cards in a Card iterable.

    """
    for card in cards:
        if CardType.Victory in card.type:
            assert isinstance(card, Victory)
            yield card


def get_score_cards(cards: Iterable[Card]) -> Iterator[ScoreCard]:
    """
    Returns an iterator over the victory and curse cards in a Card iterable.

    """
    for card in cards:
        if CardType.Victory in card.type or CardType.Curse in card.type:
            assert isinstance(card, ScoreCard)
            yield card

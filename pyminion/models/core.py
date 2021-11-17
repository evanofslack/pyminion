import logging
import random
from collections import Counter
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Tuple

from pyminion.exceptions import (
    EmptyPile,
    InsufficientBuys,
    InsufficientMoney,
    InvalidCardPlay,
    PileNotFound,
)

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class Card:

    """
    Base class representing a dominion card

    """

    def __init__(self, name: str, cost: int, type: Tuple[str]):
        self.name = name
        self.cost = cost
        self.type = type

    def __repr__(self):
        return f"{self.name}"


class DeckCounter(Counter):
    def __str__(self):
        return ", ".join(f"{value} {key}" for key, value in (self).items())


class AbstractDeck:

    """
    Base class representing a generic list of dominion cards

    """

    def __init__(self, cards: List[Card] = None):
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
    def __init__(self, cards: List[Card] = None):
        super().__init__(cards)

    def draw(self) -> Card:
        drawn_card = self.cards.pop()
        return drawn_card

    def shuffle(self):
        random.shuffle(self.cards)


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

    def remove(self, card: Card) -> Card:
        if len(self.cards) < 1:
            raise EmptyPile(f"{self.name} pile is empty, cannot gain card")
        self.cards.remove(card)
        return card


class Playmat(AbstractDeck):
    def __init__(self, cards: List[Card] = None):
        super().__init__(cards)


class Trash(AbstractDeck):
    def __init__(self, cards: List[Card] = None):
        super().__init__(cards)


@dataclass
class State:
    """
    Hold state during a player's turn

    """

    actions: int = 1
    money: int = 0
    buys: int = 1


class Player:
    """
    Basic representation of a player including the piles of cards they own
    and the basic actions they can take to manipulate the state of the game

    """

    def __init__(
        self,
        deck: Deck = None,
        discard_pile: DiscardPile = None,
        hand: Hand = None,
        playmat: Playmat = None,
        state: State = None,
        player_id: str = None,
    ):
        self.deck = deck if deck else Deck()
        self.discard_pile = discard_pile if discard_pile else DiscardPile()
        self.hand = hand if hand else Hand()
        self.playmat = playmat if playmat else Playmat()
        self.state = state if state else State()
        self.player_id = player_id
        self.turns: int = 0
        self.shuffles: int = 0

    def __repr__(self):
        return f"{self.player_id}"

    def reset(self):
        """
        Reset the state of the player to a pre-game state

        Required for resetting players between games when running simulations

        """
        self.turns = 0
        self.deck.cards = []
        self.discard_pile.cards = []
        self.hand.cards = []

    def draw(self, num_cards: int = 1, destination: AbstractDeck = None) -> None:
        """
        Draw cards from deck and add them to the specified destination

        Defaults to drawing one card and adding to the player's hand

        """
        if destination is None:
            destination = self.hand
        for i in range(num_cards):
            # Both deck and discard empty -> do nothing
            if len(self.discard_pile) == 0 and len(self.deck) == 0:
                pass
            # Deck is empty -> shuffle in the discard pile
            elif len(self.deck) == 0:
                self.discard_pile.move_to(self.deck)
                self.deck.shuffle()
                self.shuffles += 1
                destination.add(self.deck.draw())
            else:
                destination.add(self.deck.draw())

    def discard(self, target_card: Card) -> None:
        """
        Move specified card from the player's hand to the player's discard pile

        """
        for card in self.hand.cards:
            if card == target_card:
                self.discard_pile.add(self.hand.remove(card))
                return

    def play(self, target_card: Card, game: "Game", generic_play: bool = True) -> None:
        """
        Find target card in player's hand and play it

        If generic_play is true, card is moved from player's hand to playmat
        and player action count decreased by 1. This is the default behavior
        but is overridden for cards like vassal and throne room

        """
        for card in self.hand.cards:
            if card.name == target_card.name:
                if "Action" in card.type:
                    try:
                        card.play(player=self, game=game, generic_play=generic_play)
                        return

                    except:
                        raise InvalidCardPlay(
                            f"Invalid play, {target_card} has no play method"
                        )
                if "Treasure" in card.type:
                    try:
                        card.play(player=self, game=game)
                        return
                    except:
                        raise InvalidCardPlay(
                            f"Invalid play, {target_card} has no play method"
                        )

        raise InvalidCardPlay(f"Invalid play, {target_card} not in hand")

    def exact_play(self, card: Card, game: "Game", generic_play: bool = True) -> None:
        """
        Similar to previous play method, except exact card to play must be specified

        This is method is necessary when playing cards not in the player's hand, such as vassal

        """
        try:
            if "Action" in card.type:
                card.play(player=self, game=game, generic_play=generic_play)
            elif "Treasure" in card.type:
                card.play(player=self, game=game)
        except:
            raise InvalidCardPlay(f"Invalid play, cannot play {card}")

    def buy(self, card: Card, supply: "Supply") -> None:
        """
        Buy a card from the supply and add to player's discard pile.

        Assert that player has sufficient money and buys to gain the card

        """
        assert isinstance(card, Card)
        if card.cost > self.state.money:
            raise InsufficientMoney(
                f"{self.player_id}: Not enough money to buy {card.name}"
            )
        if self.state.buys < 1:
            raise InsufficientBuys(
                f"{self.player_id}: Not enough buys to buy {card.name}"
            )
        try:
            supply.gain_card(card)
        except EmptyPile as e:
            raise e
        self.state.money -= card.cost
        self.state.buys -= 1
        self.discard_pile.add(card)
        logger.info(f"{self} buys {card}")

    def gain(
        self, card: Card, supply: "Supply", destination: AbstractDeck = None
    ) -> None:
        """
        Gain a card from the supply and add to destination

        Defaults to adding the card to the player's discard pile

        """
        if destination is None:
            destination = self.discard_pile

        gain_card = supply.gain_card(card)
        destination.add(gain_card)

    def trash(self, target_card: Card, trash: "Trash") -> None:
        """
        Move card from player's hand to the trash

        """
        for card in self.hand.cards:
            if card == target_card:
                trash.add(self.hand.remove(card))
                break

    def start_turn(self) -> None:
        self.turns += 1
        self.state.actions = 1
        self.state.money = 0
        self.state.buys = 1

    def get_all_cards(self) -> List[Card]:
        """
        Get a list of all the cards the player has in their possesion

        """

        all_cards = (
            self.deck.cards
            + self.discard_pile.cards
            + self.playmat.cards
            + self.hand.cards
        )
        return all_cards

    def get_card_count(self, card: Card) -> int:
        """
        Get count of a specific card in player's whole deck

        """

        return self.get_all_cards().count(card)

    def get_victory_points(self) -> int:
        total_vp: int = 0
        for card in self.get_all_cards():
            if "Victory" in card.type or "Curse" in card.type:
                total_vp += card.score(self)
        return total_vp

    def get_treasure_money(self) -> int:
        total_money: int = 0
        for card in self.get_all_cards():
            if "Treasure" in card.type:
                total_money += card.money
        return total_money

    def get_action_money(self) -> int:
        total_money: int = 0
        for card in self.get_all_cards():
            if "Action" in card.type:
                total_money += card.money
        return total_money

    def get_deck_money(self) -> int:
        treasure_money = self.get_treasure_money()
        action_money = self.get_action_money()
        return treasure_money + action_money


class Supply:
    """
    Collection of card piles that make up the game's supply

    """

    def __init__(self, piles: List[Pile] = None):
        if piles:
            self.piles = piles
        else:
            self.piles = []

    def __repr__(self):
        return str(self.avaliable_cards())

    def __len__(self):
        return len(self.piles)

    def gain_card(self, card: Card) -> Optional[Card]:
        """
        Gain a card from the supply

        """
        for pile in self.piles:
            if card.name == pile.name:
                try:
                    return pile.remove(card)

                except EmptyPile as e:
                    raise e

        raise PileNotFound(f"{card} not found in the supply")

    def return_card(self, card: Card):
        """
        Return a card to the supply

        """
        for pile in self.piles:
            if card.name == pile.name:
                pile.add(card)

    def avaliable_cards(self) -> List[Card]:
        """
        Returns a list containing a single card from each non-empty pile in the supply

        """
        cards = [pile.cards[0] for pile in self.piles if pile]
        return cards

    def num_empty_piles(self) -> int:
        """
        Returns the number of empty piles in the supply

        """
        empty_piles: int = 0
        for pile in self.piles:
            if len(pile) == 0:
                empty_piles += 1
        return empty_piles

    def pile_length(self, pile_name: str) -> int:
        for pile in self.piles:
            if pile.name == pile_name:
                return len(pile)
        raise PileNotFound(f"{pile_name} pile is not valid")

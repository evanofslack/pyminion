from typing import List, Optional, Tuple
import random
from dataclasses import dataclass

from pyminion.exceptions import (
    InsufficientMoney,
    InsufficientBuys,
    PileNotFound,
    EmptyPile,
    InvalidCardPlay,
    InvalidPlayerCount,
    InvalidGameSetup,
)
import copy


class Card:

    """
    Base class representing a dominion card

    """

    def __init__(self, name: str, cost: int, type: str):
        self.name = name
        self.cost = cost
        self.type = type

    def __repr__(self):
        return f"{self.name} ({self.type})"


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
        return f"{type(self).__name__} {[card.name for card in self.cards]}"

    def __len__(self):
        return len(self.cards)

    def add(self, card: Card) -> Card:
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
            raise EmptyPile
        self.cards.remove(card)
        return card


class Playmat(AbstractDeck):
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
    Collection of card piles associated with each player

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

    def start_turn(self):
        self.turns += 1
        self.state.actions = 1
        self.state.money = 0
        self.state.buys = 1

    def draw(self, num_cards: int = 1, destination: AbstractDeck = None) -> None:
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
                destination.add(self.deck.draw())
            else:
                destination.add(self.deck.draw())

    def discard(self, target_card: Card) -> None:
        for card in self.hand.cards:
            if card == target_card:
                self.discard_pile.add(self.hand.remove(card))
                return

    def play(self, target_card: Card, game: "Game", generic_play: bool = True) -> None:
        for card in self.hand.cards:
            try:
                if card == target_card:
                    card.play(player=self, game=game, generic_play=generic_play)
                    return
            except:
                raise InvalidCardPlay(f"Invalid play, {target_card} has no play method")
        raise InvalidCardPlay(f"Invalid play, {target_card} not in hand")

    def exact_play(self, card: Card, game: "Game", generic_play: bool = True) -> None:
        try:
            card.play(player=self, game=game, generic_play=generic_play)
            # return
        except:
            raise InvalidCardPlay(f"Invalid play, cannot play {card}")

    def autoplay_treasures(self) -> None:
        i = 0  # Pythonic way to pop in loop?
        while i < len(self.hand):
            if self.hand.cards[i].type == "Treasure":
                self.hand.cards[i].play(self)
            else:
                i += 1

    def buy(self, card: Card, supply: "Supply") -> None:
        assert isinstance(card, Card)
        if card.cost > self.state.money:
            raise InsufficientMoney(
                f"{self.player_id}: Not enough money to buy {card.name}"
            )
        if self.state.buys < 1:
            raise InsufficientBuys(
                f"{self.player_id}: Not enough buys to buy {card.name}"
            )
        self.state.money -= card.cost
        self.state.buys -= 1
        self.discard_pile.add(card)
        supply.gain_card(card)

    def gain(
        self, card: Card, supply: "Supply", destination: AbstractDeck = None
    ) -> None:
        if destination is None:
            destination = self.discard_pile

        gain_card = supply.gain_card(card)
        destination.add(gain_card)

    def cleanup(self) -> None:
        self.discard_pile.cards += self.hand.cards
        self.discard_pile.cards += self.playmat.cards
        self.hand.cards = []
        self.playmat.cards = []
        self.draw(5)

    def trash(self, target_card: Card, trash: "Trash") -> None:
        for card in self.hand.cards:
            if card == target_card:
                trash.add(self.hand.remove(card))
                break

    def get_all_cards(self) -> List[Card]:
        return (
            self.deck.cards
            + self.discard_pile.cards
            + self.playmat.cards
            + self.hand.cards
        )

    def get_victory_points(self):
        total_vp: int = 0
        for card in self.get_all_cards():
            if card.type == "Victory" or card.type == "Curse":
                total_vp += card.score(self)
        return total_vp


class Supply:
    """
    Collection of card piles that make up the game's supply

    """

    def __init__(self, piles: List[Pile] = None):
        if piles:
            self.piles = piles
        else:
            self.piles = []

    def __len__(self):
        return len(self.piles)

    def gain_card(self, card: Card) -> Optional[Card]:
        for pile in self.piles:
            if card.name == pile.name:
                try:
                    return pile.remove(card)
                except EmptyPile:
                    print("Pile is empty, you cannot gain that card")
                    return None

        raise PileNotFound

    def return_card(self, card: Card):
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


class Trash(AbstractDeck):
    def __init__(self, cards: List[Card] = None):
        super().__init__(cards)


class Game:
    def __init__(
        self,
        players: List[Player],
        expansions: List[List[Card]],
        basic_cards: List[Card] = None,
        start_cards: List[Card] = None,
        kingdom_cards: List[Card] = None,
    ):
        if len(players) < 1:
            raise InvalidPlayerCount("Game must have at least one player")
        if len(players) > 4:
            raise InvalidPlayerCount("Game can have at most four players")
        self.players = players
        self.expansions = expansions
        self.basic_cards = basic_cards
        self.start_cards = start_cards
        self.kingdom_cards = kingdom_cards
        self.trash = Trash()

    def _create_supply(self) -> Supply:
        """
        Create the supply. The supply consists of two parts.

        1.) The basic card piles avaliable in every game of dominion
        2.) The kingdom cards, a set of 10 piles of cards that change from game to game

        Returns a fully populated supply

        """

        if len(self.players) == 1:
            VICTORY_LENGTH = 5
            CURSE_LENGTH = 10
            COPPER_LENGTH = 53

        if len(self.players) == 2:
            VICTORY_LENGTH = 8
            CURSE_LENGTH = 10
            COPPER_LENGTH = 46

        elif len(self.players) == 3:
            VICTORY_LENGTH = 12
            CURSE_LENGTH = 20
            COPPER_LENGTH = 39

        elif len(self.players) == 4:
            VICTORY_LENGTH = 12
            CURSE_LENGTH = 30
            COPPER_LENGTH = 32

        SILVER_LENGTH = 40
        GOLD_LENGTH = 30

        basic_piles = []
        for card in self.basic_cards:
            if card.name == "Copper":
                basic_piles.append(Pile([card] * COPPER_LENGTH))
            elif card.name == "Silver":
                basic_piles.append(Pile([card] * SILVER_LENGTH))
            elif card.name == "Gold":
                basic_piles.append(Pile([card] * GOLD_LENGTH))
            elif card.type == "Victory":
                basic_piles.append(Pile([card] * VICTORY_LENGTH))
            elif card.name == "Curse":
                basic_piles.append(Pile([card] * CURSE_LENGTH))
            else:
                raise InvalidGameSetup(f"Invalid basic card: {card}")

        PILE_LENGTH: int = 10
        KINGDOM_PILES: int = 10

        # If user chooses kingdom cards, put them in the supply
        chosen_cards = len(self.kingdom_cards) if self.kingdom_cards else 0
        chosen_piles = (
            [Pile([card] * PILE_LENGTH) for card in self.kingdom_cards]
            if chosen_cards
            else []
        )
        # The rest of the supply is random cards
        kingdom_options = [card for expansion in self.expansions for card in expansion]
        if chosen_cards:
            for card in self.kingdom_cards:
                kingdom_options.remove(card)  # Do not duplicate any user chosen cards
        kingdom_ten = random.sample(kingdom_options, KINGDOM_PILES - chosen_cards)
        random_piles = [Pile([card] * PILE_LENGTH) for card in kingdom_ten]

        return Supply(basic_piles + chosen_piles + random_piles)

    def start(self) -> None:
        self.supply = self._create_supply()
        for player in self.players:
            player.deck = Deck(copy.deepcopy(self.start_cards))
            player.deck.shuffle()
            player.draw(5)

    def is_over(self) -> bool:
        """
        The game is over if any 3 supply piles are empty or
        if the province pile is empty.

        Returns True if the game is over

        """
        empty_piles: int = 0
        for pile in self.supply.piles:
            if pile.name == "Province" and len(pile) == 0:
                return True
            if len(pile) == 0:
                empty_piles += 1
            if empty_piles >= 3:
                return True

    def get_winner(self) -> Optional[Player]:
        """
        The player with the most victory points wins.
        If the highest scores are tied at the end of the game,
        the tied player who has had the fewest turns wins the game.
        If the tied players have had the same number of turns, they tie.

        Returns the winning player or None if there is a tie.

        """
        if len(self.players) == 1:
            return self.players[0]

        high_score = self.players[0].get_victory_points()
        winner = self.players[0]
        tie = False

        for player in self.players[1:]:
            score = player.get_victory_points()
            if score > high_score:
                high_score = score
                winner = player

            elif score == high_score:
                if player.turns < winner.turns:
                    winner = player
                    tie = False
                elif player.turns == winner.turns:
                    tie = True
        return None if tie else winner  # todo return just the players that tie

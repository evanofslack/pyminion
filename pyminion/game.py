from pyminion.models.core import Card, Supply, Trash, Pile, Deck, Player
from pyminion.exceptions import InvalidPlayerCount, InvalidGameSetup

from typing import List, Optional
import random
import copy


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
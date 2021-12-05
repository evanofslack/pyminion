import copy
import logging
import random
from typing import List, Optional

from pyminion.core import Card, Deck, DeckCounter, Pile, Supply, Trash
from pyminion.exceptions import InvalidGameSetup, InvalidPlayerCount
from pyminion.expansions.base import (
    copper,
    curse,
    duchy,
    estate,
    gold,
    province,
    silver,
)
from pyminion.players import Player

logger = logging.getLogger()


class Game:
    """
    Core class the emulates a game of Dominion

    Attributes:
        players: List of players in the game.
        expansions: List expansions (and their cards) eligible to be used in the game's supply.
        kingdom_cards: Specify any specific cards to be used in the supply.
        start_deck: List of cards each player will start the game with. Default = [7 Coppers + 3 Estates].
        random_order: If True, scrambles the order of players (to offset first player advantage).
        use_logger: If True, logs the game to a log file.
        log_file_name: Name of the file to be logged to. Default = "game.log"

    """

    def __init__(
        self,
        players: List[Player],
        expansions: List[List[Card]],
        kingdom_cards: List[Card] = None,
        start_deck: List[Card] = None,
        random_order: bool = True,
        use_logger: bool = True,
        log_file_name: str = "game.log",
    ):

        if len(players) < 1:
            raise InvalidPlayerCount("Game must have at least one player")
        if len(players) > 4:
            raise InvalidPlayerCount("Game can have at most four players")
        self.players = players
        self.expansions = expansions
        self.kingdom_cards = kingdom_cards
        self.start_deck = start_deck
        self.random_order = random_order
        self.trash = Trash()

        if use_logger:
            # Set up a handler that dumps the log to a file
            f_handler = logging.FileHandler(log_file_name, mode="w")
            f_handler.setLevel(logging.INFO)
            f_format = logging.Formatter("%(message)s")
            f_handler.setFormatter(f_format)
            logger.addHandler(f_handler)

    def _create_basic_piles(self) -> List[Card]:
        """
        Create the basic piles that are applicable to almost all games of Dominion.

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

        basic_cards = [
            copper,
            silver,
            gold,
            estate,
            duchy,
            province,
            curse,
        ]

        basic_piles = []
        for card in basic_cards:
            if card.name == "Copper":
                basic_piles.append(Pile([card] * COPPER_LENGTH))
            elif card.name == "Silver":
                basic_piles.append(Pile([card] * SILVER_LENGTH))
            elif card.name == "Gold":
                basic_piles.append(Pile([card] * GOLD_LENGTH))
            elif "Victory" in card.type:
                basic_piles.append(Pile([card] * VICTORY_LENGTH))
            elif card.name == "Curse":
                basic_piles.append(Pile([card] * CURSE_LENGTH))

        return basic_piles

    def _create_kingdom_piles(self) -> List[Card]:
        """
        Create the kingdom piles that vary from kingdom to kingdom. This should be 10 piles each with 10 cards.

        """
        PILE_LENGTH: int = 10
        KINGDOM_PILES: int = 10

        # All avaliable cards from chosen expansions
        kingdom_options = [card for expansion in self.expansions for card in expansion]

        # If user chooses kingdom cards, put them in the supply
        if self.kingdom_cards:
            if invalid_cards := [
                card for card in self.kingdom_cards if card not in kingdom_options
            ]:
                raise InvalidGameSetup(
                    f"Invalid game setup: {invalid_cards} not in provided expansions"
                )
            chosen_cards = len(self.kingdom_cards)

        else:
            chosen_cards = 0

        chosen_piles = (
            [Pile([card] * PILE_LENGTH) for card in self.kingdom_cards]
            if chosen_cards
            else []
        )
        # The rest of the supply is random cards
        if chosen_cards:
            for card in self.kingdom_cards:
                kingdom_options.remove(card)  # Do not duplicate any user chosen cards
        kingdom_ten = random.sample(kingdom_options, KINGDOM_PILES - chosen_cards)
        random_piles = [Pile([card] * PILE_LENGTH) for card in kingdom_ten]

        return chosen_piles + random_piles

    def _create_supply(self) -> Supply:
        """
        Create a supply consisting of the basic cards avaliable in every kingdom as well as the kingdom specific cards.

        """

        basic_piles = self._create_basic_piles()
        kingdom_piles = self._create_kingdom_piles()
        return Supply(basic_piles + kingdom_piles)

    def start(self) -> None:
        logger.info("\nStarting Game...\n")

        self.supply = self._create_supply()
        logger.info(f"Supply: \n{self.supply}")

        if self.random_order:
            random.shuffle(self.players)
        if not self.start_deck:
            self.start_deck = [copper] * 7 + [estate] * 3

        for player in self.players:
            player.reset()
            player.discard_pile = Deck(copy.deepcopy(self.start_deck))
            logger.info(f"\n{player} starts with {player.discard_pile}")
            player.draw(5)

    def is_over(self) -> bool:
        """
        The game is over if any 3 supply piles are empty or
        if the province pile is empty.

        Return True if the game is over

        """
        empty_piles: int = 0
        for pile in self.supply.piles:
            if pile.name == "Province" and len(pile) == 0:
                return True
            if len(pile) == 0:
                empty_piles += 1
        if empty_piles >= 3:
            return True

    def play(self):
        self.start()
        while True:
            for player in self.players:
                player.take_turn(self)
                if self.is_over():
                    self.get_stats()
                    return

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
        return None if tie else winner

    def get_stats(self):
        if winner := self.get_winner():
            logger.info(f"\n{winner} won in {winner.turns} turns!")
        else:
            logger.info(f"\nGame ended in a tie after {self.players[0].turns} turns")

        for player in self.players:
            logger.info(
                f"\n\nPlayer: {player} \nScore: {player.get_victory_points()} \nDeck: {DeckCounter(player.get_all_cards())}"
            )

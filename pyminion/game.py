import copy
import logging
import random
from typing import List, Optional

from pyminion.core import Card, Deck, DeckCounter, Pile, Supply, Trash
from pyminion.exceptions import InvalidGameSetup, InvalidPlayerCount
from pyminion.expansions.base import (copper, curse, duchy, estate, gold,
                                      province, silver)
from pyminion.players import Player
from pyminion.result import GameOutcome, GameResult, PlayerSummary

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
        log_stdout: If True, logs game to stdout.
        log_file: If True, logs game to log file.
        log_file_name: Name of the file to be logged to. Default = "game.log"

    """

    def __init__(
        self,
        players: List[Player],
        expansions: List[List[Card]],
        kingdom_cards: Optional[List[Card]] = None,
        start_deck: Optional[List[Card]] = None,
        random_order: bool = True,
        log_stdout: bool = True,
        log_file: bool = False,
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

        if log_stdout:
            # Set up a handler that logs to stdout
            c_handler = logging.StreamHandler()
            c_handler.setLevel(logging.INFO)
            c_format = logging.Formatter("%(message)s")
            c_handler.setFormatter(c_format)
            logger.addHandler(c_handler)

        if log_file:
            # Set up a handler that dumps the log to a file
            f_handler = logging.FileHandler(log_file_name, mode="w")
            f_handler.setLevel(logging.INFO)
            f_format = logging.Formatter("%(message)s")
            f_handler.setFormatter(f_format)
            logger.addHandler(f_handler)

    def _create_basic_piles(self) -> List[Pile]:
        """
        Create the basic piles that are applicable to almost all games of Dominion.

        """

        if len(self.players) == 1:
            VICTORY_LENGTH = 5
            CURSE_LENGTH = 10
            COPPER_LENGTH = 53

        elif len(self.players) == 2:
            VICTORY_LENGTH = 8
            CURSE_LENGTH = 10
            COPPER_LENGTH = 46

        elif len(self.players) == 3:
            VICTORY_LENGTH = 12
            CURSE_LENGTH = 20
            COPPER_LENGTH = 39

        else:
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

    def _create_kingdom_piles(self) -> List[Pile]:
        """
        Create the kingdom piles that vary from kingdom to kingdom.
        This should be 10 piles each with 10 cards.

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
        Create a supply consisting of basic cards
        avaliable in every kingdom as well
        as the kingdom specific cards.

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

            # are provinces empty?
            if pile.name == "Province" and len(pile) == 0:
                return True

            # are three piles empty?
            if len(pile) == 0:
                empty_piles += 1
                if empty_piles >= 3:
                    return True

        return False

    def play(self) -> GameResult:
        self.start()
        while True:
            for player in self.players:
                player.take_turn(self)
                if self.is_over():
                    result = self.summerize_game()
                    logging.info(f"\n{result}")
                    return result

    def get_winners(self) -> List[Player]:
        """
        The player with the most victory points wins.
        If the highest scores are tied at the end of the game,
        the tied player who has had the fewest turns wins the game.
        If the tied players have had the same number of turns, they tie.

        Returns a list of players. If there is a single player in
        the list, that is the sole winner. If there are multiple players
        in the list, they are have tied for first.

        """
        # if one player only, they win by default
        if len(self.players) == 1:
            return [self.players[0]]

        # temporarily set first player as winner
        high_score = self.players[0].get_victory_points()
        winners = [self.players[0]]

        # iterate the rest of the players in the game
        for player in self.players[1:]:
            score = player.get_victory_points()

            # if this player scored more,
            # mark them as winner and high score
            if score > high_score:
                high_score = score
                winners = [player]

            # if scores are equal
            elif score == high_score:

                # players tie if number of turns is equal
                if player.turns == winners[0].turns:
                    winners.append(player)

                # otherwise, player with fewer turns wins
                elif player.turns < winners[0].turns:
                    winners = [player]

                # note
                # we can compare to just the first player in winners,
                # because if there were multiple players in winners
                # they would have equal score and turns

        return winners

    def summerize_game(self) -> GameResult:
        """
        Called at the end of the game,
        this creates a summary of the game

        """

        player_summaries = []
        winners = self.get_winners()

        for order, player in enumerate(self.players):

            # player won
            if player in winners and len(winners) == 1:
                result = GameOutcome.win

            # player tied
            elif player in winners:
                result = GameOutcome.tie

            # player lost
            else:
                result = GameOutcome.loss

            summary = PlayerSummary(
                player=player,
                result=result,
                score=player.get_victory_points(),
                turns=player.turns,
                shuffles=player.shuffles,
                turn_order=order + 1,
                deck=DeckCounter(player.get_all_cards()),
            )
            player_summaries.append(summary)

        game_result = GameResult(
            game=self,
            turns=winners[0].turns,
            winners=winners,
            player_summaries=player_summaries,
        )
        return game_result

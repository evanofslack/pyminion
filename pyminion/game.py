from enum import IntEnum, unique
import logging
import random
from typing import Iterator

from pyminion.core import Card, DeckCounter, DiscardPile, Pile, Supply, Trash
from pyminion.effects import EffectRegistry
from pyminion.exceptions import InvalidGameSetup, InvalidPlayerCount
from pyminion.expansions.base import (copper, curse, duchy, estate, gold,
                                      province, silver)
from pyminion.expansions.alchemy import potion
from pyminion.player import Player
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

    @unique
    class Phase(IntEnum):
        Action = 0
        Buy = 1
        CleanUp = 2

    def __init__(
        self,
        players: list[Player],
        expansions: list[list[Card]],
        kingdom_cards: list[Card]|None = None,
        start_deck: list[Card]|None = None,
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
        self.current_player = self.players[0]
        self.expansions = expansions
        self.kingdom_cards = [] if kingdom_cards is None else kingdom_cards
        self.all_game_cards: list[Card] = []
        self.card_cost_reduction = 0
        self.start_deck = start_deck
        self.random_order = random_order
        self.trash = Trash()
        self.current_phase: Game.Phase = Game.Phase.Action

        self.effect_registry = EffectRegistry()

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

    def _create_basic_score_piles(self) -> list[Pile]:
        """
        Create the basic victory and curse piles that are applicable to almost all games of Dominion.

        """

        basic_cards: list[Card] = [
            estate,
            duchy,
            province,
            curse,
        ]

        basic_piles = [
            Pile([card] * card.get_pile_starting_count(self))
            for card in basic_cards
        ]

        return basic_piles

    def _create_basic_treasure_piles(self, kingdom_piles: list[Pile]) -> list[Pile]:
        """
        Create the basic treasure piles that are applicable to almost all games of Dominion.

        """

        basic_cards: list[Card] = [
            copper,
            silver,
            gold,
        ]

        for pile in kingdom_piles:
            if pile.cards[0].base_cost.potions > 0:
                basic_cards.insert(0, potion)
                break

        basic_piles = [
            Pile([card] * card.get_pile_starting_count(self))
            for card in basic_cards
        ]

        return basic_piles

    def _create_kingdom_piles(self) -> list[Pile]:
        """
        Create the kingdom piles that vary from kingdom to kingdom.
        This should be 10 piles each with 10 cards.

        """
        KINGDOM_PILES: int = 10

        # All available cards from chosen expansions
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
            [Pile([card] * card.get_pile_starting_count(self)) for card in self.kingdom_cards]
            if chosen_cards
            else []
        )
        # The rest of the supply is random cards
        if chosen_cards:
            for card in self.kingdom_cards:
                kingdom_options.remove(card)  # Do not duplicate any user chosen cards
        kingdom_ten = random.sample(kingdom_options, KINGDOM_PILES - chosen_cards)
        random_piles = [Pile([card] * card.get_pile_starting_count(self)) for card in kingdom_ten]

        piles = chosen_piles + random_piles

        def pile_sort(pile: Pile) -> tuple[int, int, str]:
            cost = pile.cards[0].base_cost
            return (cost.money, cost.potions, pile.name)

        # sort piles by cost and name
        piles.sort(key=pile_sort)

        return piles

    def _create_supply(self) -> Supply:
        """
        Create a supply consisting of basic cards
        available in every kingdom as well
        as the kingdom specific cards.

        """

        kingdom_piles = self._create_kingdom_piles()
        basic_score_piles = self._create_basic_score_piles()
        basic_treasure_piles = self._create_basic_treasure_piles(kingdom_piles)
        all_piles = basic_score_piles + basic_treasure_piles + kingdom_piles
        self.all_game_cards = [pile.cards[0] for pile in all_piles]
        return Supply(basic_score_piles, basic_treasure_piles, kingdom_piles)

    def start(self) -> None:
        logger.info("\nStarting Game...\n")

        self.trash.cards.clear()
        self.effect_registry.reset()

        self.supply = self._create_supply()
        logger.info(self.supply.get_pretty_string(self.players[0], self))

        for card in self.all_game_cards:
            card.set_up(self)

        if self.random_order:
            random.shuffle(self.players)
        if not self.start_deck:
            self.start_deck = []
            for _ in range(7):
                self.start_deck.append(copper)
            for _ in range(3):
                self.start_deck.append(estate)

        for player in self.players:
            player.reset()
            player.hand.on_add = lambda card, player=player: self.effect_registry.on_hand_add(player, card, self)
            player.hand.on_remove = lambda card, player=player: self.effect_registry.on_hand_remove(player, card, self)
            player.deck.on_shuffle = lambda player=player: self.effect_registry.on_shuffle(player, self)
            player.discard_pile = DiscardPile(self.start_deck[:])
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

    def play_turn(self, player: Player) -> None:
        # if player played Possession while being possessed, take the extra turn
        # before their main turn
        if player.take_possession_turn:
            player.possess(self)
            self.card_cost_reduction = 0
            if self.is_over():
                return

        extra_turn_count = 0
        take_turn = True
        while take_turn:
            player.take_turn(self, is_extra_turn=extra_turn_count > 0)

            # reset card cost reduction
            self.card_cost_reduction = 0

            if self.is_over():
                return

            extra_turn_count += 1
            take_turn = player.take_extra_turn and extra_turn_count < 2

        # if player just played Possession, take the extra turn after their main turn
        if player.take_possession_turn:
            player.possess(self)
            self.card_cost_reduction = 0
            if self.is_over():
                return

        # reset extra turn flags
        player.take_extra_turn = False

    def play(self) -> GameResult:
        self.start()
        while True:
            for player in self.players:
                self.current_player = player
                self.play_turn(player)

                if self.is_over():
                    result = self.summarize_game()
                    logging.info(f"\n{result}")
                    return result

    def get_left_player(self, player: Player) -> Player:
        """
        Returns the player to the left of the given player.

        """
        player_idx = self.players.index(player)
        left_player_idx = (player_idx + 1) % len(self.players)
        left_player = self.players[left_player_idx]
        return left_player

    def get_right_player(self, player: Player) -> Player:
        """
        Returns the player to the right of the given player.

        """
        player_idx = self.players.index(player)
        right_player_idx = (player_idx - 1) % len(self.players)
        right_player = self.players[right_player_idx]
        return right_player

    def get_opponents(self, player: Player) -> Iterator[Player]:
        """
        Iterate over the given player's opponents in turn order.

        """
        start_idx = self.players.index(player) + 1
        num_players = len(self.players)
        for i in range(num_players - 1):
            idx = (start_idx + i) % num_players
            opponent = self.players[idx]
            yield opponent

    def distribute_curses(self, attacking_player: Player, attack_card: Card) -> None:
        """
        Distribute curses in turn order.

        """
        for opponent in self.get_opponents(attacking_player):
            if opponent.is_attacked(attacking_player, attack_card, self):
                # attempt to gain a curse. if curse pile is empty, proceed
                opponent.try_gain(curse, self)

    def get_winners(self) -> list[Player]:
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

    def summarize_game(self) -> GameResult:
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

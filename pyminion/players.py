import logging
import sys
from collections import Counter
from contextlib import contextmanager
from io import StringIO
from typing import List, Optional

from pyminion.decisions import single_card_decision, validate_input
from pyminion.exceptions import (
    InsufficientMoney,
    InvalidBinaryInput,
    InvalidCardPlay,
    InvalidMultiCardInput,
    InvalidSingleCardInput,
)
from pyminion.game import Game
from pyminion.models.core import Card, Deck, Player

logger = logging.getLogger()


class Human(Player):
    """
    Human player can make choices as to which cards
    to play and buy in real time through the terminal

    """

    def __init__(
        self,
        deck: Deck = None,
        player_id: str = "human",
    ):
        super().__init__(deck=deck, player_id=player_id)

    @staticmethod
    @validate_input(exceptions=InvalidBinaryInput)
    def binary_decision(prompt: str) -> bool:
        """
        Get user response to a binary "yes" or "no" question.

        Raise exception is input is anything other than 'y' or 'n'

        """
        decision = input(prompt)
        if decision == "y" or decision == "yes":
            return True
        elif decision == "n" or decision == "no":
            return False
        else:
            raise InvalidBinaryInput("Invalid response, valid choices are 'y' or 'n'")

    @staticmethod
    @validate_input(exceptions=InvalidSingleCardInput)
    def single_card_decision(
        prompt: str,
        valid_cards: List[Card],
    ) -> Optional[Card]:
        """
        Get user response when given the option to select one card

        Raise exception if user provided selection is not valid.

        """
        card_input = input(prompt)
        if not card_input:
            return None

        for valid_card in valid_cards:
            if card_input.casefold() == valid_card.name.casefold():
                return valid_card

        raise InvalidSingleCardInput(
            f"Invalid input, {card_input} is not a valid selection"
        )

    @staticmethod
    @validate_input(exceptions=InvalidMultiCardInput)
    def multiple_card_decision(
        prompt: str,
        valid_cards: List[Card],
    ) -> Optional[List[Card]]:
        """
        Get user response when given the option to select multiple cards

        Raise exception if user provided selection is not valid.

        """
        card_input = input(prompt)
        if not card_input:
            return
        card_strings = [x.strip() for x in card_input.split(",")]
        selected_cards = []
        for card_string in card_strings:
            for valid_card in valid_cards:
                # compare strings regardless of case i.e. 'Copper' = 'copper'
                if card_string.casefold() == valid_card.name.casefold():
                    selected_cards.append(valid_card)
                    break

        if not selected_cards:
            raise InvalidMultiCardInput(
                f"Invalid input, {card_strings[0]} is not a valid card"
            )

        selected_count = Counter(selected_cards)
        valid_count = Counter(valid_cards)

        for element in selected_count:
            if selected_count[element] > valid_count[element]:
                raise InvalidMultiCardInput(
                    f"Invalid input, attempted to select too many copies of {element}"
                )
        return selected_cards

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        for card in self.hand.cards:
            if card.name == "Moat":
                block = self.binary_decision(
                    prompt=f"Would you like to block {player.player_id}'s {attack_card} with your Moat? y/n: "
                )
                return not block
        return True

    def start_action_phase(self, game: Game):
        while self.state.actions:

            viable_actions = [card for card in self.hand.cards if "Action" in card.type]
            if not viable_actions:
                return

            @validate_input(exceptions=InvalidSingleCardInput)
            def choose_action(game: Game) -> bool:
                logger.info(f"Hand: {self.hand}")
                card = single_card_decision(
                    prompt="Choose an action card to play: ",
                    valid_cards=viable_actions,
                )
                if not card:
                    return False
                self.play(card, game)
                return True

            if not choose_action(game):
                return

    def start_treasure_phase(self, game: Game):
        viable_treasures = [card for card in self.hand.cards if "Treasure" in card.type]
        while viable_treasures:

            @validate_input(exceptions=InvalidSingleCardInput)
            def choose_treasure(game: Game):
                logger.info(f"Hand: {self.hand}")
                card = single_card_decision(
                    prompt="Choose an treasure card to play or 'all' to autoplay treasures: ",
                    valid_cards=viable_treasures,
                    valid_mixin="all",
                )
                if not card:
                    return False
                if card == "all":
                    i = 0
                    while i < len(viable_treasures):
                        self.exact_play(viable_treasures[i], game)
                        viable_treasures.remove(viable_treasures[i])
                    return True
                self.exact_play(card, game)
                logger.info(f"{self.player_id} played {card}")
                viable_treasures.remove(card)
                return True

            if not choose_treasure(game):
                return

    def start_buy_phase(self, game: Game):
        while self.state.buys and self.state.money:
            logger.info(f"Money: {self.state.money}")
            logger.info(f"Buys: {self.state.buys}")

            @validate_input(exceptions=(InvalidSingleCardInput, InsufficientMoney))
            def choose_buy(game: Game) -> bool:
                card = single_card_decision(
                    prompt="Choose a card to buy: ",
                    valid_cards=game.supply.avaliable_cards(),
                )
                if not card:
                    return False
                self.buy(card, game.supply)
                logger.info(f"{self.player_id} bought {card}")
                return True

            if not choose_buy(game):
                return

    def start_cleanup_phase(self):
        self.discard_pile.cards += self.hand.cards
        self.discard_pile.cards += self.playmat.cards
        self.hand.cards = []
        self.playmat.cards = []
        self.draw(5)

    def take_turn(self, game: Game) -> None:
        logger.info(f"\nTurn {self.turns} - {self.player_id}")
        self.start_turn()
        self.start_action_phase(game)
        self.start_treasure_phase(game)
        self.start_buy_phase(game)
        self.start_cleanup_phase()


class Bot(Player):
    def __init__(
        self,
        deck: Deck = None,
        player_id: str = "bot",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def play(self, target_card: Card, game: "Game", generic_play: bool = True) -> None:
        for card in self.hand.cards:
            try:
                if card.name == target_card.name and "Action" in card.type:
                    card.play(player=self, game=game, generic_play=generic_play)
                    return
            except Exception as e:
                logging.error(e)
                raise InvalidCardPlay(
                    f"Invalid play, {target_card} could not be played"
                )
        raise InvalidCardPlay(f"Invalid play, {target_card} not in hand")

    def exact_play(self, card: Card, game: Game, generic_play: bool = True) -> None:
        try:
            if "Action" in card.type:
                card.play(player=self, game=game, generic_play=generic_play)
            elif "Treasure" in card.type:
                card.play(player=self, game=game)
        except:
            raise InvalidCardPlay(f"Invalid play, cannot play {card}")

    def binary_decision(self, card: Card) -> bool:
        if card.name == "Moneylender":
            return True
        else:
            return False

    def multiple_card_decision(
        self, card: Card, valid_cards: List[Card]
    ) -> Optional[List[Card]]:
        if card.name == "Cellar":
            return [
                card
                for card in valid_cards
                if card.name == "Estate" or card.name == "Copper"
            ]

    def single_card_decision(
        self, card: Card, valid_cards: List[Card]
    ) -> Optional[Card]:
        pass

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        for card in self.hand.cards:
            if card.name == "Moat":
                return False
        return True

    def start_action_phase(self, game: Game):
        viable_actions = [card for card in self.hand.cards if "Action" in card.type]
        logger.info(f"{self.player_id}'s hand: {self.hand}")
        while viable_actions and self.state.actions:

            # Add logic for playing action cards here

            return

    def start_treasure_phase(self, game: Game):
        viable_treasures = [card for card in self.hand.cards if "Treasure" in card.type]
        i = 0
        while i < len(viable_treasures):
            self.exact_play(viable_treasures[i], game)
            viable_treasures.remove(viable_treasures[i])
        logger.info(f"{self.player_id} has {self.state.money} money")

    def start_buy_phase(self, game: Game):
        while self.state.buys and self.state.money:

            # Add logic for buying cards here
            if self.buy:
                logger.info(f"{self.player_id} buys **card**")

            return

    def start_cleanup_phase(self):
        self.discard_pile.cards += self.hand.cards
        self.discard_pile.cards += self.playmat.cards
        self.hand.cards = []
        self.playmat.cards = []
        self.draw(5)

    def take_turn(self, game: Game) -> None:
        logger.info(f"\nTurn {self.turns} - {self.player_id}")
        self.start_turn()
        self.start_action_phase(game)
        self.start_treasure_phase(game)
        self.start_buy_phase(game)
        self.start_cleanup_phase()


@contextmanager
def input_redirect(input: str):
    """
    Outdated context manager to mock the input() calls required to make decisions

    """
    saved_input = sys.stdin
    sys.stdin = StringIO(input)
    yield
    sys.stdin = saved_input

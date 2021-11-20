import logging
from collections import Counter
from typing import List, Optional

from pyminion.decisions import (
    binary_decision,
    multiple_card_decision,
    single_card_decision,
    validate_input,
)
from pyminion.exceptions import (
    InsufficientMoney,
    InvalidBinaryInput,
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
        Wrap binary_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """
        return binary_decision(prompt=prompt)

    @staticmethod
    @validate_input(exceptions=InvalidSingleCardInput)
    def single_card_decision(
        prompt: str,
        valid_cards: List[Card],
    ) -> Optional[Card]:
        """
        Wrap single_card_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """

        return single_card_decision(prompt=prompt, valid_cards=valid_cards)

    @staticmethod
    @validate_input(exceptions=InvalidMultiCardInput)
    def multiple_card_decision(
        prompt: str,
        valid_cards: List[Card],
    ) -> Optional[List[Card]]:
        """
        Wrap multiple_card_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """
        return multiple_card_decision(prompt=prompt, valid_cards=valid_cards)

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        for card in self.hand.cards:
            if card.name == "Moat":
                block = self.binary_decision(
                    prompt=f"Would you like to block {player.player_id}'s {attack_card} with your Moat? y/n: "
                )
                return not block
        return True

    def start_action_phase(self, game: Game) -> None:
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

    def start_treasure_phase(self, game: Game) -> None:
        viable_treasures = [card for card in self.hand.cards if "Treasure" in card.type]
        while viable_treasures:

            @validate_input(exceptions=InvalidSingleCardInput)
            def choose_treasure(game: Game) -> bool:
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
                        logger.info(f"{self} played {viable_treasures}")
                    return True
                self.exact_play(card, game)
                logger.info(f"{self.player_id} played {card}")
                viable_treasures.remove(card)
                return True

            if not choose_treasure(game):
                return

    def start_buy_phase(self, game: Game) -> None:
        while self.state.buys:
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

    def start_cleanup_phase(self) -> None:
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

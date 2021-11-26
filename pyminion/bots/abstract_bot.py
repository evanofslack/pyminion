import logging
from typing import TYPE_CHECKING, Iterator, List, Optional

from pyminion.core import Card
from pyminion.exceptions import CardNotFound, EmptyPile
from pyminion.players import Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class AbstractBot(Player):
    """
    Abstract implementation of a Bot. Outlines methods that must be implemented for specific bot variations.

    """

    def __init__(
        self,
        player_id: str = "bot",
    ):
        super().__init__(player_id=player_id)

    def binary_resp():
        raise NotImplementedError

    def discard_resp():
        raise NotImplementedError

    def multiple_discard_resp():
        raise NotImplementedError

    def gain_resp():
        raise NotImplementedError

    def multiple_gain_resp():
        raise NotImplementedError

    def trash_resp():
        raise NotImplementedError

    def multiple_trash_resp():
        raise NotImplementedError

    def topdeck_resp():
        raise NotImplementedError

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        raise NotImplementedError

    def start_action_phase(self, game: "Game"):
        viable_actions = [card for card in self.hand.cards if "Action" in card.type]
        logger.info(f"{self.player_id}'s hand: {self.hand}")
        while viable_actions and self.state.actions:
            for card in self.action_priority(game=game):
                try:
                    self.play(target_card=card, game=game)
                except CardNotFound:
                    pass
            return

    def action_priority(self, game: "Game") -> Iterator[Card]:
        """
        Add logic for playing action cards through this method

        This function should be a generator where each call
        yields a desired card to play if conditions are met

        """
        raise NotImplementedError

    def start_treasure_phase(self, game: "Game"):
        viable_treasures = [card for card in self.hand.cards if "Treasure" in card.type]
        self.autoplay_treasures(viable_treasures=viable_treasures, game=game)

    def start_buy_phase(self, game: "Game"):

        logger.info(f"{self.player_id} has {self.state.money} money")

        while self.state.buys:
            for card in self.buy_priority(game=game):
                try:
                    self.buy(card, supply=game.supply)
                    break

                except EmptyPile:
                    pass
            else:
                logger.info(f"{self} buys nothing")
                return

    def buy_priority(self, game: "Game") -> Iterator[Card]:
        """
        Add logic for buy priority through this method

        This function should be a generator where each call
        yields a desired card to buy if conditions are met

        """
        raise NotImplementedError

    def take_turn(self, game: "Game") -> None:
        logger.info(f"\nTurn {self.turns} - {self.player_id}")
        self.start_turn()
        self.start_action_phase(game)
        self.start_treasure_phase(game)
        self.start_buy_phase(game)
        self.start_cleanup_phase()
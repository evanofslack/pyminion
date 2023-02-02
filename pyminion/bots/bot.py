import logging
from typing import TYPE_CHECKING, Iterator, List, Optional

from pyminion.core import Card
from pyminion.exceptions import CardNotFound, EmptyPile
from pyminion.players import Player

if TYPE_CHECKING:
    from pyminion.game import Game

logger = logging.getLogger()


class Bot(Player):
    """
    Abstract representation of Bot.

    Defines at a high level how a bot can play and buy cards.
    The intention is to inherit from this class to make concrete bot implementations.

    Does not implement any logic for playing or buying cards, as those functions
    (action_priority and buy_priority), are meant to be implemented when defining new bots.

    Does implement default responses to any decision the bot might have to make
    when playing a card or responding to an attack as to not crash the game.

    """

    def __init__(
        self,
        player_id: str = "bot",
    ):
        super().__init__(player_id=player_id)

    def action_priority(self, game: "Game") -> Iterator[Card]:
        """
        Add logic for playing action cards through this method

        This function should be a generator where each call
        yields a desired card to play if conditions are met

        """
        raise NotImplementedError

    def start_action_phase(self, game: "Game"):
        """
        Attempts to play cards from the action_priority queue if possible

        """
        viable_actions = [card for card in self.hand.cards if "Action" in card.type]
        logger.info(f"{self.player_id}'s hand: {self.hand}")
        while viable_actions and self.state.actions:
            for card in self.action_priority(game=game):
                try:
                    self.play(target_card=card, game=game)
                except CardNotFound:
                    pass
                if not self.state.actions:
                    return
            return

    def start_treasure_phase(self, game: "Game"):
        """
        At start of action phase, bot simply plays all of their treasures

        """
        viable_treasures = [card for card in self.hand.cards if "Treasure" in card.type]
        self.autoplay_treasures(viable_treasures=viable_treasures, game=game)

    def buy_priority(self, game: "Game") -> Iterator[Card]:
        """
        Add logic for buy priority through this method

        This function should be a generator where each call
        yields a desired card to buy if conditions are met

        """
        raise NotImplementedError

    def start_buy_phase(self, game: "Game"):
        """
        Attempts to buy cards from the buy_priority queue if possible

        """
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

    def take_turn(self, game: "Game") -> None:
        self.start_turn()
        logger.info(f"\nTurn {self.turns} - {self.player_id}")
        self.start_action_phase(game)
        self.start_treasure_phase(game)
        self.start_buy_phase(game)
        self.start_cleanup_phase()

    # DEFAULT RESPONSES
    # These methods can be implemented with specific game logic
    # when creating new bots. In this class, these methods just return
    # a valid response as to not crash the game.

    def binary_resp(
        self, game: "Game", card: Card, relevant_cards: Optional[List[Card]] = None
    ) -> bool:
        return True

    def discard_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def multiple_discard_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_discard: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:
        if required:
            return valid_cards[:num_discard]
        else:
            return None

    def gain_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def multiple_gain_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_gain: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:
        if required:
            return valid_cards[:num_gain]
        else:
            return None

    def trash_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def multiple_trash_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_trash: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:
        if required:
            return valid_cards[:num_trash]
        else:
            return None

    def topdeck_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def double_play_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        return True

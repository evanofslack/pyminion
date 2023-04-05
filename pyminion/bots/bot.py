import logging
from typing import TYPE_CHECKING, Iterator, List, Optional

from pyminion.core import CardType, Card
from pyminion.decider import Decider
from pyminion.exceptions import CardNotFound, EmptyPile
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class BotDecider:
    """
    Basic representation of Bot decision making.
    These methods can be implemented with specific game logic
    when creating new bots. In this class, these methods just return
    a valid response as to not crash the game.

    """

    def action_phase_decision(
        self,
        valid_actions: List["Card"],
        player: "Player",
        game: "Game",
    ) -> Optional["Card"]:
        pass

    def treasure_phase_decision(
        self,
        valid_treasures: List["Card"],
        player: "Player",
        game: "Game",
    ) -> List["Card"]:
        return valid_treasures

    def binary_decision(
        self,
        prompt: str,
        card: Card,
        player: "Player",
        game: "Game",
        relevant_cards: Optional[List[Card]] = None,
    ) -> bool:
        return True

    def discard_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_discard: int = 0,
        max_num_discard: int = -1,
    ) -> List["Card"]:
        return valid_cards[:min_num_discard]

    def trash_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_trash: int = 0,
        max_num_trash: int = -1,
    ) -> List["Card"]:
        return valid_cards[:min_num_trash]

    def gain_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_gain: int = 0,
        max_num_gain: int = -1,
    ) -> List["Card"]:
        return valid_cards[:min_num_gain]

    def topdeck_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_topdeck: int = 0,
        max_num_topdeck: int = -1,
    ) -> List["Card"]:
        return valid_cards[:min_num_topdeck]

    def multi_play_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        required: bool = True,
    ) -> Optional["Card"]:
        if required:
            return valid_cards[0]
        else:
            return None


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
        decider: Optional[Decider] = None,
        player_id: str = "bot",
    ):
        decider = decider if decider else BotDecider()
        super().__init__(decider=decider, player_id=player_id)

    # TODO: remove
    def action_priority(self, game: "Game") -> Iterator[Card]:
        """
        Add logic for playing action cards through this method

        This function should be a generator where each call
        yields a desired card to play if conditions are met

        """
        raise NotImplementedError

    # TODO: remove
    def start_treasure_phase(self, game: "Game"):
        """
        At start of action phase, bot simply plays all of their treasures

        """
        viable_treasures = [card for card in self.hand.cards if CardType.Treasure in card.type]
        self.autoplay_treasures(viable_treasures=viable_treasures, game=game)

    # TODO: remove
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

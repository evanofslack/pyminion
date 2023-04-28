from typing import TYPE_CHECKING, Iterator, List, Optional

from pyminion.core import Card
from pyminion.decider import Decider
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


class BotDecider:
    """
    Basic representation of Bot decision making.
    These methods can be implemented with specific game logic
    when creating new bots. In this class, these methods just return
    a valid response as to not crash the game.

    Does not implement any logic for playing or buying cards, as those functions
    (action_priority and buy_priority), are meant to be implemented when defining new bots.

    Does implement default responses to any decision the bot might have to make
    when playing a card or responding to an attack as to not crash the game.

    """

    def action_priority(self, player: "Player", game: "Game") -> Iterator[Card]:
        """
        Add logic for playing action cards through this method

        This function should be a generator where each call
        yields a desired card to play if conditions are met

        """
        raise NotImplementedError("action_priority is not implemented")

    def action_phase_decision(
        self,
        valid_actions: List["Card"],
        player: "Player",
        game: "Game",
    ) -> Optional["Card"]:
        for card in self.action_priority(player, game):
            if card in player.hand.cards:
                return card

        return None

    def treasure_phase_decision(
        self,
        valid_treasures: List["Card"],
        player: "Player",
        game: "Game",
    ) -> List["Card"]:
        return valid_treasures

    def buy_priority(self, player: "Player", game: "Game") -> Iterator[Card]:
        """
        Add logic for buy priority through this method

        This function should be a generator where each call
        yields a desired card to buy if conditions are met

        """
        raise NotImplementedError("buy_priority is not implemented")

    def buy_phase_decision(
        self,
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
    ) -> Optional["Card"]:
        for card in self.buy_priority(player, game):
            if game.supply.pile_length(card.name) > 0:
                return card

        return None

    def binary_decision(
        self,
        prompt: str,
        card: Card,
        player: "Player",
        game: "Game",
        relevant_cards: Optional[List[Card]] = None,
    ) -> bool:
        return True

    def multiple_option_decision(
        self,
        card: "Card",
        options: List[str],
        player: "Player",
        game: "Game",
        num_choices: int = 1,
        unique: bool = True,
    ) -> List[int]:
        return list(range(num_choices))

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

    def deck_position_decision(
        self,
        prompt: str,
        card: "Card",
        player: "Player",
        game: "Game",
        num_deck_cards: int,
    ) -> int:
        return num_deck_cards

    def reveal_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_reveal: int = 0,
        max_num_reveal: int = -1,
    ) -> List["Card"]:
        return valid_cards[:min_num_reveal]

    def pass_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_pass: int = 0,
        max_num_pass: int = -1,
    ) -> List["Card"]:
        return valid_cards[:min_num_pass]

    def name_card_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_name: int = 0,
        max_num_name: int = -1,
    ) -> List["Card"]:
        return valid_cards[:min_num_name]

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

    """

    def __init__(
        self,
        decider: Optional[Decider] = None,
        player_id: str = "bot",
    ):
        decider = decider if decider else BotDecider()
        super().__init__(decider=decider, player_id=player_id)

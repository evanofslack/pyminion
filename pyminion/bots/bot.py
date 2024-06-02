from typing import TYPE_CHECKING, Iterator, Sequence

from pyminion.core import Card
from pyminion.decider import Decider
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.effects import Effect
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
        valid_actions: list[Card],
        player: "Player",
        game: "Game",
    ) -> Card|None:
        for card in self.action_priority(player, game):
            if card in player.hand.cards:
                return card

        return None

    def treasure_phase_decision(
        self,
        valid_treasures: list[Card],
        player: "Player",
        game: "Game",
    ) -> list[Card]:
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
        valid_cards: list[Card],
        player: "Player",
        game: "Game",
    ) -> Card|None:
        for card in self.buy_priority(player, game):
            if game.supply.pile_length(card.name) > 0:
                return card

        return None

    def effects_order_decision(
        self,
        effects: Sequence["Effect"],
        player: "Player",
        game: "Game",
    ) -> int:
        return 0

    def binary_decision(
        self,
        prompt: str,
        card: Card,
        player: "Player",
        game: "Game",
        relevant_cards: list[Card]|None = None,
    ) -> bool:
        return True

    def multiple_option_decision(
        self,
        card: "Card",
        options: list[str],
        player: "Player",
        game: "Game",
        num_choices: int = 1,
        unique: bool = True,
    ) -> list[int]:
        return list(range(num_choices))

    def discard_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list[Card],
        player: "Player",
        game: "Game",
        min_num_discard: int = 0,
        max_num_discard: int = -1,
    ) -> list[Card]:
        return valid_cards[:min_num_discard]

    def trash_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list[Card],
        player: "Player",
        game: "Game",
        min_num_trash: int = 0,
        max_num_trash: int = -1,
    ) -> list[Card]:
        return valid_cards[:min_num_trash]

    def gain_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list[Card],
        player: "Player",
        game: "Game",
        min_num_gain: int = 0,
        max_num_gain: int = -1,
    ) -> list[Card]:
        return valid_cards[:min_num_gain]

    def topdeck_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list[Card],
        player: "Player",
        game: "Game",
        min_num_topdeck: int = 0,
        max_num_topdeck: int = -1,
    ) -> list[Card]:
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
        valid_cards: list[Card],
        player: "Player",
        game: "Game",
        min_num_reveal: int = 0,
        max_num_reveal: int = -1,
    ) -> list[Card]:
        return valid_cards[:min_num_reveal]

    def pass_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list[Card],
        player: "Player",
        game: "Game",
        min_num_pass: int = 0,
        max_num_pass: int = -1,
    ) -> list[Card]:
        return valid_cards[:min_num_pass]

    def name_card_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list[Card],
        player: "Player",
        game: "Game",
        min_num_name: int = 0,
        max_num_name: int = -1,
    ) -> list[Card]:
        return valid_cards[:min_num_name]

    def multi_play_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list[Card],
        player: "Player",
        game: "Game",
        required: bool = True,
    ) -> Card|None:
        if required:
            return valid_cards[0]
        else:
            return None

    def set_aside_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list[Card],
        player: "Player",
        game: "Game",
        min_num_set_aside: int = 0,
        max_num_set_aside: int = -1,
    ) -> list[Card]:
        return valid_cards[:min_num_set_aside]


class Bot(Player):
    """
    Abstract representation of Bot.

    """

    def __init__(
        self,
        decider: Decider|None = None,
        player_id: str = "bot",
    ):
        decider = decider if decider else BotDecider()
        super().__init__(decider=decider, player_id=player_id)

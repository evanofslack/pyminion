from typing import TYPE_CHECKING, Protocol, Sequence

if TYPE_CHECKING:
    from pyminion.core import Card, Player
    from pyminion.effects import Effect
    from pyminion.game import Game


class Decider(Protocol):
    """
    Interface for prompting a player for a decision.

    """

    def action_phase_decision(
        self,
        valid_actions: list["Card"],
        player: "Player",
        game: "Game",
    ) -> "Card|None":
        raise NotImplementedError("action_phase_decision is not implemented")

    def treasure_phase_decision(
        self,
        valid_treasures: list["Card"],
        player: "Player",
        game: "Game",
    ) -> list["Card"]:
        raise NotImplementedError("treasure_phase_decision is not implemented")

    def buy_phase_decision(
        self,
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
    ) -> "Card|None":
        raise NotImplementedError("buy_phase_decision is not implemented")

    def effects_order_decision(
        self,
        effects: Sequence["Effect"],
        player: "Player",
        game: "Game",
    ) -> int:
        raise NotImplementedError("effects_order_decision is not implemented")

    def binary_decision(
        self,
        prompt: str,
        card: "Card",
        player: "Player",
        game: "Game",
        relevant_cards: "list[Card]|None" = None,
    ) -> bool:
        raise NotImplementedError("binary_decision is not implemented")

    def multiple_option_decision(
        self,
        card: "Card",
        options: list[str],
        player: "Player",
        game: "Game",
        num_choices: int = 1,
        unique: bool = True,
    ) -> list[int]:
        raise NotImplementedError("multiple_option_decision is not implemented")

    def discard_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_discard: int = 0,
        max_num_discard: int = -1,
    ) -> list["Card"]:
        raise NotImplementedError("discard_decision is not implemented")

    def trash_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_trash: int = 0,
        max_num_trash: int = -1,
    ) -> list["Card"]:
        raise NotImplementedError("trash_decision is not implemented")

    def gain_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_gain: int = 0,
        max_num_gain: int = -1,
    ) -> list["Card"]:
        raise NotImplementedError("gain_decision is not implemented")

    def topdeck_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_topdeck: int = 0,
        max_num_topdeck: int = -1,
    ) -> list["Card"]:
        raise NotImplementedError("topdeck_decision is not implemented")

    def deck_position_decision(
        self,
        prompt: str,
        card: "Card",
        player: "Player",
        game: "Game",
        num_deck_cards: int,
    ) -> int:
        raise NotImplementedError("deck_position_decision is not implemented")

    def reveal_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_reveal: int = 0,
        max_num_reveal: int = -1,
    ) -> list["Card"]:
        raise NotImplementedError("reveal_decision is not implemented")

    def pass_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_pass: int = 0,
        max_num_pass: int = -1,
    ) -> list["Card"]:
        raise NotImplementedError("pass_decision is not implemented")

    def name_card_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_name: int = 0,
        max_num_name: int = -1,
    ) -> list["Card"]:
        raise NotImplementedError("name_card_decision is not implemented")

    def multi_play_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        required: bool = True,
    ) -> "Card|None":
        raise NotImplementedError("multi_play_decision is not implemented")

    def set_aside_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_set_aside: int = 0,
        max_num_set_aside: int = -1,
    ) -> list["Card"]:
        raise NotImplementedError("set_aside_decision is not implemented")

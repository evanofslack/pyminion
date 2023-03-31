from typing import TYPE_CHECKING, List, Optional, Protocol

if TYPE_CHECKING:
    from pyminion.core import Card, Player
    from pyminion.game import Game


class Decider(Protocol):
    """
    Interface for prompting a player for a decision.

    """

    def binary_decision(
        self,
        prompt: str,
        card: "Card",
        player: "Player",
        game: "Game",
        relevant_cards: Optional[List["Card"]] = None,
    ) -> bool:
        raise NotImplementedError("binary_decision is not implemented")

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
        raise NotImplementedError("discard_decision is not implemented")

    # TODO:
    # trash_decision
    # multiple_trash_decision
    # gain_decision
    # multiple_gain_decision
    # topdeck_decision
    # double_play_decision

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

    # TODO:
    # get_discard_decision
    # get_multiple_discard_decision
    # get_gain_decision
    # get_multiple_gain_decision
    # get_trash_decision
    # get_multiple_trash_decision
    # get_topdeck_decision
    # get_double_play_decision

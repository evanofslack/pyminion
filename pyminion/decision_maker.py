from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from pyminion.core import Card
    from pyminion.game import Game


class DecisionMaker:
    """
    Interface for prompting a player for a decision.

    """

    def get_binary_decision(
        self,
        prompt: str,
        card: "Card",
        game: "Game",
        relevant_cards: Optional[List["Card"]] = None,
    ) -> bool:
        raise NotImplementedError("get_binary_decision is not implemented")

    # TODO:
    # get_discard_decision
    # get_multiple_discard_decision
    # get_gain_decision
    # get_multiple_gain_decision
    # get_trash_decision
    # get_multiple_trash_decision
    # get_topdeck_decision
    # get_double_play_decision

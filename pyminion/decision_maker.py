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
        card: Card,
        game: Game,
        relevant_cards: Optional[List[Card]] = None,
    ) -> bool:
        raise NotImplementedError("get_binary_decision is not implemented")

    # TODO:
    # discard_resp
    # multiple_discard_resp
    # gain_resp
    # multiple_gain_resp
    # trash_resp
    # multiple_trash_resp
    # topdeck_resp
    # double_play_resp

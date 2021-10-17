import pytest

from pyminion.models.base import Turn, Player
from pyminion.models.cards import Smithy
from pyminion.base_set.base_cards import smithy
from pyminion.exceptions import InsufficientActions


def test_smithy_draw(turn: Turn, player: Player):
    """
    Create a hand with one smithy then play that smithy.
    Assert smithy on playmat, handsize increases to 3, action count goes to 0

    """
    turn.player.hand.add(smithy)
    assert len(turn.player.hand) == 1
    turn.player.hand.cards[0].play(turn, player)
    assert len(turn.player.hand) == 3
    assert len(turn.player.playmat) == 1
    assert type(turn.player.playmat.cards[0]) is Smithy
    assert turn.actions == 0


def test_smithy_draw_no_actions(turn: Turn, player: Player):
    turn.player.hand.add(smithy)
    turn.player.hand.cards[0].play(turn, player)
    turn.player.hand.add(smithy)
    with pytest.raises(InsufficientActions):
        turn.player.hand.cards[-1].play(turn, turn.player)

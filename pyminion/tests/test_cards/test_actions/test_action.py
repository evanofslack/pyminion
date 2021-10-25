import pytest

from pyminion.models.core import Turn, Player
from pyminion.models.cards import Action
from pyminion.exceptions import InsufficientActions

action = Action(name="test", cost="0", type="Action")


def test_action_common_play(turn: Turn, player: Player):

    player.hand.add(action)
    assert len(player.hand) == 1
    player.hand.cards[0].common_play(turn, player)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Action
    assert turn.actions == 0


def test_action_draw_no_actions(turn: Turn, player: Player):
    player.hand.add(action)
    player.hand.cards[0].common_play(turn, player)
    player.hand.add(action)

    with pytest.raises(InsufficientActions):
        player.hand.cards[-1].common_play(turn, player)

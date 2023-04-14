import pytest
from pyminion.core import Action, CardType
from pyminion.exceptions import InsufficientActions
from pyminion.player import Player

action = Action(name="test", cost="0", type=CardType.Action, actions=0, draw=0, money=0)


def test_action_common_play(player: Player):

    player.hand.add(action)
    assert len(player.hand) == 1
    player.hand.cards[0].generic_play(player)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Action
    assert player.state.actions == 0


def test_action_draw_no_actions(player: Player):
    player.hand.add(action)
    player.hand.cards[0].generic_play(player)
    player.hand.add(action)

    with pytest.raises(InsufficientActions):
        player.hand.cards[-1].generic_play(player)

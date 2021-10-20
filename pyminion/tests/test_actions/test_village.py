from pyminion.models.core import Turn, Player
from pyminion.models.base import Village
from pyminion.expansions.base import village


def test_village(turn: Turn, player: Player):
    player.hand.add(village)
    assert len(player.hand) == 1
    player.hand.cards[0].play(turn, player)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Village
    assert turn.actions == 2

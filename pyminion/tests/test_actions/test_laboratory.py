from pyminion.models.base import Turn, Player
from pyminion.models.cards import Laboratory
from pyminion.base_set.base_cards import laboratory


def test_laboratory(turn: Turn, player: Player):
    player.hand.add(laboratory)
    assert len(player.hand) == 1
    player.hand.cards[0].play(turn, player)
    assert len(player.hand) == 2
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Laboratory
    assert turn.actions == 1

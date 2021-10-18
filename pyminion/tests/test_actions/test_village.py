from pyminion.models.base import Turn, Player
from pyminion.models.cards import Village
from pyminion.base_set.base_cards import village


def test_village(turn: Turn, player: Player):
    player.hand.add(village)
    assert len(player.hand) == 1
    player.hand.cards[0].play(turn, player)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Village
    assert turn.actions == 2

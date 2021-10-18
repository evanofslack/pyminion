from pyminion.models.base import Turn, Player
from pyminion.models.cards import Market
from pyminion.base_set.base_cards import market


def test_market(turn: Turn, player: Player):
    player.hand.add(market)
    assert len(player.hand) == 1
    player.hand.cards[0].play(turn, player)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Market
    assert turn.actions == 1
    assert turn.money == 1
    assert turn.buys == 2

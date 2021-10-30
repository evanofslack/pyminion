from pyminion.models.core import Player, Game
from pyminion.models.base import Festival
from pyminion.expansions.base import festival


def test_festival(player: Player, game: Game):
    player.hand.add(festival)
    assert len(player.hand) == 1
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Festival
    assert player.state.actions == 2
    assert player.state.money == 2
    assert player.state.buys == 2

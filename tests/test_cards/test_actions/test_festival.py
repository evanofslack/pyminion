from pyminion.expansions.base import festival
from pyminion.game import Game
from pyminion.expansions.base import Festival
from pyminion.player import Player


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

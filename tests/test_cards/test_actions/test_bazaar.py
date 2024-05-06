from pyminion.expansions.seaside import Bazaar, bazaar
from pyminion.game import Game
from pyminion.player import Player

def test_bazaar(player: Player, game: Game):
    player.hand.add(bazaar)

    player.play(bazaar, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Bazaar
    assert player.state.actions == 2
    assert player.state.money == 1

from pyminion.expansions.intrigue import Harem, harem
from pyminion.game import Game
from pyminion.player import Player


def test_money(player: Player, game: Game):
    player.hand.add(harem)

    harem.play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Harem
    assert player.state.money == 2


def test_vp(player: Player):
    player.hand.add(harem)
    assert harem.score(player) == 2

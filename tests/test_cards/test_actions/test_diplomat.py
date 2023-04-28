from pyminion.expansions.base import copper
from pyminion.expansions.intrigue import Diplomat, diplomat
from pyminion.player import Player
from pyminion.game import Game


def test_diplomat_actions(player: Player, game: Game):
    player.hand.add(diplomat)
    assert len(player.hand) == 1

    player.play(diplomat, game)
    assert len(player.hand) == 2
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Diplomat
    assert player.state.actions == 2


def test_diplomat_no_actions(player: Player, game: Game):
    for _ in range(4):
        player.hand.add(copper)
    player.hand.add(diplomat)
    assert len(player.hand) == 5

    player.play(diplomat, game)
    assert len(player.hand) == 6
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Diplomat
    assert player.state.actions == 0

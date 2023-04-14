from pyminion.expansions.base import Laboratory, laboratory
from pyminion.game import Game
from pyminion.player import Player


def test_laboratory(player: Player, game: Game):
    player.hand.add(laboratory)
    assert len(player.hand) == 1
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 2
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Laboratory
    assert player.state.actions == 1

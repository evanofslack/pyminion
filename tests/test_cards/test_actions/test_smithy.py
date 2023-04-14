from pyminion.expansions.base import smithy
from pyminion.game import Game
from pyminion.expansions.base import Smithy
from pyminion.player import Player


def test_smithy_draw(player: Player, game: Game):
    """
    Create a hand with one smithy then play that smithy.
    Assert smithy on playmat, handsize increases to 3, action count goes to 0

    """
    player.hand.add(smithy)
    assert len(player.hand) == 1
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 3
    assert type(player.playmat.cards[0]) is Smithy
    assert player.state.actions == 0

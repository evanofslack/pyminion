from pyminion.expansions.seaside import Caravan, caravan
from pyminion.game import Game
from pyminion.player import Player

def test_caravan(player: Player, game: Game):
    player.hand.add(caravan)

    player.play(caravan, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Caravan
    assert len(player.discard_pile) == 0
    assert player.state.actions == 1

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Caravan
    assert len(player.discard_pile) == 1
    assert type(player.discard_pile.cards[0]) is not Caravan

    player.start_turn(game)

    assert len(player.hand) == 6
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Caravan
    assert len(player.discard_pile) == 1
    assert type(player.discard_pile.cards[0]) is not Caravan

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 0

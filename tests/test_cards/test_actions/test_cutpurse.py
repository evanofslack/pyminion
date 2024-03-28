from pyminion.expansions.base import copper
from pyminion.expansions.seaside import cutpurse
from pyminion.game import Game


def test_cutpurse(multiplayer_game: Game):
    player1 = multiplayer_game.players[0]
    player2 = multiplayer_game.players[1]

    player1.hand.add(cutpurse)
    player1.play(cutpurse, multiplayer_game)
    assert len(player1.hand) == 5
    assert player1.state.actions == 0
    assert player1.state.money == 2
    assert player1.state.buys == 1

    assert len(player2.hand) == 4
    assert len(player2.discard_pile) == 1
    assert player2.discard_pile.cards[0] is copper

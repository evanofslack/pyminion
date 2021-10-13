from pyminion.models.base import Player, Turn
from pyminion.base_set.base_cards import copper


def test_create_turn(player: Player):
    turn = Turn(player=player)
    assert turn.actions == 1
    assert turn.money == 0
    assert turn.buys == 1


def test_play_copper(turn: Turn):
    """
    Create a hand with one copper then play that copper.
    Assert copper moves from hand to playmat and money increases to 1

    """
    turn.player.hand.add(copper)
    assert len(turn.player.hand) == 1
    turn.player.hand.cards[0].play(turn)
    assert turn.money == 1
    assert len(turn.player.hand) == 0
    assert len(turn.player.playmat) == 1

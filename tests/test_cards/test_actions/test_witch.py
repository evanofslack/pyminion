from pyminion.expansions.base import Witch, curse, witch
from pyminion.game import Game


def test_witch(multiplayer_game: Game):
    player = multiplayer_game.players[0]
    player.hand.add(witch)
    assert len(player.hand) == 6
    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.discard_pile) == 0
    player.play(witch, multiplayer_game)
    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.discard_pile) == 1
            assert p.discard_pile.cards[-1] is curse
    assert len(player.hand) == 7
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Witch
    assert player.state.actions == 0
    assert player.state.money == 0
    assert player.state.buys == 1


def test_witch_empty_curses(multiplayer_game: Game):
    """
    with an empty curse pile, playing witch should only draw two cards and not give out any curses.

    """

    # empty the curse pile
    for pile in multiplayer_game.supply.piles:
        if pile.name == "Curse":
            pile.cards = []

    player = multiplayer_game.players[0]
    player.hand.add(witch)
    player.play(witch, multiplayer_game)

    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.discard_pile) == 0
    assert len(player.hand) == 7
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Witch
    assert player.state.actions == 0
    assert player.state.money == 0
    assert player.state.buys == 1

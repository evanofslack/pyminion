from pyminion.expansions.base import militia
from pyminion.game import Game


def test_militia_makes_2_money(multiplayer_game: Game):
    player = multiplayer_game.players[0]
    player.hand.add(militia)
    assert player.state.money == 0

    opponent = multiplayer_game.players[1]
    for i in range(2):
        opponent.hand.remove(opponent.hand.cards[0])

    player.play(militia, multiplayer_game)
    assert player.state.money == 2


def test_militia_opponent_no_discard(multiplayer_game: Game):
    player = multiplayer_game.players[0]
    player.hand.add(militia)
    opponent = multiplayer_game.players[1]
    for i in range(2):
        opponent.hand.remove(opponent.hand.cards[0])

    assert len(opponent.hand) == 3
    player.hand.cards[-1].play(player, multiplayer_game)
    assert len(opponent.hand) == 3


def test_militia_opponent_discards(multiplayer_game: Game, monkeypatch):
    player = multiplayer_game.players[0]
    player.hand.add(militia)
    opponent = multiplayer_game.players[1]
    assert len(opponent.discard_pile) == 0

    monkeypatch.setattr("builtins.input", lambda _: "copper, copper")

    player.play(militia, multiplayer_game)
    assert len(opponent.hand) == 3
    assert len(opponent.discard_pile) == 2

from pyminion.expansions.base import province, silver
from pyminion.expansions.seaside import smugglers
from pyminion.game import Game


def test_smugglers_gain(multiplayer_game: Game, monkeypatch):
    player1 = multiplayer_game.players[0]
    player2 = multiplayer_game.players[1]

    player1.start_turn(multiplayer_game)
    player1.gain(silver, multiplayer_game)
    player1.end_turn(multiplayer_game)

    player2.start_turn(multiplayer_game)
    player2.hand.add(smugglers)

    responses = ["silver"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    player2.play(smugglers, multiplayer_game)
    assert len(responses) == 0
    assert player2.state.actions == 0
    assert len(player2.discard_pile) == 1
    assert player2.discard_pile.cards[0].name == "Silver"


def test_smugglers_no_gain(multiplayer_game: Game):
    player1 = multiplayer_game.players[0]
    player2 = multiplayer_game.players[1]

    player1.start_turn(multiplayer_game)
    player1.gain(province, multiplayer_game)
    player1.end_turn(multiplayer_game)

    player2.start_turn(multiplayer_game)
    player2.hand.add(smugglers)

    player2.play(smugglers, multiplayer_game)
    assert player2.state.actions == 0
    assert len(player2.discard_pile) == 0

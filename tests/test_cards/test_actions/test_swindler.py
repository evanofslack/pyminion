from pyminion.expansions.base import copper, moat
from pyminion.expansions.intrigue import Swindler, swindler
from pyminion.game import Game


def test_swindler(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(swindler)
    p2.deck.add(copper)

    monkeypatch.setattr("builtins.input", lambda _: "curse")

    p1.play(swindler, multiplayer_game)
    assert len(p1.hand) == 5
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Swindler
    assert p1.state.actions == 0
    assert p1.state.money == 2

    assert len(p2.discard_pile) > 0
    assert p2.discard_pile.cards[-1].name == "Curse"


def test_swindler_moat(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(swindler)
    p2.hand.add(moat)
    p2.deck.add(moat)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    p1.play(swindler, multiplayer_game)
    assert len(p1.hand) == 5
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Swindler
    assert p1.state.actions == 0
    assert p1.state.money == 2

    assert p2.deck.cards[-1].name == "Moat"
    assert len(p2.discard_pile) == 0

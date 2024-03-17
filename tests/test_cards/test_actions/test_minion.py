from pyminion.expansions.base import moat
from pyminion.expansions.intrigue import Minion, minion
from pyminion.game import Game
import pytest


def test_minion_money(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(minion)

    monkeypatch.setattr("builtins.input", lambda _: "1")

    p1.play(minion, multiplayer_game)
    assert len(p1.hand) == 5
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Minion
    assert len(p1.discard_pile) == 0
    assert p1.state.actions == 1
    assert p1.state.money == 2

    assert len(p2.hand) == 5
    assert len(p2.discard_pile) == 0


def test_minion_discard_draw(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(minion)

    monkeypatch.setattr("builtins.input", lambda _: "2")

    p1.play(minion, multiplayer_game)
    assert len(p1.hand) == 4
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Minion
    assert len(p1.discard_pile) == 5
    assert p1.state.actions == 1
    assert p1.state.money == 0

    assert len(p2.hand) == 4
    assert len(p2.discard_pile) == 5


def test_minion_opponent_no_discard(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(minion)
    p2.hand.remove(p2.hand.cards[0])
    assert len(p2.hand) == 4

    monkeypatch.setattr("builtins.input", lambda _: "2")

    p1.play(minion, multiplayer_game)
    assert len(p1.hand) == 4
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Minion
    assert len(p1.discard_pile) == 5
    assert p1.state.actions == 1
    assert p1.state.money == 0

    assert len(p2.hand) == 4
    assert len(p2.discard_pile) == 0


@pytest.mark.kingdom_cards([moat])
def test_minion_moat(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(minion)
    p2.deck.add(moat)
    p2.draw()

    responses = iter(["y", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    p1.play(minion, multiplayer_game)
    assert len(p1.hand) == 4
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Minion
    assert len(p1.discard_pile) == 5
    assert p1.state.actions == 1
    assert p1.state.money == 0

    assert len(p2.hand) == 6
    assert len(p2.discard_pile) == 0

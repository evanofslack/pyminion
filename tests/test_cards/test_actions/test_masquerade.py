from pyminion.expansions.base import Silver, Copper, silver, copper
from pyminion.expansions.intrigue import Masquerade, masquerade
from pyminion.game import Game
from pyminion.human import Human


def test_masquerade_no_trash(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.cards = [copper, masquerade]

    p2.hand.cards = [silver]

    responses = iter(["copper", "silver", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    masquerade.play(p1, multiplayer_game)
    assert len(p1.hand) == 3
    assert len([c for c in p1.hand.cards if isinstance(c, Silver)]) == 1
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Masquerade

    assert len(p2.hand) == 1
    assert type(p2.hand.cards[0]) is Copper


def test_masquerade_trash(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.cards = [copper, masquerade]

    p2.hand.cards = [silver]

    responses = iter(["copper", "silver", "y", "silver"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    masquerade.play(p1, multiplayer_game)
    assert len(p1.hand) == 2
    assert len([c for c in p1.hand.cards if isinstance(c, Silver)]) == 0
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Masquerade
    assert len(multiplayer_game.trash) == 1
    assert type(multiplayer_game.trash.cards[0]) is Silver

    assert len(p2.hand) == 1
    assert type(p2.hand.cards[0]) is Copper

from pyminion.expansions.base import estate
from pyminion.expansions.intrigue import Replace, mill, replace
from pyminion.game import Game
import pytest

def test_replace_gain_treasure(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(replace)
    p1.hand.add(estate)

    responses = iter(["estate", "silver"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    p1.play(replace, multiplayer_game)
    assert len(p1.hand) == 5
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Replace
    assert p1.deck.cards[-1].name == "Silver"
    assert len(p1.discard_pile) == 0
    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Estate"

    assert len(p2.discard_pile) == 0


def test_replace_gain_victory(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(replace)
    p1.hand.add(estate)

    responses = iter(["estate", "estate"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    p1.play(replace, multiplayer_game)
    assert len(p1.hand) == 5
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Replace
    assert len(p1.discard_pile) == 1
    assert p1.discard_pile.cards[0].name == "Estate"
    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Estate"

    assert len(p2.discard_pile) == 1
    assert p2.discard_pile.cards[0].name == "Curse"


@pytest.mark.kingdom_cards([mill])
def test_replace_gain_action_victory(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(replace)
    p1.hand.add(estate)

    responses = iter(["estate", "mill"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    p1.play(replace, multiplayer_game)
    assert len(p1.hand) == 5
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Replace
    assert p1.deck.cards[-1].name == "Mill"
    assert len(p1.discard_pile) == 0
    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Estate"

    assert len(p2.discard_pile) == 1
    assert p2.discard_pile.cards[0].name == "Curse"

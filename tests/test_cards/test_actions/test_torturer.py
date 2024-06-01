from pyminion.core import Card, CardType
from pyminion.expansions.base import moat
from pyminion.expansions.intrigue import Torturer, torturer
from pyminion.game import Game
import pytest


def test_torturer_discard(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1_hand_cards: list[Card] = [torturer]
    p1.hand.cards = p1_hand_cards

    responses = iter(["1", "copper, copper"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    p1.play(torturer, multiplayer_game)
    assert len(p1.hand) == 3
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Torturer

    assert len(p2.hand) == 3
    assert len(p2.discard_pile) == 2


def test_torturer_discard_no_cards(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1_hand_cards: list[Card] = [torturer]
    p1.hand.cards = p1_hand_cards
    p2.hand.cards = []

    monkeypatch.setattr("builtins.input", lambda _: "1")

    p1.play(torturer, multiplayer_game)
    assert len(p1.hand) == 3
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Torturer

    assert len(p2.hand) == 0
    assert len(p2.discard_pile) == 0


def test_torturer_gain_curse(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1_hand_cards: list[Card] = [torturer]
    p1.hand.cards = p1_hand_cards

    monkeypatch.setattr("builtins.input", lambda _: "2")

    p1.play(torturer, multiplayer_game)
    assert len(p1.hand) == 3
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Torturer

    assert len(p2.hand) == 6
    assert any(CardType.Curse in c.type for c in p2.hand.cards)
    assert len(p2.discard_pile) == 0


def test_torturer_gain_curse_no_curses(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    curse_pile = multiplayer_game.supply.get_pile("Curse")
    curse_pile.cards = []

    p1_hand_cards: list[Card] = [torturer]
    p1.hand.cards = p1_hand_cards

    monkeypatch.setattr("builtins.input", lambda _: "2")

    p1.play(torturer, multiplayer_game)
    assert len(p1.hand) == 3
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Torturer

    assert len(p2.hand) == 5
    assert len(p2.discard_pile) == 0


@pytest.mark.kingdom_cards([moat])
def test_torturer_moat(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1_hand_cards: list[Card] = [torturer]
    p1.hand.cards = p1_hand_cards

    monkeypatch.setattr("builtins.input", lambda _: "y")

    p2.deck.add(moat)
    p2.draw()

    p1.play(torturer, multiplayer_game)
    assert len(p1.hand) == 3
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Torturer

    assert len(p2.hand) == 6
    assert len(p2.discard_pile) == 0

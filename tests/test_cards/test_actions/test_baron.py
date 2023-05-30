from pyminion.expansions.base import Copper, Estate, copper, estate
from pyminion.expansions.intrigue import Baron, baron
from pyminion.game import Game
from pyminion.human import Human


def test_baron_discard_estate(human: Human, game: Game, monkeypatch):
    human.hand.add(baron)
    human.hand.add(estate)

    monkeypatch.setattr("builtins.input", lambda _: "1")

    baron.play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Baron
    assert len(human.discard_pile) == 1
    assert type(human.discard_pile.cards[0]) is Estate
    assert human.state.actions == 0
    assert human.state.money == 4
    assert human.state.buys == 2


def test_baron_no_discard_estate(human: Human, game: Game, monkeypatch):
    human.hand.add(baron)
    human.hand.add(estate)

    monkeypatch.setattr("builtins.input", lambda _: "2")

    baron.play(human, game)
    assert len(human.hand) == 1
    assert type(human.hand.cards[0]) is Estate
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Baron
    assert len(human.discard_pile) == 1
    assert type(human.discard_pile.cards[0]) is Estate
    assert human.state.actions == 0
    assert human.state.money == 0
    assert human.state.buys == 2


def test_baron_no_estate(human: Human, game: Game, monkeypatch):
    human.hand.add(baron)
    human.hand.add(copper)

    baron.play(human, game)
    assert len(human.hand) == 1
    assert type(human.hand.cards[0]) is Copper
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Baron
    assert len(human.discard_pile) == 1
    assert type(human.discard_pile.cards[0]) is Estate
    assert human.state.actions == 0
    assert human.state.money == 0
    assert human.state.buys == 2

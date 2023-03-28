from pyminion.expansions.base import Cellar, Copper, Estate, cellar, copper, estate
from pyminion.game import Game
from pyminion.human import Human


def test_cellar_discard_one(human: Human, game: Game, monkeypatch):
    human.hand.add(cellar)
    human.hand.add(copper)
    human.hand.add(copper)
    assert len(human.hand) == 3
    assert len(human.discard_pile) == 0

    monkeypatch.setattr("builtins.input", lambda _: "Copper")

    human.play(target_card=cellar, game=game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1
    assert type(human.playmat.cards[0]) is Cellar
    assert human.state.actions == 1
    assert type(human.discard_pile.cards[0]) is Copper


def test_cellar_discard_multiple(human: Human, game: Game, monkeypatch):
    human.hand.add(cellar)
    human.hand.add(copper)
    human.hand.add(copper)
    human.hand.add(estate)
    assert len(human.hand) == 4
    assert len(human.discard_pile) == 0

    monkeypatch.setattr("builtins.input", lambda _: "Copper, Estate")

    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 3
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 2
    assert type(human.playmat.cards[0]) is Cellar
    assert human.state.actions == 1
    assert type(human.discard_pile.cards[0]) is Copper
    assert type(human.discard_pile.cards[1]) is Estate


def test_cellar_empty_hand(human: Human, game: Game):
    human.hand.add(cellar)
    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert human.state.actions == 1


def test_cellar_discard_none(human: Human, game: Game, monkeypatch):
    human.hand.add(cellar)
    monkeypatch.setattr("builtins.input", lambda _: "")
    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert human.state.actions == 1

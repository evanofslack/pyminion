from pyminion.expansions.base import Chapel, Copper, Estate, chapel, copper, estate
from pyminion.game import Game
from pyminion.human import Human


def test_chapel_trash_one(human: Human, game: Game, monkeypatch):
    human.hand.add(chapel)
    human.hand.add(copper)
    human.hand.add(copper)
    assert len(human.hand) == 3
    assert len(game.trash) == 0

    monkeypatch.setattr("builtins.input", lambda _: "Copper")

    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert len(game.trash) == 1
    assert type(human.playmat.cards[0]) is Chapel
    assert human.state.actions == 0
    assert type(game.trash.cards[0]) is Copper


def test_chapel_trash_multiple(human: Human, game: Game, monkeypatch):
    human.hand.add(chapel)
    human.hand.add(copper)
    human.hand.add(copper)
    human.hand.add(estate)
    assert len(human.hand) == 4
    assert len(game.trash) == 0

    monkeypatch.setattr("builtins.input", lambda _: "Copper, Estate")

    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert len(game.trash) == 2
    assert type(human.playmat.cards[0]) is Chapel
    assert type(game.trash.cards[0]) is Copper
    assert type(game.trash.cards[1]) is Estate


def test_chapel_empty_hand(human: Human, game: Game):
    human.hand.add(chapel)
    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1


def test_chapel_trash_none(human: Human, game: Game, monkeypatch):
    human.hand.add(chapel)
    monkeypatch.setattr("builtins.input", lambda _: "")
    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1

from pyminion.expansions.base import copper
from pyminion.expansions.intrigue import Steward, steward
from pyminion.game import Game
from pyminion.human import Human


def test_steward_cards(human: Human, game: Game, monkeypatch):
    human.hand.add(steward)

    monkeypatch.setattr("builtins.input", lambda _: "1")

    steward.play(human, game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Steward
    assert human.state.actions == 0
    assert human.state.money == 0


def test_steward_money(human: Human, game: Game, monkeypatch):
    human.hand.add(steward)

    monkeypatch.setattr("builtins.input", lambda _: "2")

    steward.play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Steward
    assert human.state.actions == 0
    assert human.state.money == 2


def test_steward_trash(human: Human, game: Game, monkeypatch):
    human.hand.add(steward)
    human.hand.add(copper)
    human.hand.add(copper)
    human.hand.add(copper)

    responses = iter(["3", "copper, copper"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    steward.play(human, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Steward
    assert human.state.actions == 0
    assert human.state.money == 0
    assert len(game.trash) == 2


def test_steward_trash_one(human: Human, game: Game, monkeypatch):
    human.hand.add(steward)
    human.hand.add(copper)

    monkeypatch.setattr("builtins.input", lambda _: "3")

    steward.play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Steward
    assert human.state.actions == 0
    assert human.state.money == 0
    assert len(game.trash) == 1

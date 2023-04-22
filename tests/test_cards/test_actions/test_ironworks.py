from pyminion.expansions.base import Estate, Silver, Smithy
from pyminion.expansions.intrigue import Ironworks, Mill, ironworks
from pyminion.game import Game
from pyminion.human import Human


def test_ironworks_action(human: Human, game: Game, monkeypatch):
    human.hand.add(ironworks)

    monkeypatch.setattr("builtins.input", lambda _: "smithy")

    human.play(ironworks, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Ironworks
    assert len(human.discard_pile) == 1
    assert type(human.discard_pile.cards[0]) is Smithy
    assert human.state.actions == 1
    assert human.state.money == 0


def test_ironworks_treasure(human: Human, game: Game, monkeypatch):
    human.hand.add(ironworks)

    monkeypatch.setattr("builtins.input", lambda _: "silver")

    human.play(ironworks, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Ironworks
    assert len(human.discard_pile) == 1
    assert type(human.discard_pile.cards[0]) is Silver
    assert human.state.actions == 0
    assert human.state.money == 1


def test_ironworks_victory(human: Human, game: Game, monkeypatch):
    human.hand.add(ironworks)

    monkeypatch.setattr("builtins.input", lambda _: "estate")

    human.play(ironworks, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Ironworks
    assert len(human.discard_pile) == 1
    assert type(human.discard_pile.cards[0]) is Estate
    assert human.state.actions == 0
    assert human.state.money == 0


def test_ironworks_action_victory(human: Human, game: Game, monkeypatch):
    human.hand.add(ironworks)

    monkeypatch.setattr("builtins.input", lambda _: "mill")

    human.play(ironworks, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Ironworks
    assert len(human.discard_pile) == 1
    assert type(human.discard_pile.cards[0]) is Mill
    assert human.state.actions == 1
    assert human.state.money == 0
from pyminion.expansions.base import copper, silver
from pyminion.expansions.seaside import salvager
from pyminion.game import Game
from pyminion.human import Human


def test_salvager(human: Human, game: Game, monkeypatch):
    responses = ["silver"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.hand.add(salvager)
    human.hand.add(silver)
    human.hand.add(copper)

    human.play(salvager, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Salvager"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Silver"
    assert human.state.actions == 0
    assert human.state.money == 3


def test_salvager_1_card(human: Human, game: Game):
    human.hand.add(salvager)
    human.hand.add(silver)

    human.play(salvager, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Salvager"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Silver"
    assert human.state.actions == 0
    assert human.state.money == 3


def test_salvager_no_cards(human: Human, game: Game):
    human.hand.add(salvager)

    human.play(salvager, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Salvager"
    assert len(game.trash) == 0
    assert human.state.actions == 0
    assert human.state.money == 0

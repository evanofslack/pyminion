from pyminion.expansions.intrigue import Pawn, pawn
from pyminion.game import Game
from pyminion.human import Human


def test_pawn_card_action(human: Human, game: Game, monkeypatch):
    human.hand.add(pawn)

    monkeypatch.setattr("builtins.input", lambda _: "1, 2")

    pawn.play(human, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Pawn
    assert human.state.actions == 1
    assert human.state.buys == 1
    assert human.state.money == 0


def test_pawn_card_buy(human: Human, game: Game, monkeypatch):
    human.hand.add(pawn)

    monkeypatch.setattr("builtins.input", lambda _: "3, 1")

    pawn.play(human, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Pawn
    assert human.state.actions == 0
    assert human.state.buys == 2
    assert human.state.money == 0


def test_pawn_action_buy(human: Human, game: Game, monkeypatch):
    human.hand.add(pawn)

    monkeypatch.setattr("builtins.input", lambda _: "3, 2")

    pawn.play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Pawn
    assert human.state.actions == 1
    assert human.state.buys == 2
    assert human.state.money == 0


def test_pawn_buy_money(human: Human, game: Game, monkeypatch):
    human.hand.add(pawn)

    monkeypatch.setattr("builtins.input", lambda _: "3, 4")

    pawn.play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Pawn
    assert human.state.actions == 0
    assert human.state.buys == 2
    assert human.state.money == 1

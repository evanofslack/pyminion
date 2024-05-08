from pyminion.expansions.base import Gold, copper
from pyminion.expansions.intrigue import Courtier, courtier, nobles
from pyminion.game import Game
from pyminion.human import Human


def test_courtier_1_type_action(human: Human, game: Game, monkeypatch):
    human.hand.add(courtier)
    human.hand.add(nobles)
    human.hand.add(copper)

    responses = iter(["copper", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    courtier.play(human, game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Courtier
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1
    assert human.state.buys == 1
    assert human.state.money == 0


def test_courtier_2_types_buy_money(human: Human, game: Game, monkeypatch):
    human.hand.add(courtier)
    human.hand.add(nobles)
    human.hand.add(copper)

    responses = iter(["nobles", "2, 3"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    courtier.play(human, game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Courtier
    assert len(human.discard_pile) == 0
    assert human.state.actions == 0
    assert human.state.buys == 2
    assert human.state.money == 3


def test_courtier_2_types_buy_gain_gold(human: Human, game: Game, monkeypatch):
    human.hand.add(courtier)
    human.hand.add(nobles)
    human.hand.add(copper)

    responses = iter(["nobles", "2, 4"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    courtier.play(human, game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Courtier
    assert len(human.discard_pile) == 1
    assert type(human.discard_pile.cards[0]) is Gold
    assert human.state.actions == 0
    assert human.state.buys == 2
    assert human.state.money == 0


def test_courtier_empty_hand(human: Human, game: Game, monkeypatch):
    human.hand.add(courtier)

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(courtier, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Courtier
    assert len(human.discard_pile) == 0
    assert human.state.actions == 0
    assert human.state.buys == 1
    assert human.state.money == 0


def test_courtier_1_card_hand(human: Human, game: Game, monkeypatch):
    human.hand.add(courtier)
    human.hand.add(copper)

    responses = ["1"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(courtier, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Courtier
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1
    assert human.state.buys == 1
    assert human.state.money == 0

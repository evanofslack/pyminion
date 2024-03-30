from pyminion.expansions.base import Duchy, Silver, silver, duchy
from pyminion.expansions.seaside import NativeVillage, native_village
from pyminion.game import Game
from pyminion.human import Human


def test_native_village(human: Human, game: Game, monkeypatch):
    human.hand.add(native_village)
    human.hand.add(native_village)
    human.deck.add(silver)

    responses = iter(["1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(native_village, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is NativeVillage
    assert len(human.discard_pile) == 0
    assert human.state.actions == 2
    assert human.state.buys == 1
    assert human.state.money == 0
    mat = human.get_mat("Native Village")
    assert len(mat) == 1
    assert type(mat.cards[0]) is Silver

    human.play(native_village, game)
    assert len(human.hand) == 1
    assert type(human.hand.cards[0]) is Silver
    assert len(human.playmat) == 2
    assert type(human.playmat.cards[0]) is NativeVillage
    assert type(human.playmat.cards[1]) is NativeVillage
    assert len(human.discard_pile) == 0
    assert human.state.actions == 3
    assert human.state.buys == 1
    assert human.state.money == 0
    mat = human.get_mat("Native Village")
    assert len(mat) == 0


def test_native_village_score(human: Human, game: Game, monkeypatch):
    human.hand.add(native_village)
    human.deck.add(duchy)

    assert human.get_victory_points() == 6

    responses = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(native_village, game)
    mat = human.get_mat("Native Village")
    assert len(mat) == 1
    assert type(mat.cards[0]) is Duchy

    assert human.get_victory_points() == 6

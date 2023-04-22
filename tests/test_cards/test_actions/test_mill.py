from pyminion.expansions.base import Copper, copper
from pyminion.expansions.intrigue import Mill, mill
from pyminion.game import Game
from pyminion.human import Human
from pyminion.player import Player


def test_mill_discard(human: Human, game: Game, monkeypatch):
    human.hand.add(mill)
    human.hand.add(copper)
    human.hand.add(copper)

    responses = iter(["y", "copper, copper"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(mill, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Mill
    assert len(human.discard_pile) == 2
    assert type(human.discard_pile.cards[0]) is Copper
    assert type(human.discard_pile.cards[1]) is Copper
    assert human.state.actions == 1
    assert human.state.money == 2


def test_mill_discard_one(human: Human, game: Game, monkeypatch):
    human.hand.add(mill)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    human.play(mill, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Mill
    assert len(human.discard_pile) == 1
    assert human.state.actions == 1
    assert human.state.money == 0


def test_mill_no_discard(human: Human, game: Game, monkeypatch):
    human.hand.add(mill)
    human.hand.add(copper)
    human.hand.add(copper)

    monkeypatch.setattr("builtins.input", lambda _: "n")

    human.play(mill, game)
    assert len(human.hand) == 3
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Mill
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1
    assert human.state.money == 0


def test_mill_vp(player: Player):
    assert mill.score(player) == 1

    player.hand.add(mill)
    assert player.get_victory_points() == 4
    player.deck.add(mill)
    player.discard_pile.add(mill)
    assert player.get_victory_points() == 6

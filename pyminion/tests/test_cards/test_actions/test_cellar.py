from pyminion.models.core import Player, Game
from pyminion.models.base import Cellar, Copper, Estate, cellar, copper, estate


def test_cellar_discard_one(player: Player, game: Game, monkeypatch):
    player.hand.add(cellar)
    player.hand.add(copper)
    player.hand.add(copper)
    assert len(player.hand) == 3
    assert len(player.discard_pile) == 0

    # mock decision = input() as "Copper" to discard
    monkeypatch.setattr("builtins.input", lambda _: "Copper")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 2
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 1
    assert type(player.playmat.cards[0]) is Cellar
    assert player.state.actions == 1
    assert type(player.discard_pile.cards[0]) is Copper


def test_cellar_discard_multiple(player: Player, game: Game, monkeypatch):
    player.hand.add(cellar)
    player.hand.add(copper)
    player.hand.add(copper)
    player.hand.add(estate)
    assert len(player.hand) == 4
    assert len(player.discard_pile) == 0

    # mock decision = input() as "Copper, Estate" to discard
    monkeypatch.setattr("builtins.input", lambda _: "Copper, Estate")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 3
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 2
    assert type(player.playmat.cards[0]) is Cellar
    assert player.state.actions == 1
    assert type(player.discard_pile.cards[0]) is Copper
    assert type(player.discard_pile.cards[1]) is Estate


def test_cellar_empty_hand(player: Player, game: Game):
    player.hand.add(cellar)
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert player.state.actions == 1


def test_cellar_discard_none(player: Player, game: Game, monkeypatch):
    player.hand.add(cellar)
    monkeypatch.setattr("builtins.input", lambda _: "")
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert player.state.actions == 1

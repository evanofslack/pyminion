from pyminion.models.core import Player, Game
from pyminion.models.base import Moneylender, Copper
from pyminion.expansions.base import moneylender, copper


def test_moneylender_normal(player: Player, game: Game, monkeypatch):
    player.hand.add(moneylender)
    player.hand.add(copper)
    assert len(player.hand) == 2
    assert len(game.trash) == 0

    monkeypatch.setattr("builtins.input", lambda _: "y")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Moneylender
    assert player.state.actions == 0
    assert player.state.money == 3
    assert len(game.trash) == 1
    assert type(game.trash.cards[0]) is Copper


def test_moneylender_input_no(player: Player, game: Game, monkeypatch):
    player.hand.add(moneylender)
    player.hand.add(copper)
    assert len(player.hand) == 2
    assert len(game.trash) == 0

    monkeypatch.setattr("builtins.input", lambda _: "n")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Moneylender
    assert player.state.actions == 0
    assert player.state.money == 0
    assert len(game.trash) == 0


def test_moneylender_no_coppers(player: Player, game: Game, monkeypatch):
    player.hand.add(moneylender)
    assert len(player.hand) == 1
    assert len(game.trash) == 0
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Moneylender
    assert player.state.actions == 0
    assert player.state.money == 0
    assert len(game.trash) == 0

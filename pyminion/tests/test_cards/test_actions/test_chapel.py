from pyminion.models.core import Player, Game
from pyminion.models.base import Chapel, Copper, Estate, chapel, copper, estate


def test_chapel_trash_one(player: Player, game: Game, monkeypatch):
    player.hand.add(chapel)
    player.hand.add(copper)
    player.hand.add(copper)
    assert len(player.hand) == 3
    assert len(game.trash) == 0

    monkeypatch.setattr("builtins.input", lambda _: "Copper")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert len(game.trash) == 1
    assert type(player.playmat.cards[0]) is Chapel
    assert player.state.actions == 0
    assert type(game.trash.cards[0]) is Copper


def test_chapel_trash_multiple(player: Player, game: Game, monkeypatch):
    player.hand.add(chapel)
    player.hand.add(copper)
    player.hand.add(copper)
    player.hand.add(estate)
    assert len(player.hand) == 4
    assert len(game.trash) == 0

    monkeypatch.setattr("builtins.input", lambda _: "Copper, Estate")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert len(game.trash) == 2
    assert type(player.playmat.cards[0]) is Chapel
    assert type(game.trash.cards[0]) is Copper
    assert type(game.trash.cards[1]) is Estate


def test_chapel_empty_hand(player: Player, game: Game):
    player.hand.add(chapel)
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1


def test_chapel_trash_none(player: Player, game: Game, monkeypatch):
    player.hand.add(chapel)
    monkeypatch.setattr("builtins.input", lambda _: "")
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1

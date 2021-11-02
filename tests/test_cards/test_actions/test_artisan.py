from pyminion.models.core import Player, Game
from pyminion.models.base import Estate, artisan, silver


def test_artisan_valid_gain_same_topdeck(player: Player, game: Game, monkeypatch):
    player.hand.add(artisan)
    assert len(game.supply.piles[1]) == 40
    assert len(player.hand) == 1

    # mock decision = input() as "Copper" to discard
    responses = iter(["silver", "silver"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert player.deck.cards[-1] is silver
    assert len(player.playmat) == 1
    assert player.state.actions == 0
    assert len(game.supply.piles[1]) == 39


def test_artisan_invalid_gain(player: Player, game: Game, monkeypatch):
    player.hand.add(artisan)
    assert len(game.supply.piles[1]) == 40
    assert len(player.hand) == 1

    # mock decision = input() as "Copper" to discard
    responses = iter(["gold", "silver", "silver"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert player.deck.cards[-1] is silver
    assert len(player.playmat) == 1
    assert player.state.actions == 0
    assert len(game.supply.piles[1]) == 39


def test_artisan_valid_gain_diff_topdeck(player: Player, game: Game, monkeypatch):
    player.hand.add(artisan)
    player.hand.add(artisan)
    assert len(game.supply.piles[1]) == 40
    assert len(player.hand) == 2

    # mock decision = input() as "Copper" to discard
    responses = iter(["silver", "artisan"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 1
    assert player.deck.cards[-1] is artisan
    assert len(player.playmat) == 1
    assert player.state.actions == 0
    assert len(game.supply.piles[1]) == 39

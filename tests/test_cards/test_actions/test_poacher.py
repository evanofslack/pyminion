from pyminion.models.core import Player
from pyminion.game import Game
from pyminion.models.base import poacher, estate, duchy


def test_poacher_no_empty_pile(player: Player, game: Game):
    player.hand.add(poacher)
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 0
    assert player.state.actions == 1
    assert player.state.money == 1


def test_poacher_one_empty_pile(player: Player, game: Game, monkeypatch):
    for i in range(8):
        game.supply.gain_card(card=estate)
    assert game.supply.num_empty_piles() == 1
    player.hand.add(poacher)
    player.hand.add(estate)
    monkeypatch.setattr("builtins.input", lambda _: "estate")
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 1
    assert player.state.actions == 1
    assert player.state.money == 1


def test_poacher_two_empty_piles(player: Player, game: Game, monkeypatch):
    for i in range(8):
        game.supply.gain_card(card=estate)
    for i in range(8):
        game.supply.gain_card(card=duchy)
    assert game.supply.num_empty_piles() == 2
    player.hand.add(poacher)
    player.hand.add(estate)
    monkeypatch.setattr("builtins.input", lambda _: "estate")
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 2
    assert player.state.actions == 1
    assert player.state.money == 1

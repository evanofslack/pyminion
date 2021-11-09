from pyminion.game import Game
from pyminion.models.base import Moat, moat, Witch, witch, curse


def test_moat_draw(multiplayer_game: Game):
    player = multiplayer_game.players[0]
    player.hand.add(moat)
    assert len(player.hand) == 6
    player.play(moat, game=multiplayer_game)
    assert len(player.hand) == 7
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Moat
    assert player.state.actions == 0
    assert player.state.money == 0
    assert player.state.buys == 1


def test_moat_block_witch(multiplayer_game: Game, monkeypatch):
    player = multiplayer_game.players[0]
    player.hand.add(witch)
    multiplayer_game.players[1].hand.add(moat)
    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.discard_pile) == 0
    monkeypatch.setattr("builtins.input", lambda _: "y")
    player.hand.cards[-1].play(player, multiplayer_game)
    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.discard_pile) == 0


def test_moat_no_block_witch(multiplayer_game: Game, monkeypatch):
    player = multiplayer_game.players[0]
    player.hand.add(witch)
    multiplayer_game.players[1].hand.add(moat)
    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.discard_pile) == 0
    monkeypatch.setattr("builtins.input", lambda _: "n")
    player.hand.cards[-1].play(player, multiplayer_game)
    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.discard_pile) == 1
            assert p.discard_pile.cards[-1] is curse

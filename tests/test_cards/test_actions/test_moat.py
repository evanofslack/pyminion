from pyminion.game import Game
from pyminion.expansions.base import Moat, curse, moat, witch
import pytest


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


@pytest.mark.kingdom_cards([moat])
def test_moat_block_witch(multiplayer_game: Game, monkeypatch):
    witch_player = multiplayer_game.players[0]
    witch_player.hand.add(witch)

    moat_player = multiplayer_game.players[1]
    moat_player.deck.add(moat)
    moat_player.draw()

    for p in multiplayer_game.players:
        if p is not witch_player:
            assert len(p.discard_pile) == 0
    monkeypatch.setattr("builtins.input", lambda _: "y")
    witch_player.play(witch, multiplayer_game)
    for p in multiplayer_game.players:
        if p is not witch_player:
            assert len(p.discard_pile) == 0


@pytest.mark.kingdom_cards([moat])
def test_moat_no_block_witch(multiplayer_game: Game, monkeypatch):
    witch_player = multiplayer_game.players[0]
    witch_player.hand.add(witch)

    moat_player = multiplayer_game.players[1]
    moat_player.deck.add(moat)
    moat_player.draw()

    for p in multiplayer_game.players:
        if p is not witch_player:
            assert len(p.discard_pile) == 0
    monkeypatch.setattr("builtins.input", lambda _: "n")
    witch_player.play(witch, multiplayer_game)
    for p in multiplayer_game.players:
        if p is not witch_player:
            assert len(p.discard_pile) == 1
            assert p.discard_pile.cards[-1] is curse

from pyminion.expansions.base import Copper, Curse, copper, witch
from pyminion.expansions.intrigue import Diplomat, intrigue_set, diplomat
from pyminion.player import Player
from pyminion.game import Game
import pytest


def test_diplomat_actions(player: Player, game: Game):
    player.hand.add(diplomat)
    assert len(player.hand) == 1

    player.play(diplomat, game)
    assert len(player.hand) == 2
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Diplomat
    assert player.state.actions == 2


def test_diplomat_no_actions(player: Player, game: Game):
    for _ in range(4):
        player.hand.add(copper)
    player.hand.add(diplomat)
    assert len(player.hand) == 5

    player.play(diplomat, game)
    assert len(player.hand) == 6
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Diplomat
    assert player.state.actions == 0


@pytest.mark.expansions([intrigue_set])
@pytest.mark.kingdom_cards([diplomat])
def test_diplomat_block_witch(multiplayer_game: Game, monkeypatch):
    p1 = multiplayer_game.players[0]
    p2 = multiplayer_game.players[1]

    p1.hand.cards.clear()
    for _ in range(4):
        p1.hand.add(copper)
    p1.deck.add(diplomat)
    p1.draw()
    assert len(p1.hand) == 5

    p2.hand.add(witch)

    responses = iter(["y", "copper, copper, copper"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    p2.play(witch, multiplayer_game)

    assert len(p1.hand) == 4
    assert len(p1.discard_pile) == 4
    for i in range(3):
        assert type(p1.discard_pile.cards[i]) is Copper
    assert type(p1.discard_pile.cards[-1]) is Curse


@pytest.mark.expansions([intrigue_set])
@pytest.mark.kingdom_cards([diplomat])
def test_diplomat_no_block_witch(multiplayer_game: Game, monkeypatch):
    p1 = multiplayer_game.players[0]
    p2 = multiplayer_game.players[1]

    p1.hand.cards.clear()
    for _ in range(4):
        p1.hand.add(copper)
    p1.deck.add(diplomat)
    p1.draw()
    assert len(p1.hand) == 5

    p2.hand.add(witch)

    monkeypatch.setattr("builtins.input", lambda _: "n")

    p2.play(witch, multiplayer_game)

    assert len(p1.hand) == 5
    assert len(p1.discard_pile) == 1
    assert type(p1.discard_pile.cards[-1]) is Curse


@pytest.mark.expansions([intrigue_set])
@pytest.mark.kingdom_cards([diplomat])
def test_diplomat_cannot_block_witch(multiplayer_game: Game):
    p1 = multiplayer_game.players[0]
    p2 = multiplayer_game.players[1]

    p1.hand.cards.clear()
    for _ in range(3):
        p1.hand.add(copper)
    p1.deck.add(diplomat)
    p1.draw()
    assert len(p1.hand) == 4

    p2.hand.add(witch)

    p2.play(witch, multiplayer_game)

    assert len(p1.hand) == 4
    assert len(p1.discard_pile) == 1
    assert type(p1.discard_pile.cards[-1]) is Curse

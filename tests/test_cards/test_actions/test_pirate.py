from pyminion.expansions.base import gold
from pyminion.expansions.seaside import pirate, seaside_set
from pyminion.game import Game
from pyminion.human import Human
import pytest


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([pirate])
def test_pirate_gain(human: Human, game: Game, monkeypatch):
    responses = ["gold"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.hand.add(pirate)

    human.play(pirate, game)
    assert len(responses) == 1
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Pirate"
    assert human.state.actions == 0

    human.start_cleanup_phase(game)
    human.end_turn(game)

    assert len(responses) == 1

    human.start_turn(game)
    assert len(responses) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Pirate"
    assert len(human.hand) == 6
    assert "Gold" in (c.name for c in human.hand)


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([pirate])
def test_pirate_reaction(multiplayer_game: Game, monkeypatch):
    responses = ["y", "gold"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    p1 = multiplayer_game.players[0]
    p2 = multiplayer_game.players[1]

    p1.hand.add(pirate)

    p2.gain(gold, multiplayer_game)
    assert len(responses) == 1
    assert len(p1.playmat) == 1
    assert p1.playmat.cards[0].name == "Pirate"

    p2.start_cleanup_phase(multiplayer_game)
    p2.end_turn(multiplayer_game)

    assert len(responses) == 1

    p1.start_turn(multiplayer_game)
    assert len(responses) == 0
    assert len(p1.playmat) == 1
    assert p1.playmat.cards[0].name == "Pirate"
    assert len(p1.hand) == 6
    assert "Gold" in (c.name for c in p1.hand)


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([pirate])
def test_pirate_decline_reaction(multiplayer_game: Game, monkeypatch):
    responses = ["n", "gold"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    p1 = multiplayer_game.players[0]
    p2 = multiplayer_game.players[1]

    p1.hand.add(pirate)

    p2.gain(gold, multiplayer_game)
    assert len(responses) == 1
    assert len(p1.playmat) == 0

    p2.start_cleanup_phase(multiplayer_game)
    p2.end_turn(multiplayer_game)

    assert len(responses) == 1

    p1.start_turn(multiplayer_game)
    assert len(responses) == 1
    assert len(p1.playmat) == 0
    assert len(p1.hand) == 6
    assert "Gold" not in (c.name for c in p1.hand)

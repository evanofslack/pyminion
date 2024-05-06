from pyminion.expansions.base import copper, gold
from pyminion.expansions.seaside import monkey, pirate, seaside_set
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


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([monkey, pirate])
def test_pirate_monkey_combo(multiplayer_game: Game, monkeypatch):
    # test case where opponent gains a treasure triggering monkey to draw a
    # pirate and the pirate is played

    responses = ["y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    p1 = multiplayer_game.players[0]
    p2 = multiplayer_game.players[1]

    # add pirate where it will be on the top of the deck at the end of p1's turn
    p1.deck.add(pirate)

    # add 5 coppers to draw at end of turn
    for _ in range(5):
        p1.deck.add(copper)

    p1.hand.add(monkey)

    p1.play(monkey, multiplayer_game)

    p1.start_cleanup_phase(multiplayer_game)
    p1.end_turn(multiplayer_game)

    # assert pirate is on top of the deck
    assert p1.deck.cards[-1].name == "Pirate"

    p2.start_turn(multiplayer_game)

    p2.gain(gold, multiplayer_game)
    assert len(responses) == 0
    assert len(p1.playmat) == 2
    assert p1.playmat.cards[0].name == "Monkey"
    assert p1.playmat.cards[1].name == "Pirate"

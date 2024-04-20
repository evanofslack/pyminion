from pyminion.core import DeckCounter
from pyminion.expansions.base import curse, smithy, witch
from pyminion.expansions.seaside import Lighthouse, blockade, lighthouse
from pyminion.game import Game
import pytest


def test_lighthouse(multiplayer_game: Game):
    lighthouse_player = multiplayer_game.players[0]
    witch_player = multiplayer_game.players[1]

    # lighthouse player plays lighthouse

    lighthouse_player.hand.add(lighthouse)

    lighthouse_player.play(lighthouse, multiplayer_game)
    assert len(lighthouse_player.hand) == 5
    assert len(lighthouse_player.playmat) == 1
    assert type(lighthouse_player.playmat.cards[0]) is Lighthouse
    assert len(lighthouse_player.discard_pile) == 0
    assert lighthouse_player.state.actions == 1
    assert lighthouse_player.state.money == 1
    assert lighthouse_player.playmat_persist_counts[lighthouse.name] == 1

    lighthouse_player.start_cleanup_phase(multiplayer_game)

    assert len(lighthouse_player.hand) == 5
    assert len(lighthouse_player.playmat) == 1
    assert type(lighthouse_player.playmat.cards[0]) is Lighthouse
    assert lighthouse_player.playmat_persist_counts[lighthouse.name] == 1

    witch_player.start_turn(multiplayer_game)

    # witch player plays witch and should be blocked

    witch_player.hand.add(witch)

    witch_player.play(witch, multiplayer_game)
    counter = DeckCounter(lighthouse_player.discard_pile.cards)
    assert counter[curse] == 0

    witch_player.start_cleanup_phase(multiplayer_game)

    # lighthouse player discards lighthouse from play

    lighthouse_player.start_turn(multiplayer_game)

    assert len(lighthouse_player.hand) == 5
    assert len(lighthouse_player.playmat) == 1
    assert type(lighthouse_player.playmat.cards[0]) is Lighthouse
    assert lighthouse_player.state.actions == 1
    assert lighthouse_player.state.money == 1
    assert lighthouse_player.playmat_persist_counts[lighthouse.name] == 0

    lighthouse_player.start_cleanup_phase(multiplayer_game)

    # witch player plays witch again and should not be blocked

    witch_player.start_turn(multiplayer_game)

    witch_player.hand.add(witch)

    witch_player.play(witch, multiplayer_game)
    counter = DeckCounter(lighthouse_player.discard_pile.cards)
    assert counter[curse] == 1


@pytest.mark.kingdom_cards([smithy])
def test_lighthouse_duration_attack(multiplayer_game: Game, monkeypatch):
    responses = ["smithy"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    p1 = multiplayer_game.players[0]
    p2 = multiplayer_game.players[1]

    p1.hand.add(lighthouse)

    p2.hand.add(blockade)

    p1.play(lighthouse, multiplayer_game)

    p1.start_cleanup_phase(multiplayer_game)
    p1.end_turn(multiplayer_game)

    multiplayer_game.current_player = p2
    p2.start_turn(multiplayer_game)

    p2.play(blockade, multiplayer_game)
    assert len(responses) == 0

    p2.start_cleanup_phase(multiplayer_game)
    p2.end_turn(multiplayer_game)

    multiplayer_game.current_player = p1
    p1.start_turn(multiplayer_game)

    p1.gain(smithy, multiplayer_game)

    assert "Curse" not in (c.name for c in p1.discard_pile)


@pytest.mark.kingdom_cards([smithy])
def test_lighthouse_duration_attack_no_block(multiplayer_game: Game, monkeypatch):
    responses = ["smithy"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    p1 = multiplayer_game.players[0]
    p2 = multiplayer_game.players[1]

    p2.hand.add(blockade)

    p2.play(blockade, multiplayer_game)
    assert len(responses) == 0

    p2.start_cleanup_phase(multiplayer_game)
    p2.end_turn(multiplayer_game)

    multiplayer_game.current_player = p1
    p1.start_turn(multiplayer_game)

    p1.hand.add(lighthouse)
    p1.play(lighthouse, multiplayer_game)

    p1.gain(smithy, multiplayer_game)

    assert "Curse" in (c.name for c in p1.discard_pile)

from pyminion.core import DeckCounter
from pyminion.expansions.base import Smithy, curse, smithy
from pyminion.expansions.seaside import Blockade, blockade
from pyminion.game import Game
import pytest


@pytest.mark.kingdom_cards([smithy])
def test_blockade(multiplayer_game: Game, monkeypatch):
    player1 = multiplayer_game.players[0]
    player2 = multiplayer_game.players[1]

    player1.hand.add(blockade)

    responses = ["smithy"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    multiplayer_game.current_player = player1
    player1.start_turn(multiplayer_game)

    player1.play(blockade, multiplayer_game)
    assert len(responses) == 0
    assert len(player1.playmat) == 1
    assert type(player1.playmat.cards[0]) is Blockade
    assert len(player1.set_aside) == 1
    assert type(player1.set_aside.cards[0]) is Smithy
    assert len(player1.discard_pile) == 0
    assert player1.state.actions == 0
    assert player1.playmat_persist_counts[blockade.name] == 1

    # player2 should not gain a curse when it is not their turn
    player2.gain(smithy, multiplayer_game)
    assert len(player2.discard_pile) == 1
    counter = DeckCounter(player2.discard_pile)
    assert counter[smithy] == 1

    player1.start_cleanup_phase(multiplayer_game)

    multiplayer_game.current_player = player2
    player2.start_turn(multiplayer_game)

    # player2 should gain a curse on their turn
    player2.gain(smithy, multiplayer_game)
    assert len(player2.discard_pile) == 3
    counter = DeckCounter(player2.discard_pile)
    assert counter[smithy] == 2
    assert counter[curse] == 1

    player2.start_cleanup_phase(multiplayer_game)

    multiplayer_game.current_player = player1
    player1.start_turn(multiplayer_game)
    counter = DeckCounter(player1.hand)
    assert counter[smithy] == 1
    assert len(player1.playmat) == 1
    assert type(player1.playmat.cards[0]) is Blockade
    assert len(player1.set_aside) == 0
    assert player1.playmat_persist_counts[blockade.name] == 0

    player1.start_cleanup_phase(multiplayer_game)

    multiplayer_game.current_player = player2
    player2.start_turn(multiplayer_game)

    # player2 should not gain another curse on their following turn
    player2.gain(smithy, multiplayer_game)
    counter = DeckCounter(player2.discard_pile)
    assert counter[smithy] == 3
    assert counter[curse] == 1

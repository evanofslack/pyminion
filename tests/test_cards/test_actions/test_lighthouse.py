from pyminion.core import DeckCounter
from pyminion.expansions.base import curse, witch
from pyminion.expansions.seaside import Lighthouse, lighthouse
from pyminion.game import Game


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

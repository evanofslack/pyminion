from pyminion.core import DeckCounter
from pyminion.expansions.base import copper
from pyminion.expansions.seaside import Wharf, wharf
from pyminion.game import Game
from pyminion.player import Player


def test_wharf(player: Player, game: Game):
    for _ in range(10):
        player.deck.add(copper)
    player.hand.add(wharf)

    player.play(wharf, game)
    assert len(player.hand) == 2
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Wharf
    assert len(player.discard_pile) == 0
    assert player.state.actions == 0
    assert player.state.buys == 2
    assert player.playmat_persist_counts[wharf.name] == 1

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Wharf
    assert len(player.discard_pile) == 2
    counter = DeckCounter(player.discard_pile.cards)
    assert counter[wharf] == 0
    assert player.playmat_persist_counts[wharf.name] == 1

    player.start_turn(game)

    assert len(player.hand) == 7
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Wharf
    assert len(player.discard_pile) == 2
    counter = DeckCounter(player.discard_pile.cards)
    assert counter[wharf] == 0
    assert player.state.actions == 1
    assert player.state.buys == 2
    assert player.playmat_persist_counts[wharf.name] == 0

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 0
    counter = DeckCounter(player.discard_pile.cards)
    assert counter[wharf] == 1
    assert player.playmat_persist_counts[wharf.name] == 0

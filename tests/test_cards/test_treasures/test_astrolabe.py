from pyminion.core import DeckCounter
from pyminion.expansions.seaside import Astrolabe, astrolabe
from pyminion.game import Game
from pyminion.player import Player


def test_astrolabe(player: Player, game: Game):
    player.hand.add(astrolabe)

    player.play(astrolabe, game)
    assert player.state.money == 1
    assert player.state.buys == 2

    player.start_cleanup_phase(game)

    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Astrolabe

    player.start_turn(game)

    assert len(player.hand) == 5
    assert player.state.money == 1
    assert player.state.buys == 2
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Astrolabe

    player.start_cleanup_phase(game)

    assert len(player.playmat) == 0
    counter = DeckCounter(player.discard_pile.cards)
    assert counter[astrolabe] == 1

from pyminion.expansions.base import silver
from pyminion.expansions.seaside import tactician
from pyminion.game import Game
from pyminion.player import Player


def test_tactician(player: Player, game: Game):
    player.hand.add(silver)
    player.hand.add(tactician)
    assert len(player.hand) == 2

    player.play(tactician, game)
    assert len(player.hand) == 0
    assert player.state.actions == 0
    assert player.state.money == 0
    assert player.state.buys == 1
    assert len(player.discard_pile) == 1
    assert player.discard_pile.cards[0].name == "Silver"

    player.start_cleanup_phase(game)
    player.end_turn(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert player.playmat.cards[0].name == "Tactician"

    player.start_turn(game)
    assert len(player.hand) == 10
    assert player.state.actions == 2
    assert player.state.money == 0
    assert player.state.buys == 2


def test_tactician_no_cards(player: Player, game: Game):
    player.hand.add(tactician)
    assert len(player.hand) == 1

    player.play(tactician, game)
    assert len(player.hand) == 0
    assert player.state.actions == 0
    assert player.state.money == 0
    assert player.state.buys == 1
    assert len(player.discard_pile) == 0

    player.start_cleanup_phase(game)
    player.end_turn(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 0

    player.start_turn(game)
    assert len(player.hand) == 5
    assert player.state.actions == 1
    assert player.state.money == 0
    assert player.state.buys == 1

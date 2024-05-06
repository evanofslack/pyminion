from pyminion.core import DeckCounter
from pyminion.expansions.seaside import MerchantShip, merchant_ship
from pyminion.game import Game
from pyminion.player import Player


def test_merchant_ship(player: Player, game: Game):
    player.hand.add(merchant_ship)

    player.play(merchant_ship, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is MerchantShip
    assert len(player.discard_pile) == 0
    assert player.state.actions == 0
    assert player.state.money == 2
    assert player.playmat_persist_counts[merchant_ship.name] == 1

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is MerchantShip
    assert len(player.discard_pile) == 0
    assert player.playmat_persist_counts[merchant_ship.name] == 1

    player.start_turn(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is MerchantShip
    assert len(player.discard_pile) == 0
    assert player.state.actions == 1
    assert player.state.money == 2
    assert player.playmat_persist_counts[merchant_ship.name] == 0

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 0
    counter = DeckCounter(player.discard_pile.cards)
    assert counter[merchant_ship] == 1
    assert player.playmat_persist_counts[merchant_ship.name] == 0

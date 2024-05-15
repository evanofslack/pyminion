from pyminion.expansions.base import copper, duchy, village
from pyminion.expansions.alchemy import vineyard
from pyminion.player import Player


def test_vineyard(player: Player):
    player.deck.cards.clear()
    player.discard_pile.cards.clear()

    assert vineyard.score(player) == 0

    # should be 0 points while less than 3 actions
    for _ in range(2):
        player.deck.add(village)
        assert vineyard.score(player) == 0

    # should be 1 point for 3-5 actions
    for _ in range(3):
        player.deck.add(village)
        assert vineyard.score(player) == 1

    # should be 2 points for 6-8 actions
    for _ in range(3):
        player.deck.add(village)
        assert vineyard.score(player) == 2

    # adding non-action cards should not affect the victory points
    for _ in range(5):
        player.deck.add(copper)
    for _ in range(5):
        player.deck.add(duchy)

    assert vineyard.score(player) == 2

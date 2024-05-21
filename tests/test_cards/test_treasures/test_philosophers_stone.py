from pyminion.expansions.base import copper
from pyminion.expansions.alchemy import philosophers_stone
from pyminion.game import Game
from pyminion.player import Player


def test_philosophers_stone(player: Player, game: Game):
    player.deck.cards.clear()
    player.discard_pile.cards.clear()

    for _ in range(4):
        player.hand.add(philosophers_stone)

    # no cards in deck/discard pile
    player.play(philosophers_stone, game)
    assert player.state.money == 0

    for _ in range(9):
        player.deck.add(copper)

    player.play(philosophers_stone, game)
    assert player.state.money == 1

    player.deck.add(copper)

    player.play(philosophers_stone, game)
    assert player.state.money == 3

    # cards in hand should not count
    for _ in range(10):
        player.hand.add(copper)

    player.play(philosophers_stone, game)
    assert player.state.money == 5

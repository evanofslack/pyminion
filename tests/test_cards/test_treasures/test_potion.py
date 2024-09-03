from pyminion.expansions.alchemy import potion
from pyminion.game import Game
from pyminion.player import Player

def test_potion(player: Player, game: Game):
    player.hand.add(potion)
    player.hand.add(potion)

    assert player.state.money == 0
    assert player.state.potions == 0

    player.play(potion, game)

    assert player.state.money == 0
    assert player.state.potions == 1

    player.play(potion, game)

    assert player.state.money == 0
    assert player.state.potions == 2

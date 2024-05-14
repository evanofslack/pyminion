from pyminion.expansions.intrigue import Farm, farm
from pyminion.game import Game
from pyminion.player import Player


def test_money(player: Player, game: Game):
    player.hand.add(farm)

    farm.play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Farm
    assert player.state.money == 2


def test_vp(player: Player):
    player.hand.add(farm)
    assert farm.score(player) == 2

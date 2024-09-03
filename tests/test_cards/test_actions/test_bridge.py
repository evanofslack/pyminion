from pyminion.expansions.base import copper, silver
from pyminion.expansions.alchemy import apothecary
from pyminion.core import Cost
from pyminion.core import DeckCounter
from pyminion.expansions.intrigue import Bridge, bridge, shanty_town
from pyminion.game import Game
from pyminion.player import Player


def test_one_bridge(player: Player, game: Game):
    player.hand.add(bridge)

    assert copper.get_cost(player, game) == 0
    assert silver.get_cost(player, game) == 3
    assert apothecary.get_cost(player, game) == Cost(2, 1)

    player.play(bridge, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Bridge
    assert player.state.buys == 2
    assert player.state.money == 1

    assert game.card_cost_reduction == 1

    assert copper.get_cost(player, game) == 0
    assert silver.get_cost(player, game) == 2
    assert apothecary.get_cost(player, game) == Cost(1, 1)


def test_two_bridges(player: Player, game: Game):
    player.hand.add(shanty_town)
    player.hand.add(bridge)
    player.hand.add(bridge)

    assert copper.get_cost(player, game) == 0
    assert silver.get_cost(player, game) == 3

    player.play(shanty_town, game)
    player.play(bridge, game)
    player.play(bridge, game)
    assert len(player.hand) == 0
    counter = DeckCounter(player.playmat.cards)
    assert sum(counter.values()) == 3
    assert counter[shanty_town] == 1
    assert counter[bridge] == 2
    assert player.state.buys == 3
    assert player.state.money == 2

    assert game.card_cost_reduction == 2

    assert copper.get_cost(player, game) == 0
    assert silver.get_cost(player, game) == 1

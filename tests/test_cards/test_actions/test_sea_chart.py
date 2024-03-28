from pyminion.expansions.base import copper
from pyminion.expansions.seaside import bazaar, sea_chart
from pyminion.game import Game
from pyminion.player import Player


def test_sea_chart_put_in_hand(player: Player, game: Game):
    player.hand.add(sea_chart)
    player.deck.add(bazaar)
    player.deck.add(copper)
    player.playmat.add(bazaar)

    player.play(sea_chart, game)

    assert len(player.hand) == 2
    assert player.state.actions == 1
    assert any(c.name == bazaar.name for c in player.hand.cards)


def test_sea_chart_put_back(player: Player, game: Game):
    player.hand.add(sea_chart)
    player.deck.add(bazaar)
    player.deck.add(copper)

    player.play(sea_chart, game)

    assert len(player.hand) == 1
    assert player.state.actions == 1
    assert not any(c.name == bazaar.name for c in player.hand.cards)


def test_sea_chart_no_deck(player: Player, game: Game):
    while len(player.deck) > 0:
        player.deck.cards.pop()
    while len(player.discard_pile) > 0:
        player.discard_pile.cards.pop()

    player.hand.add(sea_chart)

    player.play(sea_chart, game)

    assert len(player.hand) == 0
    assert player.state.actions == 1

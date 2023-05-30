from pyminion.expansions.base import duchy
from pyminion.expansions.intrigue import duke
from pyminion.player import Player


def test_duke_no_duchy(player: Player):
    player.hand.add(duke)
    assert player.hand.cards[0].score(player) == 0


def test_duke_1_duchy(player: Player):
    player.hand.add(duke)
    player.deck.add(duchy)
    assert player.hand.cards[0].score(player) == 1


def test_duke_multiple_duchies(player: Player):
    player.hand.add(duke)
    player.deck.add(duchy)
    player.deck.add(duchy)
    player.deck.add(duchy)
    assert player.hand.cards[0].score(player) == 3

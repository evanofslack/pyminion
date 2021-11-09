from pyminion.models.base import curse
from pyminion.models.core import Player


def test_curse_decrease_score(player: Player):
    player.hand.add(curse)
    assert player.hand.cards[0].score(player) == -1
    assert player.get_victory_points() == 2
    player.deck.add(curse)
    player.discard_pile.add(curse)
    assert player.get_victory_points() == 0

from pyminion.expansions.base import copper, gardens
from pyminion.player import Player


def test_gardens_score_10_cards(player: Player):
    player.hand.add(gardens)
    assert len(player.deck) == 10
    player.deck.remove(copper)
    assert player.get_all_cards_count() == 10
    assert gardens.score(player) == 1


def test_gardens_score_9_cards(player: Player):
    player.hand.add(gardens)
    player.deck.remove(copper)
    player.deck.remove(copper)
    assert player.get_all_cards_count() == 9
    assert gardens.score(player) == 0


def test_gardens_score_over_11_cards(player: Player):
    player.hand.add(gardens)
    assert player.get_all_cards_count() == 11
    assert gardens.score(player) == 1


def test_gardens_score_21_cards(player: Player):
    player.hand.add(gardens)
    for i in range(10):
        player.deck.add(copper)
    assert player.get_all_cards_count() == 21
    assert gardens.score(player) == 2

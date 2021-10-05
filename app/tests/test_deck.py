import pytest

from doughminion.models.cards import Deck
from doughminion.base_cards import copper, silver, gold, estate, duchy, province

NUM_COPPER = 7
NUM_ESTATE = 3


def test_create_deck():
    start_cards = [copper for x in range(NUM_COPPER)] + [
        estate for x in range(NUM_ESTATE)
    ]
    deck = Deck(cards=start_cards)
    assert len(deck.cards) == 10

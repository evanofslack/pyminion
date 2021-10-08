import pytest

from app.models.cards import Deck, Card, Treasure, Victory, DiscardPile
from app.base_set.base_cards import copper, silver, gold, estate, duchy, province

NUM_COPPER = 7
NUM_ESTATE = 3

@pytest.fixture
def discard():
    discard = DiscardPile()
    return discard
    

def test_discard_creates_empty_list():
    discard = DiscardPile()
    assert not discard.cards

    discard = DiscardPile([copper, copper])

    discard = DiscardPile()
    assert not discard.cards

def test_add_card_to_discard(discard: DiscardPile):
    assert not discard.cards
    discard.add(copper)
    assert len(discard.cards) == 1
    assert type(discard.cards[0]) is Treasure
    discard.add(estate)
    assert len(discard.cards) == 2




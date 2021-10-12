import pytest

from app.models.cards import Deck, Card, DiscardPile, Treasure, Victory, AbstractDeck
from app.base_set.base_cards import copper, silver, gold, estate, duchy, province

NUM_COPPER = 7
NUM_ESTATE = 3


@pytest.fixture
def deck():
    start_cards = [copper for x in range(NUM_COPPER)] + [
        estate for x in range(NUM_ESTATE)
    ]
    deck = Deck(cards=start_cards)
    return deck


def test_abstract_deck_creates_empty_list():
    abs_deck = AbstractDeck()
    assert not abs_deck.cards


def test_abstract_deck_length():
    abs_deck = AbstractDeck(cards=[copper, copper, estate])
    assert len(abs_deck) is 3


def test_abstract_deck_add():
    abs_deck = AbstractDeck()
    abs_deck.add(copper)
    assert len(abs_deck) == 1
    abs_deck.add(estate)
    assert len(abs_deck) == 2
    assert type(abs_deck.cards[0]) is Treasure
    assert type(abs_deck.cards[1]) is Victory


def test_create_deck():
    start_cards = [copper for x in range(NUM_COPPER)] + [
        estate for x in range(NUM_ESTATE)
    ]
    deck = Deck(cards=start_cards)
    assert len(deck.cards) == 10
    assert deck.cards.count(copper) is 7
    assert deck.cards.count(estate) is 3
    assert type(deck.cards[0]) is Treasure
    assert type(deck.cards[9]) is Victory


def test_draw_one_deck(deck: Deck):
    drawn_card = deck.draw()
    assert type(drawn_card) is Victory


# def test_shuffle_deck(deck: Deck):
#     deck.shuffle()
#     shuffle 100 times and get assert amount of combos is greater than x%


def test_topdeck_deck(deck: Deck):
    assert len(deck.cards) == 10
    assert type(deck.cards[-1]) is Victory

    deck.add(copper)
    assert len(deck.cards) == 11
    assert type(deck.cards[-1]) is Treasure

    deck.add(estate)
    assert len(deck.cards) == 12
    assert type(deck.cards[-1]) is Victory


def test_combine_deck(deck: Deck):
    assert len(deck.cards) == 10
    discard = DiscardPile([copper, copper])
    deck.combine(discard.cards)
    assert len(deck.cards) == 12

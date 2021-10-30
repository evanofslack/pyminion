from pyminion.models.core import AbstractDeck, Deck
from pyminion.models.base import Copper, Estate
from pyminion.expansions.base import copper, estate

NUM_COPPER = 7
NUM_ESTATE = 3


def test_abstract_deck_creates_empty_list():
    abs_deck = AbstractDeck()
    assert not abs_deck.cards


def test_abstract_deck_length():
    abs_deck = AbstractDeck(cards=[copper, copper, estate])
    assert len(abs_deck) == 3


def test_abstract_deck_add():
    abs_deck = AbstractDeck()
    abs_deck.add(copper)
    assert len(abs_deck) == 1
    abs_deck.add(estate)
    assert len(abs_deck) == 2
    assert type(abs_deck.cards[0]) is Copper
    assert type(abs_deck.cards[1]) is Estate


def test_abstract_deck_move_to():
    deck_1 = AbstractDeck([copper, copper])
    deck_2 = AbstractDeck([estate, estate, estate])
    deck_1.move_to(deck_2)
    assert len(deck_1) == 0
    assert len(deck_2) == 5


def test_create_deck():
    start_cards = [copper for x in range(NUM_COPPER)] + [
        estate for x in range(NUM_ESTATE)
    ]
    deck = Deck(cards=start_cards)
    assert len(deck.cards) == 10
    assert deck.cards.count(copper) == 7
    assert deck.cards.count(estate) == 3
    assert type(deck.cards[0]) is Copper
    assert type(deck.cards[9]) is Estate


def test_draw_one_deck(deck: Deck):
    drawn_card = deck.draw()
    assert type(drawn_card) is Estate


# def test_shuffle_deck(deck: Deck):
#     deck.shuffle()
#     shuffle 100 times and get assert amount of combos is greater than x%


def test_topdeck_deck(deck: Deck):
    assert len(deck.cards) == 10
    assert type(deck.cards[-1]) is Estate

    deck.add(copper)
    assert len(deck.cards) == 11
    assert type(deck.cards[-1]) is Copper

    deck.add(estate)
    assert len(deck.cards) == 12
    assert type(deck.cards[-1]) is Estate


def test_deck_remove(deck: Deck):
    assert len(deck) == 10
    deck.remove(copper)
    assert len(deck) == 9

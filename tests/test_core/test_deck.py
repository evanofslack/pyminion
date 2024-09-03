from pyminion.core import AbstractDeck, Card, Deck
from pyminion.expansions.base import Copper, Estate, copper, estate

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


def test_abstract_deck_on_add():
    cards: list[Card] = []
    deck = AbstractDeck(
        on_add=lambda c: cards.append(c)
    )
    deck.add(copper)
    deck.add(estate)
    deck.add(copper)

    assert len(cards) == 3
    assert cards[0] == copper
    assert cards[1] == estate
    assert cards[2] == copper


def test_abstract_deck_on_remove():
    cards: list[Card] = []
    deck = AbstractDeck(
        cards=[copper, estate, copper],
        on_remove=lambda c: cards.append(c)
    )
    deck.remove(copper)
    deck.remove(estate)
    deck.remove(copper)

    assert len(cards) == 3
    assert cards[0] == copper
    assert cards[1] == estate
    assert cards[2] == copper


def test_abstract_deck_move_to_handlers():
    added_cards: list[Card] = []
    removed_cards: list[Card] = []
    deck_1 = AbstractDeck(
        cards=[copper, copper],
        on_remove=lambda c: removed_cards.append(c),
    )
    deck_2 = AbstractDeck(
        cards=[estate, estate, estate],
        on_add=lambda c: added_cards.append(c),
    )

    deck_1.move_to(deck_2)
    assert len(deck_1) == 0
    assert len(deck_2) == 5

    assert len(added_cards) == 2
    assert added_cards[0].name == "Copper"
    assert added_cards[1].name == "Copper"

    assert len(removed_cards) == 2
    assert removed_cards[0].name == "Copper"
    assert removed_cards[1].name == "Copper"


def test_create_deck():
    start_cards: list[Card] = []
    start_cards += [copper for x in range(NUM_COPPER)] + [
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


def test_deck_draw_on_remove():
    cards: list[Card] = []
    deck = Deck(
        cards=[copper, estate, copper],
        on_remove=lambda c: cards.append(c)
    )
    deck.draw()
    deck.draw()
    deck.draw()

    assert len(cards) == 3
    assert cards[0] == copper
    assert cards[1] == estate
    assert cards[2] == copper


def test_deck_on_shuffle():
    shuffles: list[None] = []
    deck = Deck(
        on_shuffle=lambda: shuffles.append(None)
    )

    assert len(shuffles) == 0
    deck.shuffle()
    assert len(shuffles) == 1
    deck.shuffle()
    deck.shuffle()
    assert len(shuffles) == 3

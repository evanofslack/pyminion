from pyminion.models.base import Pile
from pyminion.base_set.base_cards import copper, estate


def make_empty_pile():
    empty = Pile()
    assert len(empty) == 0
    assert empty.name == None


def test_make_pile():
    estates = [estate for x in range(8)]
    estate_pile = Pile(estates)
    assert len(estate_pile) == 8
    assert estate_pile.name == "Estate"


def test_make_mixed_pile():
    mixed = Pile([estate, copper])
    assert len(mixed) == 2
    assert mixed.name == "Mixed"
